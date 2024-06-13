pipeline {
    agent none
    stages {
        stage('Checkout') {
            agent any
            steps { 
                checkout }
            }
        }
        stage('GitGuardian Scan') {
            agent {
                docker { image 'gitguardian/ggshield:latest'
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
                echo "ggshield_output.json content: ${output}"
                if (status == 0) {
                    echo "no secret found"
                    } else if (status==1) {
                        def jsonSlurper = new groovy.json.JsonSlurper()
                        def parsedOutput = jsonSlurper.parseText(output)
                            parsedOutput.scans.each { scan -> echo "Scan ID: ${scan.id}"
                                scan.entities_with_incidents.each { entity ->
                                            entity.incidents.each { incident ->
                                                echo "Incident ID: ${incident.incident_url}"
                                                def incidentUrlParts = incident.incident_url.split('/')[-1]
                                                echo incidentUrlParts
                                                def response = httpRequest(
                                                    url: "https://api.gitguardian.com/v1/incidents/secrets/${incidentUrlParts}",
                                                    customHeaders: [[name: 'Authorization', value: "Token ${GITGUARDIAN_API_KEY}"]],
                                                    validResponseCodes: '200'
                                                    )
                                                echo "response: ${response.content}"
                                            }
                                }
                        }
                    }
                }
            }
        }

    }
}
