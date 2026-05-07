# OWASP / CWE / SANS: маппинг

## Базовые API-контроли
- **A01 Broken Access Control**: доступ к заметкам в пределах пользователя (фильтры `owner_id`)
- **A02 Cryptographic Failures**: хеширование паролей + подпись JWT
- **A03 Injection**: доступ к БД через ORM, без динамического SQL в основном приложении
- **A05 Security Misconfiguration**: hardening контейнера и сканирование в CI
- **A06 Vulnerable Components**: сканирование зависимостей через `pip-audit`
- **A07 Identification and Authentication Failures**: валидация JWT и безопасный login-flow

## Покрытие уязвимых примеров
| Example | OWASP | CWE | SANS Top 25 relation |
|---|---|---|---|
| Hardcoded secret | A02 | CWE-798 | Improper credential management |
| Insecure JWT validation | A07 | CWE-347 | Improper verification |
| SQL injection | A03 | CWE-89 | Injection flaws |
| Vulnerable dependencies | A06 | CWE-1104 | Using vulnerable components |
| Insecure Dockerfile | A05 | CWE-250 | Over-privileged execution |

## Приоритизация
- **P1 (high)**: эксплуатируемый auth bypass, SQL injection, critical CVE
- **P2 (medium)**: мисконфигурации и hardcoded secrets в non-prod модулях
- **P3 (low)**: информационные возможности для hardening
