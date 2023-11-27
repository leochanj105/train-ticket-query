server=10.10.1.4
command="docker exec \$(docker ps | grep inside-payment-mongo | awk '{print \$(NF)}') mongo --eval 'db.getSiblingDB(\"ts\").addMoney.updateMany({}, {\$unset: { \"LumosContext\": 1} })'"
ssh $server $command
