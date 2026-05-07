# Secure Notes API с DevSecOps-пайплайном

Портфолио-проект по DevSecOps/AppSec на базе FastAPI. Проект показывает полный практический путь secure SDLC на небольшом, но рабочем backend API: аутентификация, контроль доступа, контейнеризация, CI/CD security gates, SAST/SCA/container scan/DAST, threat modeling и учебные vulnerable/fixed примеры.

English summary: portfolio DevSecOps/AppSec project built around a working FastAPI service. It demonstrates secure API development, Docker delivery, GitLab CI/CD security checks, OWASP/CWE mapping, and vulnerability remediation examples.

## Что демонстрирует проект
- Secure SDLC на компактном API: код, тесты, контейнеризация, CI/CD и security checks.
- Практическое понимание AppSec/DevSecOps.
- Умение встроить security-инструменты в pipeline: Ruff, Pytest, Bandit, Semgrep, pip-audit, Trivy, OWASP ZAP.
- Базовое моделирование угроз, OWASP Top 10/CWE mapping и triage уязвимостей.
- Разделение production-кода и намеренно уязвимых примеров для обучения и демонстрации исправлений.

## Возможности
- Регистрация пользователей.
- Логин с JWT access token.
- Хеширование паролей через bcrypt.
- CRUD-операции для приватных заметок.
- Контроль доступа на уровне пользователя: пользователь видит только свои заметки.
- Валидация входных данных через Pydantic, включая защиту от пустых и whitespace-only значений.
- Конфигурация через переменные окружения.
- PostgreSQL в Docker Compose.
- Security headers для базового hardening API.
- Docker image запускается под non-root пользователем.
- `.dockerignore` исключает локальные секреты, кеши, базы и служебные файлы из build context.

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
- Alembic подключен как зависимость, но миграции пока не инициализированы

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
  -> zap_scan
```

Приложение рассчитано на запуск через Docker Compose. В Docker-сценарии PostgreSQL используется как основная база данных.

## Структура проекта
```text
app/                    # FastAPI-приложение: auth + notes
tests/                  # тесты Pytest
infra/                  # вспомогательные CI-артефакты, включая ZAP config
ansible/                # базовый пример автоматизации деплоя
terraform/              # базовый пример IaC
docs/                   # документация по безопасности
vulnerable_examples/    # намеренно уязвимые примеры + исправленные версии
Dockerfile
docker-compose.yml
.gitlab-ci.yml
README.md
SECURITY.md
```

## Быстрый старт
### 1. Клонирование репозитория
```bash
git clone <repo-url>
cd <repository-folder>
```

### 2. Создание `.env` из шаблона
```bash
cp .env.example .env
```

Для PowerShell:
```powershell
Copy-Item .env.example .env
```

### 3. Настройка локальных переменных окружения
Пример `.env`:

```env
POSTGRES_DB=securenotes
POSTGRES_USER=appuser
POSTGRES_PASSWORD=replace_with_local_postgres_password
SECRET_KEY=replace_with_random_secret_at_least_32_bytes
ALGORITHM=HS256
DATABASE_URL=postgresql+psycopg2://appuser:replace_with_local_postgres_password@db:5432/securenotes
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Для локальной разработки используйте тестовые значения. Не коммитьте реальные секреты. Для CI/CD и окружений развёртывания используйте защищённые переменные/secrets.

### 4. Запуск через Docker Compose
```bash
docker compose up --build
```

### 5. Открытие документации API
```text
http://localhost:8000/docs
```

### 6. Проверка health endpoint
```bash
curl http://localhost:8000/health
```

Ожидаемый ответ:
```json
{"status":"ok"}
```

### 7. Запуск тестов
```bash
docker compose run --rm tests
```

Ожидаемый результат:
```text
9 passed
```

## Ручной demo-сценарий
Используйте Swagger UI по адресу `http://localhost:8000/docs`:

1. `POST /auth/register` - создать пользователя.
2. `POST /auth/login` - получить JWT access token.
3. Нажать `Authorize` и вставить JWT token.
4. `GET /notes` - проверить, что авторизованный пользователь может получить список заметок.
5. `POST /notes` - создать приватную заметку.
6. `GET /notes/{note_id}` - прочитать заметку.
7. `PUT /notes/{note_id}` - обновить заметку.
8. `DELETE /notes/{note_id}` - удалить заметку.
9. Создать второго пользователя и проверить, что он не может получить доступ к заметкам первого пользователя.

Негативные проверки, которые стоит попробовать:
- пустые поля заметки возвращают `422 Validation Error`;
- поля из одних пробелов возвращают `422 Validation Error`;
- заголовок длиннее 120 символов возвращает `422 Validation Error`;
- отсутствующий или некорректный JWT возвращает `401 Unauthorized`.

## DevSecOps-пайплайн
GitLab CI/CD pipeline описан в `.gitlab-ci.yml`:

