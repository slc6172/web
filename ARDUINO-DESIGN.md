# Arduino 主題設計文件

> 給接手的人(或換對話後的 Claude):這份文件記錄 Arduino 主題**已決定**的事。已決定的不要再問使用者。
> 進度與下一步看 `ARDUINO-PROGRESS.md`。GitHub 主題的通用規範看 `DESIGN.md` / `HANDOFF.md`。

## 1. 目標與讀者
讓**沒學過 Arduino、也沒有電路概念**的初學者,依主題頁面學會:用 **Arduino Uno + 麵包板 + 杜邦線**從無到有接線(實體電路,不用模擬器)、安裝 Arduino IDE、寫出該電路的程式。作業系統只寫 **Windows**,IDE 為 **2.x**。難度由極簡單開始,逐步加入觀念。

## 2. 已決定事項
| 項目 | 決定 |
|---|---|
| 範圍 | 20 篇、六階段;含進階(millis、中斷、I2C/SPI)。第 16、17 篇為「進階選讀」 |
| 板子 | 主線 **Uno R3**;R4(USB-C、需在 Boards Manager 安裝板子套件)與 CH340 相容板(Windows 需驅動)的差異放提示框 / 常見卡關 |
| 零件 | 假設常見 Uno 入門套件。第 1 篇附**分批採購清單**:名稱、規格、數量、購買注意、標示「第幾篇才需要」;**不放價格與購物連結** |
| 接線 | **由資料產生**的 SVG 麵包板圖(`bb.py`),圖、接線表、原理圖同源;一步一步播放;孔位標 `e10` 這種座標 |
| 原理圖 | 每篇接線篇附原理圖,新符號標「新符號」;另有獨立第 5 篇「讀懂電路圖」(互動:原理圖 ↔ 麵包板連動) |
| 互動 | 填入資料(腳位、間隔)、故障排除模擬、電阻色環計算機(第 2 篇)、測驗、檢查表;第 19 篇決策選擇器 |
| SPI 示範 | 第 17 篇用 **74HC595 驅動 8 顆 LED**(SPI);I2C 用第 14 篇的 LCD |
| 首頁 | 每個主題一個標籤頁;標題 / 主文 / 路徑標題 / 路徑說明 / 頁尾 **每個分類自帶**(`SITE[].hero/pathTitle/pathNote/foot`);預設開 GitHub,Arduino 網址 `#arduino` |
| 快速入口 | 8 條:上傳失敗/COM 埠(19)、LED 不亮(3)、電阻多大(2)、看不懂電路圖(5)、燈慢慢亮暗(6)、按鈕沒反應或亂跳(7)、Serial 亂碼(8)、delay 卡住(15) |
| 程式碼 | 變數與函式用英文;**註解用繁體中文**;逐行說明表;複製按鈕;每支程式附「預期現象」 |
| 查證 | 動筆前對照 `docs.arduino.cc` / 官方函式庫;外部連結只指向 `docs.arduino.cc`、`support.arduino.cc`、`www.arduino.cc`;頁尾標查證日期 |
| 交付 | 每完成一頁就打包一個 zip(容器會不定時重置);zip 不含 `.github/`(`deploy.yml` 由使用者自行維護) |

