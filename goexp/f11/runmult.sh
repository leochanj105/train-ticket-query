set -u
elist=$1

#bash ../snapother.sh

TPpath=/users/leochanj/TPnew
bash ../sendop.sh RemoveTP
curl --data-binary @$TPpath/tps11clab http://10.10.1.1:8766
sleep 1
bash ../sendop.sh TPOff
curl --data-binary @$TPpath/tps11clab_stread http://10.10.1.1:8766
sleep 1
curl --data-binary @$TPpath/tps11clab_stwrite http://10.10.1.1:8766
sleep 1

bash ../indexdraw.sh

echo 'running no tp/ormctx at all...'
bash ../sendop.sh SharedOff
bash ../rmotherctx.sh
bash ../rmssoctx.sh
bash ../rmamctx.sh
bash ../rmdrawback.sh
#bash ../deletedraw.sh
sleep 5
bash runone.sh 4000 f11_cancel_sample2_4000 < "$elist"

<<com
echo 'running with everything now...'

bash ../sendop.sh TPOn
bash ../sendop.sh SharedOn
bash ../otherctx.sh
bash ../ssoctx.sh
bash ../amctx.sh
#bash ../deletedraw.sh
sleep 5
bash runone.sh 4000 f11_cancel_on_4000 < "$elist"
com
<<com
echo 'running with a lot more now...'

for i in {1..30}
do
	curl --data-binary @$TPpath/tps11clab http://10.10.1.1:8766
done
bash ../sendop.sh TPOn
bash ../sendop.sh SharedOn
bash ../otherctx.sh
bash ../ssoctx.sh
bash ../amctx.sh
bash ../deletedraw.sh
sleep 5
bash runone.sh 500 f11_cancel_lot_comp < "$elist"
com



