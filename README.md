# python-ogn-ddb

[![Build Status](https://travis-ci.org/Meisterschueler/python-ogn-ddb.svg?branch=master)](https://travis-ci.org/Meisterschueler/python-ogn-ddb)
[![Heroku](https://heroku-badge.herokuapp.com/?app=ogn-ddb)](https://ogn-ddb.herokuapp.com)
[![Coverage Status](https://coveralls.io/repos/github/Meisterschueler/python-ogn-ddb/badge.svg?branch=master)](https://coveralls.io/github/Meisterschueler/python-ogn-ddb?branch=master)

## Installation and Setup
1. Checkout the repository

    ```
    git clone https://github.com/Meisterschueler/python-ogn-ddb.git
    cd python-ogn-ddb
    ```

2. Optional: Create and use a virtual environment

    ```
    python3 -m venv my_environment
    source my_environment/bin/activate
    ```

3. Install python requirements

    ```
    pip install -r requirements.txt
    ```

4.  Set environment variables

    ```
    export FLASK_APP=ddb.py
	export FLASK_ENV=development
    ```

	If you want the app to send emails, you also have to set the variables MAIL_USERNAME and
	MAIL_PASSWORD. Default email configuration is google mail, other server need modification
	in the file 'config.py'

5.  Optional: insert some (fake) data into the db
    
	```
    flask filldata aircrafts
	flask filldata fakedata
    ```

6.	Run the application
	
	```
    flask run
    ```
	
	Now you can open the application in your brower: http://localhost:5000
	
	They are some options, e.g. if you want to access the application from outside localhost at
	port 8080, you should use:
	
	```
    flask run -h 0.0.0.0 -p 8080
    ```