### @export "cd"
cd myado
echo $DEXY_PORT

### @export "kill"
kill -TERM `cat pidfile`

### @export "check-killed"
curl -I http://localhost:$DEXY_PORT || echo "killed"
