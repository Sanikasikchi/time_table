# Technologies used  
* Python 3.9
* Django 3.2 
* MySQL

# Dependencies
Check [requirements.txt](requirements.txt)

# Installation
* Install python from this link >> http://www.python.org/download.
* After installation add python variable in windows environment variable.
* Install all dependencies thourgh cmd >> `pip install -r requirements.txt`

# For New Django Project Installation
* Created project using cmd >> `django-admin startproject demoapp`
* Created app using cmd >> `python manage.py startapp myapp`
* Migrated DB using cmd >> `python manage.py migrate`
* Created a superuser using cmd >> `python manage.py createsuperuser`

# Virtual Env
* Install >> `pip install virtualenv`
* Create >> `virtualenv venv`
* Activate >> `venv\Scripts\activate`
* List out all dependencies >> `pip freeze > requirements.txt`
* Install all dependencies >> `pip install -r requirements.txt`

# DjangoDevelopment
* To start server use cmd >>  `python manage.py runserver`

# Procedures to create a new module
* First create a folder `backend/YOUR_MODULE_NAME`
* Run command `python manage.py startapp YOUR_MODULE_NAME backend/YOUR_MODULE_NAME`
* Add the app in `backend/installedapp.py`
```python 
INSTALLED_APPS = [
                  ..,
                 'backend.YOUR_MODULE_NAME',
                 ]
```
* Change the app name in `backend/YOUR_MODULE_NAME/apps.py` as follows
```python
class BudgetConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'YOUR_MODULE_NAME' >> name = 'backend.YOUR_MODULE_NAME'
```    

* Write Model in `YOUR_MODULE_NAME/models.py`.
* Run cmd >> `python manage.py makemigrations`
* Run cmd >> `python manage.py migrate`
* Clone `backend/products/views.py` to new file `myapp/YOUR_MODULE_NAME/views.py`.
* Forms and tables class are defined on top of the file, customize it as per requirement.
* Write route for new views  in `backend/urls.py`.