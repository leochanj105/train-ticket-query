#!/usr/bin/env bash
set -u

direc=$1

restimes=1000
paytimes=1000
canceltimes=1000

loginres=($(python3 login.py))
aid=${loginres[0]}
token=${loginres[1]}

ssh node5 'docker exec $(docker ps | grep order-mongo | awk '\''{print $1}'\'') mongodump -o snapshot1'
ssh node4 'docker exec $(docker ps | grep inside-payment-mongo | awk '\''{print $1}'\'') mongodump -o snapshot1'
python3 warmup.py ${aid} ${token}

> time_reserve
> time_pay
> time_cancel

for i in $(seq 1 $restimes)
do
if ! ((i % 10)); then
    	echo ${i}
fi
ssh node5 'docker exec $(docker ps | grep order-mongo | awk '\''{print $1}'\'') mongorestore --drop snapshot1' 2> /dev/null
ssh node4 'docker exec $(docker ps | grep inside-payment-mongo | awk '\''{print $1}'\'') mongorestore --drop snapshot1' 2> /dev/null
orderId=$(python3 reserve_once.py ${aid} ${token})
#echo $orderId
done


ssh node5 'docker exec $(docker ps | grep order-mongo | awk '\''{print $1}'\'') mongodump -o snapshot2'
ssh node4 'docker exec $(docker ps | grep inside-payment-mongo | awk '\''{print $1}'\'') mongodump -o snapshot2'
for i in $(seq 1 $paytimes)
do
if ! ((i % 10)); then
    	echo ${i}
fi
ssh node5 'docker exec $(docker ps | grep order-mongo | awk '\''{print $1}'\'') mongorestore --drop snapshot2' 2> /dev/null
ssh node4 'docker exec $(docker ps | grep inside-payment-mongo | awk '\''{print $1}'\'') mongorestore --drop snapshot2' 2> /dev/null
python3 pay_once.py ${aid} ${token} ${orderId}
done


ssh node5 'docker exec $(docker ps | grep order-mongo | awk '\''{print $1}'\'') mongodump -o snapshot3'
ssh node4 'docker exec $(docker ps | grep inside-payment-mongo | awk '\''{print $1}'\'') mongodump -o snapshot3'
for i in $(seq 1 $canceltimes)
do
if ! ((i % 10)); then
    	echo ${i}
fi
ssh node5 'docker exec $(docker ps | grep order-mongo | awk '\''{print $1}'\'') mongorestore --drop snapshot3' 2> /dev/null
ssh node4 'docker exec $(docker ps | grep inside-payment-mongo | awk '\''{print $1}'\'') mongorestore --drop snapshot3' 2> /dev/null
python3 cancel_once.py ${aid} ${token} ${orderId}
done

mkdir -p ../${direc}
cp ./time* ../${direc}