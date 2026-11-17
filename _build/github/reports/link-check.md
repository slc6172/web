# GitHub 主題 · 外部連結檢查

- 日期：2026-11-17
- 方法：WebFetch 逐條開啟（無法取得 HTTP 狀態碼）；有疑義的由專案擁有者在瀏覽器實際點開確認。
- 範圍：頁面中所有 `docs.github.com` 連結（33 條，含 `{me}`、`{repo}` 的範例網址不算）。

| 結果 | 條數 | 處理 |
|---|---|---|
| 可開啟、路徑未變 | 24 | 無 |
| 舊路徑已搬家（新舊網址都連到同一頁，擁有者在瀏覽器確認） | 8 | 已改成新路徑 |
| 舊路徑失效 | 1 | `get-started/git-basics/getting-changes-from-a-remote-repository` 擁有者確認失效，改為 `get-started/using-git/getting-changes-from-a-remote-repository`（WebFetch 回應 200） |

已改的 8 條：reviewing-proposed-changes、using-secrets、reverting-a-pull-request、resolving-a-merge-conflict-using-the-command-line、hello-world、push-protection、configure-version-updates、configure-dependabot-alerts。

尚未做：介面名稱、指令與額度的逐項事實複查；頁尾「查證日期」仍是 2026-11-06，等事實複查完成後再更新。
