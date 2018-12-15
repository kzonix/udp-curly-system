properties([
  buildDiscarder(
    logRotator(
      artifactDaysToKeepStr: '1', 
      artifactNumToKeepStr: '2', 
      daysToKeepStr: '1', 
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
