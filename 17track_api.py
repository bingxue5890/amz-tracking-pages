
import requests
import json
import time

TOKEN = "YOUR_17TRACK_API_KEY"
HEADERS = {"Content-Type": "application/json", "17token": TOKEN}

def fetch_tracking_data(tracking_number):
    requests.post("https://api.17track.net/track/v2/register", headers=HEADERS, json={"nums": [tracking_number]})
    time.sleep(2)
    res = requests.post("https://api.17track.net/track/v2/gettrackinfo", headers=HEADERS, json={"nums": [tracking_number]})
    data = res.json()
    try:
        info = data["data"]["items"][0]
        events = [{
            "time": e.get("Date", ""),
            "location": e.get("Location", ""),
            "status": e.get("StatusDescription", "")
        } for e in info.get("origin_info", {}).get("trackinfo", [])]
        result = {
            "tracking_id": info.get("number", ""),
            "status": info.get("lastEvent", "In transit"),
            "carrier": info.get("carrier", "Unknown"),
            "destination": info.get("destination_country", ""),
            "delivered_at": events[-1]["time"] if events else "",
            "events": events
        }
        with open(f"data/{info['number']}.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"✅ 已保存：{info['number']}.json")
    except Exception as e:
        print("❌ 抓取失败：", e)

if __name__ == "__main__":
    nums = ["TBA321632211637"]
    for num in nums:
        fetch_tracking_data(num)
