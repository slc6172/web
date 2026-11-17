# Arduino 主題驗證報告

產生時間:2026-11-15 05:00

驗證項目:① 麵包板規則算出的實際連線 = 原理圖預期電路;② 程式腳位 = 接線腳位;③ 程式實際編譯;④ simavr 模擬腳位行為。
**驗證不到的**:實體零件的個別差異(模組腳位順序、LCD 對比度、I2C 位址)、IDE 畫面。這些以官方文件為準並在頁面寫成「先確認再接」。

## a01 — 認識 Arduino 與第一次上傳

### 程式:`blink-builtin`

- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 2402 / 32256 bytes(7%)、SRAM 197 / 2048 bytes(9%)
- ✅ 模擬(simavr,5.2 秒):D13 腳 電位交替翻轉 6 次,間隔 1000.0、1000.0、1000.0、1000.0 … ms(預期 1000 ± 15)

## a02 — 電與麵包板基礎

### 接線:`led-5v`

- ✅ 所有孔位都存在且在圖上的 14 欄之內
- ✅ 沒有任何一個孔被兩個零件腳或導線共用
- ✅ 依麵包板規則算出的實際連線,與原理圖的預期電路完全一致(3 條連線)
- ✅ 沒有零件被自己的導線短路
- ✅ 沒有任何兩個不同的 Uno 腳位被接在一起(5V 與 GND 沒有短路)
- ✅ 5V 腳位電流估算 ≈ 13.6 mA(Vcc 5 V、LED 順向壓降 2.0 V、串聯電阻 220Ω);Uno 建議每腳 ≤ 20 mA、絕對上限 40 mA

## a03 — 外接 LED 閃爍:第一次接線與第一個程式

### 接線:`led-blink`

- ✅ 所有孔位都存在且在圖上的 16 欄之內
- ✅ 沒有任何一個孔被兩個零件腳或導線共用
- ✅ 依麵包板規則算出的實際連線,與原理圖的預期電路完全一致(3 條連線)
- ✅ 沒有零件被自己的導線短路
- ✅ 沒有任何兩個不同的 Uno 腳位被接在一起(5V 與 GND 沒有短路)
- ✅ D8 腳位電流估算 ≈ 13.6 mA(Vcc 5 V、LED 順向壓降 2.0 V、串聯電阻 220Ω);Uno 建議每腳 ≤ 20 mA、絕對上限 40 mA

### 程式:`led-blink`

- ✅ 程式 `LED_PIN = 8` ↔ 接線 `UNO.D8`
- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 2402 / 32256 bytes(7%)、SRAM 197 / 2048 bytes(9%)
- ✅ 模擬(simavr,5.2 秒):D8 腳 電位交替翻轉 6 次,間隔 1000.0、1000.0、1000.0、1000.0 … ms(預期 1000 ± 15)

## a04 — 變數、for 與陣列:三顆 LED 跑馬燈

### 接線:`led-chase`

- ✅ 所有孔位都存在且在圖上的 22 欄之內
- ✅ 沒有任何一個孔被兩個零件腳或導線共用
- ✅ 依麵包板規則算出的實際連線,與原理圖的預期電路完全一致(7 條連線)
- ✅ 沒有零件被自己的導線短路
- ✅ 沒有任何兩個不同的 Uno 腳位被接在一起(5V 與 GND 沒有短路)
- ✅ D8 腳位電流估算 ≈ 13.6 mA(Vcc 5 V、LED 順向壓降 2.0 V、串聯電阻 220Ω);Uno 建議每腳 ≤ 20 mA、絕對上限 40 mA
- ✅ D9 腳位電流估算 ≈ 13.2 mA(Vcc 5 V、LED 順向壓降 2.1 V、串聯電阻 220Ω);Uno 建議每腳 ≤ 20 mA、絕對上限 40 mA
- ✅ D10 腳位電流估算 ≈ 12.7 mA(Vcc 5 V、LED 順向壓降 2.2 V、串聯電阻 220Ω);Uno 建議每腳 ≤ 20 mA、絕對上限 40 mA

### 程式:`chase-v1`

- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 2462 / 32256 bytes(7%)、SRAM 197 / 2048 bytes(9%)
- ✅ 模擬(simavr,3.5 秒):D8、D9、D10 ── 3 顆依序亮起,每顆亮 300 ms,輪一圈 900 ms,誤差 ≤ 15 ms

