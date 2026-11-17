(function () {
  "use strict";
  var CFG = window.PAGE || {};
  function $(id){ return document.getElementById(id); }
  function esc(s){ return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;"); }
  function copyText(text, btn){
    var orig = btn.textContent;
    function flash(){
      btn.textContent = "Copied ✓"; btn.classList.add("copied");
      setTimeout(function(){ btn.textContent = orig; btn.classList.remove("copied"); }, 1200);
    }
    if (navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(text).then(flash, flash);
    } else {
      var ta = document.createElement("textarea"); ta.value = text;
      document.body.appendChild(ta); ta.select();
      try { document.execCommand("copy"); } catch(e){}
      document.body.removeChild(ta); flash();
    }
  }

  /* ---------- fill-in template values ---------- */
  var DEF = CFG.fill || {};
  var vals = {};
  var RE = /\{([A-Za-z0-9_]+)\}/g;
  function val(k){ return vals[k] || DEF[k]; }
  function resolvePlain(t){ return t.replace(RE, function(m, k){ return (k in DEF) ? val(k) : m; }); }
  function resolveHtml(t){
    var out = "", last = 0, m;
    RE.lastIndex = 0;
    while ((m = RE.exec(t))){
      if (!(m[1] in DEF)) continue;
      out += esc(t.slice(last, m.index)) + '<span class="slot">' + esc(val(m[1])) + "</span>";
      last = RE.lastIndex;
    }
    return out + esc(t.slice(last));
  }
  function lineHtml(line, cpp){
    if (cpp){
      var j = line.indexOf("//");
      if (j > -1) return resolveHtml(line.slice(0, j)) + '<span class="cm">' + resolveHtml(line.slice(j)) + "</span>";
      return resolveHtml(line);
    }
    if (line.trim().indexOf("# ") === 0) return '<span class="cm">' + resolveHtml(line) + "</span>";
    var i = line.indexOf("  # ");
    if (i > -1) return resolveHtml(line.slice(0, i)) + '<span class="cm">' + resolveHtml(line.slice(i)) + "</span>";
    return resolveHtml(line);
  }
  var tplEls = Array.prototype.slice.call(document.querySelectorAll("[data-tpl]"));
  tplEls.forEach(function(el){ el._tpl = el.textContent; });
  function renderTpl(){
    tplEls.forEach(function(el){
      if (el.tagName === "PRE") el.innerHTML = el._tpl.split("\n").map(function(l){ return lineHtml(l, el.hasAttribute("data-cpp")); }).join("\n");
      else el.innerHTML = resolveHtml(el._tpl);
    });
  }
  var inputs = Array.prototype.slice.call(document.querySelectorAll(".fill input"));
  inputs.forEach(function(inp){
    inp.placeholder = DEF[inp.dataset.k] || "";
    inp.addEventListener("input", function(){
      var v = inp.value;
      if (!inp.dataset.ns){ v = v.replace(/\s+/g, "-"); if (v !== inp.value) inp.value = v; }
      vals[inp.dataset.k] = v;
      renderTpl();
    });
  });
  var rb = $("resetBtn");
  if (rb) rb.addEventListener("click", function(){
    inputs.forEach(function(inp){ inp.value = ""; vals[inp.dataset.k] = ""; });
    renderTpl();
  });
  document.querySelectorAll(".cmd .copy").forEach(function(btn){
    btn.addEventListener("click", function(){
      var pre = btn.parentNode.querySelector("pre");
      copyText(pre._tpl !== undefined ? resolvePlain(pre._tpl) : pre.textContent, btn);
    });
  });

  /* ---------- reading progress + toc spy ---------- */
  var readBar = $("readBar");
  function updateBar(){
    var max = document.documentElement.scrollHeight - window.innerHeight;
    readBar.style.width = (max > 0 ? Math.min(100, window.scrollY / max * 100) : 0) + "%";
  }
  window.addEventListener("scroll", updateBar, { passive: true });
  window.addEventListener("resize", updateBar);
  updateBar();
  var tocLinks = Array.prototype.slice.call(document.querySelectorAll("nav.toc a"));
  if ("IntersectionObserver" in window){
    var spy = new IntersectionObserver(function(es){
      es.forEach(function(en){
        if (en.isIntersecting) tocLinks.forEach(function(a){ a.classList.toggle("active", a.getAttribute("href") === "#" + en.target.id); });
      });
    }, { rootMargin: "-15% 0px -70% 0px" });
    tocLinks.forEach(function(a){ var sec = document.querySelector(a.getAttribute("href")); if (sec) spy.observe(sec); });
  }

  /* ---------- scenario simulators ---------- */
  var SIM = CFG.sim || {};
  document.querySelectorAll("[data-simgroup]").forEach(function(group){
    var btns = Array.prototype.slice.call(group.querySelectorAll("[data-sim]"));
    var out = group.querySelector(".sim-result");
    btns.forEach(function(btn){
      btn.addEventListener("click", function(){
        btns.forEach(function(b){ b.classList.toggle("selected", b === btn); });
        out.innerHTML = SIM[btn.dataset.sim] || "";
      });
    });
  });

  /* ---------- quiz ---------- */
  var QUIZ = CFG.quiz || [];
  if (QUIZ.length && $("quiz")){
    var qi = 0, qScore = 0, qDone = false;
    var qCount = $("quizCount"), qQ = $("quizQ"), qAns = $("quizAns"), qFb = $("quizFb"), qNext = $("quizNext"), qScoreEl = $("quizScore");
    var renderQuiz = function(){
      var item = QUIZ[qi]; qDone = false;
      qCount.textContent = (qi + 1) + " / " + QUIZ.length;
      qQ.innerHTML = item.q;
      qAns.innerHTML = "";
      qFb.className = "feedback"; qFb.textContent = "";
      qNext.disabled = true;
      qNext.textContent = qi === QUIZ.length - 1 ? "重新測驗 ↻" : "下一題 →";
      item.a.forEach(function(text, i){
        var b = document.createElement("button");
        b.type = "button"; b.className = "answer";
        b.innerHTML = '<span class="letter">' + String.fromCharCode(65 + i) + "</span><span>" + esc(text) + "</span>";
        b.addEventListener("click", function(){ pick(i); });
        qAns.appendChild(b);
      });
    };
    var pick = function(i){
      if (qDone) return; qDone = true;
      var item = QUIZ[qi], good = i === item.c;
      Array.prototype.forEach.call(qAns.querySelectorAll("button"), function(b, n){
        b.disabled = true;
        if (n === item.c) b.classList.add("correct");
        if (n === i && !good) b.classList.add("wrong");
      });
      if (good) qScore++;
      qFb.className = "feedback show " + (good ? "good" : "bad");
      qFb.innerHTML = "<b>" + (good ? "答對了!" : "再記一下這個觀念。") + "</b> " + esc(item.why);
      qScoreEl.textContent = "答對 " + qScore + " / " + (qi + 1) + " 題";
      qNext.disabled = false;
    };
    qNext.addEventListener("click", function(){
      if (qi === QUIZ.length - 1){ qi = 0; qScore = 0; } else { qi++; }
      renderQuiz();
      qScoreEl.textContent = "答對 " + qScore + " 題";
    });
    renderQuiz();
  }

  /* ---------- checklist ---------- */
  var checks = Array.prototype.slice.call(document.querySelectorAll("#checks input"));
  function updateChecks(){
    var n = checks.filter(function(c){ return c.checked; }).length;
    $("checkProgress").textContent = "已完成 " + n + " / " + checks.length + " 項";
    $("checkBar").style.width = (n / checks.length * 100) + "%";
    checks.forEach(function(c){ c.closest(".check-item").classList.toggle("done", c.checked); });
  }
  checks.forEach(function(c){ c.addEventListener("change", updateChecks); });

  /* ---------- role tabs (dual-view pages) ---------- */
  var roleBtns = Array.prototype.slice.call(document.querySelectorAll("[data-role]"));
  var rolePanels = Array.prototype.slice.call(document.querySelectorAll("[data-panel]"));
  function setRole(r, focus){
    roleBtns.forEach(function(b){
      var on = b.dataset.role === r;
      b.classList.toggle("on", on);
      b.setAttribute("aria-selected", on ? "true" : "false");
      b.tabIndex = on ? 0 : -1;
      if (on && focus) b.focus();
    });
    rolePanels.forEach(function(p){ p.hidden = p.dataset.panel !== r; });
  }
  roleBtns.forEach(function(b){
    b.addEventListener("click", function(){ setRole(b.dataset.role); });
    b.addEventListener("keydown", function(e){
      if (e.key === "ArrowLeft" || e.key === "ArrowRight"){
        e.preventDefault(); setRole(b.dataset.role === "c" ? "o" : "c", true);
      }
    });
  });
  if (roleBtns.length) setRole("c");

  /* ---------- stage stepper (two columns) ---------- */
  var STAGES = CFG.stages || [];
  if (STAGES.length && $("stages")){
    var stage = 0;
    var stagesEl = $("stages");
    var renderStages = function(){
      stagesEl.innerHTML = STAGES.map(function(s, i){
        return '<button type="button" data-i="' + i + '" class="' + (i === stage ? "on" : "") + '" aria-pressed="' + (i === stage) + '">' +
          '<span class="si">階段 ' + (i + 1) + "</span><span>" + s.label + '</span><span class="badge ' + s.tone + '">' + s.badge + "</span></button>";
      }).join("");
      var s = STAGES[stage];
      $("c-h").textContent = s.c.h; $("o-h").textContent = s.o.h;
      $("c-list").innerHTML = s.c.items.map(function(t){ return "<li>" + t + "</li>"; }).join("");
      $("o-list").innerHTML = s.o.items.map(function(t){ return "<li>" + t + "</li>"; }).join("");
      $("prevStage").disabled = stage === 0;
      $("nextStage").disabled = stage === STAGES.length - 1;
    };
    stagesEl.addEventListener("click", function(e){
      var b = e.target.closest("button[data-i]"); if (!b) return;
      stage = +b.dataset.i; renderStages();
    });
    $("prevStage").addEventListener("click", function(){ if (stage > 0){ stage--; renderStages(); } });
    $("nextStage").addEventListener("click", function(){ if (stage < STAGES.length - 1){ stage++; renderStages(); } });
    renderStages();
  }

  /* ---------- decision picker ---------- */
  var DECIDE = CFG.decide || [];
  if (DECIDE.length && $("decideBtns")){
    var decBtns = $("decideBtns"), decOut = $("decideOut");
    decBtns.innerHTML = DECIDE.map(function(d, i){
      return '<button type="button" data-d="' + i + '">' + d.label + "</button>";
    }).join("");
    decBtns.addEventListener("click", function(e){
      var b = e.target.closest("button[data-d]"); if (!b) return;
      var d = DECIDE[+b.dataset.d];
      Array.prototype.forEach.call(decBtns.querySelectorAll("button"), function(x){ x.classList.toggle("selected", x === b); });
      var tone = d.risk === "高" ? "bad" : (d.risk === "中" ? "warn" : "ok");
      decOut.innerHTML = '<div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:8px"><b>建議做法</b><span class="badge ' + tone + '">風險:' + d.risk + "</span></div>" +
        '<div class="cmd" style="margin:8px 0"><pre></pre><button type="button" class="copy">Copy</button></div><div>' + d.why + "</div>";
      decOut.querySelector("pre").textContent = d.cmd;
      decOut.querySelector(".copy").addEventListener("click", function(ev){ copyText(d.cmd, ev.currentTarget); });
    });
  }

  renderTpl();
  if (checks.length) updateChecks();
})();
