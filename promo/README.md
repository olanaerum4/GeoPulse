# GeoPulse promo videos

Generates vertical 1080×1920 quiz videos (TikTok / Reels / Shorts) with a hook, 3 questions with a 3-2-1 countdown and reveal, and an outro. Sound effects (ticks, ding, whoosh) are synthesised, so there are no music rights to worry about. Add a trending sound in the TikTok app if you like.

```bash
node promo/render.js                                   # default video (McDonald's / islands / tea)
node promo/render.js promo/example-europe.json out.mp4 # your own questions
```

Requirements: Node with Playwright (Chromium), ffmpeg, python3 with numpy.

To make a new video, copy `example-europe.json` and change the texts and numbers. `a` is the top card and `b` the bottom card. The higher value wins; add `"lower": true` to a question to make the lower value win. Use `<u>…</u>` to highlight a word and `<b>…</b>` in facts.

Preview in a browser: open `promo/video.html` and run `render(5)` in the console to see the frame at 5 seconds.
