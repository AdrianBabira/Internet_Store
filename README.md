Дипломный проект к курсу "Python-фреймворк Django" от Skillbox. 
Автор: Adrian Babira (+37369640292) adrianbabira@gmail.com

## Что из себя представляет проект
  Представляет собой подключаемое django-приложение для 
развертывания и запуска в докер-контйнере. Берет на себя все 
что связано с отобоажением страниц, а обращение за данными 
происходит по API, который будет реализован в ходе выполения 
задания дипломного проекта.

## API на данный момент реализованы следующие команды:
   api/sign-in    
   api/sign-out
   api/sign-up
   api/categories
   api/catalog
   api/tags
   api/products
   api/products/popular
   api/products/limited
   api/product/<id>
   api/product/<id>/review
   api/banners
   api/basket   
   api/orders
   api/order/<id>
   api/payment/<id>
   api/profile
   api/profile/password
   api/profile/avatar


## Сборка и запуск проекта:
1) Клонировать репозиторий в локальную папку. 
2) Копируем папку "frontend" из "python_django_diploma\diploma-frontend\"
   в папку "python_django_diploma\diploma_backend\"  
3) Создаем докер контейнер: в терминале выполнить 
   "docker build . -t app". 
   В ходе создания котнейнера запустятся миграции будет создан 
   суперпользователь с логином "admin" и паролем "123456", а также будут 
   созданы две новая группа пользователей "Buyers" с пользователями
   "user_1", "user_2", и "user_3" и группа "Sellers" с пользователями
   "user_4", "user_5", и "user_6" и общий пароль для всех "123456".
   Также загрзятся данные из файла фикстуры "myapifixtures.json". 
4) Запуск докер контейнера: в терминале выполнить 
   "docker compose build app", затем "docker compose up app"






