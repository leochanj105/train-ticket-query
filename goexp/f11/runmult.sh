set -u
elist=$1

#bash ../snapother.sh

TPpath=/users/leochanj/TPnew
bash ../sendop.sh RemoveTP
curl --data-binary @$TPpath/tps11clab http://10.10.1.1:8766
sleep 1
curl --data-binary @$TPpath/tps11clab_stread http://10.10.1.1:8766
sleep 1
curl --data-binary @$TPpath/tps11clab_stwrite http://10.10.1.1:8766
sleep 1

echo 'running no tp/ormctx at all...'
bash ../sendop.sh TPOff
bash ../sendop.sh SharedOff
bash ../rmotherctx.sh
bash ../rmssoctx.sh
bash ../rmamctx.sh
bash ../rmdrawback.sh
bash ../deletedraw.sh
sleep 5
bash runone.sh 500 f11_cancel_off_tr < "$elist"


echo 'running with everything now...'

bash ../sendop.sh TPOn
bash ../sendop.sh SharedOn
bash ../otherctx.sh
bash ../ssoctx.sh
bash ../amctx.sh
bash ../deletedraw.sh
sleep 5
bash runone.sh 500 f11_cancel_on_tr < "$elist"

