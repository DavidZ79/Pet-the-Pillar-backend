# activate venv, bin for unix and scripts for windows
source venv/bin/activate


# python manage.py runserver
chmod +x petpal/manage.py
python3 ./petpal/manage.py runserver


echo "End of run.sh"
