import requests
import json
import os

API_KEY = "8ca57585-60c7-4c05-a90e-4368bc232ef6"
BASE_URL = "https://data.moenv.gov.tw/api/v2/fac_p_07"
OUTPUT_FILE = "research_data/all_toilets.json"

def fetch_all():
    all_records = []
    limit = 1000
    offset = 0
    
    print(f"正在開始下載全國公廁資料...")
    
    while True:
        url = f"{BASE_URL}?api_key={API_KEY}&format=JSON&limit={limit}&offset={offset}"
        print(f"下載進度: {offset} 筆...", end='\r')
        
        # 關閉 SSL 驗證以避開憑證錯誤，並停用警告訊息
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        response = requests.get(url, verify=False)
        if response.status_code != 200:
            print(f"\n下載失敗! 狀態碼: {response.status_code}")
            break
            
        records = response.json()
        
        if not isinstance(records, list) or not records:
            break
            
        all_records.extend(records)
        offset += limit
        
        # 若抓取數量小於 limit，代表已是最後一頁
        if len(records) < limit:
            break
            
    print(f"\n下載完成! 總計取得 {len(all_records)} 筆資料。")
    
    # 確保目錄存在
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_records, f, ensure_ascii=False, indent=2)
        
    print(f"資料已成功存入 {OUTPUT_FILE}")

if __name__ == "__main__":
    fetch_all()
