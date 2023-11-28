set -u
elist=$1

#bash ../snapother.sh
bash ../dbchange.sh 1
TPpath=/users/leochanj/TPnew
bash ../sendop.sh RemoveTP
curl --data-binary @$TPpath/tps8clab http://10.10.1.1:8766
sleep 1
curl --data-binary @$TPpath/tps8clab_stread http://10.10.1.1:8766
sleep 1
#curl --data-binary @$TPpath/tps8clab_stwrite http://10.10.1.1:8766
#sleep 1

echo 'running no tp/ormctx at all...'
bash ../sendop.sh TPOff
bash ../sendop.sh SharedOff
bash ../rmotherctx.sh
sleep 5
bash runone.sh 500 f8_calc_off_nj < "$elist"


echo 'running with everything now...'
bash ../sendop.sh TPOn
bash ../sendop.sh SharedOn
bash ../otherctx.sh
sleep 5
bash runone.sh 500 f8_calc_on_nj < "$elist"

