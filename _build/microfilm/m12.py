from mh import *

Z_A = move("zoom", 0, label="變焦起點"); Z_B = move("zoom", 1, label="變焦終點:背景一起放大", cam=dict(kind="push"))
D_A = move("push", 0, label="推起點"); D_B = move("push", 1, label="推終點:背景放大得比較少", cam=dict(kind="push"))
V_A = move("vertigo", 0, label="希區考克式變焦起點:背景看起來很近"); V_B = move("vertigo", 1, label="終點:小安一樣大,背景被拉得好遠")
L_A = move("longtake", .02, label="長鏡頭起點:小安剛走進走廊"); L_B = move("longtake", .4, label="走到置物櫃前"); L_C = move("longtake", .7, label="停下來讀紙條,表情變驚訝"); L_D = move("longtake", 1, label="轉向窗外,看見小宇在校門口")
S_B = move("slow", .5, label="慢動作:同一個跑步動作,拉長成更多格")

TL_CSS = """
  .tl { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:6px; margin:10px 0 0; }
  .tl span { padding:8px 10px; border:var(--border); border-radius:10px; background:#fff; font:600 12px var(--mono); color:var(--gray-500); text-align:center; }
  .tl span.on { background:var(--slate); color:#fff; border-color:var(--slate); }
  @media (max-width: 520px) { .tl { grid-template-columns:repeat(2,minmax(0,1fr)); } }
"""

start = section("start", "進階選讀:四個「用了很有感覺」的特殊手法",
  '<p class="sub" style="margin-bottom:10px">' + lv(1, "先讀這段") + '這一篇是<b>進階選讀</b>。這些手法用得好很驚艷,用不好會很突兀,所以<b>一支短片裡一兩個就夠</b>。每個都由簡單到複雜:<b>變焦 → 慢動作 → 長鏡頭 → 希區考克式變焦</b>。</p>',
  table("g3", ["手法", "一句話", "觀眾的感受"], [
    ["變焦(zoom)", "鏡頭不動,把看法拉窄或拉寬", "被「拉近」或「推遠」,有時帶點紀錄片感"],
    ["慢動作", "動作被拉得很長", "強調、感動、衝擊"],
    ["長鏡頭", "一個鏡頭拍完整段,中間不切", "像在現場、時間連續、緊張慢慢累積"],
    ["希區考克式變焦", "一邊走近一邊拉寬看法(或相反)", "不安、暈眩、「突然發現了」"]]))

zm = section("zm", "變焦和推:看起來像,但不一樣",
  '<p>' + lv(2, "再多認識") + '第 10 篇的「推」是鏡頭<b>真的走近</b>;變焦是鏡頭<b>站在原地,改變看的範圍</b>。兩個都能讓小安變大,但要注意<b>背景</b>:</p>',
  figrow(fig(Z_A, "<b>變焦</b>起點"), fig(Z_B, "<b>變焦</b>終點"), fig(D_A, "<b>推</b>起點"), fig(D_B, "<b>推</b>終點"), cols=4),
  animbox("zm", "動畫:變焦(左)與推(右)", "小安都從小變大。看看她後面的櫃子:變焦時,櫃子和她一起放大;推時,櫃子放大得比較少,空間感也不同。", two=True),
  tip("簡單記:<b>變焦把整張圖一起放大</b>(像用手指放大照片);<b>推是鏡頭走過去</b>,近的東西變化大、遠的東西變化小。"),
  feel(("變焦 · 觀眾的感受", "比較平、像從遠處「拉近看」,常有紀錄片、監視、偷看的味道。"), ("推 · 觀眾的感受", "像自己走近,更有身歷其境與進入角色內心的感覺。")))

slow = section("slow", "慢動作:把一瞬間拉長",
  '<p>慢動作是<b>同一個動作,在畫面裡花更久的時間</b>。小安跑過去,一般速度很快就過了;慢動作時,同一段動作被拉得很長,觀眾能看清每一個細節。</p>',
  animbox("slow", "動畫:一般速度(左)與慢動作(右)", "同一個跑步動作。左邊很快結束,右邊慢慢走完。", two=True),
  '<div class="sbone">' + fig(S_B, "慢動作畫面:小安跑在走廊中間。這一格和一般速度的畫面看起來一樣,差別在<b>它停留的時間</b>。") + '</div>',
  feel(("觀眾的感受", "強調這一瞬間:感動、衝擊、美、悲傷,或讓人屏住呼吸。"), ("適合什麼情節", "重逢、告別、勝利的瞬間、意外發生的一刻,或遞出紙條的那一下。")),
  '<div class="warn"><b class="l">少用</b>慢動作用多了,節奏會變得拖。留給<b>最重要的那一個瞬間</b>。</div>')

