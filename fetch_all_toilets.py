"""
全國公廁資料抓取工具 (Fetch Tool)
功能：從環境部環境資料開放平臺 API 抓取全台灣所有公廁資料。
"""

import requests
import json
import os
import urllib3

# 停用不安全的請求警告（針對環境部 API 的 SSL 憑證問題）
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 配置參數
API_KEY = "8ca57585-60c7-4c05-a90e-4368bc232ef6"
BASE_URL = "https://data.moenv.gov.tw/api/v2/fac_p_07"
OUTPUT_FILE = "research_data/all_toilets.json"

def fetch_all():
    """
    循環執行 API 請求，處理分頁 (Pagination)，直到抓取所有紀錄。
    """
    all_records = []
    limit = 1000  # API 每次請求的筆數上限
    offset = 0    # 分頁偏移量
    
    print(f"--- 開始抓取原始資料 ---")
    
    while True:
        # 組合 API 請求網址
        url = f"{BASE_URL}?api_key={API_KEY}&format=JSON&limit={limit}&offset={offset}"
        print(f"進度: 已抓取 {offset} 筆...", end='\r')
        
        try:
            # 執行請求，跳過 SSL 驗證以避開憑證錯誤
            response = requests.get(url, verify=False, timeout=30)
            if response.status_code != 200:
                print(f"\n[錯誤] API 回傳狀態碼: {response.status_code}")
                break
                
            records = response.json()
            
            # 判斷是否還有資料
            if not isinstance(records, list) or not records:
                break
                
            all_records.extend(records)
            offset += limit
            
            # 若回傳數量小於 limit，代表已抓取到最後一頁
            if len(records) < limit:
                break
        except Exception as e:
            print(f"\n[異常] 請求發生錯誤: {str(e)}")
            break
            
    print(f"\n抓取完成! 總計取得 {len(all_records)} 筆原始紀錄。")
    
    # 確保儲存目錄存在
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    # 以 UTF-8 編碼儲存 JSON，確保中文不亂碼
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_records, f, ensure_ascii=False, indent=2)
        
    print(f"原始資料已存入: {OUTPUT_FILE}")

if __name__ == "__main__":
    fetch_all()
