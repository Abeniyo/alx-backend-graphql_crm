#!/bin/bash

# Set working directory to project root based on current script path
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )"/../.. && pwd )"
cd "$DIR"

# Run Python Django shell to delete inactive customers
deleted_count=$(python3 manage.py shell -c "
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer

cutoff = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.filter(order__isnull=True, created__lt=cutoff)
count = inactive_customers.count()
inactive_customers.delete()
print(count)
")

# Log timestamp and count
timestamp=$(date "+%Y-%m-%d %H:%M:%S")
echo \"$timestamp - Deleted customers: $deleted_count\" >> /tmp/customer_cleanup_log.txt
