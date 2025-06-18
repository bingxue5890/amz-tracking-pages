
import os
import json
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))
tpl_index = env.get_template('index.html')
tpl_detail = env.get_template('tracking_page.html')

os.makedirs('tracking_pages', exist_ok=True)
cards = []

for file in os.listdir('data'):
    if file.endswith('.json'):
        with open(os.path.join('data', file), encoding='utf-8') as f:
            data = json.load(f)
        tracking_id = data.get("tracking_id")
        html = tpl_detail.render(**data)
        with open(f"tracking_pages/{tracking_id}.html", "w", encoding="utf-8") as out:
            out.write(html)
        cards.append({
            "tracking_id": tracking_id,
            "status": data.get("status", "未知"),
            "delivered_at": data.get("delivered_at", "未知")
        })

with open("tracking_pages/index.html", "w", encoding="utf-8") as f:
    f.write(tpl_index.render(tracking_cards=cards))
