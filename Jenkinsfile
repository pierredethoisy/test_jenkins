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
                    def status = sh(script: "ggshield secret scan repo . --json > ggshield_output.json", returnStatus: true)
                    def output = readFile('ggshield_output.json')
                    def limitDate = $(date -d "2024-07-01"" +%s)
                    echo "ggshield_output.json content: ${output}"
                    
                    if (status == 0) {
                        echo "No secrets found"
                    } else if (status == 1) {
                        def incidents = parseOutput(output)
                        if (incidents.size() > 0) {
                            incidents.each { incidentUrlPart ->
                                def response = callGitGuardianAPI(incidentUrlPart)
                                def jsonResponse = new groovy.json.JsonSlurper().parseText(response.content)
                                def incidentDate = $(date -d "${jsonResponse.date}" +%s)
                                if ($limitDate -lt $incidentDate) {
                                    def error_status = 1
                                    echo "Date is after July 1st"
                                    echo $incidentDate 
                                }
                            }
                            error "Secrets detected in the repository. Failing the pipeline."
                        }
                    }
                }
            }
        }
    }
}

@NonCPS
def parseOutput(String output) {
    def jsonSlurper = new groovy.json.JsonSlurper()
    def parsedOutput = jsonSlurper.parseText(output)
    def incidentUrlPartsList = []

    parsedOutput.scans.each { scan -> 
        echo "Scan ID: ${scan.id}"
        scan.entities_with_incidents.each { entity ->
            entity.incidents.each { incident ->
                echo "Incident ID: ${incident.incident_url}"
                def incidentUrlParts = incident.incident_url.split('/')[-1]
                echo "Incident URL Part: ${incidentUrlParts}"
                incidentUrlPartsList << incidentUrlParts
            }
        }
    }
    return incidentUrlPartsList
}

def callGitGuardianAPI(String incidentUrlParts) {
    return httpRequest(
        url: "https://api.gitguardian.com/v1/incidents/secrets/${incidentUrlParts}",
        customHeaders: [[name: 'Authorization', value: "Token ${env.GITGUARDIAN_API_KEY}"]],
        validResponseCodes: '200'
    )
}
