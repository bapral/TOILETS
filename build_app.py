"""
全國公廁 App 一鍵更新建置腳本 (Build Tool)
功能：自動串聯 抓取 -> 清理 -> 封裝 -> 更新版本號 的完整流程。
"""

import os
import time
import re
import subprocess
import shutil

def build():
    print("========================================")
    print("   開始執行全國公廁 App 一鍵更新流程")
    print("========================================")
    
    # 1. 抓取最新原始資料
    print("\n[步驟 1/4] 正在從環境部 API 同步最新數據...")
    subprocess.run(["python", "fetch_all_toilets.py"])
    
    # 2. 清理與聚合資料
    print("\n[步驟 2/4] 正在執行資料清洗與座標聚合...")
    subprocess.run(["python", "clean_toilets.py"])
    
    # 3. 封裝資料包至根目錄
    # 將資料視為程式的一部分，讓 PWA 的 Service Worker 可以快取
    print("\n[步驟 3/4] 正在封裝靜態資料包...")
    source_data = "research_data/cleaned_toilets.json"
    target_data = "toilets.json"
    if os.path.exists(source_data):
        shutil.copy(source_data, target_data)
        print(f"   - {target_data} 更新成功")
    else:
        print("   - [錯誤] 找不到清理後的資料，終止更新。")
        return
    
    # 4. 更新 Service Worker 快取版本號
    # 透過修改 sw.js 內的 CACHE_NAME，強制手機端 App 在下次啟動時下載新資料
    print("\n[步驟 4/4] 正在產生新的快取版本編號...")
    new_version = time.strftime("%Y%m%d-%H%M%S") # 使用時間戳作為版本號
    sw_path = "sw.js"
    
    if os.path.exists(sw_path):
        with open(sw_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 使用正規表達式替換 CACHE_NAME 的值
        new_content = re.sub(
            r"const CACHE_NAME = 'toilet-app-v[^']+';",
            f"const CACHE_NAME = 'toilet-app-v{new_version}';",
            content
        )
        
        with open(sw_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"   - sw.js 版本已更新為: v{new_version}")

    print("\n========================================")
    print("   更新完成！App 已備妥最新資料包。")
    print("========================================")

if __name__ == "__main__":
    build()
