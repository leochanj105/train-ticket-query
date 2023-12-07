set -u
elist=$1

#bash ../snapother.sh

TPpath=/users/leochanj/TPnew
bash ../sendop.sh RemoveTP
bash ../sendop.sh SharedOff
bash ../sendop.sh TPOff
curl --data-binary @$TPpath/tps11clab http://10.10.1.1:8766
sleep 1
curl --data-binary @$TPpath/tps11clab_stread http://10.10.1.1:8766
sleep 1
curl --data-binary @$TPpath/tps11clab_stwrite http://10.10.1.1:8766
sleep 1

bash ../indexdraw.sh

echo 'running no tp/ormctx at all...'
bash ../rmotherctx.sh
bash ../rmssoctx.sh
bash ../rmamctx.sh
bash ../rmdrawback.sh
#bash ../deletedraw.sh
sleep 5
bash runone.sh 4000 f11_cancel_sample_4000 < "$elist"


