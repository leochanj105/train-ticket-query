
num=$1
server=10.10.1.4
command="docker exec \$(docker ps | grep order-mongo | awk '{print \$(NF)}') mongo --eval 'var copy = db.orders.findOne({},{_id:0}); for (var i = 0; i<$1; i++){db.orders.insert(copy);}'"
ssh $server $command
