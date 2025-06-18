import os
import json
from jinja2 import Environment, FileSystemLoader

# 配置Jinja2环境
env = Environment(loader=FileSystemLoader("templates"))

# 数据文件夹路径
data_dir = "data"

def load_logistics_data():
    """加载所有物流数据"""
    logistics = []
    for filename in os.listdir(data_dir):
        if filename.endswith(".json"):
            try:
                with open(os.path.join(data_dir, filename), "r", encoding="utf-8") as f:
                    data = json.load(f)
                    logistics.append(data)
            except Exception as e:
                print(f"加载{filename}失败: {e}")
    return logistics

def generate_index_page(logistics):
    """生成首页HTML"""
    index_template = env.get_template("index.html")
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(index_template.render(logistics=logistics))
    print("首页生成成功: index.html")

def generate_detail_pages(logistics):
    """生成每个物流的详情页"""
    detail_template = env.get_template("detail.html")
    for item in logistics:
        tracking_id = item.get("tracking_id", "未知单号")
        filename = f"{tracking_id.replace('/', '_')}.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(detail_template.render(logistics=item))
        print(f"详情页生成成功: {filename}")

def main():
    # 确保数据文件夹存在
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"创建数据文件夹: {data_dir}")
        print("请在data文件夹中添加物流JSON数据")
        return
    
    # 加载数据并生成页面
    logistics = load_logistics_data()
    if not logistics:
        print("未找到物流数据，请在data文件夹中添加JSON文件")
        return
    
    generate_index_page(logistics)
    generate_detail_pages(logistics)
    print("所有页面生成完成!")

if __name__ == "__main__":
    main()