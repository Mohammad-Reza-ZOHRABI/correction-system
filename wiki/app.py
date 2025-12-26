"""
Wiki - Documentation pour les étudiants
Technologies de Containérisation
"""

from fastapi import FastAPI, Request, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import markdown
import frontmatter
from pathlib import Path
from typing import Dict, List, Optional
import os
import json

app = FastAPI(title="Wiki - Containérisation")

# Configuration
CONTENT_DIR = Path("content")
STATIC_DIR = Path("static")
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "en")

# Charger les traductions
with open("translations.json", "r", encoding="utf-8") as f:
    TRANSLATIONS = json.load(f)

# Templates
templates = Jinja2Templates(directory="templates")

# Monter les fichiers statiques
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Configuration Markdown avec extensions
md = markdown.Markdown(extensions=[
    'fenced_code',
    'codehilite',
    'tables',
    'toc',
    'attr_list',
    'admonition'
])

def get_translation(lang: str, key: str):
    """Récupère une traduction"""
    keys = key.split(".")
    value = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    for k in keys:
        value = value.get(k, key)
    return value

def get_page_content(page_name: str) -> Dict:
    """Charge le contenu d'une page markdown"""
    page_path = CONTENT_DIR / f"{page_name}.md"
    
    if not page_path.exists():
        return None
    
    # Lire le fichier avec frontmatter
    post = frontmatter.load(page_path)
    
    # Convertir markdown en HTML
    html_content = md.convert(post.content)
    
    return {
        "title": post.get("title", page_name.title()),
        "description": post.get("description", ""),
        "content": html_content,
        "metadata": post.metadata
    }

def get_all_pages() -> List[Dict]:
    """Liste toutes les pages disponibles"""
    pages = []
    
    if not CONTENT_DIR.exists():
        return pages
    
    for md_file in CONTENT_DIR.glob("*.md"):
        post = frontmatter.load(md_file)
        pages.append({
            "slug": md_file.stem,
            "title": post.get("title", md_file.stem.title()),
            "description": post.get("description", ""),
            "order": post.get("order", 999),
            "category": post.get("category", "Général")
        })
    
    # Trier par ordre
    pages.sort(key=lambda x: x["order"])
    
    return pages

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, lang: Optional[str] = Cookie(default=DEFAULT_LANGUAGE)):
    """Page d'accueil"""
    # Valider la langue
    if lang not in ["en", "fr"]:
        lang = DEFAULT_LANGUAGE

    pages = get_all_pages()

    # Grouper par catégorie et traduire les noms de catégories
    categories = {}
    for page in pages:
        cat = page["category"]
        # Traduire le nom de la catégorie
        translated_cat = get_translation(lang, f"categories.{cat}")
        if translated_cat == f"categories.{cat}":  # Si pas de traduction, utiliser l'original
            translated_cat = cat

        if translated_cat not in categories:
            categories[translated_cat] = []
        categories[translated_cat].append(page)

    return templates.TemplateResponse("home.html", {
        "request": request,
        "categories": categories,
        "lang": lang,
        "t": lambda key: get_translation(lang, key)
    })

@app.get("/page/{page_name}", response_class=HTMLResponse)
async def show_page(request: Request, page_name: str, lang: Optional[str] = Cookie(default=DEFAULT_LANGUAGE)):
    """Afficher une page"""
    # Valider la langue
    if lang not in ["en", "fr"]:
        lang = DEFAULT_LANGUAGE

    content = get_page_content(page_name)

    if not content:
        return templates.TemplateResponse("404.html", {
            "request": request,
            "title": "Page non trouvée"
        }, status_code=404)

    # Liste des pages pour la navigation
    all_pages = get_all_pages()

    return templates.TemplateResponse("page.html", {
        "request": request,
        "title": content["title"],
        "description": content["description"],
        "content": content["content"],
        "all_pages": all_pages,
        "lang": lang,
        "t": lambda key: get_translation(lang, key)
    })

@app.get("/set-language/{language}")
async def set_language(language: str):
    """Changer la langue de l'interface"""
    if language not in ["en", "fr"]:
        language = DEFAULT_LANGUAGE

    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(
        key="lang",
        value=language,
        max_age=31536000,  # 1 an
        httponly=True,
        samesite="lax"
    )
    return response

@app.get("/health")
async def health():
    """Healthcheck"""
    return {"status": "ok"}

@app.get("/search")
async def search(request: Request, q: str = ""):
    """Recherche dans les pages"""
    if not q:
        return RedirectResponse("/")
    
    results = []
    query = q.lower()
    
    for md_file in CONTENT_DIR.glob("*.md"):
        post = frontmatter.load(md_file)
        content = post.content.lower()
        title = post.get("title", "").lower()
        
        if query in title or query in content:
            results.append({
                "slug": md_file.stem,
                "title": post.get("title", md_file.stem.title()),
                "description": post.get("description", ""),
                "snippet": content[:200] + "..."
            })
    
    return templates.TemplateResponse("search.html", {
        "request": request,
        "query": q,
        "results": results,
        "title": f"Recherche: {q}"
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)