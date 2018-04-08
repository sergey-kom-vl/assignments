# Тестовое задание для разработчика на python

У сети ресторанов доставки "ФорФар" есть множество точек, на которых готовятся заказы для клиентов.
Каждый клиент хочет вместе с заказом получить чек, содержащий детальную информацию о заказе.
Сотрудники кухни также хотят чек, чтобы в процессе готовки и упаковки заказа не забыть положить всё что нужно.
Наша задача помочь и тем и другим, написав сервис печатающий<sup>1</sup> оба тип чеков.

<sup>1</sup>На самом деле печатать будет один из принтеров на точке, а сервис будет всего лишь генерировать PDF-файл
с чеком из HTML-шаблона



### Схема работы сервиса
![][arch_schema]
1. Сервис принимает запрос на создание чеков для заказа, проверяет есть ли для точки указанной в запросе настроенные 
принтеры, если их нет возвращает ошибку, затем проверяет наличие чеков для данного заказа, если они есть возвращает 
ошибку, иначе создаёт в БД записи для чеков каждого типа и ставит асинхронные задачи на генерацию PDF-файлов для этих чеков
2. Асинхронный воркер с помощью wkhtmltopdf конвертирует HTML-шаблон чека в PDF-файл, сохраняет его в папку ./media/pdf
находящуюся в корне проекта, обновляет статус чека, сохраняет ссылку на PDF-файл в БД. Имя файла должно иметь следущий 
вид <ID заказа>_<тип чека>.pdf (123456_client.pdf). 
3. Принтер опрашивает сервис на наличие новых чеков. Запрос происходит по следующему пути: принтер отправляет свой ключ
API и ID последнего напечатанного им чека, если принтера с таким ключом не существует, сервис возвращает ошибку, иначе
возвращает список чеков для этого принтера, у которых сгенерирован PDF-файл (status=rendered)



### Технические требования
1. Сервис должен быть написан на python2 на Django v1.11
2. База данных - PostgreSQL
2. Для асинхронных задач можно использовать либо Celery либо RQ
3. Брокер для асинхронных задач - Redis
4. Все инфраструктурные вещи необходимые для сервиса ([PostgreSQL], [Redis], [wkhtmltopdf]) и сам сервис должны разворачиваться 
с помощью docker-compose



### Примечания
1. Модели и методы API описаны в документе ниже, вёрстка HTML-шаблонов для чеков лежит в репозитории в папке templates
2. Во время написания сервиса не стоит изобретать велосипеды, лучше взять что-то существующие



### Модели
1. Принтер (Printer)

| Поле       | Тип    | Значение        | Описание                                      |
|------------|--------|-----------------|-----------------------------------------------|
| name       | string |                 | название принтера                             |
| check_type | string | kitchen\|client | тип чека                                      |
| api_key    | string |                 | ключ доступа к API для desktop-клиента печати |
| point_id   | int    |                 | точка к которой привязан принтер              |

2. Чек (Check)

| Поле       | Тип    | Значение        | Описание                     |
|------------|--------|-----------------|------------------------------|
| printer_id | int    |                 | принтер                      |
| type       | string | kitchen\|client | тип чека                     |
| order      | JSON   |                 | информация о заказе          |
| status     | string | new\|rendered   | статус чека                  |
| pdf_file   | URL    |                 | ссылка на созданный PDF-файл |



### Методы API
**1. Создание чеков**  
  _Создаёт чеки для переданного заказа._

* **URL**  
  _/create_checks_

* **Method:**  
  `POST`

