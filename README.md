# 🌍 GeoPulse

A fast geography game in a single HTML file. Compare countries on population, area, wealth, borders, time zones and more, or guess the flag.

## Modes
- **⬆⬇ Higher or Lower**: is the next country's value higher or lower?
- **⚔️ This or That**: pick the country with the higher (or lower) value.
- **🚩 Flag Quiz**: pick the right country for the flag, from four options.

You level up every 5 correct answers. The timer gets shorter, and from level 3 the whole world joins in.

## Data
Country data (population, area, borders, time zones, flags, capitals and regions) is loaded live from [REST Countries](https://restcountries.com) and cached for 24 hours. If the API is unreachable, the game falls back to built-in data for 50 countries. The menu shows which source is in use.

The API key is set in the `RC` object at the top of the script in `index.html`. Because it runs in the browser, anyone can see the key.

## Run
Open `index.html` in a browser, or enable GitHub Pages (Settings → Pages → Deploy from branch `main`, root).

## Controls
↑ ↓ Higher/Lower · ← → This or That · 1–4 Flag Quiz · Enter play again · Esc menu
