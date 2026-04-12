import os
import time
import re
import subprocess

def build():
    print("--- 開始執行一鍵更新流程 ---")
    
    # 1. 執行抓取
    print("1. 正在從環境部 API 抓取最新資料...")
    subprocess.run(["python", "fetch_all_toilets.py"])
    
    # 2. 執行清理
    print("2. 正在執行資料清理與聚合...")
    subprocess.run(["python", "clean_toilets.py"])
    
    # 3. 搬移資料至根目錄
    print("3. 正在封裝資料包...")
    if os.path.exists("research_data/cleaned_toilets.json"):
        import shutil
        shutil.copy("research_data/cleaned_toilets.json", "toilets.json")
        print("   - toilets.json 已更新")
    
    # 4. 更新 Service Worker 版本號
    print("4. 正在更新程式快取版本號...")
    new_version = time.strftime("%Y%m%d-%H%M%S")
    sw_path = "sw.js"
    
    if os.path.exists(sw_path):
        with open(sw_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = re.sub(
            r"const CACHE_NAME = 'toilet-app-v[^']+';",
            f"const CACHE_NAME = 'toilet-app-v{new_version}';",
            content
        )
        
        with open(sw_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"   - sw.js 版本已更新為: {new_version}")

    print("--- 更新完成！您的 PWA 應用程式已備妥最新資料 ---")

if __name__ == "__main__":
    build()
