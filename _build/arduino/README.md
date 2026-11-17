# Arduino 主題（`public/arduino/`，20 篇）

先讀上一層的 [`../README.md`](../README.md)（總入口、設計規範、指令）。本文件只記 Arduino 主題特有的事。**已確認的決定不要再問使用者。**

## 已確認的決定

| 項目 | 決定 |
|---|---|
| 讀者與範圍 | 沒學過 Arduino、也沒有電路概念的人；用 **Arduino Uno + 麵包板 + 杜邦線**接實體電路（不用模擬器）、安裝 Arduino IDE、寫程式。作業系統只寫 **Windows**，IDE 為 **2.x**。難度由極簡單開始，逐步加概念 |
| 篇數 | 20 篇、六階段（起步、輸出、輸入、感測與驅動、進階、附錄）；第 16、17 篇為進階選讀；第 15 篇 `millis()` 第 18 篇會用到，**不可選讀** |
| 板子 | 主線 Uno R3；R4（USB-C、需在 Boards Manager 安裝板子套件）與 CH340 相容板（Windows 需驅動）的差異放提示框／常見卡關 |
| 零件 | 假設常見 Uno 入門套件；第 1 篇附分批採購清單（名稱、規格、數量、購買注意、標示第幾篇才需要），**不放價格與購物連結** |
| 接線 | 由資料產生的 SVG 麵包板圖（`bb.py`），圖、接線表、原理圖同源；一步一步播放；孔位標 `e10` 這種座標。每篇接線篇附原理圖，新符號標「新符號」 |
| 程式碼 | 變數與函式用英文，**註解用繁體中文**；逐行說明表；複製按鈕；每支程式附「預期現象」 |
| 查證 | 動筆前對照 `docs.arduino.cc` 與官方函式庫；外部連結只指向 `docs.arduino.cc`、`support.arduino.cc`、`www.arduino.cc`；頁尾標查證日期 |

## 每個實作頁的固定流程

成品效果 → 零件 → 接線（SVG 步驟播放＋接線表＋原理圖）→ 上傳前檢查 → 程式碼（逐行說明）→ 你會看到 → 改改看（1–3 個小挑戰）→ 常見卡關 → 演練、測驗、檢查表 → 官方文件連結。`a03.py` 就是範本。

## 建置

```text
_build/arduino/aNN.py      每頁一個規格檔（SPEC + CIRC + CODE + SKETCHES）
_build/arduino/bb.py       麵包板圖／原理圖／接線表／電路檢查
_build/arduino/arduino.css / arduino.js   只有 Arduino 頁面才內嵌（build.py 的 THEMES 設定）
```

- 組頁：`python3 _build/build.py a03`。規格檔寫 `dir="arduino"`。
- `prev` / `next` 指向的檔案還不存在時，自動顯示「製作中」的虛線卡片，檔案出現後重建就會變成真連結。
- `cmd(code, cpp=True)` 讓程式碼區支援 `//` 註解上色；`{pin}` 這類佔位符會被「填入資料」取代。

## bb.py 用法（接線資料只寫一次）

```python
CIRC = bb.Circuit("led-blink", 16,                       # id, 圖上畫幾欄
    parts=[bb.Resistor("R1", 220, "b5", "b9", 1),        # 最後一個數字 = 第幾步放
           bb.LED("LED1", "red", "d9", "d10", 2),         # 長腳(A)孔, 短腳(K)孔
           bb.Wire("W1", "UNO.D8", "a5", "orange", 3),
           bb.Wire("W2", "UNO.GND", "a10", "black", 4)],
    steps=[(標題, 說明HTML), ...],                        # 第 i 項 ↔ 零件 step == i
    chain=["UNO.D8", "R1", "LED1", "UNO.GND"],            # 預期電路（串聯鏈）→ 原理圖與預期連線都由它產生
    code_pins={"LED_PIN": "UNO.D8"}, intro="…", done="…")
bb.stepper_html(CIRC)      # 步驟播放的接線圖
bb.wiring_table(CIRC)      # 文字接線表
bb.schematic_svg(CIRC)     # (svg, 圖例) 原理圖
bb.parts_info(CIRC)        # 原理圖 ↔ 麵包板連動說明（放進 PAGE.parts）
bb.wiring_config(CIRC)     # 步驟文字（放進 PAGE.wiring）
```

