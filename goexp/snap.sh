server=10.10.1.4
command="docker exec \$(docker ps | grep order-mongo | awk '{print \$(NF)}') mongorestore --drop /etc/ordersnapshot"
ssh $server $command
