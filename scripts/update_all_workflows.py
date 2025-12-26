#!/usr/bin/env python3
"""
Script pour mettre à jour le workflow de correction dans tous les repositories étudiants
Ajoute la vérification de la limite de 5 tentatives
"""

import requests
import sys
import time
from typing import List, Dict

# Configuration
GITEA_URL = "https://git.zohrabi.cloud"
GITEA_ADMIN_TOKEN = ""  # À remplir avec votre token admin
WORKFLOW_FILE_PATH = ".gitea/workflows/correction.yml"

# Nouveau contenu du workflow (avec limitation de tentatives)
NEW_WORKFLOW_CONTENT = """
# Workflow de correction automatique v2.0.0
# Avec limitation à 5 tentatives par TD

name: Automatic Correction

on:
  push:
    branches:
      - main
      - master

jobs:
  correction:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    
    steps:
      - name: 🔍 Check Attempts Limit
        id: check_attempts
        env:
          POSTGRES_HOST: postgres
          POSTGRES_DB: grades
          POSTGRES_USER: gitea
          POSTGRES_PASSWORD: gitea_secure_password_2024
        run: |
          echo "=== Checking attempts limit ==="
          
          apt-get update && apt-get install -y postgresql-client
          
          STUDENT_USERNAME="${{ github.actor }}"
          ASSIGNMENT_CODE="TD1"  # À adapter selon le TD
          
          REMAINING=$(PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DB -t -c "
            SELECT get_remaining_attempts(
              (SELECT id FROM students WHERE gitea_username = '$STUDENT_USERNAME'),
              (SELECT id FROM assignments WHERE code = '$ASSIGNMENT_CODE')
            );
          " | xargs)
          
          echo "attempts_remaining=$REMAINING" >> $GITHUB_OUTPUT
          
          if [ "$REMAINING" -le 0 ]; then
            echo "❌ Maximum attempts reached (5/5)"
            echo "max_attempts_reached=true" >> $GITHUB_OUTPUT
            exit 1
          else
            echo "✅ Attempts remaining: $REMAINING/5"
            echo "max_attempts_reached=false" >> $GITHUB_OUTPUT
          fi
      
      # ... (reste du workflow identique)
"""

def get_all_student_repos() -> List[Dict]:
    """Récupère tous les repositories étudiants"""
    headers = {
        "Authorization": f"token {GITEA_ADMIN_TOKEN}",
        "Content-Type": "application/json"
    }
    
    all_repos = []
    
    # Récupérer toutes les organisations (groupes)
    orgs_response = requests.get(
        f"{GITEA_URL}/api/v1/orgs",
        headers=headers
    )
    
    if orgs_response.status_code != 200:
        print(f"❌ Erreur récupération organisations: {orgs_response.status_code}")
        return []
    
    orgs = orgs_response.json()
    
    # Pour chaque organisation, récupérer les repos
    for org in orgs:
        org_name = org["username"]
        
        # Ignorer l'organisation "Administration" (enseignants)
        if org_name == "Administration":
            continue
        
        print(f"📁 Organisation: {org_name}")
        
        repos_response = requests.get(
            f"{GITEA_URL}/api/v1/orgs/{org_name}/repos",
            headers=headers
        )
        
        if repos_response.status_code == 200:
            repos = repos_response.json()
            for repo in repos:
                # Filtrer les repos étudiants (format: nom-tds)
                if "-tds" in repo["name"]:
                    all_repos.append({
                        "owner": org_name,
                        "name": repo["name"],
                        "full_name": repo["full_name"]
                    })
    
    return all_repos

def check_workflow_exists(owner: str, repo_name: str) -> bool:
    """Vérifie si le workflow existe déjà"""
    headers = {
        "Authorization": f"token {GITEA_ADMIN_TOKEN}"
    }
    
    response = requests.get(
        f"{GITEA_URL}/api/v1/repos/{owner}/{repo_name}/contents/{WORKFLOW_FILE_PATH}",
        headers=headers
    )
    
    return response.status_code == 200

