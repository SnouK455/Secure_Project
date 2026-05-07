# История изменений

## Не выпущено

### Исправлено
- Запрещены значения заметок, состоящие только из пробелов: `POST /notes` и `PUT /notes/{note_id}` теперь возвращают `422 Validation Error` вместо `500 Internal Server Error`, а невалидные заметки не попадают в базу.
- Обновлены уязвимые Python-зависимости, чтобы SCA-проверки проходили без известных уязвимостей.
- `python-jose` заменен на `PyJWT`, `passlib` удален в пользу прямого использования `bcrypt` для хеширования паролей.
- Исправлена обработка невалидных JWT: теперь некорректный токен возвращает `401 Unauthorized`, а не приводит к внутренней ошибке.
- Устаревший FastAPI startup event заменен на lifespan handler.
- Базовый Docker-образ заменен с Debian slim на Alpine, чтобы убрать High/Critical-находки Trivy.
- Исправлен порядок стадий GitLab CI: `build_image` теперь выполняется до `trivy_container_scan`.
- В CI добавлены login в Docker registry, push образа и Trivy-сканирование опубликованного CI-образа.
- Исправлен DAST job: добавлено подключение рабочей директории ZAP и использование project baseline config.
- Fallback-путь SQLite по умолчанию перенесен в `/tmp`, чтобы контейнер под non-root пользователем мог стартовать без ошибок.
- Default/example/test значения `SECRET_KEY` увеличены до рекомендуемой длины для HS256.

### Добавлено
- Добавлены публичные endpoints `/` и `/robots.txt` для аккуратной API-метаинформации и более чистого DAST-поведения.
- Добавлен middleware с security headers:
  - `X-Content-Type-Options: nosniff`
  - `Cache-Control: no-store`
  - `Cross-Origin-Resource-Policy: same-origin`
- Добавлены regression-тесты для:
  - публичных metadata endpoints и security headers
  - обработки некорректного JWT
  - повторной регистрации пользователя
  - изоляции доступа к заметкам между пользователями
  - валидации пустого обновления заметки
  - валидации пробельных `title` и `content` при создании и обновлении заметки
- Добавлена конфигурация ZAP baseline для API-специфичного шума сканера.

### Изменено
- README и документация security pipeline обновлены под актуальный CI/CD flow и локальные команды проверки.
- Улучшена изоляция тестов: таблицы БД пересоздаются для каждого тест-кейса.

### Проверено
- `pytest`: 7 тестов прошли
- `ruff`: все проверки прошли
- `bandit`: проблем не найдено
- `pip-audit`: известных уязвимостей не найдено
- `semgrep`: 0 findings
- `trivy`: 0 High/Critical findings
- `OWASP ZAP baseline`: 0 FAIL, 0 WARN
- Docker image успешно собирается
- `.gitlab-ci.yml` успешно парсится
