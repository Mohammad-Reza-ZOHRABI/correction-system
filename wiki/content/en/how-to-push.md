---
title: "How to Push"
description: "Complete guide to submit your project via Git"
order: 2
category: "🚀 Getting Started"
---

# How to Push

This guide explains in detail how to submit your project to Gitea with Git.

## 📋 Prerequisites

Before getting started, make sure you have:

- ✅ Git installed on your machine
- ✅ Your Gitea account created
- ✅ Repository cloned locally

### Verify Git is Installed

```bash
git --version
# Expected result: git version 2.x.x
```

If Git is not installed:

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install git
```

**macOS:**
```bash
brew install git
```

**Windows:**
Download from: https://git-scm.com/download/win

## 🔧 Initial Git Configuration

### Configure Your Identity

```bash
# Your name
git config --global user.name "Jean Dupont"

# Your email
git config --global user.email "jean.dupont@students.zohrabi.cloud"

# Verify configuration
git config --list
```

## 📥 Clone Your Repository

### First Time: Cloning

```bash
# Replace with YOUR username and group
git clone https://git.zohrabi.cloud/Groupe-A/jean.dupont-tds.git

# Enter the folder
cd jean.dupont-tds
```

During cloning, Git will ask you:
- **Username**: `jean.dupont`
- **Password**: your Gitea password

## 🏗️ Complete Submission Workflow

### Step 1: Create/Modify Your Files

Create your project in the cloned folder:

```bash
# Example: Create necessary files
touch Dockerfile
touch docker-compose.yml
mkdir app
touch app/index.html
```

### Step 2: Check Git Status

```bash
# See modified files
git status
```

Result:
```
On branch main
Untracked files:
  (use "git add <file>..." to include in what will be committed)
	Dockerfile
	docker-compose.yml
	app/

nothing added to commit but untracked files present
```

### Step 3: Add Files to Staging

```bash
# Add all files
git add .

# OR add specific files
git add Dockerfile docker-compose.yml app/
```

Verify again:
```bash
git status
```

Result:
```
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	new file:   Dockerfile
	new file:   docker-compose.yml
	new file:   app/index.html
```

### Step 4: Create a Commit

```bash
# Commit with a descriptive message
git commit -m "TD1: Web application with Nginx"
```

**Best practices for commit messages:**

✅ **GOOD**:
```bash
git commit -m "TD1: Web application with Nginx and Docker Compose"
git commit -m "Add healthcheck in Dockerfile"
git commit -m "Fix: Incorrectly configured ports in compose.yml"
```

❌ **BAD**:
```bash
git commit -m "update"
git commit -m "fix"
git commit -m "test"
```

### Step 5: Push to Gitea

```bash
# Push to main branch
git push origin main
```

Git will ask for your Gitea credentials again.

## 🔄 Update Workflow

### After First Submission

If you modify your files after the first push:

```bash
# 1. Check modifications
git status

# 2. Add modifications
git add .

# 3. Commit
git commit -m "TD1: Dockerfile improvements"

# 4. Push
git push origin main
```

### Useful Commands

```bash
# See commit history
git log

# See differences before commit
git diff

# Undo file changes
git checkout -- Dockerfile

# See branches
git branch

# Fetch latest changes from Gitea
git pull origin main
```

## 📊 Verify the Push Worked

### In Your Terminal

After `git push`, you should see:

```
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using up to 8 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 345 bytes | 345.00 KiB/s, done.
Total 3 (delta 2), reused 0 (delta 0), pack-reused 0
remote: . Processing 1 references
remote: Processed 1 references in total
To https://git.zohrabi.cloud/Groupe-A/jean.dupont-tds.git
   abc1234..def5678  main -> main
