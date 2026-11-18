/* EEG 交互示例：固定种子合成信号 + 原生 canvas。
   三 demo：波形→patch / 窗口→时频图（手写 STFT）/ 随机 vs 时空块掩码。 */
(function () {
  "use strict";
  if (!document.getElementById("d1-canvas")) return;

  /* 固定种子 PRNG（mulberry32），保证同参数重绘一致 */
  function prng(seed) {
    return function () {
      seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
      var t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  function synth(sr, dur, f1, f2, seed) {
    var rnd = prng(seed), n = Math.round(sr * dur), x = new Float64Array(n);
    for (var i = 0; i < n; i++) {
      var t = i / sr;
      x[i] = Math.sin(2 * Math.PI * f1 * t) + 0.5 * Math.sin(2 * Math.PI * f2 * t) + 0.15 * (rnd() - 0.5);
    }
    return x;
  }

  function setupCanvas(id, ctxColor) {
    var c = document.getElementById(id);
    var dpr = window.devicePixelRatio || 1;
    var w = c.width, h = c.height;
    c.style.width = w + "px"; c.style.maxWidth = "100%";
    c.width = w * dpr; c.height = h * dpr;
    var ctx = c.getContext("2d");
    ctx.scale(dpr, dpr);
    ctx.fillStyle = ctxColor || "#fafafa";
    ctx.fillRect(0, 0, w, h);
    return ctx;
  }

  /* ---------- 示例一：波形 → patch ---------- */
  var d1 = { sr: 256, dur: 4, f1: 10, f2: 30, win: 1, ov: 0.1 };
  function draw1() {
    var x = synth(d1.sr, d1.dur, d1.f1, d1.f2, 42);
    var ctx = setupCanvas("d1-canvas");
    var W = 760, H = 180, pad = 30, gw = W - 2 * pad, gh = H - 2 * pad;
    // 波形
    ctx.strokeStyle = "#3949ab"; ctx.lineWidth = 1; ctx.beginPath();
    var mn = -1.8, mx = 1.8;
    for (var i = 0; i < x.length; i++) {
      var px = pad + gw * i / (x.length - 1);
      var py = pad + gh * (1 - (x[i] - mn) / (mx - mn));
      i ? ctx.lineTo(px, py) : ctx.moveTo(px, py);
    }
    ctx.stroke();
    // patch 边界
    var step = Math.max(1, Math.round(d1.win * (1 - d1.ov) * d1.sr));
    ctx.strokeStyle = "rgba(230,81,0,0.55)";
    for (var s = 0; s * step < x.length; s++) {
      var bx = pad + gw * (s * step) / (x.length - 1);
      ctx.beginPath(); ctx.moveTo(bx, pad); ctx.lineTo(bx, pad + gh); ctx.stroke();
    }
    var nPatch = Math.ceil((x.length - d1.win * d1.sr) / step) + 1;
    // 轴
    ctx.fillStyle = "#555"; ctx.font = "11px sans-serif";
    ctx.fillText("0 s", pad, H - 10);
    ctx.fillText(d1.dur + " s", pad + gw - 20, H - 10);
    ctx.fillText("振幅（µV 归一化）", 4, pad - 12);
    var info = document.getElementById("d1-info");
    if (info) info.textContent = "→ " + nPatch + " 个 patch（每窗 " + d1.win + "s，重叠 " + (d1.ov * 100) + "%）";
  }
  ["d1-sr", "d1-dur", "d1-f1", "d1-f2", "d1-win", "d1-ov"].forEach(function (id) {
    var el = document.getElementById(id);
    el && el.addEventListener("input", function () {
      d1.sr = +document.getElementById("d1-sr").value;
      d1.dur = +document.getElementById("d1-dur").value;
      d1.f1 = +document.getElementById("d1-f1").value;
      d1.f2 = +document.getElementById("d1-f2").value;
      d1.win = +document.getElementById("d1-win").value;
      d1.ov = +document.getElementById("d1-ov").value;
      draw1();
    });
  });
  draw1();

  /* ---------- 示例二：STFT 时频图 ---------- */
  function draw2() {
    var winN = +document.getElementById("d2-win").value;
    var sr = 256, dur = 4;
    document.getElementById("d2-winlabel").textContent = winN + " 样本（" + (winN / sr).toFixed(2) + " s）";
    var x = synth(sr, dur, 10, 30, 42);
    var hop = 8, nT = Math.floor((x.length - winN) / hop);
    var fMax = 50, nF = 64;
    var spec = [];
    for (var ti = 0; ti < nT; ti++) {
      var col = new Float64Array(nF);
      var off = ti * hop;
      for (var fi = 0; fi < nF; fi++) {
        var f = fi / nF * fMax, re = 0, im = 0;
        for (var k = 0; k < winN; k++) {
          var w = 0.5 - 0.5 * Math.cos(2 * Math.PI * k / winN); // Hann
          var v = x[off + k] * w;
          re += v * Math.cos(2 * Math.PI * f * k / sr);
          im -= v * Math.sin(2 * Math.PI * f * k / sr);
        }
        col[fi] = Math.hypot(re, im);
      }
      spec.push(col);
    }
    var peak = 0;
    spec.forEach(function (c) { c.forEach(function (v) { peak = Math.max(peak, v); }); });
    var ctx = setupCanvas("d2-canvas");
    var W = 760, H = 220, pad = 34, gw = W - pad - 12, gh = H - pad - 12;
    for (var ti = 0; ti < nT; ti++) {
      for (var fi = 0; fi < nF; fi++) {
        var v = spec[ti][fi] / peak;
        var px = pad + gw * ti / nT, pw = gw / nT + 1;
        var py = pad + gh * (1 - fi / nF), ph = gh / nF + 1;
        var g = Math.round(255 * (1 - v));
        ctx.fillStyle = "rgb(" + g + "," + g + ",255)";
        ctx.fillRect(px, py - ph, pw, ph);
      }
    }
    ctx.fillStyle = "#555"; ctx.font = "11px sans-serif";
    ctx.fillText("50 Hz", 2, pad + 8);
    ctx.fillText("0 Hz", 2, pad + gh);
    ctx.fillText("10 Hz 谱峰 ←", pad + 8, pad + gh * (1 - 10 / fMax) - 3);
    ctx.fillText("30 Hz（幅度减半）→", pad + gw - 130, pad + gh * (1 - 30 / fMax) - 3);
    ctx.fillText("0 s", pad, H - 4);
    ctx.fillText(dur + " s", pad + gw - 20, H - 4);
    ctx.fillText("频率分辨率 " + (sr / winN).toFixed(2) + " Hz", pad + gw - 120, pad - 8);
  }
  var d2el = document.getElementById("d2-win");
  d2el && d2el.addEventListener("input", draw2);
  draw2();

  /* ---------- 示例三：随机 vs 时空块掩码 ---------- */
  function draw3() {
    var ratio = +document.getElementById("d3-ratio").value;
    var rs = +document.getElementById("d3-rs").value;
    var rt = +document.getElementById("d3-rt").value;
    document.getElementById("d3-ratiolabel").textContent = ratio + "%";
    var C = 8, T = 24;
    var mask = [], maskB = [];
    var rnd = prng(7);
    // 随机点：每格独立伯努利
    for (var c = 0; c < C; c++) { mask[c] = []; for (var t = 0; t < T; t++) mask[c][t] = rnd() * 100 < ratio; }
    // 时空块：随机选种子 patch，挖 (2rs+1)×(2rt+1) 邻域，直到达标
    var rndB = prng(11);
    maskB = Array.from({ length: C }, function () { return new Array(T).fill(false); });
    var target = Math.round(ratio / 100 * C * T), masked = 0, guard = 0;
    while (masked < target && guard++ < 500) {
      var sc = Math.floor(rndB() * C), st = Math.floor(rndB() * T);
      for (var dc = -rs; dc <= rs; dc++) for (var dt = -rt; dt <= rt; dt++) {
        var cc = sc + dc, tt = st + dt;
        if (cc >= 0 && cc < C && tt >= 0 && tt < T && !maskB[cc][tt]) { maskB[cc][tt] = true; masked++; }
      }
    }
    function drawGrid(x0, grid, label) {
      var ctx = document.getElementById("d3-canvas").getContext("2d");
      var pad = 30, gw = 320, gh = 160;
      var cw = gw / T, ch = gh / C;
      ctx.fillStyle = "#555"; ctx.font = "12px sans-serif";
      ctx.fillText(label, x0, pad - 10);
      for (var c = 0; c < C; c++) for (var t = 0; t < T; t++) {
        ctx.fillStyle = grid[c][t] ? "rgba(229,57,53,0.85)" : "#d8dce6";
        ctx.fillRect(x0 + t * cw + 1, pad + c * ch + 1, cw - 2, ch - 2);
      }
      ctx.fillStyle = "#555"; ctx.font = "10px sans-serif";
      ctx.fillText("通道 1→" + C, x0 - 2, pad + gh + 14);
      ctx.fillText("时间 patch 1→" + T, x0 + gw / 2 - 40, pad + gh + 14);
    }
    var ctx = setupCanvas("d3-canvas");
    drawGrid(24, mask, "随机点掩码（MAE 式）");
    drawGrid(410, maskB, "时空块掩码（REVE 式）");
    var cnt = 0, blocks = 0; maskB.forEach(function (r) { r.forEach(function (v) { v && cnt++; }); });
    mask.forEach(function (r) { r.forEach(function (v) { v && blocks++; }); });
    var info = document.getElementById("d3-info");
    if (info) info.textContent = "→ 随机掩 " + blocks + " 格 / 块掩 " + cnt + " 格（目标 " + Math.round(ratio / 100 * C * T) + "）";
  }
  ["d3-ratio", "d3-rs", "d3-rt"].forEach(function (id) {
    var el = document.getElementById(id);
    el && el.addEventListener("input", draw3);
  });
  draw3();
})();
