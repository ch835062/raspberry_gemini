# test.py 程式說明

## 概述

這是一個 **Open WebUI Filter（過濾器）** 的範例程式。Filter 是 Open WebUI 的插件機制，讓你可以在 AI 回應的「前」和「後」插入自訂邏輯，例如：限制對話輪數、過濾內容、記錄日誌等。

---

## 程式結構

```
Filter
├── Valves        # 管理員層級的設定
├── UserValves    # 使用者層級的設定
├── __init__()    # 初始化
├── inlet()       # 前處理器（請求送出前執行）
└── outlet()      # 後處理器（回應收到後執行）
```

---

## 各部分詳細說明

### `Valves`（管理員設定）

```python
class Valves(BaseModel):
    priority: int = Field(default=0, ...)
    max_turns: int = Field(default=8, ...)
```

- `priority`：這個 Filter 的執行優先順序，數字越小越先執行，預設為 0。
- `max_turns`：管理員設定的最大對話輪數上限，預設為 8。這是整個系統的硬上限。

---

### `UserValves`（使用者設定）

```python
class UserValves(BaseModel):
    max_turns: int = Field(default=4, ...)
```

- `max_turns`：每個使用者自己可設定的最大對話輪數，預設為 4。
- 實際生效的上限會取 `UserValves.max_turns` 和 `Valves.max_turns` 兩者中較小的值（`min()`），避免使用者繞過管理員限制。

---

### `__init__()`（初始化）

```python
def __init__(self):
    self.valves = self.Valves()
```

- 建立 `Valves` 實例，載入管理員預設設定。
- 註解中提到的 `self.file_handler = True` 是選用功能，啟用後可自訂檔案處理邏輯，目前被註解掉（停用）。

---

### `inlet()`（前處理器）

```python
def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
```

- 在請求送到 AI 模型**之前**執行。
- 接收 `body`（請求內容）和 `__user__`（當前使用者資訊）。
- 執行流程：
  1. 印出 debug 資訊（模組名稱、請求內容、使用者資訊）。
  2. 確認使用者角色是 `"user"` 或 `"admin"`。
  3. 取出對話歷史 `messages`，計算目前的對話輪數。
  4. 用 `min()` 取使用者上限和管理員上限中較小的值作為實際上限。
  5. 如果對話輪數超過上限，拋出例外（錯誤），阻止請求繼續。
- 最後回傳（可能被修改過的）`body`。

---

### `outlet()`（後處理器）

```python
def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
```

- 在 AI 模型回應**之後**執行。
- 接收 `body`（回應內容）和 `__user__`（當前使用者資訊）。
- 目前只印出 debug 資訊，不做任何修改，直接回傳 `body`。
- 這裡可以擴充，例如：過濾敏感詞、記錄回應內容、統計 token 用量等。

---

## 執行流程圖

```
使用者送出訊息
      ↓
  inlet() 執行
  ├─ 對話輪數 ≤ 上限 → 繼續，請求送到 AI
  └─ 對話輪數 > 上限 → 拋出例外，中止請求
      ↓
  AI 模型處理
      ↓
  outlet() 執行
      ↓
  回應顯示給使用者
```

---

## 重點整理

| 項目 | 說明 |
|------|------|
| `inlet` | 請求的守門員，可以擋下不合規的請求 |
| `outlet` | 回應的後處理，可以修改或分析 AI 的輸出 |
| `Valves` | 管理員控制的全域設定 |
| `UserValves` | 使用者自訂設定，但不能超過管理員上限 |
| `max_turns` 實際值 | `min(使用者上限, 管理員上限)` |
