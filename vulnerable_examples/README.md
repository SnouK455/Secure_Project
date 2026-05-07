# Уязвимые примеры (только для обучения)

Эти примеры намеренно содержат уязвимости и отделены от основного (production) приложения.

## 1) Захардкоженный секрет
- Уязвимый вариант: `hardcoded_secret_vuln.py`
- Исправленный вариант: `hardcoded_secret_fixed.py`
- Сканер: Bandit / Semgrep
- OWASP/CWE: A02 Cryptographic Failures, CWE-798

## 2) Небезопасная обработка JWT
- Уязвимый вариант: `jwt_insecure_vuln.py`
- Исправленный вариант: `jwt_insecure_fixed.py`
- Сканер: Semgrep
- OWASP/CWE: A07 Identification and Authentication Failures, CWE-347

## 3) SQL-инъекция
- Уязвимый вариант: `sqli_vuln.py`
- Исправленный вариант: `sqli_fixed.py`
- Сканер: Bandit / Semgrep
- OWASP/CWE: A03 Injection, CWE-89

## 4) Уязвимые зависимости
- Уязвимый вариант: `requirements_vuln.txt`
- Исправленный вариант: `requirements_fixed.txt`
- Сканер: pip-audit / Trivy
- OWASP/CWE: A06 Vulnerable and Outdated Components, CWE-1104

## 5) Небезопасная конфигурация контейнера
- Уязвимый вариант: `Dockerfile.vuln`
- Исправленный вариант: `Dockerfile.fixed`
- Сканер: Trivy
- OWASP/CWE: A05 Security Misconfiguration, CWE-250
