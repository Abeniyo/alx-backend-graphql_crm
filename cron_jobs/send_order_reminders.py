import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

query = gql("""
query {
  orders(lastWeek: true) {
    id
    customer {
      email
    }
  }
}
""")

client = Client(transport=RequestsHTTPTransport(
    url='http://localhost:8000/graphql', verify=False), fetch_schema_from_transport=True)

result = client.execute(query)
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open("/tmp/order_reminders_log.txt", "a") as f:
    for order in result.get("orders", []):
        f.write(f"{timestamp} - Order {order['id']} -> {order['customer']['email']}\n")

print("Order reminders processed!")