### 程式:`chase-v2`

- ✅ 程式 `RED_PIN = 8` ↔ 接線 `UNO.D8`
- ✅ 程式 `YELLOW_PIN = 9` ↔ 接線 `UNO.D9`
- ✅ 程式 `GREEN_PIN = 10` ↔ 接線 `UNO.D10`
- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 2488 / 32256 bytes(7%)、SRAM 199 / 2048 bytes(9%)
- ✅ 模擬(simavr,3.5 秒):D8、D9、D10 ── 3 顆依序亮起,每顆亮 300 ms,輪一圈 900 ms,誤差 ≤ 15 ms

### 程式:`chase-v3`

- ✅ 程式 `ledPins = [8, 9, 10]` ↔ 接線 `['UNO.D8', 'UNO.D9', 'UNO.D10']`
- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 2452 / 32256 bytes(7%)、SRAM 205 / 2048 bytes(10%)
- ✅ 模擬(simavr,3.5 秒):D8、D9、D10 ── 3 顆依序亮起,每顆亮 300 ms,輪一圈 900 ms,誤差 ≤ 15 ms

### 程式:`chase-v4`

- ✅ 程式 `ledPins = [8, 9, 10]` ↔ 接線 `['UNO.D8', 'UNO.D9', 'UNO.D10']`
- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 2470 / 32256 bytes(7%)、SRAM 205 / 2048 bytes(10%)

## a05 — 讀懂電路圖:原理圖與麵包板互相對照

### 接線:`ex1-ok`

- ✅ 所有孔位都存在且在圖上的 16 欄之內
- ✅ 沒有任何一個孔被兩個零件腳或導線共用
- ✅ 依麵包板規則算出的實際連線,與原理圖的預期電路完全一致(3 條連線)
- ✅ 沒有零件被自己的導線短路
- ✅ 沒有任何兩個不同的 Uno 腳位被接在一起(5V 與 GND 沒有短路)
- ✅ D8 腳位電流估算 ≈ 13.6 mA(Vcc 5 V、LED 順向壓降 2.0 V、串聯電阻 220Ω);Uno 建議每腳 ≤ 20 mA、絕對上限 40 mA

### 接線:`ex2-ok`

- ✅ 所有孔位都存在且在圖上的 14 欄之內
- ✅ 沒有任何一個孔被兩個零件腳或導線共用
- ✅ 依麵包板規則算出的實際連線,與原理圖的預期電路完全一致(5 條連線)
- ✅ 沒有零件被自己的導線短路
- ✅ 沒有任何兩個不同的 Uno 腳位被接在一起(5V 與 GND 沒有短路)
- ✅ D8 腳位電流估算 ≈ 13.6 mA(Vcc 5 V、LED 順向壓降 2.0 V、串聯電阻 220Ω);Uno 建議每腳 ≤ 20 mA、絕對上限 40 mA
- ✅ D9 腳位電流估算 ≈ 12.7 mA(Vcc 5 V、LED 順向壓降 2.2 V、串聯電阻 220Ω);Uno 建議每腳 ≤ 20 mA、絕對上限 40 mA

### 接線:`ex3`

- ✅ 所有孔位都存在且在圖上的 12 欄之內
- ✅ 沒有任何一個孔被兩個零件腳或導線共用
- ✅ 依麵包板規則算出的實際連線,與原理圖的預期電路完全一致(3 條連線)
- ✅ 沒有零件被自己的導線短路
- ✅ 沒有任何兩個不同的 Uno 腳位被接在一起(5V 與 GND 沒有短路)
- ✅ D8 腳位電流估算 ≈ 13.6 mA(Vcc 5 V、LED 順向壓降 2.0 V、串聯電阻 220Ω);Uno 建議每腳 ≤ 20 mA、絕對上限 40 mA

## a06 — PWM 呼吸燈與蜂鳴器

### 接線:`pwm-buzzer`

