# UWI NCB AGILE LABS 2021 - SCRUM CYCLE 8 

 - The following commands are expected to be run in the root directory, scrum8-event-management

## Create venv
```
python -m venv venv
source venv/bin/activate
venv\Scripts\activate (windows)
```
## Install requirements
```
pip install --upgrade pip (can be skipped)
pip install -r requirements.txt
```

## Start development server
```
python run.py
```

## Migration Commands (Use carefully)
```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
python manage.py db downgrade
```
