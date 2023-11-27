server=10.10.1.4
command="docker exec \$(docker ps | grep account-mongo | awk '{print \$(NF)}') mongo --eval 'db.getSiblingDB(\"ts\").login_user_list.updateMany({}, {\$unset: { \"LumosContext\": 1 }  })'"
ssh $server $command