def get_file_sha(owner: str, repo_name: str, file_path: str) -> str:
    """Récupère le SHA d'un fichier existant"""
    headers = {
        "Authorization": f"token {GITEA_ADMIN_TOKEN}"
    }
    
    response = requests.get(
        f"{GITEA_URL}/api/v1/repos/{owner}/{repo_name}/contents/{file_path}",
        headers=headers
    )
    
    if response.status_code == 200:
        return response.json().get("sha", "")
    return ""

def update_workflow(owner: str, repo_name: str, workflow_content: str) -> bool:
    """Met à jour le workflow dans un repository"""
    headers = {
        "Authorization": f"token {GITEA_ADMIN_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Lire le workflow depuis un fichier template
    try:
        with open(".gitea/workflows/correction.yml", "r") as f:
            workflow_content = f.read()
    except FileNotFoundError:
        print(f"⚠️  Fichier template non trouvé, utilisation du contenu par défaut")
        workflow_content = NEW_WORKFLOW_CONTENT
    
    # Vérifier si le fichier existe
    file_sha = get_file_sha(owner, repo_name, WORKFLOW_FILE_PATH)
    
    data = {
        "message": "Update: Add 5 attempts limit to correction workflow",
        "content": workflow_content,
        "branch": "main"
    }
    
    # Si le fichier existe, ajouter le SHA pour la mise à jour
    if file_sha:
        data["sha"] = file_sha
        print(f"  ↻ Mise à jour du workflow existant...")
    else:
        print(f"  + Création du workflow...")
    
    response = requests.put(
        f"{GITEA_URL}/api/v1/repos/{owner}/{repo_name}/contents/{WORKFLOW_FILE_PATH}",
        headers=headers,
        json=data
    )
    
    if response.status_code in [200, 201]:
        print(f"  ✅ Workflow mis à jour")
        return True
    else:
        print(f"  ❌ Erreur: {response.status_code} - {response.text}")
        return False

def main():
    if not GITEA_ADMIN_TOKEN:
        print("❌ Erreur: GITEA_ADMIN_TOKEN non défini")
        print("Récupérez un token admin depuis: Gitea > Settings > Applications > Generate Token")
        sys.exit(1)
    
    print("🚀 Mise à jour des workflows de correction")
    print("=" * 50)
    print()
    
    # Récupérer tous les repos étudiants
    print("📋 Récupération des repositories étudiants...")
    repos = get_all_student_repos()
    
    if not repos:
        print("⚠️  Aucun repository trouvé")
        sys.exit(0)
    
    print(f"✅ {len(repos)} repositories trouvés")
    print()
    
    # Confirmation
    print("⚠️  Cette opération va mettre à jour le workflow dans TOUS les repositories étudiants")
    response = input("Continuer ? (y/n): ")
    
    if response.lower() != 'y':
        print("❌ Opération annulée")
        sys.exit(0)
    
    print()
    print("🔄 Mise à jour en cours...")
    print()
    
    # Statistiques
    success_count = 0
    failed_count = 0
    failed_repos = []
    
    # Mettre à jour chaque repository
    for i, repo in enumerate(repos, 1):
        print(f"[{i}/{len(repos)}] {repo['full_name']}")
        
        if update_workflow(repo['owner'], repo['name'], NEW_WORKFLOW_CONTENT):
            success_count += 1
        else:
            failed_count += 1
            failed_repos.append(repo['full_name'])
        
        # Pause pour éviter le rate limiting
        time.sleep(0.5)
        print()
    
    # Résumé
    print()
    print("=" * 50)
    print("📊 Résumé de la mise à jour")
    print("=" * 50)
    print(f"✅ Succès: {success_count}/{len(repos)}")
    print(f"❌ Échecs: {failed_count}/{len(repos)}")
    
    if failed_repos:
        print()
        print("❌ Repositories en échec:")
        for repo in failed_repos:
            print(f"  - {repo}")
    
    print()
    print("✅ Mise à jour terminée !")
    print()
    
    # Prochaines étapes
    print("📋 Prochaines étapes:")
    print("1. Vérifier manuellement quelques repositories")
    print("2. Tester avec un push sur un repository")
    print("3. Informer les étudiants de la limitation")
    print()

if __name__ == "__main__":
    main()