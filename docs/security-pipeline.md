# Security-пайплайн

CI/CD-пайплайн реализован в `.gitlab-ci.yml` и содержит:

1. `lint` - проверка качества кода (`ruff`)
2. `tests` - unit-тесты (`pytest`)
3. `sast` - `bandit` + `semgrep`
4. `sca` - `pip-audit` для Python-зависимостей
5. `build` - сборка Docker-образа и публикация в GitLab Container Registry
6. `container_scan` - сканирование опубликованного образа через `trivy`
7. `dast` - OWASP ZAP baseline против запущенного API

## Философия gate-проверок
- Уязвимости High/Critical в зависимостях или образе валят пайплайн
- SAST-находки видны на ранних этапах SDLC
- DAST baseline проверяет проблемы веб-слоя во время выполнения

## Локальное воспроизведение
```bash
docker compose run --rm tests
docker compose run --rm --user root tests /bin/sh -c "pip install ruff && ruff check app tests"
docker compose run --rm --user root tests /bin/sh -c "pip install bandit && bandit -r app -x tests -f txt"
docker compose run --rm --user root tests /bin/sh -c "pip install pip-audit && pip-audit -r requirements.txt"
docker build -t secure-notes:local .
trivy image secure-notes:local
```