- ✅ 所有孔位都存在且在圖上的 22 欄之內
- ✅ 沒有任何一個孔被兩個零件腳或導線共用
- ✅ 依麵包板規則算出的實際連線,與原理圖的預期電路完全一致(5 條連線)
- ✅ 沒有零件被自己的導線短路
- ✅ 沒有任何兩個不同的 Uno 腳位被接在一起(5V 與 GND 沒有短路)
- ✅ D9 腳位電流估算 ≈ 13.6 mA(Vcc 5 V、LED 順向壓降 2.0 V、串聯電阻 220Ω);Uno 建議每腳 ≤ 20 mA、絕對上限 40 mA

### 程式:`pwm-fade`

- ✅ 程式 `LED_PIN = 9` ↔ 接線 `UNO.D9`
- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 2626 / 32256 bytes(8%)、SRAM 197 / 2048 bytes(9%)
- ✅ 模擬(simavr,2.3 秒,取樣 PWM 暫存器 OCR 0x88,對應 D9):OCR 暫存器:最大值 250 出現在 1010 ms(預期 1040 ± 60;255 會被核心改成直接輸出 HIGH)、上升段中點 125(預期約 128)、一輪結束時降到 5

### 程式:`pwm-beep`

- ✅ 程式 `BUZZER_PIN = 8` ↔ 接線 `UNO.D8`
- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 2430 / 32256 bytes(7%)、SRAM 197 / 2048 bytes(9%)
- ✅ 模擬(simavr,3.5 秒):D8 腳 ── 前 12 段電位與時間都符合(誤差 ≤ 5 ms)

### 程式:`pwm-tone`

- ✅ 程式 `BUZZER_PIN = 8` ↔ 接線 `UNO.D8`
- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 3768 / 32256 bytes(11%)、SRAM 211 / 2048 bytes(10%)
- ✅ 模擬(simavr,1.2 秒):D8 腳 ── 前 500 ms 內有 220 個脈衝(預期約 220,即 440 Hz)

### 程式:`pwm-sos`

- ✅ 程式 `BUZZER_PIN = 8` ↔ 接線 `UNO.D8`
- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 2496 / 32256 bytes(7%)、SRAM 197 / 2048 bytes(9%)

## a07 — 按鈕:讀取輸入、上拉電阻與去彈跳

### 接線:`button-led`

- ✅ 所有孔位都存在且在圖上的 22 欄之內
- ✅ 沒有任何一個孔被兩個零件腳或導線共用
- ✅ 依麵包板規則算出的實際連線,與原理圖的預期電路完全一致(4 條連線)
- ✅ 沒有零件被自己的導線短路
- ✅ 沒有任何兩個不同的 Uno 腳位被接在一起(5V 與 GND 沒有短路)
- ✅ D8 腳位電流估算 ≈ 13.6 mA(Vcc 5 V、LED 順向壓降 2.0 V、串聯電阻 220Ω);Uno 建議每腳 ≤ 20 mA、絕對上限 40 mA

### 程式:`btn-hold`

- ✅ 程式 `BUTTON_PIN = 2` ↔ 接線 `UNO.D2`
- ✅ 程式 `LED_PIN = 8` ↔ 接線 `UNO.D8`
- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 2292 / 32256 bytes(7%)、SRAM 197 / 2048 bytes(9%)
- ✅ 模擬(simavr,1.3 秒,注入按鈕輸入 D2 在 500 ms 按下、900 ms 放開):輸出腳位的變化:['1@500', '0@900'](預期 ['1@500', '0@900'],誤差 ≤ 5 ms)

### 程式:`btn-toggle`

- ✅ 程式 `BUTTON_PIN = 2` ↔ 接線 `UNO.D2`
- ✅ 程式 `LED_PIN = 8` ↔ 接線 `UNO.D8`
- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 2534 / 32256 bytes(7%)、SRAM 198 / 2048 bytes(9%)
- ✅ 模擬(simavr,1.8 秒,注入按鈕輸入 兩次按下,每次按下與放開都帶 2–4 ms 的彈跳,LED 仍只切換一次):輸出腳位的變化:['1@500', '0@1200'](預期 ['1@500', '0@1200'],誤差 ≤ 5 ms)

### 程式:`btn-float`

- ✅ 程式 `BUTTON_PIN = 2` ↔ 接線 `UNO.D2`
- ✅ 程式 `LED_PIN = 8` ↔ 接線 `UNO.D8`
- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 2292 / 32256 bytes(7%)、SRAM 197 / 2048 bytes(9%)

### 程式:`btn-three`

