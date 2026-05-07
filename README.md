# Secure Notes API с DevSecOps-пайплайном

Портфолио-проект по DevSecOps/AppSec на базе FastAPI: компактный API, на котором показан secure SDLC в формате, близком к реальному production-процессу.  
Проект учебный, но практичный: security-проверки встроены в GitLab CI/CD, а в `vulnerable_examples/` есть уязвимые и исправленные примеры для демонстрации триажа и устранения уязвимостей.

## Зачем этот проект
- Показать практический secure SDLC: код, контейнеризация, CI/CD и security checks.
- Продемонстрировать уровень junior в AppSec/DevSecOps без завышенных обещаний.
- Дать репозиторий, который выглядит как аккуратный GitHub-проект для портфолио и собеседования.

## Технологии
- Python, FastAPI, SQLAlchemy, Pydantic
- PostgreSQL
- JWT, bcrypt
- Docker, Docker Compose
- GitLab CI/CD
- Ruff, Pytest
- Bandit, Semgrep
- pip-audit
- Trivy
- OWASP ZAP
- Ansible
- Terraform
- Alembic (зависимость подключена, но миграции пока не инициализированы)

## Архитектура
```text
Клиент
  -> FastAPI API
  -> PostgreSQL

GitLab CI/CD
  -> lint
  -> tests
  -> sast
  -> sca
  -> build
  -> container_scan
  -> dast
```

Приложение запускается через Docker Compose, PostgreSQL используется как основная база данных.

## Структура проекта
```text
app/                    # FastAPI-приложение (auth + notes)
tests/                  # unit-тесты (pytest)
infra/                  # вспомогательные артефакты CI (например, конфиг ZAP)
ansible/                # базовый пример автоматизации деплоя
terraform/              # базовый пример IaC
docs/                   # документация по безопасности
vulnerable_examples/    # намеренно уязвимые примеры + исправленные варианты
Dockerfile
docker-compose.yml
.gitlab-ci.yml
README.md
SECURITY.md
```

## Возможности
- регистрация пользователей
- вход с JWT access-токеном
- хеширование паролей через bcrypt
- CRUD-операции для заметок
- контроль доступа на уровне пользователя
- валидация через Pydantic
- конфигурация через переменные окружения
- хранение данных в PostgreSQL (в Docker-сценарии)
- базовые security-контроли с привязкой к OWASP Top 10

## Быстрый старт
### 1) Клонирование репозитория
```bash
git clone <repo-url>
cd <имя-папки-репозитория>
```

### 2) Создание `.env` из шаблона
```bash
cp .env.example .env
```

### 3) Пример переменных окружения
```env
DATABASE_URL=postgresql+psycopg2://appuser:strongpassword@db:5432/securenotes
SECRET_KEY=replace_with_random_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Актуальный шаблон переменных находится в `.env.example`.  
Не храните реальные секреты в Git. Для локальной разработки используйте тестовые значения, для CI/CD и окружений развертывания - защищенные переменные.

### 4) Запуск через Docker Compose
```bash
docker compose up --build
```

### 5) Проверка документации API
`http://localhost:8000/docs`

### 6) Проверка healthcheck
```bash
curl http://localhost:8000/health
```

### 7) Запуск тестов
```bash
docker compose run --rm tests
```

## DevSecOps-пайплайн (GitLab CI/CD)
Стадии в `.gitlab-ci.yml`:
- `lint`: Ruff - проверка качества кода
- `tests`: Pytest - unit-тесты API
- `sast`: Bandit и Semgrep - статический анализ уязвимостей
- `sca`: pip-audit - проверка зависимостей на известные CVE
- `build`: сборка Docker-образа и публикация в GitLab Container Registry
- `container_scan`: Trivy - сканирование Docker-образа
- `dast`: OWASP ZAP baseline scan против запущенного API

Важно: DAST должен запускаться против уже поднятого приложения (в текущем пайплайне используется `http://127.0.0.1:8000` внутри job).

## Примеры security-проверок
```bash
docker compose run --rm --user root tests /bin/sh -c "pip install bandit && bandit -r app -x tests -f txt"
docker compose run --rm --user root tests /bin/sh -c "pip install pip-audit && pip-audit -r requirements.txt"
docker build -t secure-notes:local .
trivy image secure-notes:local
```

## Учебные уязвимые кейсы
Папка `vulnerable_examples/` содержит учебные примеры.

Предупреждение:
- эти примеры намеренно содержат уязвимости
- они не используются основным приложением
- они добавлены только для обучения и проверки security-инструментов

Для каждой категории в `vulnerable_examples/README.md` указываются:
- тип уязвимости
- инструмент, который её выявляет
- связанный OWASP/CWE
- исправленная версия

## Документация по безопасности
- `SECURITY.md` - политика безопасности, правила ответственного раскрытия и базовые требования безопасности проекта.
- `docs/threat-model.md` - базовая модель угроз, активы, точки входа и ключевые риски.
- `docs/security-pipeline.md` - описание security-этапов в CI/CD и ожидаемых артефактов.
- `docs/owasp-mapping.md` - маппинг практик/уязвимостей на OWASP Top 10 и CWE.

## Что проект демонстрирует
- понимание secure SDLC
- умение контейнеризировать приложение
- умение встраивать security-инструменты в CI/CD
- базовое моделирование угроз
- базовый триаж и устранение уязвимостей
- понимание OWASP Top 10 и CWE-маппинга
- базовую автоматизацию деплоя через Ansible
- базовую IaC-структуру на Terraform

## Следующие улучшения
- ограничение частоты запросов (rate limiting) для API
- refresh-токены
- Kubernetes-манифесты
- проверки admission policy
- автоматизация обновления зависимостей
- security report artifacts в GitLab CI

## Известные ограничения текущей версии
- миграции Alembic пока не инициализированы (используется `Base.metadata.create_all`)
- по умолчанию приложение может работать на SQLite, если `DATABASE_URL` не задан
- пока не реализованы refresh-токены и ограничение частоты запросов
