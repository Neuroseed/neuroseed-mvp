docker run --rm --net=host \
-v ./config/rabbitmq/rabbitmq.conf:/etc/rabbitmq/rabbitmq.conf \
-v ./config/rabbitmq/cert.cer:/etc/cert.cer \
-v ./config/rabbitmq/key.pem:/etc/key.pem \
rabbitmq
