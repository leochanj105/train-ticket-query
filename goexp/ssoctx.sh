server=10.10.1.4
command="docker exec \$(docker ps | grep account-mongo | awk '{print \$(NF)}') mongo --eval 'db.getSiblingDB(\"ts\").login_user_list.updateMany({}, {\$set: { \"LumosContext\": \"84d29403477978cba9d6dba26f8be99a_115_000\" }  })'"
ssh $server $command
