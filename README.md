## Тестовое задание

### Установка и запуск

1. После клонирования репозитория необходимо создать новое виртуальное окружение, активировать его, установить требуемые библиотеки:
```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt 
```
2. Запустить Docker-контейнер с Mongo. 
```
sudo docker run --name mongo1 -d --rm -p 27017:27017 mongo:4.4.5
```
Для того, чтобы не засорять систему лишними контейнерами при запуске команды указан флаг --rm который после завершения работы с базой данных удалится из системы
Также необходимо указать порт через который мы будем соединяться с портом mongo.

3. После этого необходимо запустить приложение командой:
```
python3 views.py
```
При необходимости сохранить базу данных, необходимо настроить Docker volume, в который будут сохраняться результаты выполнения приложения.

### Команды
#### GET-запросы
- Получить все товары из базы данных
```
http://host:port/products
```
- Для получения информации о товаре по индексу:
```
 http://host:port/products/5
```
- Для получения списка товаров фильтрованного имени товара:
```
 http://host:port/products?good_name=phone
```
- Для получения списка товаров фильтрованного по параметрам товара:
```
 http://host:port/products?motherboard=asus
```
#### POST-запросы
Для передачи POST-запроса использовал утилиту curl

- Для добавления товара в базу данных:
```
curl -i -H "Content-Type: application/json" -X POST -d '{"product_name":"phone", "description":"This is a new smartphone", "params":[{"battery": "li-ion"}, {"display":"micromax a36"}]}' host:port/products
curl -i -H "Content-Type: application/json" -X POST -d '{"product_name":"computer", "description":"This is a new computer", "params":[{"memory":"32Gb"}, {"motherboard":"asus"}, {"processor": "Amd Ryzen"}]}' host:port/products
```
На /products можно отправлять как GET так и POST-запросы

### Примеры

1. Запускаем микросервис и запускаем бд
```
python3 views.py
sudo docker run --name mongo1 -d --rm -p 27017:27017 mongo:4.4.5
```
2. Наполним базу данных товарами при помощи curl (POST):
```
curl -i -H "Content-Type: application/json" -X POST -d '{"product_name":"computer", "description":"This is a new computer", "params":[{"memory":"32Gb"}, {"motherboard":"asus"}, {"processor": "Amd Ryzen"}]}' 192.168.0.110:5000/products
curl -i -H "Content-Type: application/json" -X POST -d '{"product_name":"phone", "description":"This is a new smartphone", "params":[{"battery": "li-ion"}, {"display":"micromax a36"}]}' 192.168.0.110:5000/products
curl -i -H "Content-Type: application/json" -X POST -d '{"product_name":"computer", "description":"This is a new computer", "params":[{"memory":"16Gb"}, {"motherboard":"asus"}, {"processor": "intel"}]}' 192.168.0.110:5000/products
```
3. Получаем товар с id 2
```
curl -i -H "Accept: application/json" "192.168.0.110:5000/products/2"
```

4. Получаем все товары отфильтрованные по названию:
```
curl -i -H "Accept: application/json" "192.168.0.110:5000/products?product_name=computer"
curl -i -H "Accept: application/json" "192.168.0.110:5000/products?product_name=phone"
```

5. Получаем данные по параметру и значению:
```
curl -i -H "Accept: application/json" "192.168.0.110:5000/products?battery=li-ion"
curl -i -H "Accept: application/json" "192.168.0.110:5000/products?processor=intel"
```
