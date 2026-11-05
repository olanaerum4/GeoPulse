"""Generates GeoWawe's content pages: fact articles, facts index, how to play, about, privacy.

Run from the repo root:  python3 tools/build_pages.py
Edit the text below and re-run; pages are written as folder/index.html for clean URLs.
"""
import html, json, os

SITE = "https://geowawe.org"
UPDATED = "November 2026"


def page(path, title, desc, body, active="", schema=None):
    depth = path.count("/")
    up = "../" * depth
    nav = [("facts/", "Facts"), ("how-to-play/", "How to play"), ("about/", "About")]
    navh = "".join(f'<a href="{up}{h}"{" aria-current=\"page\"" if active == h else ""}>{t}</a>' for h, t in nav)
    ld = f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>' if schema else ""
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{SITE}/{path}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="article">
<meta property="og:url" content="{SITE}/{path}">
<meta name="theme-color" content="#0b1020">
<link rel="icon" href="{up}icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{up}apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@500;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}site.css">
<script data-goatcounter="https://geowawe.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>
{ld}
</head>
<body><div class="wrap">
<header class="site"><a class="brand" href="{up}"><img src="{up}icon.svg" alt="">GeoWawe</a>
<nav class="top">{navh}<a class="play" href="{up}">▶ Play</a></nav></header>
<main>
{body}
</main>
<footer class="site"><a href="{up}">Play GeoWawe</a><a href="{up}facts/">Facts</a><a href="{up}how-to-play/">How to play</a><a href="{up}about/">About</a><a href="{up}privacy/">Privacy</a><span>© 2026 GeoWawe</span></footer>
</div></body></html>
"""
    os.makedirs(os.path.dirname(path + "index.html") or ".", exist_ok=True)
    with open(path + "index.html", "w", encoding="utf-8") as f:
        f.write(doc)


# ---------------------------------------------------------------- fact articles
# rank rows: (flag, country, value text, paragraph)
ARTICLES = [
 dict(slug="countries-with-the-most-islands", emoji="🏝️", play="ff",
  title="The 5 countries with the most islands", short="Most islands",
  desc="Sweden, not Indonesia or the Philippines, has the most islands in the world. Here are the five countries with the most islands and why the Nordics dominate.",
  intro="Ask people which country has the most islands and most will guess Indonesia or the Philippines. The real answer is much colder: the top three are all in the Nordics.",
  rows=[("🇸🇪","Sweden","≈267,570 islands","Statistics Sweden counted 267,570 islands, including tiny rocky skerries along the Baltic coast and in its many lakes. Fewer than about 1,000 of them have permanent residents."),
        ("🇳🇴","Norway","≈239,000 islands","Norway's long, fjord-cut coastline is lined with islands, from the Lofoten archipelago to the far north. The Norwegian Mapping Authority's count is just over 239,000."),
        ("🇫🇮","Finland","≈179,000 islands","Many of Finland's islands sit inside its lakes. The country is often called the land of a thousand lakes, but the real number of lakes is closer to 188,000."),
        ("🇨🇦","Canada","≈52,000 islands","Canada's Arctic archipelago includes some of the largest islands on Earth, such as Baffin Island, Victoria Island and Ellesmere Island."),
        ("🇺🇸","United States","≈18,600 islands","From Alaska's Aleutian chain to Hawaii and the Florida Keys, the US has thousands of islands spread across two oceans.")],
  extra=("Why do the counts vary so much?","There is no single definition of an island. Some surveys count every rock that sticks out of the water, others only count islands above a certain size. Countries with detailed national surveys, like Sweden and Norway, end up with enormous numbers. Indonesia is usually listed with around 17,000 islands, and it has far more <em>inhabited</em> islands than Sweden."),
  sources="Statistics Sweden; Norwegian Mapping Authority (Kartverket); national surveys. Figures are rounded and definitions differ between countries."),
 dict(slug="countries-with-the-most-time-zones", emoji="🕰️", play="tt",
  title="The 5 countries with the most time zones", short="Most time zones",
  desc="France has more time zones than Russia. See the five countries with the most time zones and how overseas territories change the ranking.",
  intro="Russia is the biggest country on Earth, so it must have the most time zones, right? Not quite. Once overseas territories are counted, France takes first place.",
  rows=[("🇫🇷","France","12 time zones","Thanks to territories in the Caribbean, the Indian Ocean and the Pacific, such as Guadeloupe, Réunion and French Polynesia, France spans 12 time zones. Counting its claim in Antarctica, it is 13."),
        ("🇷🇺","Russia","11 time zones","Russia has the most time zones in one connected piece of land. When it is evening in Kaliningrad, it is already the next morning in Kamchatka."),
        ("🇺🇸","United States","11 time zones","The 50 states use six time zones. Territories such as Guam, Puerto Rico and American Samoa add five more."),
        ("🇬🇧","United Kingdom","9 time zones","Britain itself uses just one time zone, but its overseas territories, from the Falkland Islands to Pitcairn, stretch across the globe."),
        ("🇦🇺","Australia","9 time zones","Mainland Australia has three main time zones, and several of them shift by 30 minutes rather than a full hour. External territories bring the total higher.")],
  extra=("The opposite extreme: China","China is about as wide as the contiguous United States, which would naturally span around five time zones. Yet the whole country officially runs on Beijing time. In the far west, the sun can rise as late as 10 in the morning."),
  sources="Counts include overseas territories and dependencies; sources differ slightly depending on what is counted."),
 dict(slug="largest-countries-by-area", emoji="🗺️", play="hl",
  title="The 5 largest countries in the world by area", short="Biggest countries",
  desc="Russia, Canada, the USA, China and Brazil are the five largest countries on Earth. Here is how big they really are, and why the US vs China ranking is tricky.",
  intro="Five countries together cover close to a third of all the land on Earth. Some of the comparisons between them are closer than most people expect.",
  rows=[("🇷🇺","Russia","≈17.1 million km²","Russia covers roughly an eighth of the world's land area. Its surface is larger than that of the dwarf planet Pluto."),
        ("🇨🇦","Canada","≈10.0 million km²","Canada is the second-largest country and has more lakes than any other country."),
        ("🇺🇸","United States","≈9.8 million km²","Whether the US or China comes third depends on how coastal and inland water is counted. Including water areas, the US is usually ranked ahead."),
        ("🇨🇳","China","≈9.6 million km²","China's land area alone is slightly larger than that of the US, which is why some lists swap places three and four."),
        ("🇧🇷","Brazil","≈8.5 million km²","Brazil is bigger than the contiguous United States and takes up almost half of South America.")],
  extra=("Why maps fool us","The common Mercator map makes countries near the poles look far bigger than they are. Greenland looks as large as Africa on many maps, but Africa is about 14 times larger. Russia and Canada look enormous on maps too, and they really are huge, though not as huge as Mercator suggests."),
  sources="Total area figures as commonly reported (UN, CIA World Factbook). Rounded."),
 dict(slug="most-populous-countries", emoji="👥", play="hl",
  title="The 5 most populous countries in the world", short="Most people",
  desc="India overtook China as the world's most populous country. These are the five countries with the most people in 2024, and where the world is heading.",
  intro="For centuries China was the most populous country on Earth. That changed in 2023, when India took the top spot according to UN estimates.",
  rows=[("🇮🇳","India","≈1.45 billion","India passed China in 2023 and is still growing, although more slowly than before."),
        ("🇨🇳","China","≈1.41 billion","China's population started to shrink in 2022, the first decline in decades."),
        ("🇺🇸","United States","≈340 million","The US is the third most populous country, with growth driven largely by immigration."),
        ("🇮🇩","Indonesia","≈283 million","Spread across thousands of islands, Indonesia is the world's most populous Muslim-majority country."),
        ("🇵🇰","Pakistan","≈251 million","Pakistan has one of the fastest-growing large populations and a very young median age.")],
  extra=("The country to watch: Nigeria","Nigeria is sixth with around 230 million people. It is growing fast and is projected to become one of the most populous countries in the world later this century."),
  sources="UN World Population Prospects 2024 estimates. Rounded."),
 dict(slug="countries-that-drink-the-most-coffee", emoji="☕", play="ff",
  title="The 5 countries that drink the most coffee per person", short="Most coffee",
  desc="Italy and Brazil are famous for coffee, but the Nordic countries drink the most per person. Here are the top five coffee-drinking countries.",
  intro="Espresso is Italian and most coffee is grown in Brazil, but per person, the biggest coffee drinkers live in the far north of Europe.",
  rows=[("🇫🇮","Finland","≈12 kg per person/year","Finns are the world's biggest coffee drinkers. Coffee breaks are a fixed part of the working day, and many workplaces have them written into their agreements."),
        ("🇳🇴","Norway","≈9.9 kg","Norwegians drink filter coffee from morning to evening, often black and often in large mugs."),
        ("🇮🇸","Iceland","≈9 kg","Long, dark winters may help explain why Iceland's coffee culture is so strong."),
        ("🇩🇰","Denmark","≈8.7 kg","Coffee is central to Danish <em>hygge</em>, the idea of cosy time together."),
        ("🇳🇱","Netherlands","≈8.4 kg","The Dutch were among the first to bring coffee to Europe in the 1600s through their trading empire.")],
  extra=("What about Italy and the US?","Italians drink lots of small espressos, which use less coffee per cup. Per person they consume roughly half as much as Finns. Americans drink around 4 to 5 kg per person per year."),
  sources="Often-cited per-capita estimates based on International Coffee Organization data. Figures differ between sources and years."),
 dict(slug="countries-that-drink-the-most-tea", emoji="🍵", play="ff",
  title="The 5 countries that drink the most tea per person", short="Most tea",
  desc="Britain is famous for tea, but Türkiye drinks the most per person. Here are the five biggest tea-drinking countries.",
  intro="Afternoon tea is a British icon, but the UK is only third. The world's biggest tea drinkers per person live in Türkiye.",
  rows=[("🇹🇷","Türkiye","≈3.2 kg per person/year","Strong black tea served in small tulip-shaped glasses is offered everywhere, from homes to shops. Most of it is grown along the Black Sea coast."),
        ("🇮🇪","Ireland","≈2.2 kg","The Irish drink more tea per person than the British, usually strong and with milk."),
        ("🇬🇧","United Kingdom","≈1.9 kg","Tea is still the UK's national drink, even if coffee has been catching up."),
        ("🇮🇷","Iran","≈1.5 kg","Tea is served with almost every social occasion in Iran, often with sugar cubes held between the teeth."),
        ("🇷🇺","Russia","≈1.4 kg","Russian tea culture is built around the samovar, a large heated urn for boiling water.")],
  extra=("Growers vs drinkers","China and India produce most of the world's tea and drink huge amounts in total. Because their populations are so large, however, they rank lower per person."),
  sources="Often-cited per-capita estimates. Figures differ between sources and years."),
 dict(slug="most-visited-countries", emoji="🧳", play="tt",
  title="The 5 most visited countries in the world", short="Most visited",
  desc="France welcomes around 100 million international tourists a year, more than any other country. See the five most visited countries.",
  intro="Paris, Barcelona, New York, Rome and Istanbul all pull in huge crowds. These are the countries that welcome the most international visitors.",
  rows=[("🇫🇷","France","≈100 million visitors","France has been the world's most visited country for decades. It receives more foreign visitors each year than it has residents."),
        ("🇪🇸","Spain","≈85 million","Spain's beaches, islands and cities attract almost twice as many visitors as the country has inhabitants."),
        ("🇺🇸","United States","≈66 million","The US earns more money from tourism than any other country, even though it gets fewer visitors than France."),
        ("🇮🇹","Italy","≈57 million","Italy has some of the most visited cities on Earth, including Rome, Venice and Florence."),
        ("🇹🇷","Türkiye","≈55 million","Türkiye has grown quickly as a destination, with Istanbul and the Mediterranean coast leading the way.")],
  extra=("How tourists are counted","These numbers count international arrivals, so one person visiting twice counts twice, and travellers crossing a border for a day trip may also be included."),
  sources="UN Tourism (UNWTO) international arrival figures for 2023. Rounded."),
 dict(slug="countries-with-the-tallest-men", emoji="📏", play="ff",
  title="The 5 countries with the tallest men", short="Tallest men",
  desc="Dutch men are the tallest in the world, but number two surprises most people. Here are the five countries with the tallest men.",
  intro="The Netherlands is famous for its tall people, but the rest of the top five includes a few countries most people would never guess.",
  rows=[("🇳🇱","Netherlands","≈183.8 cm","Dutch men grew around 20 cm taller in about 150 years, thanks to better nutrition and health."),
        ("🇲🇪","Montenegro","≈183.3 cm","This small Balkan country on the Adriatic coast is almost level with the Netherlands."),
        ("🇪🇪","Estonia","≈182.8 cm","Estonia and its Baltic neighbours rank among the tallest nations in Europe."),
        ("🇧🇦","Bosnia and Herzegovina","≈182.5 cm","The Dinaric Alps region of the Balkans is known for some of the tallest people in the world."),
        ("🇮🇸","Iceland","≈182.1 cm","Iceland completes a top five dominated by Europe.")],
  extra=("Why are some countries taller?","Genes play a role, but height also depends on childhood nutrition, health care and living conditions. That is why average heights in many countries rose sharply during the 20th century."),
  sources="NCD Risk Factor Collaboration (NCD-RisC), average height of 19-year-old men, 2019. Rounded."),
 dict(slug="countries-with-the-longest-coastline", emoji="🌊", play="hl",
  title="The 5 countries with the longest coastline", short="Longest coastline",
  desc="Canada's coastline is over 200,000 km long, enough to wrap around the Earth about five times. See the five countries with the longest coastlines.",
  intro="One country completely dominates this list. Canada's coastline is longer than the next four countries' coastlines combined.",
  rows=[("🇨🇦","Canada","≈202,080 km","Canada borders three oceans, and its Arctic islands add a huge amount of shoreline. The total could wrap around the Earth about five times."),
        ("🇮🇩","Indonesia","≈54,716 km","With thousands of islands, Indonesia has the longest coastline in Asia."),
        ("🇷🇺","Russia","≈37,653 km","Much of Russia's coast faces the Arctic Ocean and is frozen for a large part of the year."),
        ("🇵🇭","Philippines","≈36,289 km","More than 7,000 islands give the Philippines an enormous coastline for its size."),
        ("🇯🇵","Japan","≈29,751 km","Japan's four main islands and thousands of smaller ones are surrounded by coast.")],
  extra=("The coastline paradox","The length of a coastline depends on how closely you measure it. The smaller your ruler, the more twists and inlets you capture, and the longer the coast becomes. That is why Norway's coast is listed at around 25,000 km by the CIA, but at over 100,000 km by a detailed Norwegian measurement that includes every island."),
  sources="CIA World Factbook coastline figures. Other measurement methods give different results."),
 dict(slug="countries-with-the-most-starbucks", emoji="☕", play="ff",
  title="The 5 countries with the most Starbucks stores", short="Most Starbucks",
  desc="South Korea has more Starbucks stores than Japan, and Australia famously rejected the chain. See the five countries with the most Starbucks.",
  intro="Starbucks has tens of thousands of stores worldwide, but they are spread very unevenly. Number three surprises most people.",
  rows=[("🇺🇸","United States","≈16,500 stores","The US has more Starbucks stores than the next four countries on this list combined."),
        ("🇨🇳","China","≈7,600 stores","China is Starbucks' fastest-growing big market, with thousands of stores opened in about a decade."),
        ("🇰🇷","South Korea","≈2,000 stores","South Korea has one of the highest numbers of Starbucks stores per person in the world, especially around Seoul."),
        ("🇯🇵","Japan","≈1,900 stores","Japan was Starbucks' first market outside North America, in 1996."),
        ("🇨🇦","Canada","≈1,450 stores","Canada has a large Starbucks presence, even alongside its own coffee chains.")],
  extra=("Where Starbucks struggled","In 2008 Starbucks closed most of its stores in Australia, where people preferred local cafés and their flat whites. In Italy, the home of espresso, the first Starbucks only opened in 2018."),
  sources="Starbucks store counts as reported around 2024. Rounded."),
]


def article(a):
    rows = "".join(
        f'<li><div class="hd"><span class="no">#{i+1}</span><span class="fl">{f}</span><span class="nm">{n}</span><span class="val">{v}</span></div><p>{p}</p></li>'
        for i, (f, n, v, p) in enumerate(a["rows"]))
    others = [o for o in ARTICLES if o is not a][:3]
    rel = "".join(f'<a href="../{o["slug"]}/"><span class="e">{o["emoji"]}</span><b>{o["short"]}</b><span>{o["desc"][:70]}…</span></a>' for o in others)
    h, t = a["extra"]
    body = f"""<div class="crumbs"><a href="../../">GeoWawe</a> › <a href="../">Facts</a></div>
