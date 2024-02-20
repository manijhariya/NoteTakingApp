## Note Taking App with Authentication and note history.
### Start Note Taking App Server
##### Setup enviornment for 
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
```
##### Run Tests
```bash
python manage.py test
```

##### Start Server
```bash
python manage.py runserver
```



