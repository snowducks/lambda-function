import json
import requests

def lambda_handler(event, context):
    # body -> Json
    payload = json.loads(event['body'])
    
    dr_pipeline_token = ''
    github_pipeline_token = ''
    
    # divide DR event / Github
    if payload.get('dr_event', False):
        jenkins_url = "http://10.0.3.227:8080/generic-webhook-trigger/invoke?token=" + dr_pipeline_token
    else:
        # check 'main' brach push
        if payload.get('ref') != 'refs/heads/main':
            return {
                'statusCode': 200,
                'body': 'Not pushed to main branch'
            }
        
        jenkins_url = "http://10.0.3.227:8080/generic-webhook-trigger/invoke?token=" + github_pipeline_token
    
    body_content = event['body']

    try:
        headers = {
            "Content-Type": "application/json"
        }
        
        response = requests.post(jenkins_url, data=body_content, headers=headers)
        return {
            'statusCode': response.status_code,
            'body': response.text
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': 'Error invoking Jenkins: ' + str(e)
        }
