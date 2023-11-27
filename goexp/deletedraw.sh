server=10.10.1.4
command="docker exec \$(docker ps | grep ts-inside-payment-mongo | awk '{print \$(NF)}') mongo --eval 'db.getSiblingDB(\"ts\").drawBack.deleteMany({})'"
ssh $server $command
