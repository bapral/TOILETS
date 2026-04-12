# 全國廁所地圖 - 系統分析報告

## 1. 系統目標
為使用者提供即時、精確的公私立廁所位置資訊，並支援依類別（如加油站、超商）、等級（如特優級）及設施（如尿布檯）進行篩選。

## 2. 資料模型設計 (Database Schema)
基於環境部 `FAC_P_07` 資料集，建議資料表結構如下：

### Table: `toilets`
| 欄位名稱 | 型態 | 說明 | 來源欄位 |
| :--- | :--- | :--- | :--- |
| `id` | UUID/INT | 系統唯一識別碼 | - |
| `source_id` | STRING | 原始資料編號 | `number` |
| `name` | STRING | 廁所名稱 | `name` |
| `county` | STRING | 縣市名稱 | `county` |
| `town` | STRING | 鄉鎮市區 | `areacode` |
| `address` | STRING | 詳細地址 | `address` |
| `latitude` | DOUBLE | 緯度 (用於地圖定位) | `latitude` |
| `longitude` | DOUBLE | 經度 (用於地圖定位) | `longitude` |
| `grade` | STRING | 衛生等級 (特優/優等/普通) | `grade` |
| `type` | STRING | 場所類別 (加油站/超商/公園等) | `type` |
| `gender_type` | STRING | 廁所性別類別 (男/女/無障礙) | `type2` |
| `has_diaper` | BOOLEAN | 是否有尿布檯 | `diaper` (需轉換) |
| `last_updated` | DATETIME | 資料更新時間 | - |

## 3. 核心功能分析

### A. 附近廁所搜尋 (Proximity Search)
- **邏輯**: 根據使用者目前的 GPS 座標 (lat, lng)，計算與資料庫中廁所的距離。
- **演算法**: 建議使用 `Haversine Formula` (哈福賽公式) 計算球體距離，或在資料庫使用 `PostGIS` / `MongoDB Spatial Index` 進行空間索引查詢，以提升效能。
- **預設範圍**: 500公尺至 1公里。

### B. 進階篩選 (Filtering)
- **類別篩選**: 使用者可勾選「只要加油站」或「只要超商」。
- **設施篩選**: 勾選「需有尿布檯」或「需有無障礙設施」。
- **等級篩選**: 僅顯示「特優級」或「優等級」以上。

### C. 導航整合 (Navigation)
- **邏輯**: 點擊地圖標記後，串接 Google Maps 或 Apple Maps API 進行路徑規劃。

## 4. 使用者介面 (UI) 規劃
1.  **地圖主視圖**: 以使用者為中心顯示地圖，地圖上以不同顏色/圖示標記不同類別的廁所。
2.  **底部抽屜 (Bottom Sheet)**: 點擊標記時，從底部滑出詳細資訊（名稱、地址、等級、設施清單、導航按鈕）。
3.  **搜尋/過濾列**: 位於地圖上方，提供關鍵字搜尋與快速篩選切換開關。

## 5. 資料更新機制
- **自動同步**: 建議每 24 小時執行一次 ETL 腳本，從環境部 API 抓取最新資料。
- **衝突處理**: 以 `number` (建檔編號) 作為 Key，若編號已存在則更新資訊，不存在則新增。
