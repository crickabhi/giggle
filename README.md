# giggle
giggle
=============

Giggle - A Twitter Clone made using Django

***

To set the application locally, first clone the repo

```  
git clone https://github.com/crickabhi/giggle.git
```

Make a virtual environment

```
virtualenv --no-site-packages giggle_env
```
  
With the the virtual environment activated, install the dependencies

```
pip install Django==1.4 South
```
  
Next, `cd` into the repository and run the `syncdb` command to create the tables and superuser account

```
python manage.py syncdb
```

Then, apply the migrations

```
python manage.py migrate giggle_app
```
  
Finally, start the development server to preview the application

```
python manage.py runserver
```

