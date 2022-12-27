# api_yamdb
Данный API даёт возможность собирать ваши отзывы на различные произведения. <br/>
Здесь сможете делиться своими идеями, искать единомышленников и дискутировать. <br/>
Проект полностью реализован при помощи Django Rest Framework. <br/>

![image](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white) <br/>
Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/MelodiousWarbler/api_yamdb/
```
![image](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green) <br/>
Cоздать и активировать виртуальное окружение:

Для ![image](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white) <br/>
```
python -m venv venv
```

```
source venv/scripts/activate
```

Для ![image](https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=apple&logoColor=white) <br/>
```
virtualenv venv -p python3
```

```
source venv/bin/activate
```

Для  ![image](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black) <br/>
```
python3 -m venv venv
```

```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

Для ![image](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white) <br/>
```
pip install -r requirements.txt
```

Для ![image](https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=apple&logoColor=white) <br/>
```
python -m pip install requirements.txt
```

Для  ![image](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black) <br/>
```
pip install -r /path/to/requirements.txt
```

Выполнить миграции:

```
./manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

![image](https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white) <br/>


Полная документация проекта api_yamdb:

```
http://127.0.0.1:8000/redoc/
```
