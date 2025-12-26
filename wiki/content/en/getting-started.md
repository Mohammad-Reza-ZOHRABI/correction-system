---
title: "Getting Started"
description: "Quick start guide to begin with the system"
order: 1
category: "🚀 Démarrage"
---

# Getting Started

Welcome to the automatic grading system! This guide explains how to get started quickly.

## 📧 1. Receiving your account

You will receive an email containing:

- **Username**: `firstname.lastname`
- **Temporary password**: To be changed on first login
- **Gitea link**: https://git.zohrabi.cloud
- **Your group**: Group-A, Group-B, etc.

## 🔑 2. First login

### Step 1: Access Gitea

1. Open your browser
2. Go to: **https://git.zohrabi.cloud**
3. Click **"Sign in"** in the top right

### Step 2: Login

1. **Username**: The one received by email
2. **Password**: The temporary password
3. Click **"Sign in"**

### Step 3: Change password

⚠️ **Important**: You will need to change your password on first login.

1. Choose a strong password (min. 8 characters)
2. Confirm the new password
3. Validate

## 📁 3. Access your repository

After logging in, you will see:

- **Organizations**: Your group (e.g., Group-A)
- **Repositories**: Your personal repository (e.g., `john.doe-tds`)

### Click on your repository

You will see the basic structure:
```
README.md
.gitea/
  └── workflows/
      └── correction.yml
```

The `correction.yml` file contains the automatic grading workflow (do not modify it).

## 💻 4. Clone your repository

### Option A: HTTPS (Recommended for beginners)

```bash
# Replace with your username
git clone https://git.zohrabi.cloud/Group-A/john.doe-tds.git

cd john.doe-tds
```

When cloning, Git will ask you for:
- **Username**: your Gitea username
- **Password**: your Gitea password

### Option B: SSH (Advanced)

**Prerequisites**: Have configured an SSH key in Gitea

1. Generate an SSH key (if you don't have one):
   ```bash
   ssh-keygen -t ed25519 -C "your.email@example.com"
   ```

2. Copy the public key:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

3. In Gitea: **Settings → SSH/GPG Keys → Add Key**

4. Clone with SSH:
   ```bash
   git clone git@git.zohrabi.cloud:Group-A/john.doe-tds.git
   ```

## 🏗️ 5. Create your first project

### Minimum required structure

Your project must contain **at minimum**:

```
my-project/
├── Dockerfile              # Required
├── docker-compose.yml      # Required
├── app/                    # Your application files
│   └── index.html
└── README.md              # Recommended
```

### Example: Simple web application

**Dockerfile**:
```dockerfile
FROM nginx:alpine
COPY app/ /usr/share/nginx/html/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "80:80"
    networks:
      - frontend

networks:
  frontend:
```

**app/index.html**:
```html
<!DOCTYPE html>
<html>
<head>
    <title>My TD1 Project</title>
</head>
<body>
    <h1>Hello Docker!</h1>
    <p>My first containerized project</p>
</body>
</html>
```

## 📤 6. Submit your project

### Verify everything works locally

**Before pushing**, test locally:

```bash
# Build
docker compose build

# Start
docker compose up -d

# Test
curl http://localhost
# OR open http://localhost in a browser

# Check logs
docker compose logs

# Stop
docker compose down
```

### Git: Add, Commit, Push

Once everything works:

```bash
# Add all files
git add .

# Commit with a descriptive message
git commit -m "TD1: Web application with Nginx"

# Push to Gitea
git push origin main
```

## ✅ 7. Automatic grading

### Triggering

As soon as you do `git push`, automatic grading starts:

1. **Gitea Actions** detects the push
2. The **grading workflow** starts
3. Tests and evaluation of your project
4. **Email sent** with your grade

### Follow grading in real-time

1. Go to Gitea
2. Open your repository
3. Click on the **"Actions"** tab
4. View the running workflow

You will see:
- ✅ **Running**: Grading in progress
- ✅ **Success**: Grading completed successfully
- ❌ **Failure**: Error detected

### View the report

You will receive an **email** containing:

- 📊 **Your grade** out of 100
- 📋 **Detailed report** in HTML
- ✅ **Points obtained** by criterion
- 📝 **Logs** of the grading
- 💡 **Improvement tips**

## 🔄 8. Iterate and improve

You can submit **multiple times**:

- The **best grade** is kept
- Each push triggers a new grading
- Check the logs to understand errors

```bash
# Modify your files
nano Dockerfile

# Test locally
docker compose up -d

# If OK, push again
git add .
git commit -m "TD1: Dockerfile improvement"
git push origin main
```

## 📌 Important points

### ✅ TO DO

- ✅ Test **locally** before pushing
- ✅ Use **official images**
- ✅ Follow the **required structure**
- ✅ Document with a **README.md**
- ✅ **Descriptive** commit messages

### ❌ TO AVOID

- ❌ Push without local testing
- ❌ Images without specific tags
- ❌ Passwords in plain text
- ❌ Unnecessary files (node_modules, etc.)

## 🆘 Need help?

- 📖 Check the [FAQ](/page/faq)
- 💡 See [Project Examples](/page/project-examples)
- 📧 Contact: admin@zohrabi.cloud

---

**Ready to start? Good luck! 🚀**