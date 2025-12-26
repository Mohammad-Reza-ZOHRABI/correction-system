"""
Dashboard de suivi des notes - Technologies de Containérisation
Authentification via OAuth2 Gitea
Support multilingue (EN/FR)
"""

from fastapi import FastAPI, Request, Depends, HTTPException, status, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from contextlib import asynccontextmanager
import os
import httpx
from datetime import datetime, timedelta
from typing import Optional
import secrets
import json

# Configuration
DATABASE_URL = os.getenv("DATABASE_URL")
GITEA_URL = os.getenv("GITEA_URL", "http://gitea:3000")
OAUTH_CLIENT_ID = os.getenv("GITEA_OAUTH_CLIENT_ID")
OAUTH_CLIENT_SECRET = os.getenv("GITEA_OAUTH_CLIENT_SECRET")
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(32))
ALLOWED_TEAM = os.getenv("ALLOWED_TEAM", "Enseignants")
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "en")

# Charger les traductions
with open("translations.json", "r", encoding="utf-8") as f:
    TRANSLATIONS = json.load(f)

# Base de données
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Sessions utilisateur (simple, en mémoire)
user_sessions = {}

def get_translation(lang: str, key: str):
    """Récupère une traduction"""
    keys = key.split(".")
    value = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    for k in keys:
        value = value.get(k, key)
    return value

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestion du cycle de vie de l'application"""
    print("🚀 Démarrage du Dashboard...")
    yield
    print("🛑 Arrêt du Dashboard...")

app = FastAPI(
    title="Dashboard Grades - Containérisation",
    lifespan=lifespan
)

templates = Jinja2Templates(directory="templates")

# Dépendance: Récupérer la session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dépendance: Vérifier l'authentification
async def get_current_user(request: Request):
    """Vérifie si l'utilisateur est authentifié"""
    session_token = request.cookies.get("session_token")
    
    if not session_token or session_token not in user_sessions:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Non authentifié"
        )
    
    user_data = user_sessions[session_token]
    
    # Vérifier l'expiration
    if datetime.now() > user_data["expires_at"]:
        del user_sessions[session_token]
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expirée"
        )
    
    return user_data["user"]

# Routes d'authentification OAuth2
@app.get("/login")
async def login():
    """Redirige vers Gitea pour l'authentification"""
    redirect_uri = "https://grades.zohrabi.cloud/callback"
    state = secrets.token_urlsafe(32)
    
    auth_url = (
        f"{GITEA_URL}/login/oauth/authorize"
        f"?client_id={OAUTH_CLIENT_ID}"
        f"&redirect_uri={redirect_uri}"
        f"&response_type=code"
        f"&state={state}"
    )
    
    return RedirectResponse(auth_url)

@app.get("/callback")
async def callback(code: str, state: str):
    """Callback OAuth2 après authentification Gitea"""
    
    # Échange du code contre un token
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            f"{GITEA_URL}/login/oauth/access_token",
            data={
                "client_id": OAUTH_CLIENT_ID,
                "client_secret": OAUTH_CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": "https://grades.zohrabi.cloud/callback"
            }
        )
        
        if token_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Échec de l'authentification")
        
        token_data = token_response.json()
        access_token = token_data.get("access_token")
        
        # Récupérer les infos utilisateur
        user_response = await client.get(
            f"{GITEA_URL}/api/v1/user",
            headers={"Authorization": f"token {access_token}"}
        )
        
        user_info = user_response.json()
        
        # Vérifier si l'utilisateur est dans l'équipe "Enseignants"
        teams_response = await client.get(
            f"{GITEA_URL}/api/v1/user/teams",
            headers={"Authorization": f"token {access_token}"}
        )

        teams = teams_response.json()
        is_teacher = any(team.get("name") == ALLOWED_TEAM for team in teams)

        # Créer une session
        session_token = secrets.token_urlsafe(32)
        user_sessions[session_token] = {
            "user": {
                "id": user_info["id"],
                "username": user_info["login"],
                "email": user_info["email"],
                "full_name": user_info.get("full_name", user_info["login"]),
                "is_teacher": is_teacher
            },
            "expires_at": datetime.now() + timedelta(hours=8)
        }
        
        # Rediriger vers le dashboard
        response = RedirectResponse(url="/", status_code=302)
        response.set_cookie(
            key="session_token",
            value=session_token,
            httponly=True,
            max_age=28800,  # 8 heures
            samesite="lax"
        )
        return response

