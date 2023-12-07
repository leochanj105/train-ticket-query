server=10.10.1.4
command="docker exec \$(docker ps | grep ts-payment-mongo | awk '{print \$(NF)}') mongo --eval 'db.getSiblingDB(\"ts\").payment.createIndex({'orderId':1})'"
ssh $server $command
