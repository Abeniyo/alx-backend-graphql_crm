#!/bin/bash

cd "$(dirname "$0")"/../..
timestamp=$(date "+%Y-%m-%d %H:%M:%S")
deleted_count=$(python3 manage.py shell -c "
from crm.models import Customer
from django.utils import timezone
from datetime import timedelta

cutoff = timezone.now() - timedelta(days=365)
qs = Customer.objects.filter(order__isnull=True, created__lt=cutoff)
count = qs.count()
qs.delete()
print(count)
")

echo "$timestamp - Deleted customers: $deleted_count" >> /tmp/customer_cleanup_log.txt
