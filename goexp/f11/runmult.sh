elist=$1

TPpath=/users/leochanj/TPnew
#bash ../snapother.sh
bash ../sendop.sh RemoveTP
curl --data-binary @$TPpath/tps11clab http://10.10.1.1:8766
sleep 1
curl --data-binary @$TPpath/tps11clab_stread http://10.10.1.1:8766
sleep 1
curl --data-binary @$TPpath/tps11clab_stwrite http://10.10.1.1:8766
sleep 1
bash ../otherctx.sh
bash ../ssoctx.sh
bash ../amctx.sh
bash ../deletedraw.sh
bash ../sendop.sh TPOn
bash ../sendop.sh SharedOn
sleep 5
bash runone.sh 400 f11_cancel_on_new < "$elist"

echo 'running noorm ctx at all...'
bash ../rmotherctx.sh
bash ../rmssoctx.sh
bash ../rmamctx.sh
bash ../rmdrawback.sh
bash ../deletedraw.sh
bash ../sendop.sh TPOff
bash ../sendop.sh SharedOff
sleep 5
bash runone.sh 400 f11_cancel_off_new < "$elist"
