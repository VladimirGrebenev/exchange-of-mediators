# website-of-mediators
From developers to mediators with love :)

### Стэк:
- python 3.11
- django 4.2.*


# Setup 
- Создайте .env файл и внесите в него переменные окружения (если требуется).
```bash
nano .env
```
- Накатите миграции
```bash
python3 manage.py migrate
```
- Запустите проект
```bash
python3 manage.py runserver
```

### Правила работы с git'om
Есть 2 ветки:
- ```master```
- ```development```

Вы работаете ТОЛЬКО в <b>development'е</b>.

Форма работы:
- Стягиваете репозиторий к себе:<br>
    ```shell
    git clone #ssh
     ```
- Переходите в ветку development <br>
    ```shell
    git switch development
    ```
- Из дева создаете новую ветку с названием эпике из беклога (creating_navbar, init_signing и т.д.)<br>
    ```shell
    git checkout -b #НАЗВАНИЕ ЭПИКА КОРОТКО
     ```
- Создаете ветку в удаленном репозитории <br>
    ```shell
    git push --set-upstream origin #тоже самое название эпика, что в прошлой команде
    ```
- Делаете изменения, пишите, трудитесь усердно ужас какой.
- КОМИТИТЕ В СВОЮ ВЕТКУ С НОМЕРОМ ЗАДАЧИ <br>
    ```shell
    git add . && git commit -m "#Номер задачи из беклога. Init user model with basic attrs"
    ```
- Следующая задача из этого же эпика.
- Так же коммит
- После того, когда полностью выполнили все задачи из эпика, за которые взялись - пушите изменения:<br>
    ```shell
    git push
    ```
- Создаете пулл реквест в DEVELOPMENT (удобнее через интерфейс github'a).

Пишите куда-то о том, что сделан пулл реквест и его надо посмотреть (желательно сразу со ссылкой на него).<br>
Код должны посмотреть 2 других человека и аппрувнуть или написать правки.<br>
После 2 апрувув делаем (скорее всего, это будут делать либо <a href="https://t.me/Flopp/">Артем</a>, либо <a href="https://t.me/Veneberg81/">Владимир</a>)<br>
COMPARE AND MERGE в ```DEVELOPMENT```.

Что там с мастером происходит - вообще никого не касается.

После этого:
- ```git switch development```
- ```git pull --rebase```
- ```git checkout -b #Номер новой задачи```
- Пишем код
- Пушим
- Делаем pull request
- Мерджим
- Стягиваем изменения c ```development'a```
- Создаем ветку
Ну и дальше по кругу

### Linter
flake8:<br>
```shell
flake8 . --ignore=E402,F841,E302,E305,W503 --max-line-length=120 --statistics --show-source --extend-exclude=venv 
```
Для linux'a:
- Устанавливаем flake8
```shell 
sudo apt install flake8 -y
```
- Открываем pre-commit (исполнять из root'а проекта (т.е. на самом верхнем уровне))<br>
```shell
nano .git/hooks/pre-commit
```
- Вставляем внутрь команду, которую перед коммитом исполнять нужно:<br>
```
#!/bin/sh
flake8 . --ignore=E402,F841,E302,E305,W503 --max-line-length=120 --statistics --show-source --extend-exclude=venv
```
- Даём права на исполнение этому файлу:
```shell
chmod +x .git/hooks/pre-commit
```

### Docker и всё такое :)
Чтобы поднять контейнер с базой postgreSQL в корне проекта:<br>
```shell 
docker-compose -f docker-compose-pg-only.yaml up
```
Пока что в этом нет нужды, оставим на SQLlite, но позже надо будет переползти в PostgreSQL

### Requirements.txt
Все "новинки" сюда попадают ТОЛЬКО руками. <b>НЕ НАДО ДЕЛАТЬ</b> <i>pip freeze > req.txt.</i><br>
Если накидывать через freeze, то файл превращается в помойку и при возникновении конфликтов в зависимостях будет не очень приятно там разбираться :)<br><br>
Установили библиотеку какую-то, посмотрели, какая версия - закинули её ручками. Ничего сложного.

### Hints
- Полностью переустановить все зависимости:<br>
    ```shell
    pip install --upgrade --force-reinstall -r requirements.txt
    ```
- Посмотреть внесенные изменения в рамках текущего коммита:<br>
    ```shell
    git diff
    ```
- Посмотреть внесенные изменения в конкретный файл:<br>
    ```shell
    git diff filename
    ```
- Перед каждым коммитом, по-хорошему, пробегаться по всем файлам и просматривать, что вы коммитите <br>(неиспользуемые импорты или оставленные принты - самая частая проблема).<br> Актуально только при отсутствии линтера, иначе он вам сам подскажет :)
