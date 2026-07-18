# LiftTeam Changelog

## v2.5.1 (hotfix)
- PROMPT.md: добавлена информация о кэшировании jsDelivr (24 часа)
- README.md: добавлено примечание о проверке актуальности через GitHub Web
- Подтверждено: push на GitHub работает корректно, проблема только в CDN-кэше

## v2.5
- Обновление версии до v2.5
- Добавлен .gitattributes для корректной работы с bundle
- push_to_github.bat: проверка интернет-соединения перед пушем
- README.md: полная инструкция по развёртыванию из bundle
- PROMPT.md: обновлена информация о работе с проектом

## v2.2.3 (hotfix)
- README.md обновлен: добавлена инструкция по распаковке bundle
- push_to_github.bat/sh: принудительный сброс remote URL на GitHub

## v2.2.3
- Исправлена критическая ошибка авторизации: LoginForm не получал данные POST
- LoginForm.__init__ теперь использует kwargs.pop('request') вместо positional arg
- login_view теперь передаёт request=request, data=request.POST явно
- Авторизация по логину admin / пароль admin123 теперь работает корректно

## v2.2.2 (hotfix)
- Исправлен lifteam_launcher.py: правильный вывод логина (admin, не admin@test.com)
- Добавлена диагностика создания пользователей
- Добавлена проверка существования таблицы core_employee
- Добавлена активация пользователя если он неактивен
- Улучшена обработка ошибок при инициализации БД

## v2.2.1 (hotfix)
- Исправлен requirements.txt: `django-channels` → `channels` (правильное название пакета)
- Убран неиспользуемый `djangorestframework-simplejwt`
- Добавлен `asgiref>=3.7` для совместимости Channels

## v2.2
- Исправлена модель Employee: авторизация по username (логину)
- Исправлен Dockerfile (был сломан — содержал Python-код)
- Исправлен lifteam_launcher.py: версия v2.2, правильные аргументы create_admin
- Списание со склада перенесено из сигналов в явные транзакции views
- Добавлена защита от race condition в генерации номера заказа (select_for_update)
- Исправлена логика истории статусов: создание новой записи вместо обновления старой
- WebSocket теперь активно отправляет обновления остатков
- nginx в docker-compose слушает 0.0.0.0:80 (доступен извне)
- SESSION_COOKIE_SECURE = True в production
- Добавлен --force флаг в create_admin команду
- Обновлены все служебные скрипты до v2.2
