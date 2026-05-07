# Security-пайплайн

CI/CD-пайплайн реализован в `.gitlab-ci.yml` и содержит:

1. `lint` - проверка качества кода (`ruff`)
2. `tests` - unit-тесты (`pytest`)
3. `sast` - `bandit` + `semgrep`
4. `sca` - `pip-audit` для Python-зависимостей
5. `container_scan` - сканирование образа через `trivy`
6. `dast` - OWASP ZAP baseline против запущенного API
7. `build` - сборка Docker-образа

## Философия gate-проверок
- Уязвимости High/Critical в зависимостях или образе валят пайплайн
- SAST-находки видны на ранних этапах SDLC
- DAST baseline проверяет проблемы веб-слоя во время выполнения

## Локальное воспроизведение
```bash
pip install -r requirements.txt
pytest -q
bandit -r app -x tests
semgrep --config auto app
pip-audit -r requirements.txt
docker build -t secure-notes:local .
trivy image secure-notes:local
```