- ✅ 程式 `BUTTON_PIN = 2` ↔ 接線 `UNO.D2`
- ✅ 程式 `LED_PIN = 8` ↔ 接線 `UNO.D8`
- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 2530 / 32256 bytes(7%)、SRAM 197 / 2048 bytes(9%)
- ✅ 模擬(simavr,1.5 秒,注入按鈕輸入 D2 在 500 ms 按下、700 ms 放開):輸出腳位的變化:['1@500', '0@650', '1@800', '0@950', '1@1100', '0@1250'](預期 ['1@500', '0@650', '1@800', '0@950', '1@1100', '0@1250'],誤差 ≤ 5 ms)

## a08 — Serial Monitor 與除錯

### 程式:`ser-hello`

- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 3068 / 32256 bytes(9%)、SRAM 227 / 2048 bytes(11%)
- ✅ 模擬(simavr,2.2 秒,UART):序列埠輸出依序包含 ['Hello, Arduino!↵', 'count = 0↵', 'count = 1↵', 'count = 2↵', 'count = 3↵']

### 程式:`ser-fmt`

- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 4618 / 32256 bytes(14%)、SRAM 261 / 2048 bytes(12%)
- ✅ 模擬(simavr,0.5 秒,UART):序列埠輸出依序包含 ['n = 42↵', 'n in BIN = 101010↵', 'n in HEX = 2A↵', 'x = 3.14↵', 'x (4 digits) = 3.1416↵']

### 程式:`ser-debug`

- ✅ 程式 `BUTTON_PIN = 2` ↔ 接線 `UNO.D2`
- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 3216 / 32256 bytes(9%)、SRAM 209 / 2048 bytes(10%)
- ✅ 模擬(simavr,1.8 秒,UART):序列埠輸出依序包含 ['button = 1↵', 'button = 0↵', 'button = 0↵', 'button = 1↵']

### 程式:`ser-key`

- ✅ 程式 `LED_PIN = 8` ↔ 接線 `UNO.D8`
- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 2654 / 32256 bytes(8%)、SRAM 235 / 2048 bytes(11%)
- ✅ 模擬(simavr,1.6 秒,UART):序列埠輸出依序包含 ['Type 1 = LED on, 0 = LED off↵', 'LED on↵', 'LED off↵'];輸出腳位的變化:['1@301', '0@901'](預期 ['1@300', '0@900'],誤差 ≤ 5 ms)

### 程式:`ser-plot`

- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 2954 / 32256 bytes(9%)、SRAM 199 / 2048 bytes(9%)
- ✅ 模擬(simavr,0.3 秒,UART):序列埠輸出依序包含 ['0↵', '1↵', '2↵', '3↵']

## a09 — 類比輸入:電位器、分壓與 map()

### 接線:`pot-led`

- ✅ 所有孔位都存在且在圖上的 22 欄之內
- ✅ 沒有任何一個孔被兩個零件腳或導線共用
- ✅ 依麵包板規則算出的實際連線,與原理圖的預期電路完全一致(5 條連線)
- ✅ 沒有零件被自己的導線短路
- ✅ 沒有任何兩個不同的 Uno 腳位被接在一起(5V 與 GND 沒有短路)
- ✅ D9 腳位電流估算 ≈ 13.6 mA(Vcc 5 V、LED 順向壓降 2.0 V、串聯電阻 220Ω);Uno 建議每腳 ≤ 20 mA、絕對上限 40 mA

### 程式:`pot-read`

- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 2994 / 32256 bytes(9%)、SRAM 201 / 2048 bytes(9%)
- ✅ 模擬(simavr,1.7 秒,UART):序列埠輸出依序包含 ['0↵', '511↵', '1023↵']

### 程式:`pot-led`

- ✅ 程式 `LED_PIN = 9` ↔ 接線 `UNO.D9`
- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 2854 / 32256 bytes(8%)、SRAM 197 / 2048 bytes(9%)
- ✅ 模擬(simavr,1.5 秒,注入類比電壓 1000、2500、4000 mV):在 [300, 800, 1300] 取得的 PWM 暫存器值 [50, 127, 203](預期 [51, 127, 203],誤差 ≤ 3)

### 程式:`pot-volts`

- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 4768 / 32256 bytes(14%)、SRAM 235 / 2048 bytes(11%)
- ✅ 模擬(simavr,1.2 秒,UART):序列埠輸出依序包含 ['value = 511  voltage = 2.50↵']

### 程式:`pot-speed`

- ✅ 程式 `LED_PIN = 9` ↔ 接線 `UNO.D9`
- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 2480 / 32256 bytes(7%)、SRAM 197 / 2048 bytes(9%)
- ✅ 模擬(simavr,3.3 秒,注入類比電壓 2000 mV → wait = 409):D9 腳 電位交替翻轉 9 次,間隔 409.0、409.1、409.0、409.1 … ms(預期 409 ± 15)

## a10 — 光敏電阻小夜燈:分壓、門檻與遲滯

### 接線:`ldr-night`

- ✅ 所有孔位都存在且在圖上的 22 欄之內
- ✅ 沒有任何一個孔被兩個零件腳或導線共用
- ✅ 依麵包板規則算出的實際連線,與原理圖的預期電路完全一致(5 條連線)
- ✅ 沒有零件被自己的導線短路
- ✅ 沒有任何兩個不同的 Uno 腳位被接在一起(5V 與 GND 沒有短路)
- ✅ D8 腳位電流估算 ≈ 13.6 mA(Vcc 5 V、LED 順向壓降 2.0 V、串聯電阻 220Ω);Uno 建議每腳 ≤ 20 mA、絕對上限 40 mA

### 程式:`ldr-read`

- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 2994 / 32256 bytes(9%)、SRAM 201 / 2048 bytes(9%)
- ✅ 模擬(simavr,1.2 秒,UART):序列埠輸出依序包含 ['800↵', '200↵']

### 程式:`ldr-night`

- ✅ 程式 `LED_PIN = 8` ↔ 接線 `UNO.D8`
- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 3158 / 32256 bytes(9%)、SRAM 201 / 2048 bytes(9%)
- ✅ 模擬(simavr,1.6 秒,UART):序列埠輸出依序包含 ['800↵', '200↵'];輸出腳位的變化:['1@502', '0@1003'](預期 ['1@502', '0@1003'],誤差 ≤ 30 ms)

### 程式:`ldr-hyst`

- ✅ 程式 `LED_PIN = 8` ↔ 接線 `UNO.D8`
- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 2476 / 32256 bytes(7%)、SRAM 198 / 2048 bytes(9%)
- ✅ 模擬(simavr,2.4 秒,注入類比電壓 亮 → 中間值 → 暗 → 中間值 → 亮):輸出腳位的變化:['1@1001', '0@2003'](預期 ['1@1000', '0@2000'],誤差 ≤ 130 ms)

## a11 — 超音波測距 HC-SR04:倒車雷達雛形

### 接線:`sonar`

- ✅ 所有孔位都存在且在圖上的 22 欄之內
- ✅ 沒有任何一個孔被兩個零件腳或導線共用
- ✅ 依麵包板規則算出的實際連線,與原理圖的預期電路完全一致(6 條連線)
- ✅ 沒有零件被自己的導線短路
- ✅ 沒有任何兩個不同的 Uno 腳位被接在一起(5V 與 GND 沒有短路)

### 程式:`sonar-read`

- ✅ 程式 `TRIG_PIN = 9` ↔ 接線 `UNO.D9`
- ✅ 程式 `ECHO_PIN = 10` ↔ 接線 `UNO.D10`
- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 4966 / 32256 bytes(15%)、SRAM 229 / 2048 bytes(11%)
- ✅ 模擬(simavr,1.3 秒,UART):序列埠輸出依序包含 ['19.8 cm↵', '9.9 cm↵', 'out of range↵']

### 程式:`sonar-radar`

- ✅ 程式 `TRIG_PIN = 9` ↔ 接線 `UNO.D9`
- ✅ 程式 `ECHO_PIN = 10` ↔ 接線 `UNO.D10`
- ✅ 程式 `BUZZER_PIN = 12` ↔ 接線 `UNO.D12`
- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 4002 / 32256 bytes(12%)、SRAM 197 / 2048 bytes(9%)
- ✅ 模擬(simavr,1.2 秒,注入 每 20 ms 一個約 20 cm 的回波):D12 腳 觀察到 5 次 HIGH([30, 30, 30, 30] ms,預期 (27, 35))、4 次 LOW([170, 170, 170, 170] ms,預期 (150, 260))

