docker run --rm -d -p 5671:5671 -p 5672:5672 \
-v $PWD/config/rabbitmq/rabbitmq.conf:/etc/rabbitmq/rabbitmq.conf \
-v $PWD/config/rabbitmq/cert.cer:/etc/cert.cer \
-v $PWD/config/rabbitmq/key.pem:/etc/key.pem \
--name rabbitmq rabbitmq:3.7.0