## 3. 大綱(檔名一律 `arduino/arduino-<slug>-guide.html`)
| # | slug | 標題 | 難度 | 分鐘 | 備註 |
|---|---|---|---|---|---|
| 1 | start | 認識 Arduino 與第一次上傳 | 入門 | 20 | 採購清單、安裝 IDE(Windows)、上傳板載 LED 的 Blink(零接線)、R4 / CH340 提示 |
| 2 | electric | 電與麵包板基礎 | 入門 | 15 | 電壓電流電阻、歐姆定律、短路、麵包板內部、色環計算機 |
| 3 | led | 外接 LED 閃爍:第一次接線 | 入門 | 20 | **已完成(檢查點)** |
| 4 | loop | 變數、for 與陣列:跑馬燈 | 基礎 | 20 | 3 顆 LED,第一次用電源軌共用 GND |
| 5 | schematic | 讀懂電路圖 | 基礎 | 15 | 原理圖 ↔ 麵包板配對練習 |
| 6 | pwm | PWM 呼吸燈與蜂鳴器 | 基礎 | 20 | analogWrite、`~` 腳位、tone() |
| 7 | button | 按鈕:讀取輸入 | 基礎 | 25 | INPUT_PULLUP vs 外接下拉、浮接、去彈跳 |
| 8 | serial | Serial Monitor 與除錯 | 基礎 | 15 | |
| 9 | analog | 類比輸入:電位器 | 基礎 | 20 | 分壓、analogRead、map |
| 10 | ldr | 光敏電阻小夜燈 | 基礎 | 20 | |
| 11 | ultrasonic | 超音波測距 HC-SR04 | 進階 | 20 | 倒車雷達雛形 |
| 12 | servo | 伺服馬達 SG90 | 進階 | 20 | 內建 Servo 函式庫、供電限制 |
| 13 | dht | 溫濕度 DHT11 與安裝函式庫 | 進階 | 20 | Library Manager |
| 14 | lcd | LCD1602 I2C 顯示 | 進階 | 25 | |
| 15 | millis | millis():不卡住的計時 | 進階 | 20 | 第 18 篇會用到,**不可選讀** |
| 16 | interrupt | 外部中斷 attachInterrupt | 進階(選讀) | 15 | |
| 17 | bus | I2C 與 SPI 通訊 | 進階(選讀) | 25 | I2C 掃描器 + 74HC595 |
| 18 | project | 綜合專案:倒車雷達 | 進階 | 30 | 超音波 + LCD + 蜂鳴器 + LED |
| 19 | troubleshoot | 故障排除總整理 | 附錄 | 10 | 決策選擇器 |
| 20 | reference | 語法與電路符號速查 | 附錄 | 10 | |

首頁 `public/index.html` 的 `SITE[arduino]` 已列出全部 20 篇(未完成的 `status:"planned"`);**完成一篇就把該篇改成 `status:"done"`**。

## 4. 每個實作頁的固定流程
成品效果 → 零件 → 接線(SVG 步驟播放 + 接線表 + 原理圖)→ 上傳前檢查 → 程式碼(逐行說明)→ 你會看到 → 改改看(1–3 個小挑戰)→ 常見卡關 → 演練、測驗、檢查表 → 官方文件連結。
參考第 3 篇 `_build/a03.py` 的結構(它就是範本)。

## 5. 建置流程
```
_build/aNN.py        每頁一個規格檔(SPEC + CIRC + CODE + SKETCHES)
_build/build.py      python3 build.py a03 → public/arduino/arduino-led-guide.html
_build/bb.py         麵包板圖 / 原理圖 / 接線表 / 電路檢查
_build/arduino.css / arduino.js   只有 dir="arduino" 的頁面才內嵌
_build/common.js     所有頁面共用(含 data-cpp 的 // 註解上色)
```
- `SPEC` 新增欄位:`dir`(預設 github)、`topic`(eyebrow 前綴)、`foot`(頁尾)。GitHub 頁面重建時只有兩處差異(返回首頁連結多 `#github`、`common.js` 多支援 C++ 註解),功能不變。
- `prev` / `next` 指向的檔案還不存在時,自動顯示「製作中」的虛線卡片,檔案出現後重建就會變成真連結。
- `cmd(code, cpp=True)` 讓程式碼區支援 `//` 註解上色;`{pin}` 這類佔位符會被「填入資料」取代。

