#!/usr/bin/bash

curl --insecure --location --request POST 'https://oauth-rpa.argos-labs.com/oauth/token' --header 'Authorization: Basic YXJnb3MtYXBpOjc4Jiphcmdvcy1hcGkhQDEy' --header 'Content-Type: application/x-www-form-urlencoded' --data-urlencode 'grant_type=client_credentials'

# {"access_token":"d678be88-9827-48e4-b80b-f4cfedde3fd3","token_type":"bearer","expires_in":200948,"scope":"read write"}

curl --insecure \
  'https://api-rpa.argos-labs.com/report/v1/any_sql/query' \
  -H 'Connection: keep-alive' \
  -H 'Pragma: no-cache' \
  -H 'Cache-Control: no-cache' \
  -H 'sec-ch-ua: "Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"' \
  -H 'Authorization: Bearer d678be88-9827-48e4-b80b-f4cfedde3fd3' \
  -H 'DNT: 1' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36' \
  -H 'Content-Type: application/json' \
  -H 'Accept: */*' \
  -H 'Origin: https://admin-rpa.argos-labs.com' \
  -H 'Sec-Fetch-Site: same-site' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Referer: https://admin-rpa.argos-labs.com/' \
  -H 'Accept-Language: ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7' \
  --data-raw '{"queryId":"of_plugin_weekly_by_version","conditionMap":[]}' \
  --compressed > foo.json
