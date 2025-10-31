pipeline {
  agent any

  environment {
    DOCKERHUB_CREDENTIALS = 'dockerhub-credentials'
    DOCKERHUB_REPO = 'mricognito/flask-app'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Image') {
      steps {
        script {
          writeFile file: 'Dockerfile.ci', text: '''
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
  && rm -rf /var/lib/apt/lists/*

COPY web/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY web /app/web
COPY tests /app/tests

ENV PYTHONPATH=/app

EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "web.app:app"]
'''
          def imageTag = "${DOCKERHUB_REPO}:${env.BUILD_NUMBER}"
          bat "docker build -f Dockerfile.ci -t ${imageTag} ."
        }
      }
    }

    stage('Run Tests') {
      steps {
        script {
          def imageTag = "${DOCKERHUB_REPO}:${env.BUILD_NUMBER}"
          bat """
          docker run --rm ^
            -e DB_HOST=db ^
            -e DB_USER=exampleuser ^
            -e DB_PASSWORD=examplepass ^
            -e DB_NAME=exampledb ^
            ${imageTag} sh -c "cd /app && pytest -v tests/"
          """
        }
      }
    }

    stage('Push to Docker Hub') {
      steps {
        script {
          def imageTag = "${DOCKERHUB_REPO}:${env.BUILD_NUMBER}"
          docker.withRegistry('https://registry.hub.docker.com', DOCKERHUB_CREDENTIALS) {
            bat "docker push ${imageTag}"
            bat "docker tag ${imageTag} ${DOCKERHUB_REPO}:latest"
            bat "docker push ${DOCKERHUB_REPO}:latest"
          }
        }
      }
    }

    stage('Deploy') {
      steps {
        echo 'Deployment Steps'
      }
    }
  }

  post {
    always {
      cleanWs()
    }
  }
}
