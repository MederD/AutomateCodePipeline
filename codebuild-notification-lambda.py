import urllib3
import json, os, logging

logger = logging.getLogger()
logging.basicConfig()
logger.setLevel(logging.INFO)

http = urllib3.PoolManager()
env_url = os.environ['url']


def handler(event, context):
    url = env_url

    report = event.get("report", {})
    matches = report.get("matches", [])
    source_url = event.get("source_repository")
    source_branch = event.get("source_branch")
    build_id = event.get("build_id")

    if not matches:
        message = f"No vulnerabilities found in {source_url}/{source_branch} with build id: {build_id}"
    else:
        message_lines = [f"Vulnerabilities found in {source_url}/{source_branch} with build id: {build_id}:"]
        for match in matches:
            vulnerability = match.get("vulnerability", {})
            package = match.get("artifact", {}).get("name", "Unknown package")
            version = match.get("artifact", {}).get("version", "Unknown version")
            severity = vulnerability.get("severity", "Unknown severity")
            vulnerability_id = vulnerability.get("id", "No ID")

            message_lines.append(f"- Package: {package}, Version: {version}, Severity: {severity}, ID: {vulnerability_id}")
        
        message = "\n".join(message_lines)

    slack_message = {
        "text": message
    }
    
    encoded_msg = json.dumps(slack_message).encode('utf-8')

    try:
        resp = http.request('POST', url, body=encoded_msg, headers={'Content-Type': 'application/json'})
        logger.info("Message sent to Slack with status code: %s", resp.status)
        logger.info("Response from Slack: %s", resp.data)
    except Exception as e:
        logger.exception("Error sending message to Slack: %s", e)
        raise
