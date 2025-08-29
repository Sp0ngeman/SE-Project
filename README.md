# Term 3 Software — Django ML Starter

This is a **starter pack** for your Django project. Use it with the class instructions.

## Quick Start

1) Create & activate a virtual env, install deps
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2) Create the Django project and the `engagement` app
```bash
django-admin startproject ml_project
cd ml_project
python manage.py startapp engagement
```

3) Copy files into place
- Copy `starter/engagement/*` into `ml_project/engagement/` (overwrite the placeholders)
- Copy `starter/tests` to project root `tests/`
- Copy `starter/ml_model` to project root `ml_model/`
- Copy `starter/docs` to project root `docs/`
- Copy `requirements.txt`, `pytest.ini`, `.github/workflows/main.yml` to the repo root
- Update `ml_project/settings.py`:
  - `INSTALLED_APPS += ['engagement']`
  - `ALLOWED_HOSTS = ['127.0.0.1','localhost']`
- Update `ml_project/urls.py` to include `engagement.urls`

4) Migrate & create superuser
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

5) Visit
- http://127.0.0.1:8000/engagement → import/dashboard
- http://127.0.0.1:8000/admin → view data

> Keep screenshots & logs for the NSW project booklet.