lt = section("lt", "長鏡頭:一口氣拍完,中間不切",
  '<p>' + lv(3, "挑戰") + '長鏡頭是<b>一個鏡頭拍完整段戲,中間不剪接</b>。觀眾會覺得時間是連續的、像自己也在現場。把《紙條》第 1–4 段拍成一個長鏡頭,畫面會這樣一路變下去:</p>',
  figrow(sb(1, L_A, "小安走進走廊。", "全景,長鏡頭開始。鏡頭跟著她。"), sb(2, L_B, "她走到置物櫃前。", "鏡頭繼續跟,不切。"), sb(3, L_C, "停下來,讀紙條,表情從疑惑變驚訝。", "鏡頭慢慢推近。"), sb(4, L_D, "她抬起頭,看向窗外,小宇在那裡。", "搖攝到窗外。<b>整段只有一個鏡頭,沒有剪接。</b>"), cols=4),
  animbox("lt", "動畫:一個鏡頭,從走進走廊到發現小宇", "按播放,看鏡頭怎麼跟著她、推近、再轉向窗外。下方的時間軸會標出現在是哪一段。"),
  '<div class="tl" id="ltTl" aria-label="長鏡頭的四個階段"><span data-a="0" data-b=".5">① 走進走廊</span><span data-a=".5" data-b=".62">② 停在置物櫃前</span><span data-a=".62" data-b=".8">③ 讀紙條、推近</span><span data-a=".8" data-b="1.01">④ 轉向窗外</span></div><p class="note2" style="margin:6px 0 0;color:var(--gray-500);font-size:13px">剪接次數:<b>0</b>。如果用一般拍法,這四段通常會拆成四個以上的鏡頭再剪起來。</p>',
  '<div class="panel"><h3>長鏡頭有什麼代價?</h3><ul style="margin:0;padding-left:20px"><li><b>要練習</b>:人物與鏡頭的動作要配合,一次沒拍好就要重來整段。</li><li><b>很難「補救」</b>:中間不能切,錯了就沒辦法拿掉。</li><li><b>分鏡</b>:畫起點、中間、終點幾格,用橘色箭頭連起來,並在「鏡頭」欄寫「長鏡頭」。</li></ul></div>')

vt = section("vt", "希區考克式變焦:最難、也最特別",
  '<p>' + lv(3, "挑戰") + '這是<b>推和變焦同時做,但方向相反</b>:鏡頭一邊走近,一邊把看法拉寬(或一邊後退、一邊拉窄)。結果是:<b>人物大小不變,背景卻被拉得很遠(或擠得很近)</b>。</p>',
  figrow(fig(V_A, "<b>起點</b>:背景看起來離得近。"), fig(V_B, "<b>終點</b>:小安一樣大,背景被拉得好遠。"), cols=2),
  animbox("vt", "動畫:希區考克式變焦", "注意小安一直一樣大,但背後的空間一直變。觀眾會覺得「哪裡怪怪的」。"),
  feel(("觀眾的感受", "不安、暈眩、世界突然失控,或角色突然「發現了」什麼。"), ("想看實例可以找", "常被拿來當例子的有《迷魂記》與《大白鯊》(只提供片名,請自己找來看)。")),
  '<div class="warn"><b class="l">少用</b>這個手法很特別,<b>全片用一次</b>最有效。第一次拍短片,先不用急著做。</div>')

pick = section("pick", "你來選",
  '<p class="sub" style="margin-bottom:8px">' + lv(2, "自己改") + '讀情境,選最適合的手法。</p>',
  choose([
    dict(q="想讓小安遞出紙條的那一瞬間,被觀眾記住。", opts=["慢動作", "長鏡頭", "變焦"], ans=0, why="慢動作把一瞬間拉長,最能強調它。", pic=S_B, cap="慢動作"),
    dict(q="想讓觀眾覺得角色突然失去平衡、世界在拉扯。", opts=["希區考克式變焦", "推", "固定"], ans=0, why="人物不變、背景被拉遠,有暈眩的不安。", pic=V_B, cap="希區考克式變焦"),
    dict(q="想讓觀眾像和小安一起走過整條走廊,中間不剪接。", opts=["長鏡頭", "慢動作", "特寫"], ans=0, why="一個鏡頭拍完整段,時間連續。", pic=L_B, cap="長鏡頭"),
    dict(q="變焦和推,哪個的背景放大得比較少?", opts=["推", "變焦", "一樣"], ans=0, why="推是鏡頭走近,遠的東西變化比較小。", pic=D_B, cap="推")]),
  '<div class="panel" style="margin-top:14px"><h3>' + lv(3, "挑戰") + '</h3><p style="margin:0">把《紙條》第 1–4 段畫成<b>長鏡頭</b>:畫起點、中間、終點三格,用橘色箭頭連起來,並想想:每一格的「景別」有沒有變?</p></div>')

