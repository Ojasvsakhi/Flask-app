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
      IMAGE = docker.build("${DOCKERHUB_REPO}:${env.BUILD_NUMBER}", "-f web/Dockerfile web")
    }
  }
}


    stage('Run Tests') {
  steps {
    script {
      IMAGE.inside('-v $WORKSPACE/tests:/app/tests -e DB_HOST=db -e DB_USER=exampleuser -e DB_PASSWORD=examplepass -e DB_NAME=exampledb') {
        sh 'pytest -q /app/tests'
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
