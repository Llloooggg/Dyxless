# Dyxless

### Конфигурация
Прежде всего необходимо создать файл **config.json** на основе приложенного шаблона

Инструкция для создания базы данных находится в:
```
runscripts/postgres/createdb
```
Для конфигурации и обноления структуры бд в Windows использовать скрипт:
```
runscripts/postgres/updatedb.bat
```
В Linux:
```
runscripts/postgres/updatedb.sh
```

### Запуск приложения
На Windows запускать через:
```
runscripts/windows/startserver.bat
```
На Linux через:
```
runscripts/linux/startserverdev.sh
```