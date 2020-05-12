% prepara el repositorio para su despliegue. 
release:sh -c 'cd board && python manage.py flush && python manage.py makemigrations && python manage.py migrate && python manage.py loaddata populate.json'
% especifica el comando para lanzar Decide
web: sh -c 'cd board && gunicorn board.wsgi --log-file -'