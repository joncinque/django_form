# django_form
Playing around with django forms

## Prereqs (Debian / Ubuntu)

```bash
sudo apt install python3 python3-venv python3-pip
```

## Requirements

```bash
python3 -m venv venv
./venv/bin/pip3 install -r requirements.txt
```

## Django setup

```bash
./venv/bin/python3 manage.py migrate
./venv/bin/python3 manage.py createsuperuser
./venv/bin/python3 manage.py runserver
```

## Create new from autocomplete

To create a new entry from an autocomplete, you need to have the proper,
permissions, which requires logging in.

* Go to the [admin page](http://127.0.0.1:8000/admin/)
* Login as the super user

## Create new models

* Go to the [encounters page](http://127.0.0.1:8000/encounters/)
* Try all of the models
