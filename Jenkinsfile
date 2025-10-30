pipeline {
  agent any

  environment {
    DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials') // Replace with your Jenkins credential ID
    DOCKERHUB_REPO = 'mricognito/flask-app' // Replace with your Docker Hub repo
  }

  stages {
    stage('Debug Info') {
      steps {
        sh 'pwd && ls -la'
        sh 'docker info'
        sh 'docker images'
      }
    }
    
    stage('Checkout') {
      steps {
        checkout scm
        sh 'ls -la'  // Verify files after checkout
      }
    }

    stage('Build Image') {
      steps {
        script {
          // Show contents of important directories
          sh 'echo "Current directory contents:" && ls -la'
          sh 'echo "Web directory contents:" && ls -la web/'
          
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
          // Show the created Dockerfile
          sh 'cat Dockerfile.ci'
          
          // Build with detailed output
          def buildArgs = "-f Dockerfile.ci ."
          sh "echo 'Building with args: ${buildArgs}'"
          IMAGE = docker.build("${DOCKERHUB_REPO}:${env.BUILD_NUMBER}", buildArgs)
          
          // Verify the image was built
          sh "docker images | grep ${DOCKERHUB_REPO}"
        }
      }
    }

    stage('Run Tests') {
      steps {
        script {
          // Show available images before testing
          sh 'echo "Available Docker images:" && docker images'
          
          // Verify the image exists
          sh "docker inspect ${DOCKERHUB_REPO}:${env.BUILD_NUMBER}"
          
          // Run tests with more verbose output
          IMAGE.inside('-e DB_HOST=db -e DB_USER=exampleuser -e DB_PASSWORD=examplepass -e DB_NAME=exampledb') {
            sh '''
              echo "Container filesystem:"
              ls -la /app
              echo "Running tests..."
              cd /app && pytest -v tests/
            '''
          }
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
