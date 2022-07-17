# Vehicle Manager

Приложение для управления списком транспортных средств (далее - ТС).

Реализует следующий функционал:
- Добавить ТС
- Изменить ТС
- Удалить ТС
- Получить ТС по ID
- Получить список ТС (с возможностью фильтрации)
- Импортировать список ТС из файла (xls, xlsx, csv)
- Экспортировать список ТС (с возможностью фильтрации) в файл (xlsx, csv)



## Установка приложения

`git clone https://github.com/max-belichenko/vehicle_manager.git`



## Запуск приложения

### Docker-Compose

```#shell
cd vehicle_manager
docker-compose up
```

### Docker

```#shell
cd vehicle_manager
docker build --tag vehicle-manager --file Dockerfile .
docker run -d --name vehicle-manager -p 8000:8000 vehicle-manager
```

### Windows command line

```#shell
cd vehicle_manager
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python application\manage.py makemigrations
python application\manage.py migrate
python application\manage.py createsuperuser --email admin@example.com --username admin
python application\manage.py runserver 0.0.0.0:8000
```
