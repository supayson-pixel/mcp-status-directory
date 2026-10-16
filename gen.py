import json, os
S="https://mcp-status-directory.netlify.app"
DATA=json.load(open("data/servers.json")); srv=DATA["servers"]
CHECKED=DATA["checked_at"]; CD=CHECKED[:10]; CT=CHECKED[:10]+" "+CHECKED[11:16]+" UTC"
CHG=json.load(open("data/changes.json")) if os.path.exists("data/changes.json") else []
os.makedirs("category",exist_ok=True)
PL={"<=30d":"≤30d","30-90d":"30–90d","90-365d":"90–365d",">365d":"&gt;1 year"}
CL={"Healthy":"h","Stale":"s","Archived":"a","Broken":"a"}
CATS=[("browser","Browser &amp; scraping"),("devtools","Dev tools &amp; git"),("databases","Databases"),("files","Files &amp; office"),("search","Search"),("cloud","Cloud &amp; infra"),("productivity","Productivity"),("ai","AI &amp; memory"),("other","Other")]
slug=lambda r:r.lower().replace("/","-")
NAV='<header><a class="logo" href="/">● MCP Status</a><nav><a href="/">Ranking</a><a href="/compare/">Compare</a><a href="/status.html">Status</a><a href="/methodology.html">Methodology</a><a href="/submit.html">Submit</a></nav></header>'
def head(t,d,path,extra=""):
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{t}</title><meta name="description" content="{d}"><link rel="canonical" href="{S}{path}"><meta property="og:type" content="website"><meta property="og:site_name" content="MCP Status"><meta property="og:title" content="{t}"><meta property="og:description" content="{d}"><meta property="og:url" content="{S}{path}"><meta name="twitter:card" content="summary"><link rel="stylesheet" href="/style.css">{extra}</head><body>\n{NAV}<main>\n'
FOOT='</main><footer>MCP Status · data checked '+CT+' from GitHub &amp; npm/PyPI · <a href="/methodology.html">methodology</a> · <a href="/data/servers.json">raw JSON</a> · <a href="/llms.txt">llms.txt</a></footer></body></html>\n'
def badge(s): return f'<span class="b {CL[s["label"]]}">{s["score"]} {s["label"]}</span>'
def note(s): return '<span class="note">⚠ README: “no longer actively maintained” — Notion recommends its hosted Remote Notion MCP.</span>' if "note" in s else ""
def pkg(s):
    p=s["package"]
    if not p: return '<td class="hide-sm mut">unchecked</td>'
    reg,rest=p.split(":",1); v=rest.rsplit("@",1)[1]
    return f'<td class="hide-sm">✔ {"npm" if reg=="npm" else "PyPI"} {v}</td>'
cnt={k:sum(1 for s in srv if s["label"]==k) for k in ["Healthy","Stale","Archived","Broken"]}
ld={"@context":"https://schema.org","@type":"ItemList","name":"Healthiest MCP servers (checked "+CD+")","dateModified":CD,"itemListElement":[{"@type":"ListItem","position":s["rank"],"name":s["repo"],"url":"https://github.com/"+s["repo"]} for s in srv[:10]]}
h=head(f"MCP Status — Health-ranked MCP server directory (checked {CD})",f"{len(srv)} MCP servers ranked by a dated, evidence-based health score: archived flags, last push, package checks, stars. Find the best working MCP server for browsers, databases, search, git and more.","/",'<meta name="google-site-verification" content="vbqu_Pk-7Tv1fBKzvmXXs3_FAA5zaNYAMvvICu8ecUQ" /><script type="application/ld+json">'+json.dumps(ld)+'</script>')
h+=f'<h1>Which MCP servers actually work right now?</h1>\n<p class="lead">{len(srv)} Model Context Protocol servers ranked by a dated, evidence-based health score — repo exists, archived flag, last push, verified npm/PyPI package, and stars. Last check: <b>{CT}</b>. <a href="/methodology.html">How scoring works</a> · <a href="/data/servers.json">raw JSON</a></p>\n'
h+=f'<div class="stats"><div class="stat"><b>{len(srv)}</b>servers</div><div class="stat"><b style="color:var(--h)">{cnt["Healthy"]}</b>Healthy</div><div class="stat"><b style="color:var(--s)">{cnt["Stale"]}</b>Stale</div><div class="stat"><b style="color:var(--a)">{cnt["Archived"]}</b>Archived</div></div>\n<div class="cats">'
h+="".join(f'<a href="/category/{k}.html">{n} ({sum(1 for s in srv if s["category"]==k)})</a>' for k,n in CATS)+'</div>\n'
h+='<table><thead><tr><th>#</th><th>Server</th><th class="hide-sm">Category</th><th>Health</th><th>Stars</th><th class="hide-sm">Last push</th><th class="hide-sm">Package</th></tr></thead><tbody>\n'
for s in srv:
    h+=f'<tr id="{slug(s["repo"])}"><td>{s["rank"]}</td><td><a href="/server/{slug(s["repo"])}.html">{s["repo"]}</a>{note(s)}</td><td class="hide-sm"><a href="/category/{s["category"]}.html">{s["category"]}</a></td><td>{badge(s)}</td><td>{s["stars"]:,}</td><td class="hide-sm">{PL[s["push"]]}</td>{pkg(s)}</tr>\n'
