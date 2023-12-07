
num=$1
server=10.10.1.4
command="docker exec \$(docker ps | grep order-mongo | awk '{print \$(NF)}') mongo --eval 'db.orders.updateMany({}, {\$set: { status: ${num} }  })'"
ssh $server $command
