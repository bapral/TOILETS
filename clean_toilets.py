import json
import os
from collections import defaultdict

INPUT_FILE = "research_data/all_toilets.json"
OUTPUT_FILE = "research_data/cleaned_toilets.json"

def clean_data():
    if not os.path.exists(INPUT_FILE):
        print(f"錯誤: 找不到原始資料檔 {INPUT_FILE}")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    print(f"原始資料總筆數: {len(raw_data)}")
    
    # 用於聚合的地圖： key = (lat, lng, name)
    # value = { 完整資訊, 設施清單 }
    locations = {}
    invalid_count = 0

    for record in raw_data:
        try:
            lat = float(record.get('latitude', 0))
            lng = float(record.get('longitude', 0))
            
            # 簡單的台灣座標範圍檢查 (概略範圍)
            if not (21 < lat < 26 and 118 < lng < 123):
                invalid_count += 1
                continue
                
            name = record.get('name', '').strip()
            address = record.get('address', '').strip()
            # 產生唯一 Key (使用經緯度與名稱前 5 個字，避免微小誤差或命名差異)
            location_key = f"{lat:.5f}_{lng:.5f}_{name[:5]}"
            
            if location_key not in locations:
                locations[location_key] = {
                    "name": name,
                    "address": address,
                    "county": record.get('county'),
                    "town": record.get('areacode'),
                    "village": record.get('village'),
                    "latitude": lat,
                    "longitude": lng,
                    "grade": record.get('grade'),
                    "category": record.get('type2'), # 場所類別 (公園, 交通...)
                    "facilities": set(),
                    "has_diaper": False,
                    "raw_types": set()
                }
            
            # 判斷設施類型
            toilet_type = record.get('type', '')
            locations[location_key]["raw_types"].add(toilet_type)
            
            if "男" in toilet_type: locations[location_key]["facilities"].add("male")
            if "女" in toilet_type: locations[location_key]["facilities"].add("female")
            if "無障礙" in toilet_type: locations[location_key]["facilities"].add("accessible")
            if "性別友善" in toilet_type: locations[location_key]["facilities"].add("gender_neutral")
            
            # 尿布檯判斷
            if record.get('diaper') == "1":
                locations[location_key]["has_diaper"] = True
                
        except (ValueError, TypeError):
            invalid_count += 1
            continue

    # 格式化輸出
    cleaned_list = []
    for loc in locations.values():
        loc["facilities"] = list(loc["facilities"])
        loc["raw_types"] = list(loc["raw_types"])
        cleaned_list.append(loc)

    print(f"清理完成:")
    print(f"- 剔除無效座標: {invalid_count} 筆")
    print(f"- 聚合後唯一地點數: {len(cleaned_list)}")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(cleaned_list, f, ensure_ascii=False, indent=2)
    
    print(f"清理後的資料已存入 {OUTPUT_FILE}")

if __name__ == "__main__":
    clean_data()
