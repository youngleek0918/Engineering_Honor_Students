# eh-DSS
DSS for Engineering Honors


Install needed packages and create virtual env.
>pipenv install

This will update your pipenv environment to the lock file contents. Run if you already have a pipenv established.
>pipenv update

Activate virtual env.
>pipenv shell

Create db migrations then create db off that schema.
>python manage.py makemigrations\
>python manage.py migrate

Test. Creates test db from migration and deletes said db after testing.
>python manage.py test

To generate coverage for eh_app, run tests with coverage and view generated report. -m shows line number for statements missing tests.
>coverage run --source='./eh_app' manage.py test\
>coverage report -m

Load the test seed data. Loading of other data (other .yaml files in the fixtures folder) will populate the db with config data.
>python manage.py loaddata test_seed

Get out of virtual env.
>exit
