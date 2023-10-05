import subprocess

makemigrations = ['python', 'manage.py', 'makemigrations']
migrate = ['python', 'manage.py', 'migrate']
load_group = ['python', 'manage.py', 'loaddata', 'user/fixtures/table_group.json']
load_user = ['python', 'manage.py', 'loaddata', 'user/fixtures/table_user.json']
conflict = ['python', 'manage.py', 'loaddata', 'conflict/fixtures/table_conflict.json']
reviews = ['python', 'manage.py', 'loaddata', 'reviews/fixtures/table_reviews.json']


commands = [makemigrations, migrate, load_group, load_user, conflict, reviews]

for command in commands:
    subprocess.run(command)


# email = firstname@firstname.com  => firstname.lower()
# password = firstname  => firstname.lower()

# {'firstname': 'Ultra', 'lastname': 'Kilogram'},
# {'firstname': 'Mega', 'lastname': 'Gramm'},
# {'firstname': 'Bob', 'lastname': 'Bibovich'},
# {'firstname': 'Goga', 'lastname': 'Frog'},
# {'firstname': 'Tula', 'lastname': 'Lipov'},
# {'firstname': 'Fifa', 'lastname': 'Wins'},
# {'firstname': 'Uefa', 'lastname': 'Presents'},
# {'firstname': 'Hiphop', 'lastname': 'Pulemet'},
# {'firstname': 'Amulet', 'lastname': 'Queryset'},
# {'firstname': 'Daulet', 'lastname': 'Pistolet'},
# mediators
# {'firstname': 'Tualet', 'lastname': 'Violet'},
# {'firstname': 'Pol', 'lastname': 'Podol'},
# {'firstname': 'Potolok', 'lastname': 'Klubok'},
# {'firstname': 'Arkan', 'lastname': 'Katamaran'},
# {'firstname': 'Tuman', 'lastname': 'Baklazhan'},
# {'firstname': 'Baran', 'lastname': 'Sarafan'},
# {'firstname': 'Human', 'lastname': 'Bublik'},
# {'firstname': 'Iris', 'lastname': 'Noris'},
# {'firstname': 'Kapriz', 'lastname': 'Antifriz'},
# {'firstname': 'Tunis', 'lastname': 'Vineriz'},
