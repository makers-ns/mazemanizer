
if [ $# -lt 2 ]
then
  echo "Usage: $0 axis duty"
  exit 1
fi

URL="192.168.1.5"

curl "http://$URL/light/maze-$1/turn_on?brightness=$2" \
  -H 'Accept: */*' \
  -H 'Accept-Language: en-US,en;q=0.9,sr-RS;q=0.8,sr;q=0.7' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: text/plain;charset=UTF-8' \
  -H "Origin: http://$URL" \
  -H "Referer: http://$URL/" \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36' \
  --data-raw 'true' \
  --compressed \
  --insecure

  