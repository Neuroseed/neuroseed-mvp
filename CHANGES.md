# Neuroseed MVP Versions History

## v0.4.0

---

- Добавлены схемы для новых слоев:
- Activation
- Reshape
- Permute
- RepeatVector
- ActivityRegularization
- Masking
- Conv1D
- Cropping1D
- Cropping2D
- MaxPooling1D
- AveragePooling1D
- SimpleRNN
- ConvLSTM2D
- GRU
- LSTM
- Embedding
- BatchNormalization
- GaussianNoise
- GaussianDropout
- TimeDistributed
- Добавлены примеры создания и обучения нейронных сетей:
- CNN IMDB
- LSTM IMDB
- CNN LSTM IMDB
- MLP Reuters
- MLP mnist
- Новые слои доступны опционально

## v0.3.4

---

- Исправлен баг с дублированием расширениея файла hdf5
- Добавлена ротация логов для WEB API
- Каждый процесс из пула процессов ворке пишет логи в отдельный файл
- Исправлены базовые значения полей strides, dilation в json-схемах слоев
- Добавлена авторизация к celery flower

## v0.3.3

---

- Добавлена обработка невозможности подключения к rabbitmq
- Файл CHANGES.txt преобразован к формату Markdown
- Добавлен монитор задач Celery Flower
- Роут загрузки датасета возвращает информацию о полученом файле
- Логика программы перенесена с falcon WEB API в manager/metadata
- Добавлена возможность использовать консольные команды celery
- Worker сохраняет в базу данных статус задачи SUCCESS, FAILURE
- Исправлены ошибки в роуте model/predict/<tid>/result
- WEB API возвращает дополнительные данные для датасетов owner, hash, size, date

## v0.3.2

---

- MVP REST API теперь доступна по домену https://api.neuroseed.net
- Воркер тепрь не сохраняет информацию о метриках на бтачах для повышения производительности
- Воркер сохраняет информацию о количестве пройденных примеров
- Исправлен баг конфигурации Celery
- Во все json-схемы добавлены поля title, description, default
- Добавлен таймаут подключения к mongodb и rabbitmq (celery)

## v0.3.1

---

- В json-схемы добавлены поля title, description, default
- Из json-схемы удалены не используемые поля
- Протестирован роут DELETE /api/v1/task/<id> - остановка и удаление запущенной задачи
- Переименован роут schema/layer -> schema/model/layers
- При создании архитектуры id назначается автоматически

## v0.3.0

---

- Добавлены роуты возвращающие json-схемы валидации данных
- /api/v1/schema/dataset
- /api/v1/schema/architecture
- /api/v1/schema/model
- /api/v1/schema/model/train
- /api/v1/schema/model/test
- /api/v1/schema/model/predict
- /api/v1/schema/task
- /api/v1/schema/layers
- Добавлено описание новых роутов во внутреннюю документацию

## v0.2.3

---

- Update layers json-schemas
- Validate values in json-schemas
- Edit readme.md
- Worker handle exceptions
- Refactor worker code
- Improve docker containers start scripts
- Add simple worker tests

## v0.2.2rc

---

- Add WEB API
- Add Worker
- Add Dataset, Architecture, Model, Task resources
- Add WEB API Authorization
- Add data validation on json-schemas
- Add examples code
- Add test for WEB API
