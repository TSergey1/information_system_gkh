# Information_system_gkh
[![License MIT](https://img.shields.io/badge/licence-MIT-green)](https://opensource.org/license/mit/)
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)

[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)

<details> 
  <summary>Описание</summary>
  
1.	Реализовать модели данных «Дом», «Квартира», «Счётчик воды», «Тариф»,
учитывая связи между ними.
В доме может быть много квартир. В квартире может быть несколько счётчиков.
У квартиры должна быть площадь (будет нужно для расчёта платы за содержание
общего имущества).
Для счётчика нужно хранить показания за несколько прошедших месяцев.
Тариф — это цена услуги или ресурса (например, цена за единицу объёма воды),
используется для расчёта платы за коммунальные услуги.
2.	Реализовать API для ввода и вывода данных по дому (например, адрес дома, список
квартир и т. п., должны выводиться данные из нескольких моделей).
3.	Реализовать функцию расчёта квартплаты для всех квартир в доме за какой-либо
месяц. Результаты записывать в БД.
Квартплата включает в себя:
● Водоснабжение. Рассчитывается по расходу воды за месяц
(тариф_за_единицу_объёма × расход). Расход — это разница между показаниями
счётчика за текущий и за предыдущий месяц.
● Содержание общего имущества. Рассчитывается на основе площади квартиры
(тариф_за_единицу_площади × площадь_квартиры).
4.	Реализовать API, которое запускает процесс расчёта квартплаты
в фоновом режиме (например в celery).
На усмотрение кандидата. Рекомендуется использовать django, celery, postgresql.
</details>

# Подготовка и запуск проекта
Склонировать репозиторий на локальную машину:
```
git clone git@github.com:TSergey1/information_system_gkh.git
```
Периименовать файл .env.example в .env:

 Запускаем проект:
Для запуска проекта, необходимо выполнить в каталоге приложения: ``` docker compose up  ```

Сервер слушает по адресу ``` http://127.0.0.1:8000 ```

## Справка по API
В самом начале необходимо создать в администритивной панели Тарифы через superusera ```http://127.0.0.1:8000/admin/```:
- Тариф для горячей воды (name=hot)
- Тариф для холодной воды (name=cold)
- Тариф для общего имущества (name=property)
Создание суперюзера:
```docker compose -f docker-compose.yaml exec web python manage.py createsuperuser```


<details>
    <summary>Houses</summary>

#### Создание нового дома
``` http POST /api/houses/ ```
| Parameter | Type     | Description                        |
|:----------| :------- |:-----------------------------------|
| `address`   | `string` | **Обязательно**. Адрес дома |
| `tariff_property`   | int (Tariff `pk`) | **Обязательно**. Тариф общего имущества |

#### Получить список домов
``` http GET /api/houses/ ```

#### Получить дом по pk
``` http GET /api/houses/<int:pk>/ ```
</details>

<details>
    <summary>Аpartment</summary>

#### Создание новой квартиры
``` http POST /api/apartments/ ```
| Parameter | Type     | Description                        |
|:----------| :------- |:-----------------------------------|
| `number`   | `int` | **Обязательно**. Номер квартиры |
| `area`   | `Decimal` | **Обязательно**. Площадь квартиры |
| `house`   | int (House `pk`) | **Обязательно**. Дом |

#### Получить список квартир
``` http GET /api/apartments/ ```

#### Получить квартиру по pk
``` http GET /api/apartments/<int:pk>/ ```
</details>

<details>
    <summary>Watermeter</summary>

#### Создание показаний счетчика
``` http POST /api/watermeters/ ```
| Parameter | Type     | Description                        |
|:----------| :------- |:-----------------------------------|
| `value`   | `int` | **Обязательно**. Показания счетчика воды |
| `tariff`   | int (Tariff `pk`) | **Обязательно**. Тариф |
| `apartment`   | int (Аpartment `pk`) | **Обязательно**. Квартира |

#### Получить список счетчиков
``` http GET /api/watermeters/ ```

#### Получить счетчик по pk
``` http GET /api/watermeters/<int:pk>/ ```
</details>
