## Note Taking App with Authentication and note history.
Required Python 3.10 or higher

##### Setup enviornment to server

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
##### check server health
```bash
curl 'http://127.0.0.1:8000/healthcheck/' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate, br' -H 'Connection: keep-alive' -H 'Upgrade-Insecure-Requests: 1' -H 'Sec-Fetch-Dest: document' -H 'Sec-Fetch-Mode: navigate' -H 'Sec-Fetch-Site: cross-site' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache'
```
##### Summary of Endpoints
POST /login: Create a simple login view
POST /signup: Create a single user sign up view
POST /notes/create: Create a new note.
GET /notes/{id}: Retrieve a specific note by its ID.
POST /notes/share: Share the note with other users. 
PUT /notes/{id}: Update an existing note.
GET /notes/version-history/{id}: GET all the changes associated with the note. 
