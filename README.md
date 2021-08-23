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

- Для получения информации о товаре, необходимо ввести его индекс:
```
 http://host:port/products/5
```
- Для получения списка товаров сортированного параметру и значению:
```
 http://host:port/products?arg1=good_id&arg2=0
```
- Для получения списка товаров сортированного названию товара:
```
 http://host:port/products?arg1=product_name
```
#### POST-запросы
Для передачи POST-запроса использовал утилиту curl

- Для добавления товара в базу данных:
```
curl -i -H "Content-Type: application/json" -X POST -d '{"product_name":"phone", "description":"This is a new smartphone", "params":"[{"battery": "li-ion"}, {"display":"micromax a36"}]"}' 192.168.0.110:5000/products
```
На /products можно отправлять как GET так и POST-запросы

### Примеры

1. Запускаем приложение и запускаем бд
```
sudo docker run --name mongo1 -d --rm -p 27017:27017 mongo:4.4.5
```
2. Наполним базу данных товарами при помощи curl (POST):
```
curl -i -H "Content-Type: application/json" -X POST -d '{"product_name":"phone", "description":"This is a new smartphone xiaomi", "params":[{"battery":"li-ion"}, {"display":"micromax a36"}, {"memory": "64Gb"}]}' 192.168.0.110:5000/products
```
3. Получаем товар с id 2
```
curl -i -H "Accept: application/json" "192.168.0.110:5000/products/2"
```
`>>> {"_id": {"$oid": "6122176e2d602b5b24fd76d9"}, "good_id": 2, "product_name": "phone", "description": "This is a new smartphone", "params":[{"battery":"li=ion"}]}

4. Получаем все товары отсортированные по названию:
```
curl -i -H "Accept: application/json" "192.168.0.110:5000/products/?arg1=product_name"
```
[
{"_id": {"$oid": "61227f753131dd3db6ce752a"}, "good_id": 11, "product_name": "book", "description": "nre book", "params": "123"},
{"_id": {"$oid": "612211e0dfe1a8e8434c1833"}, "good_id": 0, "product_name": "phone", "description": "This is a new smartphone", "params": "{}"}]
...
5. Получаем данные по параметру и значению:
```
curl -i -H "Accept: application/json" "192.168.0.110:5000/products?arg1=good_id&arg2=0"
```