- 孔位：`a1`–`j63`（a–e 同欄相通，f–j 同欄相通）；電源軌 `t+5`、`t-5`、`b+5`、`b-5`；Uno `UNO.D8`、`UNO.A0`、`UNO.5V`、`UNO.GND`（數位腳位排上的 GND）、`UNO.GND2/3`（電源排）。畫面中 Uno 轉 180°：數位腳位排在下緣、朝向麵包板。
- 支援的零件：Resistor、LED、Wire、Buzzer、Button（4 腳，用對角兩腳）、Pot（3 腳）、LDR、HCSR04、Servo（SG90）、DHT11（3 腳模組）、LCD（I2C 轉接板，不經麵包板）、Shift595（74HC595）。新零件需要時擴充 `bb.py`，並同時補 `check()` 的連線比對。
- 模式：`Circuit(..., mode="breadboard" | "direct" | "both")`。`direct` = 沒有麵包板（第 14 篇），`both` = 麵包板＋下方模組（第 18 篇）。
- 路線：`auto`、`straight`、`left` / `left1`（繞過 Uno 左側，數字是車道）、`right` / `right1`、`vs`（垂直 S 形）、`down` / `down1`…（往下的弧，讓多條跳線巢狀不交叉）。電源腳要接到麵包板時用 `route="left"` 繞過板子左側。
- 鏈（chain）的端點可以是 `UNO.xx`、零件名（串聯）、或 `零件.腳名`（例如 `POT1.W`、`HC1.TRIG`、`IC1.Q4`）；多條鏈共用的端點（GND、5V）自動合併。
- 實體零件顏色（電阻色環、LED、導線）允許使用 token 以外的色碼；介面色一律用 token。

## 驗證（三層＋瀏覽器）

```bash
python3 _build/arduino/tests_bb.py          # 驗證器自我測試：故意做錯的電路必須被抓出來
python3 _build/arduino/arduino_verify.py a03 # 接線電氣檢查＋程式腳位一致＋編譯＋simavr 模擬 → reports/arduino-verify-report.md
python3 _build/arduino/verify_arduino.py    # Playwright：1280/390 版面、互動、連結、首頁分頁
python3 _build/verify.py                    # 全站驗證
```

- 環境重置後先跑 `sh _build/arduino/tools/setup_env.sh`（安裝 avr-gcc、simavr、clone ArduinoCore-avr 與函式庫、編譯 `tools/simpin`）。`tools/simpin` 是編譯產物，不需要提交。
- `SKETCHES` 的 `libs` 欄位可列函式庫（`Wire`、`SPI`、`Servo`… 內建的在 ArduinoCore-avr/libraries；第三方的放 `/tmp/avrlibs/<name>`，從 GitHub clone）。
- `arduino_verify.py` 的 `sim=dict(kind=…)`：`toggle`、`uart`（序列埠輸出，可注入按鈕／序列埠輸入／類比電壓／DHT11／I2C 裝置）、`input`、`dual`、`chase`、`pwm`/`ocr`、`pattern`、`freq`（tone）、`servo`、`adc_pwm`、`adc_edges`、`adc_toggle`、`highlow`、`spi`。`simpin` 參數：`IN@D2=0@500`（注入腳位電位）、`ADC@0=2500@500`（類比電壓，毫伏）、`RX@500=49`（序列埠輸入）、`DHT@D2=26,55`、`I2C@27`、`REG@88`。
- **驗證不到的**：實體零件個別差異（模組腳位順序、LCD 對比度、I2C 位址 0x27 / 0x3F）、IDE 畫面、`hd44780` 的 I2C 讀取探測（第 18 篇改用「LCD 空殼」版本驗證計時與警示邏輯，真正的 LCD 版本只做編譯驗證；第 14 篇 LCD 程式只編譯）。這些以官方文件為準，頁面寫成「先確認再接」。
- 最近一次全量驗證結果在 `reports/arduino-verify-report.md`；外部連結檢查在 `reports/link-check.md`（網址區分大小寫，新增前要實際開啟）。

