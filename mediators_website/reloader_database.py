import os
import subprocess

# Очищаем папки с миграциями
for item in os.listdir():
    if os.path.isdir(item):
        os.chdir(item)
        if 'migrations' in os.listdir(os.getcwd()):
            os.chdir('migrations')
            for f in os.listdir(os.getcwd()):
                if '__' in f:
                    continue
                os.remove(f)
            os.chdir('..')
        os.chdir('..')

# Удаляем базу данных
DB_NAME = 'db.sqlite3'
if DB_NAME in os.listdir():
    os.remove(DB_NAME)


MAKEMIGRATIONS = ['python', 'manage.py', 'makemigrations']
MIGRATE = ['python', 'manage.py', 'migrate']
CREATE_DATA = ['python', 'manage.py', 'create_data', '20']
CREATE_CONFLICT = ['python', 'manage.py', 'create_conflict', '-t', '10']
CREATE_REVIEWS = ['python', 'manage.py', 'create_review', '-t', '20']
CREATE_RESPONSE = ['python', 'manage.py', 'create_response', '-t', '20']

RUN_SERVER = ['python', 'manage.py', 'runserver']


commands = [MAKEMIGRATIONS, MIGRATE, CREATE_DATA, CREATE_CONFLICT, CREATE_REVIEWS, CREATE_RESPONSE, RUN_SERVER]
# Создаем сущности
for command in commands:
    subprocess.run(command)
