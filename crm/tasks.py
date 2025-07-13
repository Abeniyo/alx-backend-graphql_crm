from celery import shared_task
import requests
from datetime import datetime

@shared_task
def generate_crm_report():
    query = """
    query {
        customersCount
        ordersCount
        totalRevenue
    }
    """
    response = requests.post('http://localhost:8000/graphql', json={'query': query})
    data = response.json().get("data", {})
    with open("/tmp/crm_report_log.txt", "a") as f:
        f.write(
            f"{datetime.now()}: Report - "
            f"{data.get('customersCount')} customers, "
            f"{data.get('ordersCount')} orders, "
            f"{data.get('totalRevenue')} revenue\n"
        )
