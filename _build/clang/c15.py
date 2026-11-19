from ch import *

def fixarrows(d):
    d['arrows'] = [{'from': a['from_'], 'to': a['to']} for a in d['arrows']]
    return d

ERR_PROT = RES["p15/e1.err"]["err"].splitlines()[1].split("error: ")[1].replace("<", "&lt;")

what = section("what", "三個物件導向的關鍵想法",
  '<div class="panel"><h3>封裝、繼承、多型</h3>'
  '<p><b>封裝</b>:把資料藏在類別裡,只開放必要的入口(第 14 篇的 <code>private</code> 加 getter / setter)。</p>'
  '<p><b>繼承</b>:新的類別可以「繼承」既有類別的成員,不用重寫。狗是一種動物,所以 <code>Dog</code> 繼承 <code>Animal</code>,自動擁有動物共有的東西。</p>'
  '<p style="margin-bottom:0"><b>多型</b>:用「動物」這個通用的稱呼去操作各種動物,<b>執行時再依真正的種類做對的事</b>。這是物件導向最強、也最難一次想通的地方。</p></div>',
  '<h3 style="margin-top:26px">七個名詞</h3>',
  table("g2", ["名詞", "白話說明"], [
    ["基底類別 / 子類別", "被繼承的叫基底類別(父類別),繼承它的叫子類別。"],
    ["<code>class Dog : public Animal</code>", "Dog 繼承 Animal。冒號後面的 <code>public</code> 先照寫。"],
    ["<code>protected</code>", "外面不能碰,但子類別可以用。介於 public 與 private 之間。"],
    ["覆寫", "子類別重新寫一個和基底類別同名、同參數的函式。"],
    ["<code>virtual</code> / <code>override</code>", "基底類別用 virtual 表示「執行時決定用誰的版本」;子類別用 override 明確表示覆寫。"],
    ["多型", "同一個呼叫,依物件真正的類別有不同的行為。"],
    ["<code>-&gt;</code>", "透過指標呼叫成員:<code>a-&gt;speak()</code> 等於 <code>(*a).speak()</code>。"],
  ]))

steps_ = section("steps", "照著做:四個步驟", steps(
  step(1, "繼承:子類別自動擁有父類別的成員",
       "<code>Dog</code> 沒有自己寫 <code>getName()</code>,卻能呼叫它;也能直接使用 <code>protected</code> 的 <code>name</code>。點 ⓘ 看說明。",
       code("p15/a1"), term("p15/a1"),
       "<p>但 <code>protected</code> 在類別<b>外面</b>仍然不能碰:</p>",
       code("p15/e1.err"), errterm("p15/e1.err"),
       tip("三種權限一次整理:<code>public</code> 人人能用;<code>protected</code> 自己與子類別能用;<code>private</code> 只有自己能用。")),
  step(2, "覆寫:子類別有自己的版本——但有個陷阱",
       "<code>Dog</code> 自己寫了一個 <code>speak()</code>。直接用 Dog 呼叫沒問題;但<b>透過 Animal 指標</b>呼叫時,結果出乎意料:",
       code("p15/a2"), term("p15/a2"),
       warn("明明指著一隻狗,卻印出「(某種聲音)」!因為沒有 <code>virtual</code>,編譯器只看「指標的型態」(Animal),就決定用 Animal 的版本。", "陷阱")),
  step(3, "virtual:讓執行時決定",
       "在基底類別的函式加上 <code>virtual</code>,子類別加上 <code>override</code>。新增或改過的行用綠色底標出。",
       code("p15/a3", prev="p15/a2"), term("p15/a3"),
       see("同樣的 <code>a-&gt;speak()</code>,這次執行的是 <b>Dog 的版本</b>。編譯器改成在「執行時」看物件真正的種類——這就是多型。")),
  step(4, "多型的威力:一個迴圈處理所有動物",
       "把不同種類的動物放進同一個 <code>Animal*</code> 陣列。<b>新增一種動物,迴圈完全不用改</b>。",
       code("p15/a4"), term("p15/a4"),
       "<p>下面的關係圖可以<b>切換 <code>virtual</code></b>,並按程式碼看實際會執行誰的 <code>speak()</code>:</p>",
       '<div style="margin-top:12px"><div data-diagram="zoo"></div></div>')
))