practice = section("practice", "動手演練與檢查",
  sim("", "情境:想讓觀眾覺得「小安發現紙條的那一刻,時間好像停住了」", "你會選?",
      [("a1", "慢動作:把那一刻拉長"), ("a2", "變焦:一下子拉近"), ("a3", "長鏡頭:整段不剪")]),
  QUIZ_HTML,
  checks(["我知道這一篇是進階選讀,這些手法一支短片用一兩個就夠。",
          "我能說出變焦和推的差別:變焦背景一起放大。",
          "我知道慢動作是把一瞬間拉長,要留給最重要的瞬間。",
          "我知道長鏡頭是整段不剪,需要練習。",
          "我知道希區考克式變焦是人物不變、背景變化。",
          "我已把《紙條》第 1–4 段畫成長鏡頭的三格。"]),
  '<h3 style="margin-top:30px">可自查的延伸閱讀</h3>',
  '<div class="panel"><ul style="margin:0;padding-left:20px"><li>想看希區考克式變焦的實例,可以找《迷魂記》與《大白鯊》。</li><li>用「變焦 推軌 長鏡頭 慢動作 希區考克式變焦」當關鍵字,看不同來源怎麼說明。</li></ul></div>')

SIM = {"a1": "<b>正確!</b>慢動作把那一刻拉長,觀眾有「時間停住」的感覺。", "a2": "<b>不太對。</b>變焦只是拉近,不會有時間被拉長的感覺。", "a3": "<b>不是重點。</b>長鏡頭是整段不剪,不一定讓一瞬間變長。"}
QUIZ = quiz_cfg([
  ("變焦和推最大的差別?", ["推是鏡頭走近,變焦是原地改變看的範圍", "兩個完全一樣", "變焦比較貴"], 0, "背景的變化也不同。"),
  ("慢動作是把什麼拉長?", ["動作在畫面裡的時間", "鏡頭的長度", "人物的身高"], 0, "同一個動作花更久。"),
  ("長鏡頭是指?", ["一個鏡頭拍完整段,中間不剪接", "拍得很遠的鏡頭", "很長的劇本"], 0, "重點是中間不剪。"),
  ("希區考克式變焦,人物的大小會?", ["保持不變,背景卻改變", "越來越大", "越來越小"], 0, "人物不變、背景變化,就是它的特色。"),
  ("這些特殊手法要怎麼用?", ["有理由才用,一支短片一兩個就夠", "每個鏡頭都用", "越多越好"], 0, "用多了就不特別了。")])

REG = ("ANIMS.zm = {dur:3800, names:[\"變焦\", \"推\"], frames:[" + mvf("zoom") + ", " + mvf("push") + "]};\n"
       "ANIMS.slow = {dur:5000, names:[\"一般速度\", \"慢動作\"], frames:[function(t){ return Kit.moveFrame({name:\"slow\", t:Math.min(1, t*4)}); }, " + mvf("slow") + "]};\n"
       "ANIMS.lt = {dur:8000, names:[\"長鏡頭(一個鏡頭,不剪)\"], frames:[" + mvf("longtake") + "], onframe:function(b,t){ Array.prototype.forEach.call(document.querySelectorAll(\"#ltTl span\"), function(s){ s.classList.toggle(\"on\", t >= +s.dataset.a && t < +s.dataset.b); }); }};\n"
       "ANIMS.vt = {dur:4200, names:[\"希區考克式變焦\"], frames:[" + mvf("vertigo") + "]};")

SPEC = defaults(
  file="microfilm-special-moves-guide.html",
  title="特殊運鏡:變焦、慢動作、長鏡頭、希區考克式變焦",
  eyebrow="第 12 篇 · 特殊運鏡(進階選讀)",
  h1="特殊運鏡:用得好很驚艷,用多了就不特別",
  sub="進階選讀。由簡單到複雜學四種:變焦、慢動作、長鏡頭、希區考克式變焦。每一種都有動畫,以及什麼情節適合用。",
  tldr="<strong>變焦</strong>是原地改變看的範圍(和推不同);<strong>慢動作</strong>拉長一瞬間;<strong>長鏡頭</strong>一個鏡頭拍完整段;<strong>希區考克式變焦</strong>人物不變、背景被拉扯。每一種都<strong>很搶戲</strong>,一支短片用一兩個就夠。",
  toc=[("start", "四個手法"), ("zm", "變焦和推"), ("slow", "慢動作"), ("lt", "長鏡頭"), ("vt", "希區考克式變焦"), ("pick", "你來選"), ("practice", "演練與檢查")],
  body="\n\n".join([start, zm, slow, lt, vt, pick, practice]),
  config=dict(sim=SIM, quiz=QUIZ), js=anim_page(REG), css=MF_CSS + TL_CSS,
  prev=("microfilm-rise-handheld-guide.html", "升降、手持、穩定器、空拍"), next=("microfilm-continuity-guide.html", "軸線與連戲"),
)
