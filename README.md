# Зачем этот проект?
- Поупрожняться с python, kafka, docker-swarm
- Использовать домашние мощности (несколько ноутбуков, raspberry pi, jetson nano) для обработки фотографий
- Собрать базу лиц известных и визуализировать с помощью [digiKam](https://www.digikam.org/) и [утилит для импорта](https://github.com/Tan4ek/digikam-utils)
- Собрать метаданные из изображений 

# Что необходимо иметь на всех машинах?
- docker-compose
- docker (engine version 18.09 +)
- настроенный локальный docker registry (или docker hub)
- примонтировать одинаковую папку где хранятся изображения
- на raspberry pi необходимо увеличить файл подкачки до 1gb минимум (в моих экспериментах используется raspberry pi 3)

# Шаги

## Сборка базового образа
Для распознавания лиц использую готовую библиотеку [face_recognition](https://github.com/ageitgey/face_recognition)
```bash
git clone git@github.com:ageitgey/face_recognition.git
cd face_reginition
docker build -t tan4ek.nas.local:5000/face_recognition:amd64 .
docker push tan4ek.nas.local:5000/face_recognition:amd64
```

Для raspberry pi необходимо собрать на основе [Dockerfile](#face_recognition_docker/Dockerfile.armhf) с тэгом `armhf`. Саму сборку осуществлять на малинке, длительность около 2-х часов

## Настроить конфигурацию

Поправить [config.ini](#config.ini). 
Важно поправить ip docker swarm master (в моем случае `192.168.100.201`) на свой. Указать путь до примонтированной папки с изображениями (`RootPathForScanning` параметр).

Параметр `CroppedFacesPath` путь куда будут сохранятся распознанные лица в виде изображения отдельных лиц.

Проверить [docker-compose.yml](#docker-compose.yml), поправить пути до примонтированной папки с изображениями

## Собрать docker images

Сборка:
```bash
docker build -f Dockerfile.file_scaner -t tan4ek.nas.local:5000/image-recognition_master:latest .
docker push tan4ek.nas.local:5000/image-recognition_master:latest

docker build -f Dockerfile -t tan4ek.nas.local:5000/image-recognition_worker:amd64 .
docker push tan4ek.nas.local:5000/image-recognition_worker:amd64

docker build -f Dockerfile -t tan4ek.nas.local:5000/image-recognition_face_worker:amd64 .
docker push tan4ek.nas.local:5000/image-recognition_face_worker:amd64
```

## Запуск и остановка docker stack

Для развертывания `docker swarm` необходимо иметь мастер `x64` архитектуры. Mongo версии 3+ уже не поддерживают `arm` сборку. Так же `kafka` требует много ресурсов для старка. На данном этапе это ограничение.

Для старта
```bash
docker stack deploy --compose-file docker-compose.yml image_recognition
```

Для остановки
```bash
docker stack rm image_recognition
```

# Как работает?

- `image-recognition_master` сканируем папку `RootPathForScanning` на изображения.
- Есть файла нет в базе (`ImageDb` параметр монго бд), то сохраняем в базу и кладем в `kafka` topic
- Из топика `kafka` `worker` (`image-recognition_worker`) забирает задачу 
- Ищет лицо, вырезает, сохраняет в `CroppedFacesPath`, кладет в другой `topic` сообщение
- Из топика сервис `image-recognition_master` сообщение о распознаных лицах и сохраняет в базу `ImageDb`

# Производительность

На данный момент используется проект [face_recognition](https://github.com/ageitgey/face_recognition) и по умолчанию используется CPU для распознования лиц.

На i7 фото 12Мб, 6000x3376 ~ 10c
На raspberry pi 3 12Mb 6000x3376 ~ 215c (большой разброс от нагрева)


