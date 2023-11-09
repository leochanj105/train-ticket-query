
num=$1+5
server=10.10.1.4
command="docker exec \$(docker ps | grep order-mongo | awk '{print \$(NF)}') mongo --eval 'db.orders.find({},{_id:1}).limit($num).forEach(function(row){print(row._id.hex())})'"
ssh $server $command | tail -n +5 > tmp/ids
