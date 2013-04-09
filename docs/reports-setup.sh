### @export "create conf"
echo "plugins: 'ado.dexy_plugins'" > dexy.conf

### @export "gen"
dexy gen -t adoreport -d myado
cd myado
ls

### @export "run"
dexy setup
dexy

### @export "start-server"
echo $DEXY_PORT
nohup dexy serve -port $DEXY_PORT &
echo $! > pidfile
sleep 2
cat nohup.out
curl -I "http://localhost:$DEXY_PORT"