## a12 — 伺服馬達 SG90:第一次使用函式庫

### 接線:`servo-pot`

- ✅ 所有孔位都存在且在圖上的 22 欄之內
- ✅ 沒有任何一個孔被兩個零件腳或導線共用
- ✅ 依麵包板規則算出的實際連線,與原理圖的預期電路完全一致(4 條連線)
- ✅ 沒有零件被自己的導線短路
- ✅ 沒有任何兩個不同的 Uno 腳位被接在一起(5V 與 GND 沒有短路)

### 程式:`servo-sweep`

- ✅ 程式 `SERVO_PIN = 9` ↔ 接線 `UNO.D9`
- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 3830 / 32256 bytes(11%)、SRAM 238 / 2048 bytes(11%)
- ✅ 模擬(simavr,2.2 秒,量 D9 腳的伺服脈衝):在 [500, 1000, 2000] ms 量到的脈衝寬度 [883, 1224, 1905] µs(預期 [884, 1224, 1915],誤差 ≤ 40)

### 程式:`servo-fixed`

- ✅ 程式 `SERVO_PIN = 9` ↔ 接線 `UNO.D9`
- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 3828 / 32256 bytes(11%)、SRAM 238 / 2048 bytes(11%)
- ✅ 模擬(simavr,3.0 秒,量 D9 腳的伺服脈衝):在 [500, 1500, 2500] ms 量到的脈衝寬度 [543, 1473, 2399] µs(預期 [544, 1472, 2400],誤差 ≤ 40)

### 程式:`servo-pot`

- ✅ 程式 `SERVO_PIN = 9` ↔ 接線 `UNO.D9`
- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 3922 / 32256 bytes(12%)、SRAM 238 / 2048 bytes(11%)
- ✅ 模擬(simavr,1.5 秒,量 D9 腳的伺服脈衝):在 [300, 800, 1300] ms 量到的脈衝寬度 [904, 1460, 2018] µs(預期 [905, 1462, 2018],誤差 ≤ 40)

## a13 — 溫濕度 DHT11:安裝第三方函式庫

### 接線:`dht-led`

- ✅ 所有孔位都存在且在圖上的 22 欄之內
- ✅ 沒有任何一個孔被兩個零件腳或導線共用
- ✅ 依麵包板規則算出的實際連線,與原理圖的預期電路完全一致(5 條連線)
- ✅ 沒有零件被自己的導線短路
- ✅ 沒有任何兩個不同的 Uno 腳位被接在一起(5V 與 GND 沒有短路)
- ✅ D8 腳位電流估算 ≈ 13.6 mA(Vcc 5 V、LED 順向壓降 2.0 V、串聯電阻 220Ω);Uno 建議每腳 ≤ 20 mA、絕對上限 40 mA

### 程式:`dht-read`

- ✅ 程式 `DHT_PIN = 2` ↔ 接線 `UNO.D2`
- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 6054 / 32256 bytes(18%)、SRAM 288 / 2048 bytes(14%)
- ✅ 模擬(simavr,3.0 秒,UART):序列埠輸出依序包含 ['濕度 = 55.00 %   溫度 = 26.00 C↵', '濕度 = 55.00 %   溫度 = 26.00 C↵']

### 程式:`dht-fail`

- ✅ 程式 `DHT_PIN = 2` ↔ 接線 `UNO.D2`
- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 6054 / 32256 bytes(18%)、SRAM 288 / 2048 bytes(14%)
- ✅ 模擬(simavr,2.8 秒,UART):序列埠輸出依序包含 ['讀取失敗,請檢查接線↵', '讀取失敗,請檢查接線↵']

### 程式:`dht-alarm`

- ✅ 程式 `DHT_PIN = 2` ↔ 接線 `UNO.D2`
- ✅ 程式 `LED_PIN = 8` ↔ 接線 `UNO.D8`
- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 5884 / 32256 bytes(18%)、SRAM 270 / 2048 bytes(13%)
- ✅ 模擬(simavr,2.8 秒,UART):序列埠輸出依序包含 ['溫度 = 26.00↵'];輸出腳位的變化:['1@1226'](預期 ['1@1205'],誤差 ≤ 60 ms)

## a14 — LCD1602 I2C 顯示:四條線的小螢幕

