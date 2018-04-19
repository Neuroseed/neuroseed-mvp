docker run --rm -d -p 127.0.0.1:5671:5671 \
-v $PWD/config/rabbitmq/rabbitmq.conf:/etc/rabbitmq/rabbitmq.conf \
-v $PWD/config/rabbitmq/cert.cer:/etc/cert.cer \
-v $PWD/config/rabbitmq/key.pem:/etc/key.pem \
--name rabbitmq rabbitmq:3.7.0