stuck = section("stuck", "初學者最常卡住的四個地方",
  details("透過基底類別的指標呼叫,卻執行到基底的版本",
          "<p>忘了在<b>基底類別</b>的函式前加 <code>virtual</code>(第 2 步的陷阱)。有 <code>virtual</code> 才會依物件真正的類別決定。</p>"),
  details("<code>override</code> 寫了卻編譯失敗",
          "<p><code>override</code> 要求基底類別真的有同名、同參數的 <code>virtual</code> 函式。常見原因是函式名稱或參數拼錯了。這正是 <code>override</code> 的用處:幫你抓出「以為覆寫了,其實沒有」的錯。</p>"),
  details("子類別建構子要怎麼把參數交給基底類別",
          "<p>在子類別的建構子後面加冒號呼叫:<code>Dog(string n) : Animal(n) {}</code>。基底類別會先被建立,再輪到子類別。</p>"),
  details("有 <code>virtual</code> 函式的類別,解構子也要 <code>virtual</code>",
          "<p>當你用「基底類別的指標」去 <code>delete</code> 動態建立的子類別物件時(第 17 篇會學),基底類別的解構子必須是 <code>virtual</code>,否則子類別的清理不會被執行。現在先知道有這件事。</p>"))

QUIZ = quiz_cfg([
  ("<code>class Dog : public Animal</code> 的意思是?", ["Dog 繼承 Animal", "Animal 繼承 Dog", "Dog 與 Animal 無關"], 0, "冒號後面是被繼承的基底類別。"),
  ("<code>protected</code> 成員可以被誰存取?", ["自己與子類別", "任何人", "只有自己"], 0, "protected 介於 public 與 private 之間。"),
  ("<code>Animal* a = &amp;dog; a-&gt;speak();</code>,Animal 的 speak 沒有 virtual,會執行誰的?", ["Animal 的版本", "Dog 的版本", "編譯失敗"], 0, "沒有 virtual 時,編譯器依指標的型態(Animal)決定。"),
  ("多型指的是?", ["同一個呼叫,依物件真正的類別有不同行為", "一個類別有很多個物件", "一個函式有很多個參數"], 0, "多型讓通用的程式碼能處理各種不同的子類別。"),
  ("子類別覆寫基底類別的 virtual 函式時,建議在子類別函式後加?", ["override", "final", "static"], 0, "override 讓編譯器幫你檢查是不是真的覆寫了。"),
])

practice = section("practice", "動手演練:繼承與多型",
  '<p class="sub" style="margin-bottom:18px">每題先自己寫,再展開看參考解答。</p>',
  exercise(1, "圖形面積", "設計基底類別 <code>Shape</code>(<code>virtual double area()</code>),子類別 <code>Circle</code>(半徑 2)與 <code>Rectangle</code>(3 × 4)。放進同一個 <code>Shape*</code> 陣列,用迴圈印出各自的面積。", "p15/x1",
           note="圓面積 <code>3.14159 × r × r</code>。注意子類別的建構子要把半徑或長寬存起來。"),
  exercise(2, "新增一種動物", "在第 4 步的動物園裡,新增 <code>Cow</code>(叫聲「哞~」),並放進陣列。<b>迴圈本身不需要修改</b>。", "p15/x2",
           note="這就是多型的好處:對「新增」開放,但不用改動原本處理所有動物的程式。"),
  exercise(3, "呼叫基底建構子", "設計 <code>Person</code>(名字、年齡)與繼承它的 <code>Student</code>(多一個學校)。<code>Student</code> 的 <code>introduce()</code> 要先呼叫 <code>Person::introduce()</code> 再印出學校。", "p15/x3",
           note="<code>Person::introduce()</code> 是明確指定「呼叫基底類別版本」的寫法。"),
  QUIZ_HTML,
  chk(["我能說出封裝、繼承、多型各是什麼。", "我會用 <code>class Dog : public Animal</code> 寫繼承,並呼叫基底類別的建構子。",
       "我分得出 public、protected、private。", "我知道沒有 <code>virtual</code> 時,透過基底指標呼叫會用到基底版本。",
       "我會用 <code>virtual</code> 加 <code>override</code> 寫出多型。", "我知道多型讓新增子類別時,不必修改處理基底類別的程式。"]),
  links([("https://en.cppreference.com/cpp/language/derived_class", "cppreference:繼承", "cppreference.com"),
         ("https://en.cppreference.com/cpp/language/virtual", "cppreference:virtual 函式", "cppreference.com")]))