- `lint`: проверка качества кода через Ruff.
- `tests`: API-тесты через Pytest.
- `sast`: статический анализ безопасности через Bandit и Semgrep.
- `sca`: проверка зависимостей на известные уязвимости через pip-audit.
- `build`: сборка Docker image и публикация в GitLab Container Registry.
- `container_scan`: сканирование Docker image через Trivy.
- `zap_scan`: кастомный OWASP ZAP baseline scan против запущенного API.

DAST job ждёт успешный ответ `/health` перед запуском ZAP, вместо фиксированного `sleep`.

## Локальные команды проверки
Запуск тестов:
```bash
docker compose run --rm tests
```

Запуск lint:
```bash
docker compose run --rm --user root tests /bin/sh -c "pip install ruff && ruff check app tests"
```

Запуск Bandit:
```bash
docker compose run --rm --user root tests /bin/sh -c "pip install bandit && bandit -r app -x tests -f txt"
```

Запуск Semgrep:
```bash
docker run --rm -v "${PWD}:/src" -w /src semgrep/semgrep:latest semgrep --config auto app
```

Запуск pip-audit:
```bash
docker compose run --rm --user root tests /bin/sh -c "pip install pip-audit && pip-audit -r requirements.txt"
```

Сборка и сканирование Docker image:
```bash
docker build -t secure-notes:local .
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image secure-notes:local
```

Локальный запуск OWASP ZAP baseline против запущенного API:
```bash
docker run --rm \
  -v "${PWD}/infra/zap:/zap/wrk" \
  zaproxy/zap-stable:latest \
  zap-baseline.py \
  --autooff \
  -t http://host.docker.internal:8000 \
  -m 2 \
  -I \
  -c /zap/wrk/baseline.conf
```

Версия для PowerShell:
```powershell
docker run --rm `
  -v "${PWD}\infra\zap:/zap/wrk" `
  zaproxy/zap-stable:latest `
  zap-baseline.py `
  --autooff `
  -t http://host.docker.internal:8000 `
  -m 2 `
  -I `
  -c /zap/wrk/baseline.conf
```

## Статус проверок
Актуальные результаты локальной проверки:

```text
pytest: 9 passed
Ruff: all checks passed
Bandit: no issues identified
Semgrep: 0 findings
pip-audit: no known vulnerabilities
Trivy: 0 vulnerabilities
OWASP ZAP baseline: 0 FAIL, 0 WARN
Docker build: passed
Docker Compose startup: passed
```

## Документация по безопасности
- `SECURITY.md` - политика безопасности, responsible disclosure flow и базовые security-принципы.
- `docs/threat-model.md` - базовая модель угроз, активы, точки входа, ключевые риски и реализованные контроли.
- `docs/security-pipeline.md` - security-этапы CI/CD и ожидаемые артефакты.
- `docs/owasp-mapping.md` - маппинг на OWASP Top 10 и CWE.

## Учебные уязвимые примеры
Папка `vulnerable_examples/` содержит намеренно уязвимые учебные примеры и исправленные версии.

Эти примеры:
- намеренно содержат уязвимости;
- отделены от основного приложения;
- не используются основным API;
- добавлены только для обучения, проверки сканеров и демонстрации исправления.

Примеры покрывают:
- hardcoded secret;
- небезопасную обработку JWT;
- SQL injection;
- уязвимые зависимости;
- небезопасную конфигурацию Dockerfile.

Для каждой категории указаны:
- уязвимая версия;
- исправленная версия;
- сканер/инструмент, который выявляет проблему;
- связанный OWASP/CWE mapping.

## Что обсуждать на интервью
Этот проект можно использовать, чтобы обсудить:

- secure API design и проверки авторизации;
- обработку JWT и хеширование паролей;
- валидацию входных данных и regression testing;
- Docker hardening и запуск от non-root пользователя;
- сканирование зависимостей и контейнеров;
- различия между SAST, SCA и DAST;
- OWASP Top 10 и CWE mapping;
- основы threat modeling;
- CI/CD security gates и условия падения pipeline;
- triage и процесс исправления уязвимостей.

## План развития
- Инициализировать Alembic migrations вместо использования `Base.metadata.create_all`.
- Добавить rate limiting для auth endpoints.
- Добавить refresh tokens.
- Добавить Kubernetes manifests.
- Добавить admission policy checks.
- Добавить автоматизацию обновления зависимостей.
- Экспортировать GitLab security report artifacts.

## Известные ограничения
- Alembic migrations пока не инициализированы.
- Приложение всё ещё может fallback'нуться на SQLite, если `DATABASE_URL` не задан.
- Refresh tokens и rate limiting пока не реализованы.
- Terraform и Ansible примеры намеренно базовые: они демонстрируют структуру, а не production-grade инфраструктуру.