## 已查證的事實（2026-11-07）

- IDE 2 工具列：勾號 = Verify、右箭頭 = Upload，旁邊是板子下拉選單；也可用 Tools > Board / Tools > Port；連接埠顯示如 `COM3 (Arduino Uno)`；內建範例 File > Examples > 01.Basics > Blink。
- Uno R3：每腳 DC 20 mA 建議、40 mA 絕對上限；`LED_BUILTIN` = 13；PWM 腳 3、5、6、9、10、11；外部中斷 2、3；SPI 10–13；I2C = A4（SDA）/ A5（SCL）。
- `digitalWrite` 未設 OUTPUT 時 LED 會很暗（啟用內部上拉）；`delay()` 單位毫秒、不停用中斷。

## 與原規劃不同之處（頁面與首頁都已同步）

- 第 5 篇「讀懂電路圖」獨立成篇，全站因此是 20 篇。
- 第 17 篇 SPI 示範改用 **4 顆 LED**（Q4–Q1 → LED1–LED4），不是 8 顆：74HC595 的 8 個輸出分在晶片兩排，接 8 顆在麵包板上太擠。第 1 篇零件表已同步（LED 共約 12 顆、220Ω 12 顆）。
- LCD 函式庫主線用 **`hd44780`**（自動偵測 I2C 位址，避開 0x27 / 0x3F 與 `init()` / `begin()` 版本差異這幾個新手最常卡的點）；`LiquidCrystal I2C` 放在第 14 篇「另一個函式庫」。
- 伺服馬達線尾是**母頭插座**，要用公對公杜邦線轉接；LCD 轉接板是公針，用公對母。第 1 篇零件表已寫明。
- 第 16 篇中斷：最後採 `CHANGE` ＋「每一次電位變化都記時間」。只用 `FALLING` ＋鎖定時間時，模擬發現放開時的彈跳會被當成又按了一次。

## 已知的不確定處（需要實機或之後對照官方確認）

- 官方文件連結中，有幾個是依 `docs.arduino.cc` 的網址規律推得、並非逐一打開驗證：`pinmode`、`analogread`、`analogwrite`、`map`、`constrain`、`pulseIn`、`delayMicroseconds`、`tone`、`attachInterrupt`、`volatile`、`for`、`array`、`while`、`if`、`wire`、`spi`、`serial/println`、`libraries/servo`、`hardware/uno-rev3` 等語言參考頁。部署前建議逐一點開，若有 404 就改成官方實際網址。
- IDE 2 介面描述（File → New Sketch、板子下拉選單、Serial Monitor 位置與 baud 選單、Library Manager 與 INSTALL ALL）依官方文件與社群資料撰寫，請在實機畫面核對。
- SG90 電流、DHT11 / HC-SR04 規格為常見資料手冊的範例值，頁面已標註「以你的零件為準」；麵包板電源軌中間是否斷開、模組針腳順序因廠牌而異，頁面都寫成「先確認再接」。

## 實作中發現並修掉的問題（做新頁請注意）

- 小工具的欄位排版**不要用 `.fill` class**：頁面上「填入資料」的 Reset 按鈕會清掉所有 `.fill input`。小工具請用 `.wgrid`。
- 一頁只能有一個 `fill()` 表單（id 會重複）；多個程式需要的欄位合併到同一個表單。
- 手機版寬圖要包在 `.canvas`（可橫向捲動），否則整頁會橫向溢出。
- 帶彈跳的按鈕輸入，模擬裡一定要加上「放開時的彈跳」才算驗證到位。
