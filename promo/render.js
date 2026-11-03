// Renders promo/video.html to a 1080x1920 TikTok/Reels/Shorts MP4.
// Usage: node promo/render.js [config.json] [out.mp4]
// Needs: playwright (Chromium), ffmpeg, python3 + numpy (for sound effects).
const { chromium } = require("playwright");
const fs = require("fs"), path = require("path"), os = require("os");
const { execFileSync } = require("child_process");
(async () => {
  const [cfgPath, out = "geowawe-promo.mp4"] = process.argv.slice(2);
  const FPS = 30, dir = fs.mkdtempSync(path.join(os.tmpdir(), "gp-frames-"));
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  const cfg = cfgPath ? JSON.parse(fs.readFileSync(cfgPath, "utf8")) : null;
  await p.goto("file://" + path.join(__dirname, (cfg && cfg.template) || "video.html"));
  if (cfg) await p.evaluate(c => { CONFIG = c; }, cfg);
  const { duration, events } = await p.evaluate(() => window.ready.then(() => ({ duration: duration(), events: events() })));
  await p.evaluate(() => document.fonts.ready);
  const n = Math.round(duration * FPS);
  for (let f = 0; f < n; f++) {
    await p.evaluate(t => render(t), f / FPS);
    await p.screenshot({ path: path.join(dir, `f${String(f).padStart(5, "0")}.jpg`), type: "jpeg", quality: 92 });
    if (f % 60 === 0) process.stdout.write(`\rframe ${f}/${n}`);
  }
  await b.close();
  console.log(`\rframes done (${n})       `);
  const wav = path.join(dir, "sfx.wav");
  execFileSync("python3", [path.join(__dirname, "sfx.py"), wav, String(duration), JSON.stringify(events)], { stdio: "inherit" });
  execFileSync("ffmpeg", ["-y", "-loglevel", "error", "-framerate", String(FPS), "-i", path.join(dir, "f%05d.jpg"), "-i", wav,
    "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
    "-movflags", "+faststart", "-shortest", out], { stdio: "inherit" });
  fs.rmSync(dir, { recursive: true, force: true });
  console.log("wrote " + out);
})();
