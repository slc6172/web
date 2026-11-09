# Arduino 主題進度

更新:2026-11-07

## 頁面狀態
<!-- STATUS:START -->
完成 10 / 20 篇(依 `public/index.html` 自動產生)

| # | 標題 | 檔案 | 狀態 |
|---|---|---|---|
| 1 | 認識 Arduino 與第一次上傳 | `arduino-start-guide.html` | ✅ 完成 |
| 2 | 電與麵包板基礎 | `arduino-electric-guide.html` | ✅ 完成 |
| 3 | 外接 LED 閃爍:第一次接線 | `arduino-led-guide.html` | ✅ 完成 |
| 4 | 變數、for 與陣列:跑馬燈 | `arduino-loop-guide.html` | ✅ 完成 |
| 5 | 讀懂電路圖 | `arduino-schematic-guide.html` | ✅ 完成 |
| 6 | PWM 呼吸燈與蜂鳴器 | `arduino-pwm-guide.html` | ✅ 完成 |
| 7 | 按鈕:讀取輸入 | `arduino-button-guide.html` | ✅ 完成 |
| 8 | Serial Monitor 與除錯 | `arduino-serial-guide.html` | ✅ 完成 |
| 9 | 類比輸入:電位器 | `arduino-analog-guide.html` | ✅ 完成 |
| 10 | 光敏電阻小夜燈 | `arduino-ldr-guide.html` | ✅ 完成 |
| 11 | 超音波測距 HC-SR04 | `arduino-ultrasonic-guide.html` | ⬜ 規劃中 |
| 12 | 伺服馬達 SG90 | `arduino-servo-guide.html` | ⬜ 規劃中 |
| 13 | 溫濕度 DHT11 與安裝函式庫 | `arduino-dht-guide.html` | ⬜ 規劃中 |
| 14 | LCD1602 I2C 顯示 | `arduino-lcd-guide.html` | ⬜ 規劃中 |
| 15 | millis():不卡住的計時 | `arduino-millis-guide.html` | ⬜ 規劃中 |
| 16 | 外部中斷 attachInterrupt | `arduino-interrupt-guide.html` | ⬜ 規劃中 |
| 17 | I2C 與 SPI 通訊 | `arduino-bus-guide.html` | ⬜ 規劃中 |
| 18 | 綜合專案:倒車雷達 | `arduino-project-guide.html` | ⬜ 規劃中 |
| 19 | 故障排除總整理 | `arduino-troubleshoot-guide.html` | ⬜ 規劃中 |
| 20 | 語法與電路符號速查 | `arduino-reference-guide.html` | ⬜ 規劃中 |
<!-- STATUS:END -->

## 基礎建設
- [x] 規劃完成(大綱、決定事項見 `ARDUINO-DESIGN.md`)
- [x] 使用者看過第 3 篇檢查點後回覆「繼續」,依同樣邏輯往下做(實機回饋若有問題,最後統一回頭修)
- 每完成一頁就執行 `python3 tools/package.py pNN` 產生 zip 並更新下表

## 基礎建設
`build.py`(多主題)、`bb.py`(接線圖 / 原理圖 / Uno 導覽圖 / 檢查)、`arduino.css/js`、`arduino_verify.py`、`verify_arduino.py`、`tests_bb.py`、`tools/simpin`、`tools/package.py`、首頁 Arduino 標籤頁。

## 檢查點要使用者確認的事
1. 接線圖看不看得懂?(孔位、步驟播放、圖與接線表是否一致)
2. 實機照著接、照著上傳,LED 有沒有每秒閃一次?哪個步驟卡住?
3. IDE 的畫面與說明(File → New Sketch、板子下拉選單、Verify / Upload)是否與你看到的一致?
4. 原理圖與符號說明是否清楚?
5. 整體版面與 GitHub 主題的風格是否一致?

## 接手步驟(容器重置後)
1. 解壓最新的 zip,`cd github-tutorial-repo/_build`
2. `sh tools/setup_env.sh`(還原驗證工具)
3. 做新頁:複製 `a03.py` 為 `aNN.py` → 改 CIRC / CODE / 內容 → `python3 build.py aNN`
4. 驗證:`python3 arduino_verify.py aNN`、`python3 verify_arduino.py`、`python3 tests_bb.py`
5. 把 `public/index.html` 裡該篇的 `status` 改成 `"done"`
6. 打包 zip(不含 `.github/`、`_build/shots/`、`__pycache__/`、`tools/simpin`)

## 做完一頁要更新的地方
- `public/index.html`:該篇 `status:"done"`(`verify_arduino.py` 會檢查「已完成卡片數 = 已建置頁面數」)
- 上一篇 / 下一篇的 `prev` / `next`(檔案存在後重建即變成真連結;已完成的前後頁也要重建一次)
- 本檔的狀態清單