<h1>{a["emoji"]} {a["title"]}</h1>
<p class="meta">Updated {UPDATED} · 3 min read</p>
<p class="lead">{a["intro"]}</p>
<h2>The top 5</h2>
<ol class="rank">{rows}</ol>
<div class="box"><h2>{h}</h2><p>{t}</p></div>
<div class="cta"><h2>Think you'd have guessed it?</h2><p>Test your instincts with hundreds of country comparisons in GeoWawe. Free, no sign-up.</p><a class="btn" href="../../?play={a["play"]}">▶ Play now</a></div>
<p class="src"><b>Sources:</b> {a["sources"]}</p>
<h2>More facts</h2><div class="cards">{rel}</div>"""
    schema = {"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "description": a["desc"],
              "dateModified": "2026-11-05", "author": {"@type": "Organization", "name": "GeoWawe"},
              "publisher": {"@type": "Organization", "name": "GeoWawe"}, "mainEntityOfPage": f"{SITE}/facts/{a['slug']}/"}
    page(f"facts/{a['slug']}/", f"{a['title']} | GeoWawe", a["desc"], body, "facts/", schema)


for a in ARTICLES:
    article(a)

cards = "".join(f'<a href="{a["slug"]}/"><span class="e">{a["emoji"]}</span><b>{a["title"]}</b><span>{a["desc"][:90]}…</span></a>' for a in ARTICLES)
page("facts/", "Geography facts: surprising country rankings | GeoWawe",
     "Surprising geography facts and country rankings: most islands, time zones, coffee, tea, tourists, coastlines and more.",
     f"""<div class="crumbs"><a href="../">GeoWawe</a> › Facts</div>