SPEC = spec(
  file="clang-oop-guide.html",
  title="封裝、繼承、多型:繼承共用程式,virtual 讓同一呼叫有不同行為",
  eyebrow="第 15 篇 · 封裝、繼承、多型",
  h1="繼承共用程式,<code>virtual</code> 讓同一呼叫有不同行為",
  sub="從繼承開始,到最重要的多型:用關係圖和可切換的 <code>virtual</code>,親眼看到「同一個呼叫,執行誰的版本」是怎麼決定的。",
  tldr="<strong>繼承</strong>讓子類別自動擁有基底類別的成員;<code>protected</code> 讓子類別能用、外面不能碰。<strong>多型</strong>:基底類別函式加 <code>virtual</code>、子類別加 <code>override</code>,透過基底指標呼叫時,執行的是<strong>物件真正類別的版本</strong>。忘了 <code>virtual</code> 就會用到基底版本。",
  toc=[("what", "三個想法"), ("steps", "四個步驟"), ("stuck", "常見卡關"), ("practice", "演練與延伸閱讀")],
  body="\n\n".join([what, steps_, stuck, practice]),
  config=dict(diagram=dict(zoo=fixarrows(dict(
      rows=[["animal"], ["dog", "cat"]],
      arrows=[dict(from_="dog", to="animal"), dict(from_="cat", to="animal")],
      boxes=dict(
        animal=dict(name="Animal", sub="基底類別", fields=[dict(t="string", n="name", v="pro", note="名字。protected:子類別可以用,外面不能碰。")],
                    methods=[dict(t="", n="Animal(string n)", v="pub", note="建構子。子類別會用 : Animal(n) 呼叫它。"),
                             dict(t="string", n="getName()", v="pub", note="取得名字。Dog 與 Cat 都繼承了它,不用重寫。"),
                             dict(t="virtual void", n="speak()", v="pub", note="發出聲音。「virtual」讓執行時依物件真正的類別決定用誰的版本(用上面的勾選切換)。")]),
        dog=dict(name="Dog", sub="子類別", methods=[dict(t="void", n="speak() override", v="pub", note="覆寫:狗叫「汪汪!」。")]),
        cat=dict(name="Cat", sub="子類別", methods=[dict(t="void", n="speak() override", v="pub", note="覆寫:貓叫「喵喵!」。")])),
      toggle=dict(label="基底類別的 speak() 有加 virtual", on=True),
      testsTitle="試試看:按下面的程式碼,看會執行誰的 speak()",
      tests=[dict(code="Dog d; d.speak();", ok=True, msg="直接用 Dog 物件呼叫:執行 Dog 的版本,印出「汪汪!」。", hl="dog.speak() override"),
             dict(code="Animal* a = &d; a->speak();",
                  on=dict(ok=True, msg="有 virtual:執行時看物件真正的類別(Dog),執行 Dog 的版本,印出「汪汪!」。這是多型。", hl="dog.speak() override"),
                  off=dict(ok=False, msg="沒有 virtual:編譯器只看指標的型態(Animal),執行 Animal 的版本,印出「(某種聲音)」。通常這不是你要的!", hl="animal.speak()")),
             dict(code="Animal* a = &c; a->speak();",
                  on=dict(ok=True, msg="有 virtual:物件真正是 Cat,執行 Cat 的版本,印出「喵喵!」。", hl="cat.speak() override"),
                  off=dict(ok=False, msg="沒有 virtual:一樣只看指標的型態,執行 Animal 的版本,印出「(某種聲音)」。", hl="animal.speak()")),
             dict(code="cout << d.getName();", ok=True, msg="可以。getName 是 public,Dog 從 Animal 繼承而來。", hl="animal.getName()"),
             dict(code="cout << d.name;", ok=False, msg="編譯失敗:<code>" + ERR_PROT + "</code>。name 是 protected,類別外面不能直接碰。", hl="animal.name")]))), quiz=QUIZ),
  **nav(15),
)
