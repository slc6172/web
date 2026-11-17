import json
from mh import *

BAD_HEAD = shot(people=[P(160, 130, expr="smile")], vb=[103, 48, 114, 64], label="頭被切掉了:取景框太低")
GOOD_HEAD = shot(people=[P(160, 130, expr="smile")], vb=[103, 20, 114, 64], label="頭上留了一點空間")
VB = vbfor(78, 62, 160)
J_A = shot(scene="gate", people=[P(160, 130)], vb=VB, label="小安,腰上景")
J_B = shot(scene="gate", people=[P(163, 130)], vb=[VB[0] + 2, VB[1], VB[2], VB[3]], label="幾乎一模一樣的下一格")
J_C = shot(scene="gate", people=[P(160, 130, expr="surprise")], vb=[103, 20, 114, 64], label="換成特寫")
TWOBAD = shot(scene="gate", people=[P(125, 130, who="yu", facing="r")], vb=VB, label="跨過軸線:小宇跑到左邊,看向右邊")

LIST = [
  dict(n=1, scene="走廊", text="小安快步走", shot="全景，橫移"),
  dict(n=2, scene="走廊", text="櫃門縫的紙條", shot="大特寫（插入），固定"),
  dict(n=3, scene="走廊", text="她讀紙條", shot="近景，推"),
  dict(n=4, scene="校門口", text="小宇低頭看手機", shot="近景，俯拍"),
  dict(n=5, scene="走廊", text="小安衝下樓", shot="全景，跟拍"),
  dict(n=6, scene="校門口", text="兩人面對面，遞出紙條", shot="腰上景（雙人），固定"),
]

start = section("start", "從分鏡表到「鏡頭清單」",
  '<p class="sub" style="margin-bottom:10px">' + lv(1, "跟著做") + '分鏡表是畫給「看故事」的人;拍攝當天需要的是<b>鏡頭清單</b>:一份「今天要拍哪些、拍好了沒」的待辦表。做法很簡單:把第 15 篇分鏡表的每一格,抄成一行,再加一個「拍好了」的格子。</p>',
  table("g3", ["欄位", "寫什麼", "例子"], [
    ["編號", "和分鏡表同一個編號", "3"],
    ["場景", "在哪裡拍", "走廊"],
    ["鏡頭", "景別、角度、運鏡", "近景，推"],
    ["拍好了", "拍完就打勾", "☐"]]),
  tip("鏡頭清單<b>只寫鏡頭本身</b>就夠了;每一格寫得太長,反而當天找不到重點。"))

order = section("order", "拍攝順序不等於故事順序",
  '<p>' + lv(2, "自己改") + '《紙條》的六格,故事是 1→6。但拍的時候,<b>同一個場景的鏡頭一次拍完</b>最省時間:不用走來走去、光線和背景也一樣。按下面的按鈕,看看順序怎麼變。拍好一格就勾一下。</p>',
  '''<div class="panel"><div class="fx" id="ordPick" role="group" aria-label="排序方式"><button type="button" data-k="story" class="on">故事順序</button><button type="button" data-k="shoot">拍攝順序(依場景分組)</button></div>
  <div id="ordList" style="margin-top:12px"></div><div class="check-progress" id="ordProg" style="margin-top:8px"></div><div class="bar"><span id="ordBar"></span></div></div>''',
  tip("連續兩格<b>人物在同一個地方、鏡頭差很多</b>(例如先全景再特寫),也可以接著拍。分組只是原則,現場看狀況調整。"))

take = section("take", "每一格多拍幾次,再多拍幾個備用",
  '<p>' + lv(2, "再多認識") + '現場拍的時候,<b>每一格多拍兩三次</b>:演員會越來越自然,也比較不怕剪的時候發現「剛好那一次糊掉了」。另外順手多拍這幾種<b>備用鏡頭</b>,剪接時很救命:</p>',
  '<div class="panel"><ul style="margin:0;padding-left:20px;line-height:1.9"><li><b>反應鏡頭</b>:聽的人的臉(第 6 篇)。</li><li><b>插入鏡頭</b>:重要的物件或細節(第 6 篇)。</li><li><b>空鏡</b>:沒有人的環境畫面,轉場時很好用。</li><li><b>每個鏡頭的頭尾</b>:開始前、結束後多停一兩秒(第 9 篇的起幅、落幅)。</li></ul></div>')

