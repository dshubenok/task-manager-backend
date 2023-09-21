# task-manager-backend

execute commands
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/manage.py makemigrations
python src/manage.py migrate
python src/manage.py runserver
```

and open http://127.0.0.1:8000/api/schema/swagger-ui/
