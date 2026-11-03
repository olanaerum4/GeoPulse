"""Synthesises simple sound effects (tick, ding, whoosh) at given times into a WAV."""
import sys, json, wave
import numpy as np
out, dur, evs = sys.argv[1], float(sys.argv[2]), json.loads(sys.argv[3])
SR = 44100
track = np.zeros(int(SR * (dur + 1)))
def env(n, a=.004, d=8.0):
    t = np.arange(n) / SR
    return np.minimum(1, t / a) * np.exp(-d * t)
def tick():
    n = int(.09 * SR); t = np.arange(n) / SR
    return .5 * np.sin(2 * np.pi * 1250 * t) * env(n, .002, 45)
def ding():
    n = int(1.1 * SR); t = np.arange(n) / SR
    s = sum(a * np.sin(2 * np.pi * f * t) for f, a in [(880, .5), (1320, .3), (1760, .15), (2640, .08)])
    up = np.where(t > .09, 1.0, 0.0)  # second note a fifth higher: "ding-ding"
    s2 = sum(a * np.sin(2 * np.pi * f * 1.5 * t) for f, a in [(880, .45), (1320, .25), (1760, .1)])
    return .55 * (s * (1 - up) + s2 * up) * env(n, .003, 4.5)
def whoosh():
    n = int(.45 * SR); t = np.arange(n) / SR
    noise = np.random.default_rng(1).standard_normal(n)
    k = np.ones(40) / 40; noise = np.convolve(noise, k, "same")  # low-pass
    shape = np.sin(np.pi * t / t[-1]) ** 2
    return .9 * noise * shape
def kick():
    n = int(.35 * SR); t = np.arange(n) / SR
    f = 50 + 110 * np.exp(-t * 28)                      # pitch drop 160 -> 50 Hz
    return 1.0 * np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, .001, 9)
def hat():
    n = int(.05 * SR)
    x = np.random.default_rng(7).standard_normal(n); x = x - np.convolve(x, np.ones(6) / 6, "same")  # high-pass
    return .35 * x * env(n, .0005, 70)
def riser():
    n = int(1.0 * SR); t = np.arange(n) / SR
    x = np.random.default_rng(3).standard_normal(n)
    out = np.zeros(n); w = 60
    for i in range(0, n, 2205):                          # opening filter: less smoothing over time
        k = max(2, int(w * (1 - i / n)))
        seg = x[i:i + 2205]; out[i:i + 2205] = np.convolve(seg, np.ones(k) / k, "same")
    tone = np.sin(2 * np.pi * np.cumsum(200 + 900 * t ** 2) / SR) * .25
    return (out * 2.5 + tone) * (t / t[-1]) ** 2 * .7
def hit():
    k = kick(); n = int(.9 * SR)
    x = np.random.default_rng(5).standard_normal(n) * env(n, .001, 5) * .45
    out = x.copy(); out[:len(k)] += k * 1.2
    return out
FX = {"tick": tick(), "ding": ding(), "whoosh": whoosh(), "kick": kick(), "hat": hat(), "riser": riser(), "hit": hit()}
for e in evs:
    s = FX[e["s"]] * e.get("v", 1.0); i = int(e["t"] * SR)
    track[i:i + len(s)] += s[:len(track) - i]
track = track[:int(SR * dur)]
track = np.clip(track / max(1e-9, np.abs(track).max()) * .8, -1, 1)
with wave.open(out, "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((track * 32767).astype("<i2").tobytes())