h+='</tbody></table>\n<p class="mut">“unchecked” = package not yet verified against npm/PyPI (scores 0 on that component).</p>\n'
h+='<div class="card" id="newsletter"><h2 style="margin-top:0">Weekly MCP health digest</h2><p class="mut">Which servers broke, got archived, or launched this week. No spam.</p>\n<form name="newsletter" method="POST" data-netlify="true" netlify-honeypot="bot-field" action="/thanks.html"><input type="hidden" name="form-name" value="newsletter"><p hidden><label>Leave empty <input name="bot-field"></label></p><input type="email" name="email" required placeholder="you@example.com"> <button type="submit">Subscribe</button></form></div>\n'
open("index.html","w").write(h+FOOT)
TITLE={"browser":"Best browser automation &amp; scraping MCP servers","devtools":"Best developer tools &amp; git MCP servers","databases":"Best database MCP servers (Postgres, MySQL, vector)","files":"Best file system &amp; Office (Excel, Word) MCP servers","search":"Best web search MCP servers","cloud":"Best cloud &amp; infra MCP servers: AWS, Cloudflare, Kubernetes, Terraform","productivity":"Best productivity MCP servers: Notion, n8n, Slack, Obsidian","ai":"AI, memory &amp; multi-model MCP servers","other":"Other MCP servers: Blender, Unity, Godot, KiCAD, Windows"}
def lead_txt(k):
    ss=[s for s in srv if s["category"]==k]; act=[s for s in ss if s["label"] not in ("Archived","Broken")]
    top=[s for s in act if s["label"]=="Healthy"][:3]
    if top: t=("the healthiest is " if len(top)==1 else "the healthiest are ")+", ".join(f'<b>{s["repo"]}</b> ({s["score"]}'+(", "+("npm" if s["package"].startswith("npm") else "PyPI")+" verified" if s["package"] else "")+")" for s in top)+"."
    elif act: t=f'no server in this category is currently Healthy; the best-scoring is <b>{act[0]["repo"]}</b> ({act[0]["score"]}).'
    else: t="no active servers are tracked in this category."
    w=[s["repo"] for s in top if "note" in s]
    if w: t+=" Note: "+", ".join(w)+" carries a maintenance warning (its README says it is no longer actively maintained)."
    ar=[s["repo"] for s in ss if s["archived"]]
    if ar: t+=" Archived (avoid): "+", ".join(ar)+"."
    return t
