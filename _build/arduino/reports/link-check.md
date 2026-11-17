# Arduino 主題 · 外部連結檢查

- 日期：2026-11-17
- 方法：WebFetch 逐條開啟；docs.arduino.cc 多數只回傳頁面外殼（無法驗證內文），所以以專案擁有者的瀏覽器檢查為準。
- 範圍：36 條（`docs.arduino.cc`、`support.arduino.cc`、`www.arduino.cc`）。

| 結果 | 條數 | 處理 |
|---|---|---|
| 擁有者抽測可開啟 | 其餘 | 無 |
| 失效（大小寫錯誤） | 4 | `pinmode`→`pinMode`、`analogwrite`→`analogWrite`、`analogread`→`analogRead`、`communication/spi`→`communication/SPI`。新網址 WebFetch 未回報錯誤，**尚待擁有者在瀏覽器確認** |
| 舊網域轉址 | 1 | `www.arduino.cc/en/Tutorial/Blink`（302）改用 `docs.arduino.cc/built-in-examples/basics/Blink/` |

注意：docs.arduino.cc 的函式頁網址**區分大小寫**，且各頁大小寫不一致（例如 `digitalwrite/` 為小寫、`pinMode/` 為駝峰），新增連結前要實際開啟確認。

尚未做：事實複查；頁尾「查證日期」仍是 2026-11-07。
