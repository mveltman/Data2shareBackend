# data2share backend
## Getting started
### Prerequisites
* Python 3 (3.7+ recommended)
* pip
* virtualenv
### Installation
Clone this project
```
$ git clone git@github.com:mveltman/Data2shareBackend.git
$ cd src
```
Create a new virtualenv
```
$ virtualenv -p python3.7 venv
$ source venv/bin/activate
```
On windows:
```
virtualenv -p C:\Python\Python37\python.exe venv
.\venv\Scripts\activate.bat
```
Install the dependencies
```
$ pip install Django
$ pip install djangorestframework
$ pip install django-cors-headers
$ pip install channels
$ pip install pywin32
$ pip install psycopg2
$ pip install djangorestframework_simplejwt
```
If issues happen on windows [download](https://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted
) a specific wheel and install it. 
```
pip install Twisted-19.2.0-cp37-cp37m-win_amd64.whl
pip install pywin32-224-cp37-cp37m-win_amd64.whl
```
### Configuring
```
python manage.py migrate
```
Create superuser to login later
```
python manage.py createsuperuser 
```
### Running
```
$ python manage.py runserver
```
.