LEAD={k:(TITLE[k],lead_txt(k)) for k in TITLE}
def cat_faq(k,n,ss):
    nn=n.replace("&amp;","and"); best=ss[0]; act=[s for s in ss if not s["archived"]]
    arch=[s["repo"] for s in ss if s["archived"]]
    qa=[(f"What is the best {nn} MCP server right now?",f"As of the {CD} check, {best['repo']} has the highest health score in this category ({best['score']}/100, {best['label']})."),
        (f"How many {nn} MCP servers are tracked?",f"{len(ss)} servers: {sum(s['label']=='Healthy' for s in ss)} Healthy, {sum(s['label']=='Stale' for s in ss)} Stale, {len(arch)} Archived."),
        (f"Which {nn} MCP servers are archived?",("Archived on GitHub: "+", ".join(arch)+".") if arch else f"None of the tracked servers in this category are archived as of {CD}."),
        ("How is the health score calculated?","Repo exists 25, not archived 20, last push within 30/90/365 days 25/15/5, verified npm or PyPI package 20, stars up to 10 on a log scale.")]
    ld={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in qa]}
    return '<h2>FAQ</h2>'+"".join(f'<h3>{q}</h3><p>{a}</p>' for q,a in qa)+'<script type="application/ld+json">'+json.dumps(ld)+'</script>\n'
for k,n in CATS:
    t,lead=LEAD[k]; ss=[s for s in srv if s["category"]==k]
    c=head(t+" (Oct 2026, health-ranked)",f"Health-ranked {n.replace('&amp;','and')} MCP servers with dated checks and archived/stale flags.",f"/category/{k}.html")
    c+=f'<h1>{t}</h1><p class="lead"><b>Short answer ({CD}):</b> {lead}</p>\n<table><thead><tr><th>Server</th><th>Health</th><th>Stars</th><th>Last push</th></tr></thead><tbody>\n'
    for s in ss: c+=f'<tr><td><a href="/server/{slug(s["repo"])}.html">{s["repo"]}</a>{note(s)}</td><td>{badge(s)}</td><td>{s["stars"]:,}</td><td>{PL[s["push"]]}</td></tr>\n'
    c+='</tbody></table>\n'+cat_faq(k,n,ss)+'<p><a href="/">← All servers</a></p>\n'
    open(f"category/{k}.html","w").write(c+FOOT)
arch=[s for s in srv if s["archived"]]; old=[s for s in srv if s["push"]==">365d" and not s["archived"]]; gone=[s for s in srv if not s.get("exists",True)]
st=head(f"MCP server status: archived &amp; stale flags ({CD}) — MCP Status","Archived and stale MCP servers flagged from dated GitHub checks.","/status.html")
st+=f'<h1>Status &amp; flags</h1><p class="lead">Check run <b>{CT}</b> · {len(srv)} servers · {cnt["Healthy"]} Healthy · {cnt["Stale"]} Stale · {cnt["Archived"]} Archived · {cnt["Broken"]} Broken. Refreshed daily.</p>\n'
if CHG and CHG[0]["checked_at"]==CHECKED:
    c0=CHG[0]["changes"]; st+='<h2>What changed in this check</h2>'+(f'<p class="mut">{CHG[0]["note"]}</p>' if CHG[0].get("note") else "")+('<ul>'+"".join(f"<li>{x}</li>" for x in c0)+'</ul>\n' if c0 else '<p>No changes since the previous check.</p>\n')
