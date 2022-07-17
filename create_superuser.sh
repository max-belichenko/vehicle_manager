#!/bin/bash
echo "from django.contrib.auth.models import User" > createadmin.py
echo "User.objects.create_superuser('admin', 'admin@email.io', 'first1')" >> createadmin.py
python manage.py shell < createadmin.py