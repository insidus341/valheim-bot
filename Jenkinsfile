pipeline {
  agent {
    dockerfile true
  }
  
  environment {
    DISCORD_TOKEN = credentials('DISCORD_TOKEN')
    SERVER_IP     = 0.0.0.0
    SERVER_PORT   = 2456
  }
  
  stages{
    stage('Example') {
      steps {
        echo "hello world 2"
      }
    }
  }
}
