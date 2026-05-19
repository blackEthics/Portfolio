#!/bin/bash

pip install -r requirements/production.txt

python manage.py migrate --noinput
python manage.py collectstatic --noinput --clear
