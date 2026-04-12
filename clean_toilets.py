"""
全國公廁資料清理與聚合工具 (Clean & Aggregate Tool)
功能：
1. 過濾無效座標。
2. 將同地點的不同設施（如男廁、女廁、無障礙）聚合成單一地標。
3. 格式化欄位供前端 PWA 使用。
"""

import json
import os

# 資料路徑定義
INPUT_FILE = "research_data/all_toilets.json"
OUTPUT_FILE = "research_data/cleaned_toilets.json"

def clean_data():
    """
    執行資料清洗流程
    """
    if not os.path.exists(INPUT_FILE):
        print(f"[錯誤] 找不到原始資料檔: {INPUT_FILE}")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    print(f"開始清理資料 (總筆數: {len(raw_data)})")
    
    # 存放聚合後的資料，Key 為 (緯度, 經度, 名稱前5字) 的組合
    locations = {}
    invalid_count = 0

    for record in raw_data:
        try:
            # 座標轉浮點數
            lat = float(record.get('latitude', 0))
            lng = float(record.get('longitude', 0))
            
            # 台灣座標邊界檢查 (大約範圍)
            if not (21 < lat < 26 and 118 < lng < 123):
                invalid_count += 1
                continue
                
            name = record.get('name', '').strip()
            address = record.get('address', '').strip()
            
            # 建立聚合 Key：取到小數點後 5 位 + 名稱前 5 字，避免重複點位或微小誤差
            location_key = f"{lat:.5f}_{lng:.5f}_{name[:5]}"
            
            if location_key not in locations:
                locations[location_key] = {
                    "name": name,
                    "address": address,
                    "county": record.get('county'),
                    "town": record.get('areacode'),
                    "latitude": lat,
                    "longitude": lng,
                    "grade": record.get('grade'),
                    "category": record.get('type2'),  # 場所類別 (如：交通、公園)
                    "facilities": set(),              # 設施清單 (使用 set 避免重複)
                    "has_diaper": False               # 尿布檯旗標
                }
            
            # 解析設施類型
            toilet_type = record.get('type', '')
            if "男" in toilet_type: locations[location_key]["facilities"].add("男廁")
            if "女" in toilet_type: locations[location_key]["facilities"].add("女廁")
            if "無障礙" in toilet_type: locations[location_key]["facilities"].add("無障礙")
            if "性別友善" in toilet_type: locations[location_key]["facilities"].add("性別友善")
            
            # 更新尿布檯狀態
            if record.get('diaper') == "1":
                locations[location_key]["has_diaper"] = True
                
        except (ValueError, TypeError):
            invalid_count += 1
            continue

    # 格式化輸出：將 Set 轉回 List 以符合 JSON 規範
    cleaned_list = []
    for loc in locations.values():
        loc["facilities"] = sorted(list(loc["facilities"]))
        cleaned_list.append(loc)

    print(f"清理完成:")
    print(f"- 剔除無效座標: {invalid_count} 筆")
    print(f"- 聚合後唯一地點數: {len(cleaned_list)}")

    # 儲存清理後的資料
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(cleaned_list, f, ensure_ascii=False, indent=2)
    
    print(f"清理後資料已存入: {OUTPUT_FILE}")

if __name__ == "__main__":
    clean_data()
