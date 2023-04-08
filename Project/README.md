## creating virtual environment
python -m venv env

## activating environment(windows)
env\Scripts\activate

## change directory
cd Project

## install requirements
pip install -r requirements.txt

## create Account table in mysql

## Migrations
python manage.py migrate
python manage.py makemigrations App
python manage.py migrate App

## run server
python manage.py runserver


## API REQUEST
https://docs.google.com/spreadsheets/d/16Czs9MbGGBQ3lkhfd24lvbfuL7xZBDjPUUJYQX173JY/edit#gid=0