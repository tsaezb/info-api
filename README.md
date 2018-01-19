# Infobox-api

### Develop instructions

##### 0. Copy local config file
    # Linux / OS X
    cp Infoapi/settings/local.py{.default,}

##### 1. Create virtualenv
    virtualenv -p python3 venv

##### 2. Install Python dependencies
    pip install -r requirements.txt

##### 3. Run Webservice (Django)
    python manage.py runserver

### Deploy (using Python Fabric)
    fab production:<branch or tag> deploy restart
