import requests

BASE = "http://127.0.0.1:5000"

# replace this with YOUR real content_id from /submit
content_id = "76d0f04f-a4b8-491e-a022-dfdbaa75d413"

res = requests.post(f"{BASE}/appeal", json={
    "content_id": content_id,
    "creator_reasoning": "I wrote this myself"
})

print(res.status_code)
print(res.json())