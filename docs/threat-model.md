# Модель угроз (Secure Notes API)

## Контур
- API endpoints: auth + notes CRUD.
- Данные: учетные данные пользователей, хеши паролей, JWT, содержимое заметок.
- Инфраструктура: runtime в Docker Compose, PostgreSQL, CI/CD security checks.
- Учебные vulnerable examples отделены от основного приложения и не используются API.

## Активы
- Аккаунты пользователей.
- Хеши паролей.
- Секрет подписи JWT.
- Данные заметок.
- Docker image и зависимости.
- CI/CD-конфигурация и security-артефакты.

## Точки входа
- `POST /auth/register`
- `POST /auth/login`
- `/notes*`
- Docker image
- GitLab CI/CD pipeline

## Основные угрозы
- Broken Access Control: доступ к чужим заметкам.
- Injection-атаки на auth/notes flows.
- Credential stuffing / brute-force против логина.
- Утечки секретов через hardcoded keys, `.env`, Docker build context или CI logs.
- Уязвимые зависимости и базовые образы.
- Небезопасная обработка JWT.
- Ошибки валидации входных данных, приводящие к `500` или некорректным данным в БД.
- Мисконфигурации контейнера, CI/CD или IaC.

## Реализованные security-контроли
- Хеширование паролей через `bcrypt`.
- Проверка подписи JWT и срока действия токена.
- SQLAlchemy ORM без динамического SQL в основном приложении.
- Pydantic-валидация входных данных, включая запрет whitespace-only заметок.
- AuthZ-изоляция: пользователь имеет доступ только к своим заметкам.
- Секреты вынесены в переменные окружения и не хранятся в tracked `docker-compose.yml`.
- `.dockerignore` исключает `.env`, локальные базы, кеши и `.git` из Docker build context.
- Docker image запускается под non-root пользователем.
- Security headers: `X-Content-Type-Options`, `Cache-Control`, `Cross-Origin-Resource-Policy`.
- Многоуровневое сканирование в CI: lint, tests, SAST, SCA, container scan, DAST.

## Остаточные риски
- Нет MFA.
- Нет rate limiting для auth endpoints.
- Нет refresh tokens.
- Нет централизованной интеграции с SIEM.
- Alembic migrations пока не инициализированы.
- Terraform и Ansible примеры демонстрационные, не production-grade.