@app.get("/logout")
async def logout(request: Request):
    """Déconnexion"""
    session_token = request.cookies.get("session_token")
    if session_token in user_sessions:
        del user_sessions[session_token]
    
    response = RedirectResponse(url="/login")
    response.delete_cookie("session_token")
    return response

# Routes principales
@app.get("/", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    lang: Optional[str] = Cookie(default=DEFAULT_LANGUAGE),
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Page principale du dashboard"""
    
    # Valider la langue
    if lang not in ["en", "fr"]:
        lang = DEFAULT_LANGUAGE
    
    # Récupérer les statistiques globales avec tentatives
    stats_query = text("""
        SELECT 
            COUNT(DISTINCT s.id) as total_etudiants,
            COUNT(DISTINCT a.id) as total_tds,
            COUNT(sub.id) as total_soumissions,
            COALESCE(AVG(g.note), 0) as note_moyenne_globale,
            COALESCE(AVG(am.nb_tentatives), 0) as avg_attempts
        FROM students s
        CROSS JOIN assignments a
        LEFT JOIN submissions sub ON s.id = sub.student_id
        LEFT JOIN grades g ON sub.id = g.submission_id
        LEFT JOIN activity_metrics am ON s.id = am.student_id AND a.id = am.assignment_id
    """)
    
    stats = db.execute(stats_query).fetchone()
    
    # Récupérer les groupes
    groupes_query = text("SELECT DISTINCT groupe FROM students ORDER BY groupe")
    groupes = [row[0] for row in db.execute(groupes_query).fetchall()]
    
    # Récupérer les TDs
    tds_query = text("SELECT id, code, nom FROM assignments ORDER BY code")
    tds = db.execute(tds_query).fetchall()
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
        "stats": stats,
        "groupes": groupes,
        "tds": tds,
        "lang": lang,
        "t": lambda key: get_translation(lang, key)
    })

@app.get("/api/group/{groupe}", response_class=JSONResponse)
async def get_group_data(
    groupe: str,
    lang: Optional[str] = Cookie(default=DEFAULT_LANGUAGE),
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """API: Récupérer les données d'un groupe avec tentatives"""
    
    query = text("""
        SELECT 
            s.id as student_id,
            s.prenom,
            s.nom,
            s.email,
            a.code as td_code,
            MAX(g.note) as meilleure_note,
            COUNT(sub.id) as nb_tentatives,
            5 - COUNT(sub.id) as tentatives_restantes,
            CASE WHEN COUNT(sub.id) >= 5 THEN true ELSE false END as max_atteint,
            MAX(sub.submitted_at) as derniere_soumission
        FROM students s
        CROSS JOIN assignments a
        LEFT JOIN submissions sub ON s.id = sub.student_id AND a.id = sub.assignment_id
        LEFT JOIN grades g ON sub.id = g.submission_id
        WHERE s.groupe = :groupe
        GROUP BY s.id, s.prenom, s.nom, s.email, a.id, a.code
        ORDER BY s.nom, s.prenom, a.code
    """)
    
    results = db.execute(query, {"groupe": groupe}).fetchall()
    
    return [
        {
            "student_id": r[0],
            "prenom": r[1],
            "nom": r[2],
            "email": r[3],
            "td_code": r[4],
            "note": float(r[5]) if r[5] else None,
            "tentatives": r[6],
            "tentatives_restantes": r[7],
            "max_atteint": r[8],
            "derniere_soumission": r[9].isoformat() if r[9] else None
        }
        for r in results
    ]

@app.get("/api/student/{student_id}/details", response_class=JSONResponse)
async def get_student_details(
    student_id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """API: Détails complets d'un étudiant"""
    
    query = text("""
        SELECT 
            sub.id,
            a.code,
            sub.commit_hash,
            sub.submitted_at,
            g.note,
            g.tests_passed,
            g.tests_total,
            g.rapport_html
        FROM submissions sub
        JOIN assignments a ON sub.assignment_id = a.id
        LEFT JOIN grades g ON sub.id = g.submission_id
        WHERE sub.student_id = :student_id
        ORDER BY sub.submitted_at DESC
    """)
    
    results = db.execute(query, {"student_id": student_id}).fetchall()
    
    return [
        {
            "submission_id": r[0],
            "td_code": r[1],
            "commit": r[2][:7],
            "date": r[3].isoformat(),
            "note": float(r[4]) if r[4] else None,
            "tests_passed": r[5],
            "tests_total": r[6],
            "rapport_html": r[7]
        }
        for r in results
    ]

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
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)