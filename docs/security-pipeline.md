# Security-пайплайн

CI/CD-пайплайн реализован в `.gitlab-ci.yml` и показывает базовый secure SDLC для небольшого API.

## Стадии
1. `lint` - проверка качества кода через `ruff`.
2. `tests` - API/regression-тесты через `pytest`.
3. `sast` - статический анализ безопасности через `bandit` и `semgrep`.
4. `sca` - проверка Python-зависимостей через `pip-audit`.
5. `build` - сборка Docker image и публикация в GitLab Container Registry.
6. `container_scan` - сканирование опубликованного Docker image через `trivy`.
7. `dast` - OWASP ZAP baseline scan против запущенного API.

## Gate-философия
- Тесты и lint должны проходить до security-сканирования.
- SAST/SCA/container scan дают раннюю обратную связь до ручной проверки.
- High/Critical уязвимости в зависимостях или контейнере должны останавливать pipeline.
- DAST запускается только после успешного `/health`, без фиксированного ожидания `sleep`.
- ZAP baseline запускается с `--autooff`, чтобы использовать стабильный classic baseline output и не зависеть от временных артефактов Automation Framework.
- Локальные секреты не должны попадать в Docker build context: для этого используется `.dockerignore`.

## Локальное воспроизведение
```bash
docker compose run --rm tests
docker compose run --rm --user root tests /bin/sh -c "pip install ruff && ruff check app tests"
docker compose run --rm --user root tests /bin/sh -c "pip install bandit && bandit -r app -x tests -f txt"
docker run --rm -v "${PWD}:/src" -w /src semgrep/semgrep:latest semgrep --config auto app
docker compose run --rm --user root tests /bin/sh -c "pip install pip-audit && pip-audit -r requirements.txt"
docker build -t secure-notes:local .
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image secure-notes:local
```

## Проверенный статус
```text
pytest: 9 passed
Ruff: all checks passed
Bandit: no issues identified
Semgrep: 0 findings
pip-audit: no known vulnerabilities
Trivy: 0 vulnerabilities
OWASP ZAP baseline: 0 FAIL, 0 WARN
```
