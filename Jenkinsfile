pipeline {
  agent any

  environment {
    DOCKERHUB_CREDENTIALS = 'dockerhub-credentials' // Replace with your Jenkins credential ID
    DOCKERHUB_REPO = 'mricognito/flask-app' // Replace with your Docker Hub repo
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
          // Create a temporary Dockerfile that copies everything needed
          writeFile file: 'Dockerfile.ci', text: '''
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \\
    build-essential \\
    default-libmysqlclient-dev \\
  && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY web/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application and tests
COPY web /app/web
COPY tests /app/tests

# Add web module to Python path
ENV PYTHONPATH=/app

EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "web.app:app"]
'''
          IMAGE = docker.build("${DOCKERHUB_REPO}:${env.BUILD_NUMBER}", "-f Dockerfile.ci .")
        }
      }
    }

    stage('Run Tests') {
      steps {
        script {
          sh """
docker run --rm \
  -e DB_HOST=db \
  -e DB_USER=exampleuser \
  -e DB_PASSWORD=examplepass \
  -e DB_NAME=exampledb \
  ${DOCKERHUB_REPO}:${env.BUILD_NUMBER} \
  sh -c "cd /app && pytest -v tests/"
"""

        }
      }
    }


    stage('Push to Docker Hub') {
      steps {
        script {
          docker.withRegistry('https://registry.hub.docker.com', DOCKERHUB_CREDENTIALS) {
            IMAGE.push()
            IMAGE.push('latest')
          }
        }
      }
    }

    stage('Optional Deploy') {
      steps {
        echo 'Add deploy steps here (e.g., SSH to server and run docker run)'
      }
    }
  }

  post {
    always {
      cleanWs()
    }
  }
}