<h1>🌍 Geography facts</h1>
<p class="lead">Short, surprising country rankings, the same kind of facts you'll meet in the game. Most people guess at least one of these wrong.</p>
<div class="cards">{cards}</div>
<div class="cta"><h2>Put your knowledge to the test</h2><p>Higher or lower? This or that? Guess the flag? One wrong answer ends your streak.</p><a class="btn" href="../">▶ Play GeoWawe</a></div>""", "facts/")

# ---------------------------------------------------------------- how to play
page("how-to-play/", "How to play GeoWawe: rules, modes and tips",
     "How to play GeoWawe, the free geography game: the four game modes, levels, timer, keyboard shortcuts and tips for long streaks.",
     """<div class="crumbs"><a href="../">GeoWawe</a> › How to play</div>
<h1>🎮 How to play GeoWawe</h1>
<p class="lead">GeoWawe is a fast geography game about comparing countries. Answer correctly to build a streak. One wrong answer and the game is over.</p>
<h2>The four game modes</h2>
<h3>⬆⬇ Higher or Lower</h3>
<p>You see one country's value, for example its population. Guess whether the next country's value is <b>higher or lower</b>. If you're right, the second country becomes the first one in the next round, so the chain keeps going.</p>
<h3>🍔 Fun Facts</h3>
<p>Quirky comparisons such as "Where are there more McDonald's?", "Who drinks more coffee?" or "Where are there more metal bands per person?". Tap the country you think wins. Watch out: sometimes the question asks for <b>fewer</b> or <b>less</b>.</p>
<h3>⚔️ This or That</h3>
<p>Two countries and one category. Tap the one with the higher value. From level 3, some questions ask for the <b>lower</b> value instead.</p>
<h3>🚩 Flag Quiz</h3>
<p>One flag, four countries. Pick the right one. From level 3, the wrong answers come from the same region, so you can't rely on the continent alone.</p>
<h2>Levels and the timer</h2>
<p>Every 5 correct answers takes you up a level. Each level gives you less time and closer comparisons.</p>
<table><tr><th>Level</th><th>Name</th><th>Time per question</th></tr>
<tr><td>1</td><td>Rookie</td><td>18 s</td></tr><tr><td>2</td><td>Explorer</td><td>16 s</td></tr><tr><td>3</td><td>Navigator</td><td>14 s</td></tr>
<tr><td>4</td><td>Cartographer</td><td>12 s</td></tr><tr><td>5</td><td>Geo Master</td><td>10 s</td></tr><tr><td>6</td><td>Legend</td><td>8 s</td></tr></table>
<p>Flag Quiz gives you 4 seconds less per question (minimum 6 seconds).</p>
<p>Levels 1 and 2 use around 50 well-known countries. From level 3, all 194 independent countries can appear. The timer pauses automatically if you switch tabs or apps.</p>
<h2>Categories</h2>
<p>Population, land area, population density, life expectancy, median age, GDP per person, coastline, CO₂ per person, number of neighbouring countries, and fun facts such as McDonald's, Starbucks, coffee, beer, chocolate, tea, pasta, Nobel Prizes, islands, average height, UNESCO World Heritage Sites, billionaires, tourists and heavy metal bands.</p>
<h2>Keyboard shortcuts</h2>
<ul><li><kbd>↑</kbd> / <kbd>↓</kbd>: Higher / Lower</li><li><kbd>←</kbd> / <kbd>→</kbd>: left / right country in This or That and Fun Facts</li><li><kbd>1</kbd>–<kbd>4</kbd>: answers in Flag Quiz</li><li><kbd>Enter</kbd>: play again · <kbd>Esc</kbd>: back to home</li></ul>
<h2>Tips for long streaks</h2>
<ul><li><b>Think about size first.</b> Big populations usually mean more McDonald's, more billionaires and more tourists, but not always.</li>
<li><b>Per person changes everything.</b> Small rich countries often win "per person" categories, such as coffee in Finland.</li>
<li><b>Watch the question.</b> "More" and "fewer" questions are mixed in at higher levels.</li>
<li><b>Read the fact after each answer.</b> The same countries come back, and the facts help next time.</li></ul>
<h2>FAQ</h2>
<h3>Is GeoWawe free?</h3><p>Yes. There is no sign-up and no download. It runs in your browser on phones, tablets and computers.</p>
<h3>Can I install it as an app?</h3><p>Yes. On iPhone, tap Share → Add to Home Screen. On Android, choose Install app from the browser menu. It then opens full screen and also works offline.</p>
<h3>Where does the data come from?</h3><p>Country data comes from public sources such as the UN, the World Bank, the CIA World Factbook and REST Countries. Fun-fact figures are rounded estimates from recent public figures. See <a href="../about/">About</a> for details.</p>
<div class="cta"><h2>Ready?</h2><p>Start with Higher or Lower, the classic mode.</p><a class="btn" href="../?play=hl">▶ Play now</a></div>""", "how-to-play/")

# ---------------------------------------------------------------- about
page("about/", "About GeoWawe",
     "GeoWawe is a free geography game that tests how well you really know the world, made by an independent creator. Learn about the game and its data sources.",
     """<div class="crumbs"><a href="../">GeoWawe</a> › About</div>
