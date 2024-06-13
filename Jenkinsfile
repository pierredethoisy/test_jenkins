pipeline {
    agent none
    stages {
        stage('Checkout') {
            agent any
            steps { 
                checkout scm
            }
        }
        stage('GitGuardian Scan') {
            agent {
                docker { 
                    image 'gitguardian/ggshield:latest'
                    args '-e HOME=${WORKSPACE}'       
                }
            }
            environment {
                GITGUARDIAN_API_KEY = credentials('gitguardian-api-key')
            }
            steps {
                script {
                    // Install curl using apt-get
                    sh 'apt-get update && apt-get install -y curl'

                    def status = sh(script: "ggshield secret scan repo . --json > ggshield_output.json", returnStatus: true)
                    def output = readFile('ggshield_output.json')
                    echo "ggshield_output.json content: ${output}"
                    
                    if (status == 0) {
                        echo "No secrets found"
                    } else if (status == 1) {
                        parseAndHandleOutput(output)
                    }
                }
            }
        }
    }
}

@NonCPS
def parseAndHandleOutput(String output) {
    def jsonSlurper = new groovy.json.JsonSlurper()
    def parsedOutput = jsonSlurper.parseText(output)
    
    parsedOutput.scans.each { scan -> 
        echo "Scan ID: ${scan.id}"
        scan.entities_with_incidents.each { entity ->
            entity.incidents.each { incident ->
                echo "Incident ID: ${incident.incident_url}"
                def incidentUrlParts = incident.incident_url.split('/')[-1]
                echo "Incident URL Part: ${incidentUrlParts}"
                
                // Call the API using curl and print the response
                def response = callGitGuardianAPI(incidentUrlParts)
                echo "HTTP Request Response: ${response}"
            }
        }
    }
}

@NonCPS
def callGitGuardianAPI(String incidentUrlParts) {
    def apiUrl = "https://api.gitguardian.com/v1/incidents/secrets/${incidentUrlParts}"
    def token = env.GITGUARDIAN_API_KEY
    def response = sh(
        script: """curl -s -H "Authorization: Token ${token}" "${apiUrl}" """,
        returnStdout: true
    ).trim()
    return response
}
