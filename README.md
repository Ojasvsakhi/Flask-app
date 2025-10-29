# Flask + MySQL (docker-compose) + Jenkins CI example

This repository contains a simple Python Flask web application and a MySQL service defined with Docker Compose, plus a Jenkins pipeline that builds, tests, and pushes a Docker image to Docker Hub.

Quick contents
- `docker-compose.yml` - defines `web` and `db` services and a user network/volume
- `web/` - Flask app, `Dockerfile`, and `requirements.txt`
- `Jenkinsfile` - declarative Jenkins pipeline to build, test, and push image
- `tests/` - pytest test(s)

Run locally with Docker Compose

1. From the repository root, start both services:

```powershell
docker-compose up --build
```

2. Open http://localhost:5000/ to see the Flask app. The app will attempt to connect to the MySQL container using the environment variables defined in `docker-compose.yml`.

Notes on CI/CD with GitHub and Jenkins

- Create a GitHub repository and push this project there.
- Configure a webhook in GitHub to notify your Jenkins server on push events.
- In Jenkins, create a pipeline job pointing to your Git repository or use Multibranch Pipeline.
- Add a Jenkins credential (Username with password) and give it the ID `dockerhub-credentials` (or update `Jenkinsfile` with your credential ID). The username/password should be your Docker Hub credentials.
- Update `DOCKERHUB_REPO` in the `Jenkinsfile` to your Docker Hub repository (e.g., `myuser/flask-mysql-demo`).

Security & placeholders
- Do NOT commit real credentials. Replace placeholder values in `Jenkinsfile` and in your Jenkins configuration.

Optional: Deploy stage

You can implement a deploy stage that logs into a target server (via SSH) and runs `docker pull` + `docker run` or uses docker-compose on the target.

Troubleshooting
- If MySQL isn't ready when Flask first tries to connect, the app will report a failed DB connection; `docker-compose` `depends_on` only controls start order, not readiness. Consider adding an init script or healthchecks for production.
