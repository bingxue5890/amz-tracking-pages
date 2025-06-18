import os
import json
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))
tracking_tpl = env.get_template('tracking_page.html')
index_tpl = env.get_template('index.html')

os.makedirs('tracking_pages', exist_ok=True)

tracking_ids = []

for file in os.listdir('data'):
    if file.endswith('.json'):
        with open(os.path.join('data', file), 'r', encoding='utf-8') as f:
            data = json.load(f)
        tracking_id = data.get("tracking_id", file.replace('.json', ''))
        html = tracking_tpl.render(
            tracking_id=tracking_id,
            status=data.get("status", "UNKNOWN"),
            carrier=data.get("carrier", "Amazon Logistics"),
            destination=data.get("destination", "N/A"),
            delivered_at=data.get("delivered_at", "N/A"),
            events=data.get("events", [])
        )
        with open(f'tracking_pages/{tracking_id}.html', 'w', encoding='utf-8') as out:
            out.write(html)
        tracking_ids.append(tracking_id)

# 生成首页
index_html = index_tpl.render(tracking_files=tracking_ids)
with open('tracking_pages/index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)
