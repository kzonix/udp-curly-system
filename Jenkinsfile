properties([
  buildDiscarder(
    logRotator(
      artifactDaysToKeepStr: '2', 
      artifactNumToKeepStr: '2', 
      daysToKeepStr: '2', 
      numToKeepStr: '2',
    ),
  ),
])
pipeline {
  agent any
  stages {
    stage('Print Status') {
      steps {
        echo 'Done.'
      }
    }
    stage('Sleep') {
      steps {
        sleep 1
      }
    }
  }
}
