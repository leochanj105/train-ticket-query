

bash ../otherctx.sh
bash ../ssoctx.sh
bash ../amctx.sh

bash ../sendop.sh TPOn
bash ../sendop.sh SharedOn
bash runone.sh 200 cancel_on < explist

sleep 5

bash ../sendop.sh TPOff
bash ../sendop.sh SharedOff
bash runone.sh 200 cancel_off < explist