```

### On Gitea

1. Go to https://git.zohrabi.cloud
2. Open your repository
3. Verify your files appear
4. Go to the **"Actions"** tab
5. You should see the correction workflow running

## 🚫 Common Problems and Solutions

### Problem 1: Authentication Fails

**Symptom:**
```
remote: Invalid username or password.
fatal: Authentication failed
```

**Solutions:**

1. Verify your username and password
2. If you changed your password, use the new one
3. Try logging back in at https://git.zohrabi.cloud

### Problem 2: Merge Conflict

**Symptom:**
```
error: failed to push some refs to 'https://git.zohrabi.cloud/...'
hint: Updates were rejected because the remote contains work that you do not have locally.
```

**Solution:**
```bash
# Fetch remote changes
git pull origin main

# Resolve conflicts if necessary
# Then push again
git push origin main
```

### Problem 3: Untracked Files

**Symptom:**
Your files don't appear after `git status`

**Solution:**
```bash
# Verify you're in the right folder
pwd

# List all files
ls -la

# Add explicitly
git add Dockerfile docker-compose.yml
```

### Problem 4: .gitignore Blocks Files

**Symptom:**
Certain files are never added

**Solution:**

Create/modify `.gitignore`:
```bash
# Files to ignore
node_modules/
*.log
.env
.DS_Store

# But DO NOT ignore necessary files:
# !Dockerfile
# !docker-compose.yml
```

## 🔐 SSH Authentication (Advanced)

To avoid typing your password every time:

### Step 1: Generate SSH Key

```bash
ssh-keygen -t ed25519 -C "jean.dupont@students.zohrabi.cloud"
# Press Enter to accept all defaults
```

### Step 2: Copy Public Key

```bash
cat ~/.ssh/id_ed25519.pub
```

Copy all displayed content.

### Step 3: Add Key to Gitea

1. Go to https://git.zohrabi.cloud
2. **Settings** → **SSH/GPG Keys**
3. **Add a key**
4. Paste the public key
5. Give it a name (ex: "My PC")
6. Save

### Step 4: Change Remote URL

```bash
# See current URL
git remote -v

# Change to SSH
git remote set-url origin git@git.zohrabi.cloud:Groupe-A/jean.dupont-tds.git

# Verify
git remote -v
```

Now, `git push` won't ask for a password anymore!

## 📝 Checklist Before Each Push

Before doing `git push`, verify:

- [ ] ✅ Project tested **locally**
- [ ] ✅ `docker compose up` works
- [ ] ✅ No unnecessary files (node_modules, etc.)
- [ ] ✅ No secrets/passwords in plain text
- [ ] ✅ Required files present (Dockerfile, docker-compose.yml)
- [ ] ✅ Descriptive commit message
- [ ] ✅ `git status` verified

## 📚 Essential Git Commands (Summary)

```bash
# Initial configuration
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# Clone a repository
git clone https://git.zohrabi.cloud/Groupe-A/username-tds.git

# Check status
git status

# Add files
git add .                    # All files
git add Dockerfile          # Specific file

# Create a commit
git commit -m "Descriptive message"

# Push to Gitea
git push origin main

# Pull (fetch changes)
git pull origin main

# See history
git log

# See differences
git diff

# Undo changes
git checkout -- file
```

## 🎯 Complete Example A to Z

```bash
# 1. Clone (first time only)
git clone https://git.zohrabi.cloud/Groupe-A/jean.dupont-tds.git
cd jean.dupont-tds

# 2. Create your project
echo "FROM nginx:alpine" > Dockerfile
echo "version: '3.8'" > docker-compose.yml

# 3. Test locally
docker compose up -d
docker compose ps
docker compose down

# 4. Add to Git
git add .

# 5. Commit
git commit -m "TD1: First Docker project"

# 6. Push
git push origin main

# 7. Verify on Gitea
# Go to https://git.zohrabi.cloud > Your repo > Actions
```

## 🆘 Need Help?

- 📖 Check the [FAQ](/page/faq)
- 💡 [Official Git Guide](https://git-scm.com/book/en/v2)
- 📧 Contact: admin@zohrabi.cloud

---

**Happy pushing! 🚀**