## 6. bb.py 用法(接線資料只寫一次)
```python
CIRC = bb.Circuit("led-blink", 16,                       # id, 圖上畫幾欄
    parts=[bb.Resistor("R1", 220, "b5", "b9", 1),        # 最後一個數字 = 第幾步放
           bb.LED("LED1", "red", "d9", "d10", 2),         # 長腳(A)孔, 短腳(K)孔
           bb.Wire("W1", "UNO.D8", "a5", "orange", 3),
           bb.Wire("W2", "UNO.GND", "a10", "black", 4)],
    steps=[(標題, 說明HTML), ...],                        # 第 i 項 ↔ 零件 step == i
    chain=["UNO.D8", "R1", "LED1", "UNO.GND"],            # 預期電路(串聯鏈)→ 原理圖與預期連線都由它產生
    code_pins={"LED_PIN": "UNO.D8"}, intro="…", done="…")
bb.stepper_html(CIRC)      # 步驟播放的接線圖
bb.wiring_table(CIRC)      # 文字接線表
bb.schematic_svg(CIRC)     # (svg, 圖例) 原理圖
bb.parts_info(CIRC)        # 原理圖 ↔ 麵包板連動說明(放進 PAGE.parts)
bb.wiring_config(CIRC)     # 步驟文字(放進 PAGE.wiring)
```
- 孔位:`a1`–`j63`(a–e 同欄相通,f–j 同欄相通);電源軌 `t+5`、`t-5`、`b+5`、`b-5`;Uno `UNO.D8`、`UNO.A0`、`UNO.5V`、`UNO.GND`(數位腳位排上的 GND)、`UNO.GND2/3`(電源排)。
- 畫面中 Uno 轉 180°:數位腳位排在**下緣**、朝向麵包板;電源 / 類比在上緣。電源腳要接到麵包板時用 `route="left"` 繞過板子左側。
- **尚未支援、之後的頁面需要時再擴充 `bb.py`**:按鈕(4 腳)、電位器(3 腳)、光敏電阻、蜂鳴器、HC-SR04、SG90、DHT11、LCD、74HC595;非串聯鏈的原理圖(並聯、分壓)。擴充時要同時補 `check()` 的連線比對。
- 實體零件顏色(電阻色環、LED、導線)允許使用 token 以外的色碼;介面色一律用 token。

## 7. 驗證(三層 + 瀏覽器)
```
python3 tests_bb.py            # 驗證器自我測試:故意做錯的電路必須被抓出來
python3 arduino_verify.py aNN  # 接線電氣檢查 + 程式腳位一致 + 編譯 + simavr 模擬 → reports/arduino-verify-report.md
python3 verify_arduino.py      # Playwright:1280/390 版面、互動、連結、首頁分頁
CHROME_PATH=/opt/google/chrome/chrome python3 verify.py   # GitHub 主題舊有驗證(確認沒壞)
```
容器重置後先跑 `sh _build/tools/setup_env.sh`(安裝 avr-gcc、simavr、clone ArduinoCore-avr、編譯 `tools/simpin`)。
**驗證不到的**:實體零件個別差異(模組腳位順序、LCD 對比度、I2C 位址 0x27 / 0x3F)、IDE 畫面。這些以官方文件為準,在頁面寫成「先確認再接」。
`SKETCHES` 的 `libs` 欄位可列函式庫(`Wire`、`SPI`、`Servo`… 內建的在 ArduinoCore-avr/libraries;第三方的放 `/tmp/avrlibs/<name>`,從 GitHub clone)。

## 8. 已查證的事實(2026-11-07,來源)
- IDE 2 工具列:勾號 = Verify、右箭頭 = Upload,旁邊是板子下拉選單;也可用 Tools > Board / Tools > Port;連接埠顯示如 `COM3 (Arduino Uno)`;內建範例 File > Examples > 01.Basics > Blink。(docs.arduino.cc、support.arduino.cc)
- Uno R3:每腳 DC 20 mA 建議、40 mA 絕對上限;LED_BUILTIN = 13;PWM 腳 3、5、6、9、10、11;外部中斷 2、3;SPI 10–13;I2C = A4(SDA)/A5(SCL)。(Arduino Uno 官方規格文字)
- `digitalWrite` 未設 OUTPUT 時,LED 會很暗(啟用內部上拉);`delay()` 單位毫秒、不停用中斷。(docs.arduino.cc 語言參考)
