import datetime
import requests

def log_crm_heartbeat():
    now = datetime.datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    try:
        response = requests.post('http://localhost:8000/graphql', json={"query": "{ hello }"})
        health = response.json().get("data", {}).get("hello", "No response")
    except Exception as e:
        health = f"Error: {e}"

    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(f"{now} CRM is alive - GraphQL: {health}\n")
