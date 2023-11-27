server=10.10.1.4
command="docker exec \$(docker ps | grep order-other-mongo | awk '{print \$(NF)}') mongo --eval 'db.orders.updateMany({}, {\$set: { \"LumosContext\": \"84d29403477978cba9d6dba26f8be99a_115_000\" }  })'"
ssh $server $command
