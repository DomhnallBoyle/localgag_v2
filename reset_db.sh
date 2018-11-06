rm -rf localgag/migrations/0001_initial.py*
python manage.py makemigrations
rm -rf db.sqlite3
python manage.py migrate
python manage.py loaddata localgag/fixtures.json
