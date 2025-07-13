#!/bin/bash

cd "$(dirname "$0")/../.."  # Navigate to project root

source venv/bin/activate  # Adjust if your venv path is different

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
DELETED=$(./manage.py shell <<EOF
from crm.models import Customer, Order
from datetime import timedelta
from django.utils import timezone

cutoff = timezone.now() - timedelta(days=365)
to_delete = Customer.objects.exclude(order__order_date__gte=cutoff)
count = to_delete.count()
to_delete.delete()
print(count)
EOF
)

echo "$TIMESTAMP - Deleted $DELETED inactive customers" >> /tmp/customer_cleanup_log.txt
