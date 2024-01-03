https://www.strava.com/oauth/authorize?client_id=119119&redirect_uri=http://localhost&response_type=code&scope=activity:read_all

http://localhost/?state=&code=162a78c8e31ae3fe4c8847d192704208eba6f106&scope=read,activity:read_all


 curl -X POST https://www.strava.com/oauth/token \
 -F client_id=119119 \
 -F client_secret='b5bf66e3e833464b266c4b985d9c64de65948624' \
 -F code='162a78c8e31ae3fe4c8847d192704208eba6f106' \
 -F grant_type='2996c6e27c5950e6326104d6bef172a8777e43a2'