"""
Wiki - Documentation pour les étudiants
Technologies de Containérisation
"""

from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import markdown
import frontmatter
from pathlib import Path
from typing import Dict, List, Optional
import os
import json
from urllib.parse import urlparse

app = FastAPI(title="Wiki - Containérisation")

# Configuration
CONTENT_DIR = Path("content")
STATIC_DIR = Path("static")
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "en")
SUPPORTED_LANGUAGES = ["en", "fr"]
DOMAIN = os.getenv("WIKI_DOMAIN", "zohrabi.cloud")

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

def parse_accept_language(header: str) -> List[str]:
    """Parse Accept-Language header and return ordered list of language codes"""
    if not header:
        return []

    languages = []
    for lang in header.split(','):
        parts = lang.strip().split(';')
        code = parts[0].strip()
        quality = 1.0
        if len(parts) > 1 and parts[1].startswith('q='):
            try:
                quality = float(parts[1][2:])
            except ValueError:
                quality = 1.0
        languages.append((code, quality))

    # Sort by quality (highest first)
    languages.sort(key=lambda x: x[1], reverse=True)

    # Extract language codes and normalize (en-US -> en)
    return [lang[0].split('-')[0] for lang in languages]

def detect_language(request: Request, url_lang: Optional[str] = None) -> str:
    """
    Detect user's preferred language using industry best practices:
    1. URL path (if provided)
    2. Cookie (user's explicit choice)
    3. Accept-Language header (browser preference)
    4. Default language
    """
    # Priority 1: URL path language
    if url_lang and url_lang in SUPPORTED_LANGUAGES:
        return url_lang

    # Priority 2: Cookie (user's explicit choice)
    cookie_lang = request.cookies.get("lang")
    if cookie_lang and cookie_lang in SUPPORTED_LANGUAGES:
        return cookie_lang

    # Priority 3: Accept-Language header
    accept_language = request.headers.get("accept-language", "")
    accepted_langs = parse_accept_language(accept_language)
    for lang in accepted_langs:
        if lang in SUPPORTED_LANGUAGES:
            return lang

    # Priority 4: Default
    return DEFAULT_LANGUAGE

def generate_hreflang_links(request: Request, page_path: str = "") -> List[Dict[str, str]]:
    """Generate hreflang links for SEO"""
    hreflang_links = []

    for lang in SUPPORTED_LANGUAGES:
        url = f"https://{DOMAIN}/{lang}/{page_path}".rstrip('/')
        hreflang_links.append({
            "lang": lang,
            "url": url
        })

    # Add x-default for default language
    default_url = f"https://{DOMAIN}/{DEFAULT_LANGUAGE}/{page_path}".rstrip('/')
    hreflang_links.append({
        "lang": "x-default",
        "url": default_url
    })

    return hreflang_links

def get_translation(lang: str, key: str):
    """Récupère une traduction"""
    keys = key.split(".")
    value = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    for k in keys:
        value = value.get(k, key)
    return value

def get_page_content(page_name: str, lang: str = "en") -> Dict:
    """Charge le contenu d'une page markdown pour une langue donnée"""
    # Essayer d'abord avec la langue demandée
    page_path = CONTENT_DIR / lang / f"{page_name}.md"

    # Si le fichier n'existe pas dans cette langue, essayer avec la langue par défaut
    if not page_path.exists():
        page_path = CONTENT_DIR / DEFAULT_LANGUAGE / f"{page_name}.md"

    # Si toujours pas trouvé, retourner None
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

def get_all_pages(lang: str = "en") -> List[Dict]:
    """Liste toutes les pages disponibles pour une langue donnée"""
    pages = []

    # Chercher dans le répertoire de la langue
    lang_dir = CONTENT_DIR / lang

    if not lang_dir.exists():
        # Fallback à la langue par défaut
        lang_dir = CONTENT_DIR / DEFAULT_LANGUAGE

    if not lang_dir.exists():
        return pages

    for md_file in lang_dir.glob("*.md"):
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

# Redirect root to default language
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Redirect root to language-prefixed URL"""
    lang = detect_language(request)
    return RedirectResponse(url=f"/{lang}/", status_code=302)

# Language-prefixed home page
@app.get("/{lang}/", response_class=HTMLResponse)
async def home(request: Request, lang: str):
    """Page d'accueil avec préfixe de langue"""
    # Valider la langue
    if lang not in SUPPORTED_LANGUAGES:
        lang = DEFAULT_LANGUAGE
        return RedirectResponse(url=f"/{lang}/", status_code=302)

    pages = get_all_pages(lang)

    # Grouper par catégorie et traduire les noms de catégories
    categories = {}
    for page in pages:
        cat = page["category"]
        # Traduire le nom de la catégorie
        translated_cat = get_translation(lang, f"categories.{cat}")
        if translated_cat == f"categories.{cat}":
            translated_cat = cat

        if translated_cat not in categories:
            categories[translated_cat] = []
        categories[translated_cat].append(page)

    # Generate hreflang links
    hreflang_links = generate_hreflang_links(request, "")

    template_response = templates.TemplateResponse("home.html", {
        "request": request,
        "categories": categories,
        "lang": lang,
        "hreflang_links": hreflang_links,
        "current_url": f"https://{DOMAIN}/{lang}/",
        "t": lambda key: get_translation(lang, key)
    })

    # Set HTTP headers (best practice)
    template_response.headers["Content-Language"] = lang
    template_response.headers["Vary"] = "Accept-Language, Cookie"

    return template_response

