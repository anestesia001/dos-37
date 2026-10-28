1) Написать роль (роли?) для развертывания приложения https://gitlab.com/devops201206/visits НЕ в docker
2) Написать роль для установки node-exporter НЕ в docker
3) Написать роль для настройки времени и часового пояса с помощью chrony или ntpd
4) Написать роль для установки и настройки auditd; роль должна включать
- настройку основного конфигурационного файла /etc/audit/auditd.conf через шаблон Jinja2
  - log_file
  - max_log_file
  - num_logs
  - space_left_action
  - admin_space_left
- управление правилами аудита: размещение правил в /etc/audit/rules.d/security.rules с помощью шаблона и переменных
```yaml
auditd_rules:
  - "-a always,exit -F arch=b64 -S open,openat -F success=1"
  - "-w /etc/passwd -p wa -k identity"
  - "-w /etc/sudoers -p wa -k scope"
```
