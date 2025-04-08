import time
import hmac
import hashlib
import json

api_key = 'kIjSNmSvLsMkqjFo0m'
api_secret = 'WnjGSXmPen1jXbPwk7MHcUs3jffsTRuFpIhr'
timestamp = str(int(time.time() * 1000))
recv_window = '5000'

body = {
    "coin": "USDC",
    "chain": "POLYGON",
    "address": "0x789aca852cf967f06caff82448427dad8ab94a7b",
    "amount": "5",
    "timestamp": timestamp,
    "forceChain": 0,
    "accountType": "FUND"
}

# SERIALIZAÇÃO CORRETA (ordenada e sem espaços)
body_json = json.dumps(body, separators=(',', ':'), sort_keys=True)

payload = timestamp + api_key + recv_window + body_json
signature = hmac.new(api_secret.encode(), payload.encode(), hashlib.sha256).hexdigest()

print("🧪 Corpo serializado:", body_json)
print("🧪 Payload final:", payload)
print("🧪 Assinatura HMAC:", signature)