* **Data Params**  
  **Required:**
  
  | Параметр | Тип   | Значение | Описание                             |
  |----------|-------|----------|--------------------------------------|
  | order    | Order |          |Заказ для которого нужно создать чеки |
  
  Order:
  
  | Поле     | Тип    | Значение | Описание                         |
  |----------|--------|----------|----------------------------------|
  | id       | int    |          | номер заказа                     |
  | items    | Item[] |          | список позиций заказа            |
  | price    | int    |          | стоимость заказа                 |
  | address  | string |          | адрес доставки                   |
  | client   | Client |          | информация о клиенте             |
  | point_id | int    |          | точка на которой готовится заказ |
  
  Item:
  
  | Поле       | Тип    | Значение | Описание        |
  |------------|--------|----------|-----------------|
  | name       | string |          | название        |
  | quantity   | int    |          | количество      |
  | unit_price | int    |          | цена за единицу |
  
  Client:
  
  | Поле       | Тип    | Значение | Описание       |
  |------------|--------|----------|----------------|
  | name       | string |          | имя клиента    |
  | phone      | string |          | номер телефона |

* **Success Response:**
  * **Code:** 200  
    **Content:** `{ ok : "Чеки успешно созданы" }`

* **Error Response:**
  * **Code:** 400 BAD REQUEST  
    **Content:** `{ error : "Для данного заказа уже созданы чеки" }`

  * **Code:** 400 BAD REQUEST  
    **Content:** `{ error : "Для данной точки не настроено ни одного принтера" }`

* **Sample Call:**  
  ```
  data = {
      'order': {
          'id': 123456,
          'price': 780,
          'items': [
              {
                  'name': 'Вкусная пицца',
                  'quantity': 2,
                  'unit_price': 250
              },
              {
                  'name': 'Не менее вкусный ролл',
                  'quantity': 1,
                  'unit_price': 280
              },
          ]
          'address': 'г. Уфа, ул. Ленина, д. 42'
          'client': {
              'name': 'Иван',
              'phone': '9173332222'
          }
          'point_id': 1,
      }
  }

  r = requests.post(SERVICE_URL + '/create_checks', json=data)
  ```

**2. Получение чека**  
  _Метод получения чека для заказа._

* **URL**  
  _/check_

* **Method:**  
  `GET`

* **URL Params**  
  **Required:**
  
  | Параметр | Тип    | Значение        | Описание    |
  |----------|------- |-----------------|-------------|
  | order_id | int    |                 | ID заказа   |
  | type     | string | kitchen\|client | тип чека    |
  | format   | string | html\|pdf       | формат чека |
  
* **Success Response:**  
  * **Code:** 200  
    **Content:** HTML-файл или PDF-файл

* **Error Response:**  
  * **Code:** 400 BAD REQUEST  
    **Content:** `{ error : "Для данного заказа нет чеков" }`
    
  * **Code:** 400 BAD REQUEST  
    **Content:** `{ error : "Для данного заказа не сгенерирован чек в формате PDF" }`

* **Sample Call:**  
  ```
  params = {
      'order_id': 123456,
      'type': 'kitchen',
      'format': 'pdf'
  }

  r = requests.post(SERVICE_URL + '/check', params=params)
  ```
 
**3. Наличие новых чеков**  
  _Метод проверяющий наличие новых чеков._

* **URL**  
  _/new_checks_

* **Method:**  
  `GET`

* **URL Params**  
  **Required:**
  
  | Параметр      | Тип    | Значение | Описание             |
  |---------------|------- |----------|----------------------|
  | api_key       | string |          | ключ доступа к API   |
  | last_check_id | int    |          | ID последнего чека   |
  
* **Success Response:**  
  * **Code:** 200  
    **Content:** 
    ```
    {
        cheks: [
            {
                id: 1,
                pdf_file: 'http://check.service.ru/pdf/123456_client.pdf
            }
        ]
    }
    ```

* **Error Response:**  
  * **Code:** 401 UNAUTHORIZED  
    **Content:** `{ error : "Ошибка авторизации" }`
    
* **Sample Call:**  
  ```huey python
  params = {
      'last_check_id': 0,
      'api_key': '1234qwer',
  }

  r = requests.post(SERVICE_URL + '/new_checks', params=params)
  ```



[wkhtmltopdf]: https://hub.docker.com/r/openlabs/docker-wkhtmltopdf-aas/
[PostgreSQL]: https://hub.docker.com/_/postgres/
[Redis]: https://hub.docker.com/_/redis/

[arch_schema]: images/arch_schema.png
