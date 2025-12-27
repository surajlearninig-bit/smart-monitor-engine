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
          
        stage('build images') {
            steps { 
                script {
                    def myTag = "v${env.BUILD_NUMBER}"
                    sh "APP_VERSION=${myTag} docker compose build"
                   }
               }
            }
            
           stage('securty scan (Trivy)') {
            steps { 
                script {
                    echo "scanning image for security vulnerability and genrating HTML report....."
                    def myTag = "v${env.BUILD_NUMBER}"
                     sh "trivy image --format template --template '@/usr/local/share/trivy/templates/html.tpl' --output report.html smart-monitor-backend:${myTag}"
                     sh "trivy image --exit-code 1 --severity CRITICAL smart-monitor-backend:${myTag}"
                   
                }
            }
        }
        
        stage('deploy / run service')  {
           steps {
             script {
                     def myTag = "v${env.BUILD_NUMBER}"
                     sh "APP_VERSION=${myTag} docker compose up -d "
                     }
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
                     error "PostgreSQL Health Check Failed!" 
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
    always {
     echo 'pipeline finished. cleaninig up unused Docker images....'
     archiveArtifacts artifacts:'report.html', fingerprint: true
    }
    success {
        echo 'deployment is stable and runnnig.'
    }
    failure {
        echo 'health check failed! cleaning up broken deployment...'
        sh 'docker compose down '
    }
 
       
    }
  }
