/* 微電影分鏡主題 · 共用繪圖積木(幾何剪影風)
 * 單一來源:瀏覽器(互動頁內嵌)與 Node(svgkit.py 組頁時預先產生靜態 SVG)共用同一份,保證兩邊畫出來一樣。
 * 世界座標:預設 320×180(16:9)。地平線 y=130。所有函式回傳 SVG 字串。 */
var Kit = (function () {
  "use strict";
  var C = { ivory:"#FAF9F5", white:"#FFFFFF", slate:"#141413", clay:"#D97757", clayD:"#B85C3E", oat:"#E3DACC",
            olive:"#788C5D", rust:"#B04A3F", g100:"#F0EEE6", g300:"#D1CFC5", g500:"#87867F", g700:"#3D3D3A" };
  var WHO = { an:{ body:C.clay, bag:C.clayD, hair:C.slate }, yu:{ body:C.olive, bag:null, hair:C.g700 }, x:{ body:C.g500, bag:null, hair:C.slate } };
  var seq = 0;
  function n1(v){ return Math.round(v * 10) / 10; }
  function esc(s){ return String(s == null ? "" : s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;"); }
  function rect(x,y,w,h,fill,stroke,rx,sw){
    return '<rect x="'+n1(x)+'" y="'+n1(y)+'" width="'+n1(w)+'" height="'+n1(h)+'"'+(rx?' rx="'+n1(rx)+'"':"")+' fill="'+fill+'"'+(stroke?' stroke="'+stroke+'" stroke-width="'+(sw||1.5)+'"':"")+"/>";
  }
  function line(x1,y1,x2,y2,w,col,extra){
    return '<line x1="'+n1(x1)+'" y1="'+n1(y1)+'" x2="'+n1(x2)+'" y2="'+n1(y2)+'" stroke="'+col+'" stroke-width="'+n1(w)+'" stroke-linecap="round"'+(extra||"")+"/>";
  }
  function circ(x,y,r,fill,stroke,sw){
    return '<circle cx="'+n1(x)+'" cy="'+n1(y)+'" r="'+n1(r)+'" fill="'+fill+'"'+(stroke?' stroke="'+stroke+'" stroke-width="'+(sw||1.5)+'"':"")+"/>";
  }

  /* ---------- 場景 ---------- */
  function scene(name, W, vb){
    W = W || 320; var s = "", x, i, vis = function(a, b){ return !vb || (b >= vb[0] - 4 && a <= vb[0] + vb[2] + 4); };
    if (name === "none"){ return ""; }
    if (name === "blank"){ return rect(0,0,W,180,C.g100) + rect(0,130,W,300,C.oat); }
    if (name === "gate"){
      s += rect(-900,-420,W+1800,550,C.g100) + rect(-900,130,W+1800,500,C.oat) + line(-900,130,W+900,130,1.5,C.g500);
      s += rect(16,26,170,104,C.g300,C.g500,0);
      for (i = 0; i < 4; i++) for (x = 0; x < 2; x++) s += rect(34+i*38,40+x*40,24,26,C.white,C.g500,0,1);
      s += rect(86,100,26,30,C.g500,C.g700,0,1);
      s += rect(W-118,70,14,60,C.g700) + rect(W-44,70,14,60,C.g700) + rect(W-118,76,88,6,C.g700);
      s += rect(W-86,44,10,86,C.g500) + circ(W-81,40,24,C.olive);
      return s;
    }
    /* hallway */
    s += rect(0,-420,W,550,C.g100) + rect(0,130,W,300,C.oat) + line(0,130,W,130,1.5,C.g500);
    s += line(0,152,W,152,1,C.g300) + line(0,168,W,168,1,C.g300);
    for (x = 0; x + 44 <= W - 92; x += 44){
      if (!vis(x, x + 44)) continue;
      s += rect(x+4,28,38,100,C.g300,C.g500,2);
      s += line(x+12,38,x+34,38,1.5,C.g500) + line(x+12,44,x+34,44,1.5,C.g500) + circ(x+35,84,2.4,C.g700);
    }
    if (vis(W-92, W-12)){
      s += rect(W-92,24,80,82,C.white,C.g500,2) + line(W-52,24,W-52,106,1.5,C.g500) + line(W-92,65,W-12,65,1.5,C.g500);
      s += circ(W-30,48,12,C.olive).replace('fill="'+C.olive+'"','fill="'+C.olive+'" opacity=".45"');
    }
    return s;
  }

  /* ---------- 角色 ---------- */
  function person(o){
    var x = o.x, y = o.y, h = o.h || 100, u = h / 100, face = o.facing || "r", pose = o.pose || "stand";
    var who = WHO[o.who || "an"] || WHO.an, expr = o.expr || "neutral", g = "";
    var hip = y - 38*u, sh = y - 68*u, hx = x + (face === "r" ? 2*u : 0), hy = y - 84*u;
    var lf = -5, rf = 5, a1 = [4,-42], a2 = [-4,-42];
    if (pose === "walk"){ lf = -11; rf = 12; a1 = [13,-46]; a2 = [-12,-44]; }
    if (pose === "run"){ lf = -18; rf = 20; a1 = [16,-62]; a2 = [-14,-54]; }
    if (pose === "read"){ a1 = [14,-58]; a2 = [14,-56]; }
    if (pose === "phone"){ a1 = [12,-62]; a2 = [-4,-42]; }
    if (pose === "wave"){ a1 = [14,-92]; a2 = [-4,-42]; }
    if (face === "f" || face === "b"){ a1[0] = 14; a2[0] = -14; if (pose === "read"){ a1 = [8,-56]; a2 = [-8,-56]; } }
    g += line(x,hip,x+lf*u,y,9*u,C.g700) + line(x,hip,x+rf*u,y,9*u,C.g700);
    if (who.bag && face !== "f") g += face === "b" ? rect(x-12*u,y-70*u,24*u,30*u,who.bag,null,6*u) : rect(x-27*u,y-68*u,13*u,30*u,who.bag,null,5*u);
    g += rect(x-15*u,y-74*u,30*u,40*u,who.body,null,12*u);
    g += line(x,sh+2*u,x+a2[0]*u,y+a2[1]*u,7*u,who.body) + line(x,sh+2*u,x+a1[0]*u,y+a1[1]*u,7*u,who.body);
    g += circ(x+a1[0]*u,y+a1[1]*u,3.6*u,C.oat) + circ(x+a2[0]*u,y+a2[1]*u,3.6*u,C.oat);
    if (pose === "read") g += rect(x+(face === "r" ? 8 : face === "l" ? 8 : -8)*u,y-70*u,15*u,19*u,C.white,C.g500,1*u,1);
    if (pose === "phone") g += rect(x+10*u,y-76*u,8*u,14*u,C.slate,null,1.5*u);
    g += circ(hx,hy,11*u,C.oat,C.g700,1.5);
    g += '<path d="M'+n1(hx-11.6*u)+","+n1(hy)+" A"+n1(11.6*u)+" "+n1(11.6*u)+" 0 0 1 "+n1(hx+11.6*u)+","+n1(hy)+" Z"+'" fill="'+who.hair+'"/>';
    if (face === "r") g += circ(hx-8*u,hy+1*u,5*u,who.hair);
    if (face === "b") g += circ(hx,hy,11.6*u,who.hair);
    if (face !== "b"){
      var ex = face === "f" ? [-4.5,4.5] : [5.5], k;
      for (k = 0; k < ex.length; k++) g += circ(hx+ex[k]*u,hy+1.5*u,1.6*u,C.slate);
      var mx = hx + (face === "f" ? 0 : 5*u), my = hy + 6.5*u;
      if (expr === "surprise"){
        g += circ(mx,my+1*u,2*u,C.white,C.slate,1);
        for (k = 0; k < ex.length; k++) g += line(hx+ex[k]*u-2*u,hy-3*u,hx+ex[k]*u+2*u,hy-3.6*u,1.2,C.slate);
      } else if (expr === "smile"){
        g += '<path d="M'+n1(mx-3*u)+","+n1(my-.5*u)+" Q"+n1(mx)+","+n1(my+3.5*u)+" "+n1(mx+3*u)+","+n1(my-.5*u)+'" fill="none" stroke="'+C.slate+'" stroke-width="1.3" stroke-linecap="round"/>';
      } else if (expr === "sad"){
        g += '<path d="M'+n1(mx-3*u)+","+n1(my+1.6*u)+" Q"+n1(mx)+","+n1(my-2*u)+" "+n1(mx+3*u)+","+n1(my+1.6*u)+'" fill="none" stroke="'+C.slate+'" stroke-width="1.3" stroke-linecap="round"/>';
        for (k = 0; k < ex.length; k++) g += line(hx+ex[k]*u-2*u,hy-3.6*u,hx+ex[k]*u+2*u,hy-2.2*u,1.2,C.slate);
      } else if (expr === "angry"){
        g += line(mx-2.5*u,my+.5*u,mx+2.5*u,my+.5*u,1.5,C.slate);
        for (k = 0; k < ex.length; k++) g += line(hx+ex[k]*u-2.2*u,hy-4*u,hx+ex[k]*u+2.2*u,hy-2*u,1.5,C.slate);
      } else if (expr === "fear"){
        g += '<path d="M'+n1(mx-3*u)+","+n1(my+.6*u)+" l"+n1(1.5*u)+",-"+n1(1.6*u)+" l"+n1(1.5*u)+","+n1(1.6*u)+" l"+n1(1.5*u)+",-"+n1(1.6*u)+'" fill="none" stroke="'+C.slate+'" stroke-width="1.2" stroke-linejoin="round"/>';
        for (k = 0; k < ex.length; k++){ g += circ(hx+ex[k]*u,hy+1.5*u,2.9*u,C.white,C.slate,1) + circ(hx+ex[k]*u,hy+1.5*u,1.2*u,C.slate); g += line(hx+ex[k]*u-2.2*u,hy-4.2*u,hx+ex[k]*u+2.2*u,hy-5*u,1.2,C.slate); }
      } else if (expr === "puzzled"){
        g += line(mx-2.5*u,my+1*u,mx+2.5*u,my,1.3,C.slate);
        for (k = 0; k < ex.length; k++) g += line(hx+ex[k]*u-2*u,hy-2.4*u,hx+ex[k]*u+2*u,hy-4*u,1.2,C.slate);
      } else {
        g += line(mx-2.5*u,my,mx+2.5*u,my,1.3,C.slate);
      }
    }
    if (face === "l") g = '<g transform="translate('+n1(2*x)+' 0) scale(-1 1)">' + g + "</g>";
    return g;
  }

  /* ---------- 道具、箭頭、格線 ---------- */
  function prop(o){
    var s = o.s || 1, x = o.x, y = o.y;
    if (o.name === "phone") return rect(x,y,9*s,16*s,C.slate,null,2*s) + rect(x+1.2*s,y+1.8*s,6.6*s,11*s,C.g100,null,1*s);
    var r = rect(x,y,22*s,28*s,C.white,C.g500,1.5*s,1.2);
    r += line(x+4*s,y+7*s,x+18*s,y+7*s,1.1,C.g300) + line(x+4*s,y+12*s,x+18*s,y+12*s,1.1,C.g300) + line(x+4*s,y+17*s,x+13*s,y+17*s,1.1,C.g300);
    return r;
  }
  /* kind: move=人物移動(實線、深灰);cam=鏡頭移動(橘色粗虛線) */
  function arrow(o){
    var k = o.k || 1, cam = o.kind === "cam", col = cam ? C.clay : C.g700, sw = (cam ? 3.4 : 2.4) * k;
    var s = '<line x1="'+n1(o.x1)+'" y1="'+n1(o.y1)+'" x2="'+n1(o.x2)+'" y2="'+n1(o.y2)+'" stroke="'+col+'" stroke-width="'+n1(sw)+'"'
          + (cam ? ' stroke-dasharray="'+n1(7*k)+" "+n1(5*k)+'"' : "") + ' stroke-linecap="round" marker-end="url(#'+(cam ? "cm" : "mv")+'@U)"/>';
    if (o.label) s += '<text x="'+n1((o.x1+o.x2)/2)+'" y="'+n1((o.y1+o.y2)/2-5*k)+'" text-anchor="middle" font-size="'+n1(9*k)+'" font-weight="600" fill="'+(cam ? C.clayD : C.g700)+'" style="font-family:system-ui,sans-serif">'+esc(o.label)+"</text>";
    return s;
  }
  function thirds(vb, k){
    var x0 = vb[0], y0 = vb[1], w = vb[2], h = vb[3], s = "", i, j, st = ' stroke="'+C.clay+'" stroke-width="'+n1(1.4*k)+'" stroke-dasharray="'+n1(5*k)+" "+n1(4*k)+'"';
    for (i = 1; i < 3; i++){
      s += '<line x1="'+n1(x0+w*i/3)+'" y1="'+n1(y0)+'" x2="'+n1(x0+w*i/3)+'" y2="'+n1(y0+h)+'"'+st+"/>";
      s += '<line x1="'+n1(x0)+'" y1="'+n1(y0+h*i/3)+'" x2="'+n1(x0+w)+'" y2="'+n1(y0+h*i/3)+'"'+st+"/>";
    }
    for (i = 1; i < 3; i++) for (j = 1; j < 3; j++) s += circ(x0+w*i/3,y0+h*j/3,3.2*k,C.clay);
    return s;
  }

  /* ---------- 構圖輔助層:頭上空間、視線空間 ---------- */
  function headTop(p){ return p.y - 95.6 * (p.h || 100) / 100; }
  function faceX(p){ var u = (p.h || 100) / 100, f = p.facing || "r"; return p.x + (f === "r" ? 2 * u : f === "l" ? -2 * u : 0); }
  function txt(x, y, t, k, col){
    return '<text x="'+n1(x)+'" y="'+n1(y)+'" text-anchor="middle" font-size="'+n1(10*k)+'" font-weight="700" fill="'+col+'" style="font-family:system-ui,sans-serif">'+esc(t)+"</text>";
  }
  function headroom(p, vb, k){
    var top = headTop(p), h = top - vb[1], x = p.x, s = "";
    if (h < 1) return "";
    s += '<rect x="'+n1(x-26*(p.h||100)/100)+'" y="'+n1(vb[1])+'" width="'+n1(52*(p.h||100)/100)+'" height="'+n1(h)+'" fill="'+C.clay+'" opacity=".22"/>';
    s += '<line x1="'+n1(x)+'" y1="'+n1(vb[1]+1)+'" x2="'+n1(x)+'" y2="'+n1(top)+'" stroke="'+C.clayD+'" stroke-width="'+n1(1.6*k)+'"/>';
    s += txt(x + 56 * (p.h||100) / 100 * (x > vb[0] + vb[2] * 0.6 ? -1 : 1), vb[1] + Math.max(h / 2, 8 * k) + 3 * k, "頭上空間", k, C.clayD);
    return s;
  }
  function lookroom(p, vb, k){
    var fx = faceX(p), r = (p.facing || "r") === "r", edge = r ? vb[0] + vb[2] : vb[0], y = p.y - 84 * (p.h || 100) / 100;
    var x0 = Math.min(fx, edge), w = Math.abs(edge - fx);
    if (w < 2) return "";
    return '<rect x="'+n1(x0)+'" y="'+n1(y-7*k)+'" width="'+n1(w)+'" height="'+n1(14*k)+'" fill="'+C.olive+'" opacity=".28"/>'
         + txt((x0 + x0 + w) / 2, y + 3.4 * k, "視線空間", k, "#5C6E45");
  }

  /* ---------- 組合 ---------- */
  function svg(inner, o){
    o = o || {}; var vb = o.vb || [0,0,320,180], u = o.uid || ("r" + (++seq));
    var defs = '<defs><marker id="mv'+u+'" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="'+C.g700+'"/></marker>'
             + '<marker id="cm'+u+'" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4.2" markerHeight="4.2" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="'+C.clay+'"/></marker></defs>';
    return '<svg viewBox="'+vb.map(n1).join(" ")+'" role="img" aria-label="'+esc(o.label || "")+'" preserveAspectRatio="xMidYMid slice">'
         + defs + inner.split("@U").join(u) + "</svg>";
  }
  /* shot({scene, worldW, people:[{x,y,h,facing,pose,who,expr}], props:[{name,x,y,s}], arrows:[{x1,y1,x2,y2,kind,label}],
   *       zoom, cx, cy | vb, grid, label, uid, extra}) → 完整 <svg> */
  function shot(o){
    var W = o.worldW || 320, z = o.zoom || 1, cx = o.cx == null ? 160 : o.cx, cy = o.cy == null ? 90 : o.cy;
    var vb = o.vb || [cx - 160 / z, cy - 90 / z, 320 / z, 180 / z], k = vb[2] / 320, s = scene(o.scene || "hallway", W, o.worldW ? vb : null), i;
    (o.props || []).forEach(function(p){ s += prop(p); });
    (o.people || []).forEach(function(p){ s += person(p); });
    (o.arrows || []).forEach(function(a){ a.k = k; s += arrow(a); });
    if (o.extra) s += o.extra;
    var p0 = (o.people || [])[0];
    if (p0 && o.headroom) s += headroom(p0, vb, k);
    if (p0 && o.lookroom) s += lookroom(p0, vb, k);
    if (o.grid) s += thirds(vb, k);
    if (o.cam) s += camarrow(o.cam.kind, vb, k, o.cam.dir);
    return svg(s, { vb: vb, label: o.label, uid: o.uid });
  }

  /* ---------- 攝影機動作箭頭(橘色虛線,畫在取景框內) ---------- */
  function camarrow(kind, vb, k, dir){
    var x = vb[0], y = vb[1], w = vb[2], h = vb[3], mx = x + w / 2, my = y + h / 2, d = dir === "l" ? -1 : 1, u = dir === "d" ? 1 : -1, s = "";
    function A(x1,y1,x2,y2,l){ return arrow({ x1:x1, y1:y1, x2:x2, y2:y2, kind:"cam", label:l, k:k }); }
    if (kind === "pan") s = A(mx - d*w*.3, y + h*.07, mx + d*w*.3, y + h*.07, "搖攝");
    else if (kind === "tilt") s = A(x + w*.9, my - u*h*.28, x + w*.9, my + u*h*.28, "");
    else if (kind === "track" || kind === "follow") s = A(mx - d*w*.3, y + h*.9, mx + d*w*.3, y + h*.9, kind === "track" ? "橫移" : "跟拍");
    else if (kind === "rise") s = A(x + w*.1, my - u*h*.28, x + w*.1, my + u*h*.28, "");
    else if (kind === "push" || kind === "pull"){
      var a = kind === "push" ? 1 : 0, P4 = [[.1,.12,.28,.3],[.9,.12,.72,.3],[.1,.88,.28,.7],[.9,.88,.72,.7]];
      P4.forEach(function(q){ s += a ? A(x+w*q[0],y+h*q[1],x+w*q[2],y+h*q[3]) : A(x+w*q[2],y+h*q[3],x+w*q[0],y+h*q[1]); });
      s += txt(mx, y + h*.1, kind === "push" ? "推" : "拉", k, C.clayD);
    } else if (kind === "orbit"){
      s = '<path d="M'+n1(mx-w*.3)+","+n1(y+h*.86)+" A"+n1(w*.3)+" "+n1(h*.1)+" 0 0 0 "+n1(mx+w*.3)+","+n1(y+h*.86)+'" fill="none" stroke="'+C.clay+'" stroke-width="'+n1(3.4*k)+'" stroke-dasharray="'+n1(7*k)+" "+n1(5*k)+'" stroke-linecap="round" marker-end="url(#cm@U)"/>' + txt(mx, y + h*.97, "環繞", k, C.clayD);
    }
    return s;
  }

  /* ---------- 拍攝角度:平視 / 俯拍 / 仰拍 / 荷蘭角 ---------- */
  function angleShot(o){
    var a = o.angle || "eye", who = o.who || "an", s = "", i, hz, ph, py, yw, hL, X0 = -90, X1 = 410;
    if (a === "high"){ hz = 20; ph = 62; py = 142; yw = 92; hL = 40; }
    else if (a === "low"){ hz = 152; ph = 150; py = 162; yw = 160; hL = 135; }
    else { hz = 86; ph = 110; py = 178; yw = 124; hL = 84; }
    s += rect(X0,-120,X1-X0,yw+120,C.g100) + rect(X0,yw,X1-X0,300,C.oat) + line(X0,yw,X1,yw,1.5,C.g500);
    for (i = -2; i < 9; i++){
      s += rect(i*54+8,yw-hL,46,hL,C.g300,C.g500,2) + circ(i*54+46,yw-hL*.45,2.4,C.g700) + line(i*54+16,yw-hL+8,i*54+38,yw-hL+8,1.5,C.g500);
    }
    if (o.hzline) s += '<line x1="'+X0+'" y1="'+hz+'" x2="'+X1+'" y2="'+hz+'" stroke="'+C.clayD+'" stroke-width="1.4" stroke-dasharray="6 4"/>' + '<text x="8" y="'+(hz-4)+'" font-size="9" font-weight="700" fill="'+C.clayD+'" style="font-family:system-ui,sans-serif">地平線 = 鏡頭的高度</text>';
    s += person({ x:160, y:py, h:ph, facing:"f", who:who, expr:o.expr || "neutral", pose:o.pose || "stand" });
    if (a === "dutch") s = '<g transform="rotate(-14 160 90)">' + s + "</g>";
    return svg(s, { vb:[0,0,320,180], label:o.label, uid:o.uid });
  }

  /* ---------- 焦段 / 推拉 / 變焦:用「景深物件」重算透視 ----------
   * D = 鏡頭離主角的距離,F = 焦距倍率。主角螢幕身高 = 100*F/D,其他物件 = 100*F/(D+z)。
   * 廣角:D小、F小;望遠:D大、F大。blur>0 時,離主角越遠的物件越模糊。 */
  function lens(o){
    var D = o.D, F = o.F, hz = o.hz == null ? 70 : o.hz, camH = o.camH == null ? 84 : o.camH, sh = o.shift || 0, zw = o.zw == null ? 3.2 : o.zw;
    var bl = o.blur || 0, u = o.uid || ("r" + (++seq)), s = "", k, sc = function(z){ return F / (D + z); }, ft = function(v){ return hz + camH * v; };
    var sw = sc(zw), fw = ft(sw), b3 = bl * 3.2, b2 = bl * 1.6, b1 = bl * 1.4, sv, x, y;
    s += '<filter id="bA'+u+'" filterUnits="userSpaceOnUse" x="-200" y="-200" width="720" height="600"><feGaussianBlur stdDeviation="'+n1(b3)+'"/></filter>'
       + '<filter id="bB'+u+'" filterUnits="userSpaceOnUse" x="-200" y="-200" width="720" height="600"><feGaussianBlur stdDeviation="'+n1(b2)+'"/></filter>'
       + '<filter id="bC'+u+'" filterUnits="userSpaceOnUse" x="-200" y="-200" width="720" height="600"><feGaussianBlur stdDeviation="'+n1(b1)+'"/></filter>';
    s += rect(-200,-200,720,fw+200,C.g100) + rect(-200,fw,720,400,C.oat) + line(-200,fw,520,fw,Math.max(.8,1.5*sw),C.g500);
    var wall = "";
    for (k = -60; k <= 60; k++){
      x = 160 + (k * 44 + sh) * sw;
      if (x < -40 || x > 360) continue;
      wall += rect(x,fw-100*sw,38*sw,100*sw,C.g300,C.g500,2*sw,Math.max(.6,1.5*sw)) + circ(x+31*sw,fw-50*sw,2.4*sw,C.g700);
    }
    s += '<g'+(b3 ? ' filter="url(#bA'+u+')"' : "")+">" + wall + "</g>";
    if (o.yu !== false){
      sv = sc(1.5); x = 160 + (70 + sh * .6) * sv; y = ft(sv);
      s += '<g'+(b2 ? ' filter="url(#bB'+u+')"' : "")+">" + person({ x:x, y:y, h:100*sv, facing:"f", who:"yu", pose:"stand" }) + "</g>";
    }
    sv = F / D; s += person({ x:160, y:ft(sv), h:100*sv, facing:o.face || "f", who:o.who || "an", pose:o.pose || "stand", expr:o.expr || "neutral" });
    if (o.near !== false){
      sv = sc(-.5); x = 160 + (-100 + sh * 1.2) * sv; y = ft(sv);
      s += '<g'+(b1 ? ' filter="url(#bC'+u+')"' : "")+">" + rect(x-12*sv,y-24*sv,24*sv,24*sv,C.g700,null,3*sv) + circ(x,y-34*sv,16*sv,C.olive) + circ(x-12*sv,y-28*sv,10*sv,C.olive) + circ(x+12*sv,y-28*sv,10*sv,C.olive) + "</g>";
    }
    return svg(s, { vb:[0,0,320,180], label:o.label, uid:u });
  }

  /* ---------- 俯視示意圖(軸線與機位) ----------
   * people:[{x,y,dir(度,0=朝右,90=朝下),who,name}] cams:[{x,y,tx,ty,ok,name}] axis:y(水平軸線) zone:"top"|"bottom" */
  function topdown(o){
    var s = rect(0,0,320,180,C.g100), i, ay = o.axis;
    if (ay != null){
      if (o.zone === "top") s += rect(0,0,320,ay,C.olive).replace('fill="'+C.olive+'"','fill="'+C.olive+'" opacity=".16"');
      if (o.zone === "bottom") s += rect(0,ay,320,180-ay,C.olive).replace('fill="'+C.olive+'"','fill="'+C.olive+'" opacity=".16"');
      s += '<line x1="0" y1="'+ay+'" x2="320" y2="'+ay+'" stroke="'+C.rust+'" stroke-width="1.8" stroke-dasharray="7 5"/>' + '<text x="312" y="'+(ay-5)+'" text-anchor="end" font-size="9" font-weight="700" fill="'+C.rust+'" style="font-family:system-ui,sans-serif">軸線</text>';
    }
    (o.cams || []).forEach(function(c){
      var col = c.ok === false ? C.rust : C.clay, a = Math.atan2(c.ty - c.y, c.tx - c.x), L = 52;
      s += '<path d="M'+n1(c.x)+","+n1(c.y)+" L"+n1(c.x+L*Math.cos(a-.4))+","+n1(c.y+L*Math.sin(a-.4))+" L"+n1(c.x+L*Math.cos(a+.4))+","+n1(c.y+L*Math.sin(a+.4))+' Z" fill="'+col+'" opacity=".2" stroke="'+col+'" stroke-width="1"/>';
      s += rect(c.x-6,c.y-5,12,10,col,null,2) + (c.name ? '<text x="'+n1(c.x)+'" y="'+n1(c.y + (c.y > 90 ? 19 : -9))+'" text-anchor="middle" font-size="9.5" font-weight="700" fill="'+(c.ok === false ? C.rust : C.clayD)+'" style="font-family:system-ui,sans-serif">'+esc(c.name)+"</text>" : "");
    });
    (o.people || []).forEach(function(p){
      var w = WHO[p.who || "an"] || WHO.an, d = (p.dir || 0) * Math.PI / 180;
      s += circ(p.x,p.y,11,w.body,C.g700,1.5);
      s += '<path d="M'+n1(p.x+15*Math.cos(d))+","+n1(p.y+15*Math.sin(d))+" L"+n1(p.x+8*Math.cos(d+1.1))+","+n1(p.y+8*Math.sin(d+1.1))+" L"+n1(p.x+8*Math.cos(d-1.1))+","+n1(p.y+8*Math.sin(d-1.1))+' Z" fill="'+C.slate+'"/>';
      if (p.name) s += '<text x="'+n1(p.x)+'" y="'+n1(p.y+(p.y > 90 ? -17 : 25))+'" text-anchor="middle" font-size="10" font-weight="700" fill="'+C.g700+'" style="font-family:system-ui,sans-serif">'+esc(p.name)+"</text>";
    });
    return svg(s, { vb:[0,0,320,180], label:o.label, uid:o.uid });
  }


  /* ---------- 空拍:地面視角慢慢升高,溶接成校園俯瞰圖(示意) ---------- */
  function aerial(o){
    var t = Math.max(0, Math.min(1, o.t || 0)), e = ease(t), ph = Math.max(0, Math.min(1, (t - .3) / .45)), s = "", i;
    var H = 110 + 250 * e, w = H * 16 / 9, x0 = 200 - 40 * e - w / 2, y0 = 78 - 10 * e - H / 2, kk = 320 / w;
    var a = scene("gate", 320, [x0, y0, w, H]) + person({ x:200, y:130, h:100, facing:"f", who:"yu", pose:"phone" });
    s += '<g opacity="' + n1(1 - ph) + '" transform="scale(' + n1(kk * 1000) / 1000 + ') translate(' + n1(-x0) + " " + n1(-y0) + ')">' + a + "</g>";
    var b = rect(0,0,320,180,C.g100) + rect(0,0,320,180,C.olive).replace('fill="'+C.olive+'"','fill="'+C.olive+'" opacity=".16"');
    b += rect(0,148,320,18,C.oat) + rect(150,66,16,84,C.oat);
    b += rect(24,20,150,46,C.g300,C.g500,3) + rect(24,86,96,44,C.g300,C.g500,3);
    for (i = 0; i < 6; i++) b += rect(34 + i * 24,30,14,10,C.white,C.g500,1,1) + rect(34 + i * 24,46,14,10,C.white,C.g500,1,1);
    for (i = 0; i < 3; i++) b += rect(34 + i * 28,96,16,10,C.white,C.g500,1,1) + rect(34 + i * 28,112,16,10,C.white,C.g500,1,1);
    b += rect(206,22,96,62,C.olive,C.g700,3).replace('fill="'+C.olive+'"','fill="'+C.olive+'" opacity=".5"') + rect(214,30,80,46,"none",C.white,2) + line(254,30,254,76,1.5,C.white) + circ(254,53,9,"none",C.white,1.5);
    [[190,110],[130,164],[300,120],[280,170],[196,96],[10,160],[130,84]].forEach(function(p){ b += circ(p[0],p[1],7,C.olive,C.g700,1); });
    b += rect(136,146,5,22,C.g700) + rect(176,146,5,22,C.g700);
    b += circ(160,156,4.2,C.olive,C.slate,1.5) + '<text x="160" y="143" text-anchor="middle" font-size="9" font-weight="700" fill="' + C.g700 + '" style="font-family:system-ui,sans-serif">小宇</text>';
    s += '<g opacity="' + n1(ph) + '" transform="translate(160 90) scale(' + n1(1.5 - .5 * e) + ') translate(-160 -90)">' + b + "</g>";
    if (o.cam) s += camarrow("rise", [0,0,320,180], 1, "u");
    return svg(s, { vb:[0,0,320,180], label:o.label, uid:o.uid });
  }

  /* ---------- 運鏡動畫的某一格(t = 0..1)。靜態起訖格與互動動畫共用 ---------- */
  function ease(t){ return t < .5 ? 2*t*t : 1 - Math.pow(-2*t + 2, 2) / 2; }
  function vbf(H, cy, cx){ var w = H * 16 / 9; return [cx - w / 2, cy - H / 2, w, H]; }
  function moveFrame(o){
    var n = o.name, t = Math.max(0, Math.min(1, o.t || 0)), e = ease(t), L = o.label || "", cam = o.cam, me = {};
    function S(people, vb, extra){ var q = { worldW:1200, people:people, vb:vb, label:L, uid:o.uid, props:(extra && extra.props) || [] }; if (cam) q.cam = cam; return shot(q); }
    function P1(x, f, pose, who, expr){ return { x:x, y:130, h:100, facing:f || "r", pose:pose || "stand", who:who || "an", expr:expr || "neutral" }; }
    if (n === "pan") return S([P1(260,"r","stand","an"), P1(940,"l","phone","yu")], vbf(140,82,260+680*e));
    if (n === "tilt") return S([P1(600,"r","stand")], vbf(70,100-40*e,600));
    if (n === "track"){ var px = 250 + 700 * t; return S([P1(px,"r","walk")], vbf(140,82,px+40)); }
    if (n === "follow") return lens({ D:2.4, F:2.4, zw:8-5.4*e, face:"b", pose:"walk", yu:false, near:false, label:L, uid:o.uid });
    if (n === "orbit") return lens({ D:2.4, F:2.4, zw:2.4, shift:70-140*t, face:t < .34 ? "r" : t < .67 ? "f" : "l", yu:false, near:false, label:L, uid:o.uid });
    if (n === "push" || n === "pull"){ var q = n === "push" ? e : 1 - e; return lens({ D:4.8-2.4*q, F:2.4, label:L, uid:o.uid, blur:o.blur || 0 }); }
    if (n === "rise") return lens({ D:2.4+1*e, F:2.4, camH:84+116*e, hz:70-50*e, yu:false, near:false, label:L, uid:o.uid });
    if (n === "zoom") return lens({ D:4.8, F:2.4+2.4*e, label:L, uid:o.uid });
    if (n === "vertigo") return lens({ D:5.6-3.9*e, F:5.6-3.9*e, label:L, uid:o.uid });
    if (n === "handheld"){ var A = o.amp == null ? 5 : o.amp, tt = (o.tt == null ? t : o.tt) * 40; return S([P1(600,"f","stand","an")], vbf(110,72+A*.7*(Math.sin(tt*2.3)+.6*Math.sin(tt*5.1+1)),600+A*(Math.sin(tt*1.7)+.7*Math.sin(tt*4.3+2)))); }
    if (n === "drone") return aerial({ t:t, label:L, uid:o.uid, cam:cam });
    if (n === "slow"){ var sx = 410 + 380 * t; return S([P1(sx, "r", (Math.floor(t * (o.steps || 10)) % 2) ? "run" : "walk")], vbf(240,70,600)); }
    if (n === "longtake"){
      var px2 = t < .5 ? 150 + 610 * (t / .5) : 760, H = t < .5 ? 140 : t < .8 ? 140 - 60 * ease((t - .5) / .3) : 80, cx = t < .8 ? px2 + 40 : (px2 + 40) + 340 * ease((t - .8) / .2);
      var pose = t < .5 ? "walk" : "read", ex = t < .62 ? "neutral" : t < .72 ? "puzzled" : "surprise";
      return S([{ x:1148, y:104, h:42, facing:"f", pose:"phone", who:"yu", expr:"neutral" }, P1(px2, "r", pose, "an", ex)], vbf(H, t < .8 ? 82 - (140 - H) * .2 : 70, cx));
    }
    return "";
  }

  return { aerial:aerial, camarrow:camarrow, angleShot:angleShot, lens:lens, topdown:topdown, moveFrame:moveFrame, ease:ease, vbf:vbf, C:C, scene:scene, person:person, prop:prop, arrow:arrow, thirds:thirds, headTop:headTop, faceX:faceX, svg:svg, shot:shot, esc:esc };
})();
if (typeof module !== "undefined") module.exports = Kit;
