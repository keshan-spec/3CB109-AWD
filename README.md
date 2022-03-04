# API

1. Open psql/PgAdmin and create database named 'api_db' `(or make sure to change the DB_NAME variable in the .env file)` run the app.py to create the tables.

2. Execute `run.py` 

```
NOTE: Install pipenv and install the required libraries before starting. Make sure you have python and postgresql installed. Modify the .env file to suit your application.
```


# Routes
```
NOTE: All routes begin with /api/v1/
 - / : Index -> GET
 - /login : Authentication -> POST
 - /register : Creates a user -> POST
 - /users
     -> : Gets all users -> GET
     -> /find : Finds a specific record by any column -> GET 
 - /user
     -> /<id> : Gets user by ID -> GET 
     -> /<id> : Update user records -> PUT
     -> /<id> : Delete a user record -> DELETE
     -> /workplc : Get a user's workplaces -> GET
     -> /events : Get a user's events -> GET
     -> /hours : Get a user's work hours -> GET
   
```
