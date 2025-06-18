
import os
os.system("python generate.py")
os.system("git add .")
os.system("git commit -m \"全量重构上传\"")
os.system("git push -f origin main")
