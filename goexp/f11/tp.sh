set -u

TPpath=/users/leochanj/TPnew
bash ../sendop.sh TPOn
bash ../sendop.sh SharedOn
curl --data-binary @$TPpath/tps11clab http://10.10.1.1:8766
sleep 1
curl --data-binary @$TPpath/tps11clab_stread http://10.10.1.1:8766
sleep 1
curl --data-binary @$TPpath/tps11clab_stwrite http://10.10.1.1:8766
sleep 1
