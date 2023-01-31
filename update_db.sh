#!/bin/bash

python3.8 manage.py makemigrations user audition albapick banner profiles apply
python3.8 manage.py migrate