err = section("err", "新手最常見的八個錯誤",
  '<p>' + lv(3, "挑戰") + '你學過的每一個觀念,都對應一個最常見的錯誤。看看有沒有哪一個是你的分鏡裡出現過的:</p>',
  figrow(fig(BAD_HEAD, "<b>✗ 頭被切掉</b>:取景框太低,表情不見了。"), fig(GOOD_HEAD, "<b>✓ 頭上留一點空間</b>(第 2 篇)。"), cols=2),
  figrow(fig(J_B, "<b>✗ 連續兩格太像</b>:剪起來會跳(第 13 篇)。"), fig(J_C, "<b>✓ 換景別</b>:順。"), cols=2),
  details("1. 每一格都用同樣的景別", "整支片子都是腰上景,會很單調。想想這一格要讓觀眾看見什麼,再選景別(第 3–5 篇)。"),
  details("2. 頭上空間、視線空間沒檢查", "人物頂到畫面上緣,或臉貼著畫面邊緣,看起來會很擠(第 2 篇)。"),
  details("3. 跨過軸線", "對話時攝影機跑到另一邊,人物像在看同一個方向(第 13 篇)。"),
  details("4. 連續兩格太像(跳接)", "換景別,或把鏡頭位置移開(第 13 篇)。"),
  details("5. 運鏡太多、太快", "鏡頭一直動、而且很快,觀眾會頭暈。沒有理由就固定,要動就慢(第 9–10 篇)。"),
  details("6. 搖攝沒有起幅和落幅", "一開始就搖、搖到哪停哪,很難剪。先停、慢慢轉、再停(第 9 篇)。"),
  details("7. 忘了拍反應與插入", "剪的時候才發現缺了聽的人的臉,或看不清重要物件。現場順手多拍(第 6 篇)。"),
  details("8. 沒有先排練", "分鏡畫好了,但演員不知道要走哪裡,拍起來很亂。先在現場走一遍位置,再正式拍。"))

pick = section("pick", "你來診斷",
  '<p class="sub" style="margin-bottom:8px">' + lv(2, "自己改") + '讀情境,指出問題在哪裡。</p>',
  choose([
    dict(q="剪接時發現:兩個人對話的畫面,看起來像在看同一個方向。", opts=["攝影機跨過了軸線", "景別選錯", "沒有拍空鏡"], ans=0, why="跨過軸線,左右位置對調。", pic=TWOBAD, cap="跨軸"),
    dict(q="連續兩格都是小安的腰上景,角度幾乎一樣,剪起來像跳了一下。", opts=["兩格太像,要換景別或角度", "要加更多搖攝", "要換演員"], ans=0, why="跳接:景別與角度差太少。", pic=J_B, cap="太像"),
    dict(q="拍完才發現:沒有任何一格能看清楚紙條上寫什麼。", opts=["少了插入鏡頭", "少了環繞", "少了空拍"], ans=0, why="重要物件要用插入鏡頭讓觀眾看清楚。"),
    dict(q="最省時間的拍攝順序是?", opts=["同一個場景的鏡頭一次拍完", "照故事順序一格一格拍", "隨便拍"], ans=0, why="減少走來走去、光線與背景也一致。")]),
  '<div class="panel" style="margin-top:14px"><h3>' + lv(3, "挑戰") + '</h3><p style="margin:0">用第 15 篇的分鏡表,做出自己的「鏡頭清單」:先照場景分組、再排拍攝順序,每一格旁邊寫「多拍幾次」。你可以拿它去拍你的第一支 30 秒短片。</p></div>')

practice = section("practice", "動手演練與檢查",
  sim("", "情境:明天要拍《紙條》,你想讓當天最順利", "最先做哪一件事?",
      [("a1", "把分鏡表整理成鏡頭清單,並依場景分組"), ("a2", "什麼都不準備,到現場再想"), ("a3", "每一格都換不同的運鏡,越多越好")]),
  QUIZ_HTML,
  checks(["我能把分鏡表整理成鏡頭清單。",
          "我知道拍攝順序可以依場景分組,不一定照故事順序。",
          "我知道每一格要多拍幾次,還要多拍備用鏡頭。",
          "我能說出至少五個新手常見錯誤。",
          "我拍之前會先排練位置。",
          "我已準備好拍我的第一支短片。"]),
  '<h3 style="margin-top:30px">你完成了全部 16 篇</h3>',
  '<div class="panel"><p style="margin:0">回顧一下你學過的:<b>分鏡(1)→構圖(2)→景別(3–6)→角度與焦段(7–8)→運鏡(9–12)→連戲(13)→情節(14)→實作(15)→準備(16)</b>。下一步:找一兩個朋友,用手邊有的任何設備,照你自己的分鏡拍一支 30 秒的短片。第一支拍得不完美沒關係,拍完你就會知道下一次要改什麼。</p></div>')