<h1>🌊 About GeoWawe</h1>
<p class="lead">GeoWawe is a free, fast geography game that tests how well you really know the world, and usually shows you that the world is stranger than you think.</p>
<h2>Why GeoWawe?</h2>
<p>Most geography quizzes ask you to memorise capitals. GeoWawe asks something more fun: <b>which is bigger?</b> Which country has more people, more islands, more coffee drinkers or more McDonald's? It turns out our instincts are often wrong. Sweden has more islands than Indonesia, France has more time zones than Russia, and Finland drinks twice as much coffee per person as Italy.</p>
<p>Every answer comes with a short fact, so you learn something whether you win or lose.</p>
<h2>Who makes it?</h2>
<p>GeoWawe is an independent project. It has no investors and no sign-up, and it is built to work well on phones. New categories, facts and game modes are added regularly, often based on ideas from players.</p>
<h2>Where the data comes from</h2>
<ul><li><b>Countries, capitals, regions, area and borders:</b> REST Countries and the open <em>world-countries</em> dataset.</li>
<li><b>Population:</b> UN World Population Prospects 2024 estimates for major countries; older figures adjusted for growth for smaller countries.</li>
<li><b>Life expectancy, GDP, CO₂ and similar:</b> rounded figures from the UN, World Bank and similar public sources.</li>
<li><b>Fun facts</b> (McDonald's, coffee, islands and so on): rounded estimates from recent public figures, company reports and national statistics.</li>
<li><b>Flags:</b> flag images from flagcdn.com.</li></ul>
<p>Numbers are rounded and sources sometimes disagree. If you spot something that looks wrong, please let us know and we'll check it.</p>
<h2>Contact</h2>
<p>Ideas, corrections or feedback are welcome: <a href="https://github.com/olanaerum4/GeoPulse/issues">open an issue on GitHub</a>.</p>
<div class="cta"><h2>How well do you know the world?</h2><a class="btn" href="../">▶ Play GeoWawe</a></div>""", "about/")

# ---------------------------------------------------------------- privacy
page("privacy/", "Privacy policy | GeoWawe",
     "GeoWawe's privacy policy: what data the game stores and which third-party services it uses.",
     """<div class="crumbs"><a href="../">GeoWawe</a> › Privacy</div>
<h1>Privacy policy</h1>
<p class="meta">Last updated: 5 November 2026</p>
<p>GeoWawe is designed to collect as little data as possible. You don't need an account, and we don't ask for your name or email.</p>
<h2>Data stored on your device</h2>
<p>The game uses your browser's local storage to remember your <b>best scores</b>, your <b>theme choice</b> (light/dark) and a temporary copy of country data so the game loads faster. This data stays on your device and is never sent to us. You can delete it at any time by clearing your browser's site data.</p>
<h2>Visitor statistics</h2>
<p>We use <a href="https://www.goatcounter.com">GoatCounter</a> to count visits and game events (for example "game started" or "score 5–9"). GoatCounter does <b>not use cookies</b>, does not track you across websites and does not store personal data. It records aggregated information such as page, referring website, browser, screen size and approximate country. Our hosting provider (Netlify) also keeps standard server logs.</p>
<h2>Third-party services</h2>
<p>To show the game, your browser loads resources from:</p>
<ul><li><b>Google Fonts</b> (fonts.googleapis.com, fonts.gstatic.com) for the typeface,</li><li><b>flagcdn.com</b> for flag images,</li><li><b>restcountries.com</b> for country data,</li><li><b>gc.zgo.at</b> for the GoatCounter script.</li></ul>
<p>These services receive your IP address when your browser connects to them, as with any website, and handle it under their own privacy policies.</p>
<h2>Advertising</h2>
<p>GeoWawe does not currently show advertising. If ads are added in the future, this policy will be updated, and where required you will be asked for consent before any advertising cookies are used.</p>
<h2>Children</h2>
<p>GeoWawe is a general-audience game and does not knowingly collect personal information from anyone, including children.</p>
<h2>Contact</h2>
<p>Questions about privacy: <a href="https://github.com/olanaerum4/GeoPulse/issues">open an issue on GitHub</a>.</p>""")

# ---------------------------------------------------------------- sitemap
urls = ["", "facts/", "how-to-play/", "about/", "privacy/"] + [f"facts/{a['slug']}/" for a in ARTICLES]
with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for u in urls:
        f.write(f"  <url><loc>{SITE}/{u}</loc><lastmod>2026-11-05</lastmod></url>\n")
    f.write("</urlset>\n")
print(f"wrote {len(ARTICLES)} articles + facts index, how-to-play, about, privacy, sitemap ({len(urls)} urls)")
