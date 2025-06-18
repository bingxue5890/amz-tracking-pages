
import os

os.system("python generate.py")
os.system("git add .")
os.system("git commit -m \"自动更新轨迹页面\"")
os.system("git push origin main")
