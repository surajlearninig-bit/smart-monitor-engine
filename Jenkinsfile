pipeline {
    agent any 

    environment { 
       DOCKER_COMPOSE_PROJECT = "smart_monitor"
    }

    stages {
        stage('checkout code') {
            steps { 
                checkout scm
                echo "code checked out from github successfully."
            }
        }
        
        stage('Cleanup Old Containers') {
           steps {
               echo 'Cleaning up previous deployment...'
               sh 'docker compose down --remove-orphans'
           }
       }

        stage('build & run services') {
            steps { 
              echo 'building and starting services ...'
              sh 'docker compose up -d --build'
           }
       }
     
        stage('health check & integration test') {
          steps {
              echo 'waiting for services to be ready....'

              sleep 10 

             script {
                  def response = sh(script: "curl -s http://localhost:8000/test-db", returnStdout: true).trim()
                  echo "DB Test Response : ${response}"
                  if (!response.contains("Connected")) {
                     error "PostgrlSQL Health Check Failed!" 
                  }

                  def redisResponse = sh(script: "curl -s http://localhost:8000/test-redis", returnStdout: true).trim()
                  echo "Redis Test Response: ${redisResponse}"
                  if (!redisResponse.contains("Connected")) {
                     error "Redis Health Check Failed!"
                  }
              }
          }
     }
    }

post {
    success {
        echo 'deployment is stable and runnnig.'
    }
    failure {
        echo 'health check failed! cleaning up broken deployment...'
        sh 'docker compose down '
    }
  always {
     echo 'pipeline finished. cleaninig up unused Docker images....'
       
    }
  }
}
