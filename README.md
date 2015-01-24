# giggle
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

SQLite3 database is used.
The name of the database is database.db which is located in the giggle project folder.
13 tables have been created and used.
```
The name of the tables is as follows:-
auth_group
auth_group_permissions
auth_permission
auth_user
auth_user_groups
auth_user_user_permissions
auth_content_type
django_session
django_site
giggle_app_ribbit
giggle_app_userprofile
giggle_app_userprofile_follows
south_migrationhistory
```
port is set to default and host is localhost.
