### @export "cd"
cd myado

### @export "kill"
kill -TERM `cat pidfile`

### @export "check-killed"
curl -I http://localhost:$DEXY_PORT || echo "killed"
