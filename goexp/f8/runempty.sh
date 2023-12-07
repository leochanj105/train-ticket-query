set -u
elist=$1

#bash ../snapother.sh
bash ../otherchange.sh 1
bash ../sendop.sh TPOff
bash ../sendop.sh SharedOff
TPpath=/users/leochanj/TPnew
bash ../sendop.sh RemoveTP
curl --data-binary @$TPpath/tps8clab http://10.10.1.1:8766
sleep 1
curl --data-binary @$TPpath/tps8clab_stread http://10.10.1.1:8766
sleep 1
#curl --data-binary @$TPpath/tps8clab_stwrite http://10.10.1.1:8766
#sleep 1

echo 'running nothing at all...'
bash ../rmotherctx.sh
sleep 5
bash runone.sh 5000 f8_calc_empty_5000s < "$elist"