# Language-prefixed page route
@app.get("/{lang}/page/{page_name}", response_class=HTMLResponse)
async def show_page(request: Request, lang: str, page_name: str):
    """Afficher une page avec préfixe de langue"""
    # Valider la langue
    if lang not in SUPPORTED_LANGUAGES:
        lang = DEFAULT_LANGUAGE
        return RedirectResponse(url=f"/{lang}/page/{page_name}", status_code=302)

    content = get_page_content(page_name, lang)

    if not content:
        return templates.TemplateResponse("404.html", {
            "request": request,
            "title": "Page non trouvée",
            "lang": lang
        }, status_code=404)

    # Liste des pages pour la navigation
    all_pages = get_all_pages(lang)

    # Generate hreflang links
    hreflang_links = generate_hreflang_links(request, f"page/{page_name}")

    template_response = templates.TemplateResponse("page.html", {
        "request": request,
        "title": content["title"],
        "description": content["description"],
        "content": content["content"],
        "all_pages": all_pages,
        "lang": lang,
        "hreflang_links": hreflang_links,
        "current_url": f"https://{DOMAIN}/{lang}/page/{page_name}",
        "page_name": page_name,
        "t": lambda key: get_translation(lang, key)
    })

    # Set HTTP headers (best practice)
    template_response.headers["Content-Language"] = lang
    template_response.headers["Vary"] = "Accept-Language, Cookie"

    return template_response

# Backward compatibility: redirect old URLs without language prefix
@app.get("/page/{page_name}", response_class=HTMLResponse)
async def redirect_old_page(request: Request, page_name: str):
    """Redirect old URLs to language-prefixed URLs"""
    lang = detect_language(request)
    return RedirectResponse(url=f"/{lang}/page/{page_name}", status_code=301)

# Language switcher endpoint
@app.get("/set-language/{language}")
async def set_language(request: Request, language: str):
    """Changer la langue de l'interface - stays on current page"""
    if language not in SUPPORTED_LANGUAGES:
        language = DEFAULT_LANGUAGE

    # Get referer to stay on same page
    referer = request.headers.get("referer", "/")
    if referer:
        parsed = urlparse(referer)
        path = parsed.path or "/"

        # Remove old language prefix if present
        for lang in SUPPORTED_LANGUAGES:
            if path.startswith(f"/{lang}/"):
                path = path[len(f"/{lang}"):]
                break

        # Add new language prefix
        redirect_url = f"/{language}{path}"
    else:
        redirect_url = f"/{language}/"

    response = RedirectResponse(url=redirect_url, status_code=302)
    response.set_cookie(
        key="lang",
        value=language,
        max_age=31536000,  # 1 year
        httponly=True,
        secure=os.getenv("ENVIRONMENT", "production") == "production",
        samesite="lax"
    )
    return response

@app.get("/health")
async def health():
    """Healthcheck"""
    return {"status": "ok"}

# Language-prefixed search
@app.get("/{lang}/search", response_class=HTMLResponse)
async def search(request: Request, lang: str, q: str = ""):
    """Recherche dans les pages"""
    if lang not in SUPPORTED_LANGUAGES:
        lang = DEFAULT_LANGUAGE

    if not q:
        return RedirectResponse(f"/{lang}/")

    results = []
    query = q.lower()

    # Chercher dans le répertoire de la langue
    lang_dir = CONTENT_DIR / lang
    if not lang_dir.exists():
        lang_dir = CONTENT_DIR / DEFAULT_LANGUAGE

    for md_file in lang_dir.glob("*.md"):
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

    template_response = templates.TemplateResponse("search.html", {
        "request": request,
        "query": q,
        "results": results,
        "title": f"Recherche: {q}",
        "lang": lang,
        "t": lambda key: get_translation(lang, key)
    })

    # Set HTTP headers (best practice)
    template_response.headers["Content-Language"] = lang
    template_response.headers["Vary"] = "Accept-Language, Cookie"

    return template_response

# Backward compatibility for old search
@app.get("/search")
async def redirect_old_search(request: Request, q: str = ""):
    """Redirect old search to language-prefixed search"""
    lang = detect_language(request)
    return RedirectResponse(url=f"/{lang}/search?q={q}", status_code=301)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)