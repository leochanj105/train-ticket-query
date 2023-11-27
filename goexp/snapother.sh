server=10.10.1.4
command="docker exec \$(docker ps | grep order-other-mongo | awk '{print \$(NF)}') mongorestore --drop /etc/othersnapshot"
ssh $server $command
