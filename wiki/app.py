"""
Wiki - Documentation pour les étudiants
Technologies de Containérisation
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import markdown
import frontmatter
from pathlib import Path
from typing import Dict, List
import os

app = FastAPI(title="Wiki - Containérisation")

# Configuration
CONTENT_DIR = Path("content")
STATIC_DIR = Path("static")

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
async def home(request: Request):
    """Page d'accueil"""
    pages = get_all_pages()
    
    # Grouper par catégorie
    categories = {}
    for page in pages:
        cat = page["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(page)
    
    return templates.TemplateResponse("home.html", {
        "request": request,
        "categories": categories,
        "title": "Documentation - Containérisation"
    })

@app.get("/page/{page_name}", response_class=HTMLResponse)
async def show_page(request: Request, page_name: str):
    """Afficher une page"""
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
        "all_pages": all_pages
    })

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