server=10.10.1.4
command="docker exec \$(docker ps | grep order-other-mongo | awk '{print \$(NF)}') mongo --eval 'db.orders.updateMany({}, {\$unset: { \"LumosContext\":1}})'"
ssh $server $command
