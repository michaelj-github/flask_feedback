uses the following:

* bcrypt==3.1.4
* blinker==1.4
* cffi==1.14.2
* Click==7.0
* Flask==1.0.2
* Flask-Bcrypt==0.7.1
* Flask-DebugToolbar==0.10.1
* Flask-SQLAlchemy==2.3.2
* Flask-WTF==0.14.2
* itsdangerous==0.24
* jedi==0.13.1
* Jinja2==2.10
* MarkupSafe==1.1.1
* psycopg2-binary==2.8.4
* pycparser==2.19
* six==1.11.0
* Werkzeug==0.14.1
* WTForms==2.2.1

these are all in the requirements.txt file

use:
* psql < seed.sql 
to drop and create the database
then:
* python seed.py
to add records to the tables if needed for testing