### 接線:`lcd-i2c`

- ✅ 所有接點都存在
- ✅ 沒有任何一個孔被兩個零件腳或導線共用
- ✅ 依麵包板規則算出的實際連線,與原理圖的預期電路完全一致(4 條連線)
- ✅ 沒有零件被自己的導線短路
- ✅ 沒有任何兩個不同的 Uno 腳位被接在一起(5V 與 GND 沒有短路)

### 程式:`lcd-hello`

- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 8454 / 32256 bytes(26%)、SRAM 535 / 2048 bytes(26%)

### 程式:`lcd-count`

- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 8898 / 32256 bytes(27%)、SRAM 529 / 2048 bytes(25%)

### 程式:`lcd-alt`

- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 4926 / 32256 bytes(15%)、SRAM 483 / 2048 bytes(23%)

## a15 — millis():不卡住的計時

### 接線:`millis-demo`

- ✅ 所有孔位都存在且在圖上的 26 欄之內
- ✅ 沒有任何一個孔被兩個零件腳或導線共用
- ✅ 依麵包板規則算出的實際連線,與原理圖的預期電路完全一致(6 條連線)
- ✅ 沒有零件被自己的導線短路
- ✅ 沒有任何兩個不同的 Uno 腳位被接在一起(5V 與 GND 沒有短路)
- ✅ D8 腳位電流估算 ≈ 13.6 mA(Vcc 5 V、LED 順向壓降 2.0 V、串聯電阻 220Ω);Uno 建議每腳 ≤ 20 mA、絕對上限 40 mA
- ✅ D9 腳位電流估算 ≈ 13.2 mA(Vcc 5 V、LED 順向壓降 2.1 V、串聯電阻 220Ω);Uno 建議每腳 ≤ 20 mA、絕對上限 40 mA

### 程式:`millis-blink`

- ✅ 程式 `LED_PIN = 8` ↔ 接線 `UNO.D8`
- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 2322 / 32256 bytes(7%)、SRAM 202 / 2048 bytes(9%)
- ✅ 模擬(simavr,3.2 秒,只量紅燈):D8:電位交替翻轉 6 次,間隔 499.7、499.7、500.7、499.7 … ms(預期 500 ± 3)

### 程式:`millis-two-tasks`

- ✅ 程式 `BUTTON_PIN = 2` ↔ 接線 `UNO.D2`
- ✅ 程式 `LED1_PIN = 8` ↔ 接線 `UNO.D8`
- ✅ 程式 `LED2_PIN = 9` ↔ 接線 `UNO.D9`
- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 2560 / 32256 bytes(7%)、SRAM 211 / 2048 bytes(10%)
- ✅ 模擬(simavr,3.2 秒,紅燈每 500 ms 切換,同時在 700–900 ms 按一下(帶彈跳)按鈕):D8:電位交替翻轉 6 次,間隔 499.7、499.7、500.7、499.7 … ms(預期 500 ± 3);D9:輸出腳位的變化:['1@734'](預期 ['1@734'],誤差 ≤ 5 ms)

### 程式:`delay-misses`

- ✅ 程式 `BUTTON_PIN = 2` ↔ 接線 `UNO.D2`
- ✅ 程式 `LED1_PIN = 8` ↔ 接線 `UNO.D8`
- ✅ 程式 `LED2_PIN = 9` ↔ 接線 `UNO.D9`
- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 2548 / 32256 bytes(7%)、SRAM 198 / 2048 bytes(9%)
- ✅ 模擬(simavr,2.4 秒,在 delay 期間(1200–1300 ms)按一下按鈕:黃燈完全沒反應):D9:輸出腳位的變化:[](預期 [],誤差 ≤ 5 ms)

## a16 — 外部中斷 attachInterrupt(進階選讀)

### 程式:`int-toggle`

- ✅ 程式 `BUTTON_PIN = 2` ↔ 接線 `UNO.D2`
- ✅ 程式 `LED_PIN = 8` ↔ 接線 `UNO.D8`
- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 3090 / 32256 bytes(9%)、SRAM 216 / 2048 bytes(10%)
- ✅ 模擬(simavr,2.0 秒,loop() 正在 delay(2000) 睡覺時,在 500 ms 與 1500 ms 按按鈕(都帶彈跳)):D8:輸出腳位的變化:['1@500', '0@1500'](預期 ['1@500', '0@1500'],誤差 ≤ 5 ms)

