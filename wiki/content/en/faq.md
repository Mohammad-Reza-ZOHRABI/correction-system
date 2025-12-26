---
title: "FAQ - Frequently Asked Questions"
description: "Answers to the most common questions"
order: 10
category: "❓ Aide"
---

# FAQ - Frequently Asked Questions

## 🔐 Authentication and Access

### I didn't receive my credentials

Check your spam folder. If you still can't find the email, contact your instructor at **Reza@zohrabi.fr**.

### I forgot my password

Currently, you need to contact your instructor to reset your password. Send an email to **Reza@zohrabi.fr** with your username.

### My account is locked

After 3 failed login attempts, your account may be temporarily locked. Wait 15 minutes or contact your instructor.

## 📦 Git and Repository

### How do I clone my repository?

```bash
git clone https://git.zohrabi.cloud/YourGroup/your.name-tds.git
```

Replace `YourGroup` and `your.name` with your information.

### I can't push to my repository

Check that:
- You are properly authenticated (correct username/password)
- You have write permissions on the repository
- You are on the correct branch (`main` or `master`)

```bash
git remote -v  # Check the URL
git branch     # Check the branch
```

### Error: "fatal: unable to access"

This error usually means a connection problem. Check:
- Your internet connection
- The repository URL is correct
- Your credentials are correct

## 🐳 Docker and Containers

### Docker Compose won't start

Check:
1. The syntax of your `docker-compose.yml`
2. Ports are not already in use
3. Images are correctly specified

```bash
# Check syntax
docker compose config

# See error logs
docker compose logs
```

### Error: "port is already allocated"

Another service is already using this port. Solutions:
- Change the port in `docker-compose.yml`
- Stop the service using the port
- Use `docker ps` to see active containers

### How do I clean up Docker?

```bash
# Stop all containers
docker compose down

# Remove unused images
docker image prune -a

# Remove all volumes (WARNING: data loss)
docker volume prune
```

## ✅ Automatic Grading

### The grading doesn't trigger

Check that:
- You have done `git push`
- The file `.gitea/workflows/correction.yml` exists
- You haven't modified the workflow

Go to **Actions** on Gitea to see if the workflow has started.

### My grade is 0/100

Possible causes:
- Docker build failed
- The `docker-compose.yml` is invalid
- Required services don't start
- Tests don't pass

Check the detailed report in the email to understand the error.

### I didn't receive the email with my grade

Check:
- Your spam folder
- That the grading has finished (Actions tab)
- Your email address in Gitea (Settings > Profile)

If the problem persists after 30 minutes, contact your instructor.

### Can I submit multiple times?

Yes! You can push as many times as needed. The **best grade** will be kept for the final evaluation.

## 📝 Best Practices

### What project structure should I use?

Minimal structure:
```
my-project/
├── Dockerfile
├── docker-compose.yml
├── app/
│   └── (your files)
└── README.md
```

### Which Docker images should I use?

Prefer **official images**:
- `nginx:alpine`
- `node:18-alpine`
- `python:3.11-slim`
- `postgres:15-alpine`

Always specify a **version/tag** (not `latest`).

### How do I document my project?

Create a `README.md` with:
- Project title
- Description
- Technologies used
- Build and run instructions
- Author

## 🔍 Debugging

### Where can I see my container logs?

```bash
# Real-time logs
docker compose logs -f

# Logs for a specific service
docker compose logs -f web

# Last 100 lines
docker compose logs --tail=100
```

### How do I enter a container?

```bash
# For a running container
docker compose exec web sh

# Or with bash if available
docker compose exec web bash
```

### My application doesn't respond

Check:
1. The container is running: `docker compose ps`
2. The logs: `docker compose logs`
3. Port mapping is correct
4. The firewall allows the port

## 📊 Grades and Evaluation

### How is my grade calculated?

The grade is based on:
- Successful Docker build (20%)
- Services start correctly (30%)
- Functional tests (40%)
- Best practices (10%)

### Can I contest my grade?

Yes. Send an email to **Reza@zohrabi.fr** with:
- Your username
- The relevant commit
- A detailed explanation

### Where can I view my grades?

Go to **https://grades.zohrabi.cloud** and log in with your Gitea credentials.

## 🆘 Support

### I can't solve my problem

1. Check this FAQ
2. Review the documentation on [zohrabi.cloud](https://zohrabi.cloud)
3. Contact your instructor: **Reza@zohrabi.fr**

### Are services available 24/7?

Yes, all services (Gitea, Dashboard, Grading) are available 24/7.

In case of unavailability, a message will be displayed on the home page.

---

**Question not listed?** Contact **Reza@zohrabi.fr**