if gone: st+='<h2>Repository not found</h2><ul>'+"".join(f'<li><a href="/server/{slug(s["repo"])}.html">{s["repo"]}</a></li>' for s in gone)+'</ul>\n'
st+='<h2>Archived repositories</h2><ul>'+"".join(f'<li><a href="/server/{slug(s["repo"])}.html">{s["repo"]}</a> — {s["stars"]:,}★</li>' for s in arch)+'</ul>\n'
st+='<h2>Maintenance warnings</h2><ul><li><a href="/server/makenotion-notion-mcp-server.html">makenotion/notion-mcp-server</a> — package README says this self-hosted server is “no longer actively maintained or supported”; Notion recommends its hosted Remote Notion MCP.</li></ul>\n'
st+='<h2>No push in over a year</h2><ul>'+"".join(f'<li><a href="/server/{slug(s["repo"])}.html">{s["repo"]}</a></li>' for s in old)+'</ul>\n'
st+='<h2>Check log</h2><table><thead><tr><th>When (UTC)</th><th>Healthy / Stale / Archived / Broken</th><th>Packages verified</th><th>Changes</th></tr></thead><tbody>'+"".join(f'<tr><td>{c["checked_at"][:16].replace("T"," ")}</td><td>{c["counts"]["Healthy"]} / {c["counts"]["Stale"]} / {c["counts"]["Archived"]} / {c["counts"]["Broken"]}</td><td>{c["packages_verified"]}</td><td>{len(c["changes"])}</td></tr>' for c in CHG)+'<tr><td>2026-10-15 06:50</td><td>28 / 40 / 5 / 0</td><td>6</td><td>first check</td></tr></tbody></table>\n'
open("status.html","w").write(st+FOOT)
faq={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"How is the MCP Status health score calculated?","acceptedAnswer":{"@type":"Answer","text":"Repo exists 25, not archived 20, last push within 30 days 25 (90 days 15, 365 days 5), package verified on npm or PyPI 20, stars up to 10 on a log scale. Healthy is 75+, Stale 40-74, Broken below 40; archived repos are always labelled Archived."}},{"@type":"Question","name":"How often is data refreshed?","acceptedAnswer":{"@type":"Answer","text":"Every listing shows its check date. The first full check ran 2026-10-15 and an automated check refreshes the data every day."}}]}
m=head("How MCP Status scores MCP servers — Methodology","Exact formula behind the MCP Status health score.","/methodology.html",'<script type="application/ld+json">'+json.dumps(faq)+'</script>')
m+='''<h1>Methodology</h1><p class="lead">Every score is computed only from public, verifiable signals. Nothing is estimated; unknown values are shown as “unchecked” and score zero.</p>
<table><thead><tr><th>Signal</th><th>Points</th><th>Source</th></tr></thead><tbody>
<tr><td>Repository exists</td><td>25</td><td>GitHub API</td></tr><tr><td>Not archived</td><td>20</td><td>GitHub <code>archived</code> flag</td></tr>
<tr><td>Last push ≤30 / ≤90 / ≤365 days</td><td>25 / 15 / 5</td><td>GitHub API <code>pushed_at</code></td></tr>
<tr><td>Published package resolves</td><td>20</td><td>registry.npmjs.org or pypi.org; package name taken from the repo’s own package.json / pyproject.toml, and the registry entry must link back to the same GitHub repo</td></tr>
<tr><td>Stars</td><td>0–10</td><td>round(10 × log10(stars) / 5)</td></tr></tbody></table>
<h2>Labels</h2><p><span class="b h">Healthy</span> ≥75 · <span class="b s">Stale</span> 40–74 · <span class="b a">Broken</span> &lt;40 · <span class="b a">Archived</span> whenever GitHub marks the repo archived, regardless of score.</p>
<h2>Known limits</h2><ul><li>Packages are verified for '''+str(sum(1 for s in srv if s["package"]))+' of '+str(len(srv))+''' servers. Monorepos, Go/Docker-only servers and repos without a root package.json / pyproject.toml stay “unchecked”, which caps them at 80.</li><li>Live MCP handshake tests are on the roadmap.</li><li>Maintainer notes (e.g. “no longer maintained” in a README) are flagged manually.</li></ul>
'''
open("methodology.html","w").write(m+FOOT)
sb=head("Submit an MCP server — MCP Status","List your MCP server for free and get a dated health score. Featured and verified tiers coming soon.","/submit.html")
sb+='''<h1>Submit your MCP server</h1><p class="lead">Listings are free. Every server is scored by the same <a href="/methodology.html">public formula</a>; paid tiers never change a score.</p>
<div class="card"><h2 style="margin-top:0">Free listing</h2><p>Open a GitHub issue with your repo URL, package name (npm/PyPI) and category.</p><p><a href="https://github.com/supayson-pixel/mcp-status-directory/issues/new?title=Add+server:+&amp;body=Repo:%0APackage:%0ACategory:"><button>Open submission issue</button></a></p></div>
<div class="card"><h2 style="margin-top:0">Featured listing <span class="mut">— coming soon</span></h2><p>Pinned placement at the top of a category page, clearly marked “Featured”.</p></div>
<div class="card"><h2 style="margin-top:0">Verified badge <span class="mut">— coming soon</span></h2><p>A daily live MCP handshake and tool-list test with a dated ✔ Verified badge for your README.</p></div>
'''
open("submit.html","w").write(sb+FOOT)
open("thanks.html","w").write(head("Subscribed — MCP Status","Subscribed","/thanks.html",'<meta name="robots" content="noindex">')+'<h1>You\'re subscribed.</h1><p class="lead">Thanks! The first weekly MCP health digest is coming soon. <a href="/">Back to the ranking</a></p>\n'+FOOT)
urls=["/","/status.html","/methodology.html","/submit.html"]+[f"/category/{k}.html" for k,_ in CATS]
open("sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"".join(f"<url><loc>{S}{u}</loc><lastmod>{CD}</lastmod></url>\n" for u in urls)+"</urlset>\n")
open("robots.txt","w").write(f"User-agent: *\nAllow: /\n\nSitemap: {S}/sitemap.xml\n")
open("netlify.toml","w").write('[build]\n  publish = "."\n  command = ""\n\n[[headers]]\n  for = "/data/*"\n  [headers.values]\n    Access-Control-Allow-Origin = "*"\n')
open(".gitignore","w").write(".netlify\n")
llm=f"""# MCP Status

> MCP Status ({S}) is a health-ranked directory of Model Context Protocol (MCP) servers. Every listing carries a dated, evidence-based health score (0-100) from public signals: GitHub repo exists, archived flag, last push recency, whether the npm/PyPI package resolves, and stars. Archived and stale servers are flagged explicitly.

Last full check: {CHECKED}. {len(srv)} servers: {cnt['Healthy']} Healthy, {cnt['Stale']} Stale, {cnt['Archived']} Archived.

## Key pages
- [Ranked list of all servers]({S}/)
- [Status / archived & stale flags]({S}/status.html)
- [Methodology]({S}/methodology.html)
- [Raw data JSON]({S}/data/servers.json)

## Best MCP servers by use case (healthiest first, as of {CD})
"""+"".join("- "+n.replace("&amp;","&")+": "+", ".join(s["repo"]+" ("+str(s["score"])+(", README says no longer actively maintained" if "note" in s else "")+")" for s in [x for x in srv if x["category"]==k and x["label"] not in ("Archived","Broken")][:3])+"\n" for k,n in CATS)+"""
## Category pages
"""+"".join(f"- [{n.replace('&amp;','&')}]({S}/category/{k}.html)\n" for k,n in CATS)
open("llms.txt","w").write(llm)
open("README.md","w").write(f"""# MCP Status — health-ranked MCP server directory

Live: {S}

Plain static site (no build step) ranking Model Context Protocol servers by a dated, evidence-based **health score**, flagging archived/stale projects — the gap left by the official MCP Registry, Glama, Smithery, PulseMCP, mcp.so and awesome lists.

## Contents
- `index.html` — all servers ranked by health; anchors `/#owner-repo`
- `category/*.html` — 9 use-case pages
- `status.html`, `methodology.html`, `submit.html`, `thanks.html`
- `data/servers.json` — raw data (CORS open)
- `llms.txt`, `robots.txt`, `sitemap.xml`, JSON-LD — SEO / chatbot discoverability
- Newsletter via Netlify Forms (`data-netlify="true"`)
- `gen.py` — regenerates every page from the data table

## Data (check of {CHECKED})
{len(srv)} servers: {cnt['Healthy']} Healthy, {cnt['Stale']} Stale, {cnt['Archived']} Archived. Sources: GitHub REST API and direct npm/PyPI lookups ({sum(1 for s in srv if s['package'])} packages verified; others marked unchecked). No data is invented.

## Daily refresh
`python3 refresh.py && python3 gen.py` re-checks every server, appends to `data/changes.json`, and regenerates all pages.

## Score (0–100)
Repo exists 25 · not archived 20 · last push ≤30d 25 / ≤90d 15 / ≤365d 5 · verified package 20 · stars round(10·log10(stars)/5). Healthy ≥75, Stale 40–74, Broken <40; archived repos always labelled Archived.
""")
exec(open("gen_seo.py").read())
print(cnt, len(srv))
