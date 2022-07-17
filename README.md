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

`docker-compose -f ./vehicle_manager/docker-compose.yml up`

### Docker

``

### Manual

```#shell
python ./vehicle_manager/manage.py makemigrations
python ./vehicle_manager/manage.py migrate
python ./vehicle_manager/manage.py createsuperuser --email admin@example.com --username admin
python ./vehicle_manager/manage.py runserver 0.0.0.0:8000
```