### 程式:`int-count`

- ✅ 程式 `BUTTON_PIN = 2` ↔ 接線 `UNO.D2`
- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 3298 / 32256 bytes(10%)、SRAM 215 / 2048 bytes(10%)
- ✅ 模擬(simavr,2.2 秒,UART):序列埠輸出依序包含 ['count = 0↵', 'count = 2↵', 'count = 3↵']

## a17 — I2C 與 SPI 通訊(進階選讀)

### 接線:`spi-595`

- ✅ 所有孔位都存在且在圖上的 40 欄之內
- ✅ 沒有任何一個孔被兩個零件腳或導線共用
- ✅ 依麵包板規則算出的實際連線,與原理圖的預期電路完全一致(13 條連線)
- ✅ 沒有零件被自己的導線短路
- ✅ 沒有任何兩個不同的 Uno 腳位被接在一起(5V 與 GND 沒有短路)

### 程式:`i2c-scan`

- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 5008 / 32256 bytes(15%)、SRAM 491 / 2048 bytes(23%)
- ✅ 模擬(simavr,1.2 秒,UART):序列埠輸出依序包含 ['Found device at 0x27↵', 'Found device at 0x3C↵', '--- scan done ---↵']

### 程式:`i2c-none`

- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 5008 / 32256 bytes(15%)、SRAM 491 / 2048 bytes(23%)
- ✅ 模擬(simavr,1.2 秒,UART):序列埠輸出依序包含 ['No I2C device found↵', '--- scan done ---↵']

### 程式:`spi-chase`

- ✅ 程式 `LATCH_PIN = 12` ↔ 接線 `UNO.D12`
- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 2542 / 32256 bytes(7%)、SRAM 202 / 2048 bytes(9%)
- ✅ 模擬(simavr,1.4 秒,SPI 輸出):SPI 位元組 [16, 8, 4, 2, 16](預期循環 [16, 8, 4, 2])、間隔 [300.1, 300.1, 300.1, 300.1] ms(預期 300 ± 3)、latch 上升 4 次

## a18 — 綜合專案:倒車雷達

### 接線:`parking-sensor`

- ✅ 所有接點都存在
- ✅ 沒有任何一個孔被兩個零件腳或導線共用
- ✅ 依麵包板規則算出的實際連線,與原理圖的預期電路完全一致(10 條連線)
- ✅ 沒有零件被自己的導線短路
- ✅ 沒有任何兩個不同的 Uno 腳位被接在一起(5V 與 GND 沒有短路)
- ✅ D13 腳位電流估算 ≈ 13.6 mA(Vcc 5 V、LED 順向壓降 2.0 V、串聯電阻 220Ω);Uno 建議每腳 ≤ 20 mA、絕對上限 40 mA

### 程式:`parking`

- ✅ 程式 `TRIG_PIN = 9` ↔ 接線 `UNO.D9`
- ✅ 程式 `ECHO_PIN = 10` ↔ 接線 `UNO.D10`
- ✅ 程式 `BUZZER_PIN = 12` ↔ 接線 `UNO.D12`
- ✅ 程式 `LED_PIN = 13` ↔ 接線 `UNO.D13`
- ✅ 編譯(avr-gcc + 官方 ArduinoCore-avr):Flash 11618 / 32256 bytes(36%)、SRAM 578 / 2048 bytes(28%)
- ✅ 模擬用版本編譯(LCD 以空殼取代,只為了讓模擬能跑):Flash 5366 / 32256 bytes(16%)、SRAM 429 / 2048 bytes(20%)
- ✅ 模擬(simavr,0.8 秒,每 10 ms 一個約 20 cm 的回波(LED 該亮、蜂鳴器依距離嗶)):D13:輸出腳位的變化:['1@102'](預期 ['1@102'],誤差 ≤ 6 ms);D12:輸出腳位的變化:['1@165', '0@195', '1@359', '0@388', '1@553', '0@583', '1@747', '0@776'](預期 ['1@165', '0@195', '1@359', '0@388', '1@553', '0@583', '1@747', '0@776'],誤差 ≤ 8 ms)

## a19 — 故障排除總整理

## a20 — 語法與電路符號速查

