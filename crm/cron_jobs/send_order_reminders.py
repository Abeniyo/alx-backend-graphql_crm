#!/usr/bin/env python3

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime, timedelta
import logging

# Setup logging
LOG_FILE = "/tmp/order_reminders_log.txt"
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

# Setup GraphQL client
transport = RequestsHTTPTransport(
    url="http://localhost:8000/graphql",
    verify=False,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=False)

# Calculate date 7 days ago
seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

# GraphQL query to fetch recent orders
query = gql(
    """
    query GetRecentOrders($fromDate: Date!) {
        orders(orderDate_Gte: $fromDate) {
            id
            customer {
                email
            }
        }
    }
    """
)

# Run the query
try:
    result = client.execute(query, variable_values={"fromDate": seven_days_ago})
    orders = result.get("orders", [])
    for order in orders:
        order_id = order["id"]
        email = order["customer"]["email"]
        logging.info(f"{timestamp} - Order ID: {order_id}, Email: {email}")
except Exception as e:
    logging.error(f"{timestamp} - Error: {e}")

print("Order reminders processed!")
