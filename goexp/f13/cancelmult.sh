set -u
elist=$1

#bash ../snapother.sh

TPpath=/users/leochanj/TPnew
bash ../sendop.sh RemoveTP
curl --data-binary @$TPpath/tps13clab http://10.10.1.1:8766
sleep 1
bash ../sendop.sh TPOff
curl --data-binary @$TPpath/tps13clab_stread http://10.10.1.1:8766
sleep 1
curl --data-binary @$TPpath/tps13clab_stwrite http://10.10.1.1:8766
sleep 1
bash ../sendop.sh SharedOff

echo 'running no tp/ormctx at all...'
bash ../rmorderctx.sh
bash ../rmssoctx.sh
bash ../rmamctx.sh
#bash ../deletepay.sh
sleep 5
bash cancelone.sh 5000 f13_cancel_coarse_5000s < "$elist"

echo 'running with everything now...'


bash ../sendop.sh TPOn
bash ../sendop.sh SharedOn
bash ../orderctx.sh
bash ../ssoctx.sh
bash ../amctx.sh
#bash ../deletepay.sh
sleep 5
bash cancelone.sh 5000 f13_cancel_on_5000s < "$elist"
