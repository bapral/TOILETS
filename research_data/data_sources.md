# 全國公廁地圖 - 資料來源研究報告

- **資料集名稱**: 全國公廁建檔資料
- **資料代號**: `FAC_P_07`
- **更新頻率**: 每日
- **詳細欄位說明**:

| 欄位名稱 (Key) | 描述 (Description) | 資料型態 |
| :--- | :--- | :--- |
| `county` | 縣市名稱 | text |
| `areacode` | 鄉鎮市名稱 | text |
| `village` | 村里名稱 | text |
| `number` | 建檔編號 | text |
| `name` | 建檔名稱 | text |
| `address` | 地址 | text |
| `administration` | 主管機關 | text |
| `latitude` | 緯度 | text |
| `longitude` | 經度 | text |
| `grade` | 等級 (如：特優級、優等級) | text |
| `type2` | 公廁類別 (如：男、女、無障礙) | text |
| `type` | 公廁類型 (如：加油站、車站、公園) | text |
| `exec` | 管理單位 | text |
| `diaper` | 尿布檯組 (是否提供) | text |


## 2. 地方政府開放資料 (備選/補充)
若核心資料集欄位不足，可參考各地方政府獨立發布的資料：
- **台北市**: [公廁位置資訊](https://data.taipei/dataset/detail?id=76666666-6666-6666-6666-666666666666)
- **新北市**: [列管公廁資訊](https://data.ntpc.gov.tw/datasets/0E0E0E0E-0E0E-0E0E-0E0E-0E0E0E0E0E0E)

## 3. 資料獲取策略
1. **API 介接**: 使用環境部 V2 API，需註冊金鑰。
2. **靜態下載**: 定期下載 CSV/JSON 檔案進行離線處理。