SIM = {"a1": "<b>很棒!</b>整理成鏡頭清單,依場景分組,當天不用想,照著拍就行。", "a2": "<b>風險很大。</b>沒有準備,現場容易漏拍、重複跑場景。", "a3": "<b>不是重點。</b>運鏡要有理由,越多越容易亂,也更難拍。"}
QUIZ = quiz_cfg([
  ("鏡頭清單是給誰用的?", ["拍攝當天,確認要拍哪些、拍好了沒", "給觀眾看故事", "給老師打分數"], 0, "它是當天的待辦表。"),
  ("拍攝順序通常怎麼排比較省時間?", ["依場景分組,同一個場景一次拍完", "一定要照故事順序", "越亂越好"], 0, "少走動,光線和背景一致。"),
  ("每一格建議怎麼拍?", ["多拍兩三次", "只拍一次", "越多越好,超過十次"], 0, "多拍幾次,演員會越來越自然,也有備用。"),
  ("哪一個不是常見的備用鏡頭?", ["反應鏡頭", "插入鏡頭", "把整齣戲再拍一遍"], 2, "備用鏡頭是反應、插入、空鏡等,不是整段重拍。")])

JS = """<script>
(function () {
  var L = __L__, mode = "story", done = {}, list = document.getElementById("ordList");
  function render() {
    var items = L.slice(), html = "";
    if (mode === "shoot") items.sort(function (a, b) { return a.scene === b.scene ? a.n - b.n : (a.scene === "走廊" ? -1 : 1); });
    var last = "";
    items.forEach(function (it) {
      if (mode === "shoot" && it.scene !== last) { last = it.scene; html += '<div style="font:600 11px var(--mono);letter-spacing:.06em;color:var(--gray-500);margin:12px 0 4px">場景:' + it.scene + "</div>"; }
      html += '<label class="check-item"><input type="checkbox" data-n="' + it.n + '"' + (done[it.n] ? " checked" : "") + "><span><b>第 " + it.n + " 格</b>〔" + it.scene + "〕" + it.text + "——" + it.shot + "</span></label>";
    });
    list.innerHTML = '<div class="checks" style="grid-template-columns:minmax(0,1fr)">' + html + "</div>";
    var c = Object.keys(done).filter(function (k) { return done[k]; }).length;
    document.getElementById("ordProg").textContent = "拍好了 " + c + " / " + L.length + " 格";
    document.getElementById("ordBar").style.width = (c / L.length * 100) + "%";
    Array.prototype.forEach.call(document.getElementById("ordPick").children, function (b) { b.classList.toggle("on", b.dataset.k === mode); b.setAttribute("aria-pressed", b.dataset.k === mode); });
  }
  list.addEventListener("change", function (e) { var n = e.target.dataset.n; if (n) { done[n] = e.target.checked; render(); } });
  document.getElementById("ordPick").addEventListener("click", function (e) { var b = e.target.closest("button"); if (b) { mode = b.dataset.k; render(); } });
  render();
})();
</script>""".replace("__L__", json.dumps(LIST, ensure_ascii=False)) + CHOOSE_JS

SPEC = defaults(
  file="microfilm-prep-guide.html",
  title="拍攝前準備:鏡頭清單與新手常見錯誤",
  eyebrow="第 16 篇 · 拍攝前準備",
  h1="拍攝前準備:把分鏡表變成當天的鏡頭清單",
  sub="最後一篇:把分鏡表整理成鏡頭清單、決定拍攝順序,再用八個常見錯誤檢查自己的分鏡。準備好了,就去拍你的第一支短片。",
  tldr="分鏡表是給「看故事」的人,<strong>鏡頭清單</strong>是當天的待辦表。<strong>依場景分組</strong>拍最省時間;每一格<strong>多拍幾次</strong>,再順手拍<strong>反應、插入、空鏡</strong>備用。開拍前對照八個常見錯誤。",
  toc=[("start", "鏡頭清單"), ("order", "拍攝順序"), ("take", "多拍與備用"), ("err", "八個常見錯誤"), ("pick", "你來診斷"), ("practice", "演練與檢查")],
  body="\n\n".join([start, order, take, err, pick, practice]),
  config=dict(sim=SIM, quiz=QUIZ), js=JS,
  prev=("microfilm-practice-guide.html", "實作:把劇本畫成分鏡"),
)
