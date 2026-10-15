import json, os
S="https://mcp-status-directory.netlify.app"
# repo,cat,stars,archived,push,package,score
D="""ChromeDevTools/chrome-devtools-mcp|browser|53563|0|<=30d|npm:chrome-devtools-mcp@1.10.1|99
microsoft/playwright-mcp|browser|38161|0|<=30d|npm:@playwright/mcp@0.0.83|99
firecrawl/firecrawl-mcp-server|browser|7607|0|<=30d|npm:firecrawl-mcp@3.30.1|98
exa-labs/exa-mcp-server|search|5131|0|<=30d|npm:exa-mcp-server@3.4.2|97
makenotion/notion-mcp-server|productivity|4667|0|<=30d|npm:@notionhq/notion-mcp-server@2.5.2|97
haris-musa/excel-mcp-server|files|4241|0|<=30d|pypi:excel-mcp-server@2.0.0|97
DeusData/codebase-memory-mcp|devtools|46615|0|<=30d||79
github/github-mcp-server|devtools|33626|0|<=30d||79
ahujasid/mcp-for-blender|other|30866|0|<=30d||79
czlonkowski/n8n-mcp|productivity|23074|0|<=30d||79
googleapis/mcp-toolbox|databases|16666|0|<=30d||78
xpzouying/xiaohongshu-mcp|other|16287|0|<=30d||78
GLips/Figma-Context-MCP|devtools|15988|0|<=30d||78
CoplayDev/unity-mcp|other|14963|0|<=30d||78
mrexodia/ida-pro-mcp|devtools|12878|0|<=30d||78
apify/apify-mcp-server|browser|11279|0|<=30d||78
LaurieWired/GhidraMCP|devtools|11272|0|<=30d||78
wonderwhy-er/DesktopCommanderMCP|files|10059|0|<=30d||78
awslabs/mcp|cloud|9781|0|<=30d||78
mobile-next/mobile-mcp|devtools|9439|0|<=30d||78
CursorTouch/Windows-MCP|other|8998|0|<=30d||78
getsentry/MobileBuildMCP|devtools|6480|0|<=30d||78
cloudflare/mcp-server-cloudflare|cloud|4380|0|<=30d||77
stickerdaniel/linkedin-mcp-server|productivity|3876|0|<=30d||77
blazickjp/arxiv-mcp-server|search|3218|0|<=30d||77
Jpisnice/shadcn-ui-mcp-server|devtools|3053|0|<=30d||77
mixelpixx/KiCAD-MCP-Server|other|2696|0|<=30d||77
duty1g/x64dbg-mcp-server|devtools|2506|0|<=30d||77
AgentDeskAI/browser-tools-mcp|browser|7329|0|30-90d||68
grab/cursor-talk-to-figma-mcp|devtools|7054|0|30-90d||68
21st-dev/magic-mcp|devtools|6023|0|30-90d||68
google/mcp|cloud|4642|0|30-90d||67
MarkusPfundstein/mcp-obsidian|productivity|4478|0|30-90d||67
antvis/mcp-server-chart|other|4397|0|30-90d||67
crystaldba/postgres-mcp|databases|3398|0|30-90d||67
zhizhuodemao/js-reverse-mcp|browser|2953|0|30-90d||67
6551Team/opennews-mcp|search|2417|0|30-90d||67
jamubc/gemini-mcp-tool|ai|2289|0|30-90d||67
joshuayoes/ios-simulator-mcp|devtools|2193|0|30-90d||67
benborla/mcp-server-mysql|databases|2162|0|30-90d||67
containers/kubernetes-mcp-server|cloud|2161|0|<=90d*||67
anysearch-ai/anysearch-mcp-server|search|1867|0|<=90d*||67
arabold/docs-mcp-server|devtools|1801|0|<=90d*||67
matlab/matlab-mcp-server|devtools|1664|0|<=90d*||66
mukul975/cve-mcp-server|other|1623|0|<=90d*||66
Flux159/mcp-server-kubernetes|cloud|1596|0|<=90d*||66
qdrant/mcp-server-qdrant|databases|1549|0|<=90d*||66
hashicorp/terraform-mcp-server|cloud|1549|0|<=90d*||66
hangwin/mcp-chrome|browser|12497|0|90-365d||58
tadata-org/fastapi_mcp|devtools|12021|0|90-365d||58
BeehiveInnovations/pal-mcp-server|ai|11783|0|90-365d||58
idosal/git-mcp|devtools|8460|0|90-365d||58
Coding-Solo/godot-mcp|other|6093|0|90-365d||58
executeautomation/mcp-playwright|browser|5666|0|90-365d||58
Pimzino/spec-workflow-mcp|devtools|4303|0|90-365d||57
excalidraw/excalidraw-mcp|other|5522|0|90-365d||57
louislva/claude-peers-mcp|ai|2206|0|90-365d||57
korotovsky/slack-mcp-server|productivity|1866|0|90-365d||57
isaacphi/mcp-language-server|devtools|1609|0|90-365d||56
BrowserMCP/mcp|browser|7185|0|>365d||53
lharries/whatsapp-mcp|productivity|6613|0|>365d||53
financial-datasets/mcp-server|other|2307|0|>365d||52
coleam00/mcp-crawl4ai-rag|ai|2266|0|>365d||52
cjo4m06/mcp-shrimp-task-manager|ai|2147|0|>365d||52
chongdashu/unreal-mcp|other|2096|0|>365d||52
noopstudios/interactive-feedback-mcp|ai|1704|0|>365d||51
leonardsellem/n8n-mcp-server|productivity|1631|0|>365d||51
anaisbetts/mcp-installer|other|1532|0|>365d||51
browserbase/mcp-server-browserbase|browser|3399|1|30-90d||47
PleasePrompto/notebooklm-mcp|ai|3436|1|30-90d||47
GongRzhe/Office-Word-MCP-Server|files|2108|1|90-365d||37
GongRzhe/Office-PowerPoint-MCP-Server|files|1856|1|90-365d||37
supermemoryai/apple-mcp|productivity|3122|1|>365d||32"""
NOTION="Package README states this self-hosted server is no longer actively maintained; Notion recommends its hosted Remote Notion MCP."
srv=[]
for i,l in enumerate(D.split("\n")):
    r,c,st,a,p,pk,sc=l.split("|"); sc=int(sc); a=a=="1"
    lab="Archived" if a else ("Healthy" if sc>=75 else "Stale" if sc>=40 else "Broken")
    d=dict(rank=i+1,repo=r,category=c,stars=int(st),archived=a,push=p,package=pk or None,score=sc,label=lab)
    if r.startswith("makenotion/"): d["note"]=NOTION
    srv.append(d)
os.makedirs("data",exist_ok=True); os.makedirs("category",exist_ok=True)
json.dump({"checked_at":"2026-10-15T06:50:00Z","site":S,"scoring":"repo 25 + not archived 20 + push(<=30d 25,<=90d 15,<=365d 5) + verified package 20 + round(10*log10(stars)/5)","push_note":"push buckets from GitHub search pushed:<date> queries; '<=90d*' = pushed within 90 days, 30-day bucket not verified","servers":srv},open("data/servers.json","w"),indent=1)
PL={"<=30d":"≤30d","30-90d":"30–90d","<=90d*":"≤90d*","90-365d":"90–365d",">365d":"&gt;1 year"}
CL={"Healthy":"h","Stale":"s","Archived":"a","Broken":"a"}
CATS=[("browser","Browser &amp; scraping"),("devtools","Dev tools &amp; git"),("databases","Databases"),("files","Files &amp; office"),("search","Search"),("cloud","Cloud &amp; infra"),("productivity","Productivity"),("ai","AI &amp; memory"),("other","Other")]
slug=lambda r:r.lower().replace("/","-")
NAV='<header><a class="logo" href="/">● MCP Status</a><nav><a href="/">Ranking</a><a href="/compare/">Compare</a><a href="/status.html">Status</a><a href="/methodology.html">Methodology</a><a href="/submit.html">Submit</a></nav></header>'
def head(t,d,path,extra=""):
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{t}</title><meta name="description" content="{d}"><link rel="canonical" href="{S}{path}"><meta property="og:type" content="website"><meta property="og:site_name" content="MCP Status"><meta property="og:title" content="{t}"><meta property="og:description" content="{d}"><meta property="og:url" content="{S}{path}"><meta name="twitter:card" content="summary"><link rel="stylesheet" href="/style.css">{extra}</head><body>\n{NAV}<main>\n'
FOOT='</main><footer>MCP Status · data checked 2026-10-15 06:50 UTC from GitHub &amp; npm/PyPI · <a href="/methodology.html">methodology</a> · <a href="/data/servers.json">raw JSON</a> · <a href="/llms.txt">llms.txt</a></footer></body></html>\n'
def badge(s): return f'<span class="b {CL[s["label"]]}">{s["score"]} {s["label"]}</span>'
def note(s): return '<span class="note">⚠ README: “no longer actively maintained” — Notion recommends its hosted Remote Notion MCP.</span>' if "note" in s else ""
def pkg(s):
    p=s["package"]
    if not p: return '<td class="hide-sm mut">unchecked</td>'
    reg,rest=p.split(":",1); v=rest.rsplit("@",1)[1]
    return f'<td class="hide-sm">✔ {"npm" if reg=="npm" else "PyPI"} {v}</td>'
cnt={k:sum(1 for s in srv if s["label"]==k) for k in ["Healthy","Stale","Archived","Broken"]}
ld={"@context":"https://schema.org","@type":"ItemList","name":"Healthiest MCP servers (checked 2026-10-15)","dateModified":"2026-10-15","itemListElement":[{"@type":"ListItem","position":s["rank"],"name":s["repo"],"url":"https://github.com/"+s["repo"]} for s in srv[:10]]}
h=head("MCP Status — Health-ranked MCP server directory (checked 2026-10-15)","73 MCP servers ranked by a dated, evidence-based health score: archived flags, last push, package checks, stars. Find the best working MCP server for browsers, databases, search, git and more.","/",'<script type="application/ld+json">'+json.dumps(ld)+'</script>')
h+=f'<h1>Which MCP servers actually work right now?</h1>\n<p class="lead">{len(srv)} Model Context Protocol servers ranked by a dated, evidence-based health score — repo exists, archived flag, last push, verified npm/PyPI package, and stars. Last check: <b>2026-10-15 06:50 UTC</b>. <a href="/methodology.html">How scoring works</a> · <a href="/data/servers.json">raw JSON</a></p>\n'
h+=f'<div class="stats"><div class="stat"><b>{len(srv)}</b>servers</div><div class="stat"><b style="color:var(--h)">{cnt["Healthy"]}</b>Healthy</div><div class="stat"><b style="color:var(--s)">{cnt["Stale"]}</b>Stale</div><div class="stat"><b style="color:var(--a)">{cnt["Archived"]}</b>Archived</div></div>\n<div class="cats">'
h+="".join(f'<a href="/category/{k}.html">{n} ({sum(1 for s in srv if s["category"]==k)})</a>' for k,n in CATS)+'</div>\n'
h+='<table><thead><tr><th>#</th><th>Server</th><th class="hide-sm">Category</th><th>Health</th><th>Stars</th><th class="hide-sm">Last push</th><th class="hide-sm">Package</th></tr></thead><tbody>\n'
for s in srv:
    h+=f'<tr id="{slug(s["repo"])}"><td>{s["rank"]}</td><td><a href="/server/{slug(s["repo"])}.html">{s["repo"]}</a>{note(s)}</td><td class="hide-sm"><a href="/category/{s["category"]}.html">{s["category"]}</a></td><td>{badge(s)}</td><td>{s["stars"]:,}</td><td class="hide-sm">{PL[s["push"]]}</td>{pkg(s)}</tr>\n'
h+='</tbody></table>\n<p class="mut">* pushed within 90 days; 30-day bucket not yet verified. “unchecked” = package not yet verified against npm/PyPI (scores 0 on that component).</p>\n'
h+='<div class="card" id="newsletter"><h2 style="margin-top:0">Weekly MCP health digest</h2><p class="mut">Which servers broke, got archived, or launched this week. No spam.</p>\n<form name="newsletter" method="POST" data-netlify="true" netlify-honeypot="bot-field" action="/thanks.html"><input type="hidden" name="form-name" value="newsletter"><p hidden><label>Leave empty <input name="bot-field"></label></p><input type="email" name="email" required placeholder="you@example.com"> <button type="submit">Subscribe</button></form></div>\n'
open("index.html","w").write(h+FOOT)
LEAD={
"browser":("Best browser automation &amp; scraping MCP servers","for browser automation use <b>Chrome DevTools MCP</b> or <b>Playwright MCP</b> (both 99, packages verified); for scraping use <b>Firecrawl MCP</b> (98). Avoid the archived Browserbase server."),
"devtools":("Best developer tools &amp; git MCP servers","for GitHub use the official <b>github/github-mcp-server</b> (79); for code context <b>DeusData/codebase-memory-mcp</b> (79); for Figma designs <b>GLips/Figma-Context-MCP</b> (78)."),
"databases":("Best database MCP servers (Postgres, MySQL, vector)","<b>googleapis/mcp-toolbox</b> (78) is the healthiest and covers Postgres, MySQL, BigQuery, MongoDB, Redis and more. Dedicated Postgres/MySQL servers had no push in the last 30 days."),
"files":("Best file system &amp; Office (Excel, Word) MCP servers","for Excel use <b>haris-musa/excel-mcp-server</b> (97, PyPI verified); for local files/terminal <b>DesktopCommanderMCP</b> (78). The popular GongRzhe Word and PowerPoint servers are <b>archived</b>."),
"search":("Best web search MCP servers","<b>exa-labs/exa-mcp-server</b> (97, npm verified) for web search; <b>arxiv-mcp-server</b> (77) for papers. Firecrawl (browser category) also offers search."),
"cloud":("Best cloud &amp; infra MCP servers: AWS, Cloudflare, Kubernetes, Terraform","<b>awslabs/mcp</b> (78) for AWS and <b>cloudflare/mcp-server-cloudflare</b> (77). For Kubernetes, <b>containers/kubernetes-mcp-server</b> (67) edges out Flux159’s."),
"productivity":("Best productivity MCP servers: Notion, n8n, Slack, Obsidian","<b>czlonkowski/n8n-mcp</b> (79) for automation. <b>makenotion/notion-mcp-server</b> scores 97 but its README says it is <b>no longer actively maintained</b> — Notion recommends its hosted Remote Notion MCP instead. apple-mcp is archived."),
"ai":("AI, memory &amp; multi-model MCP servers","no server in this category is currently Healthy. The freshest is <b>jamubc/gemini-mcp-tool</b> (67). notebooklm-mcp is archived. For code memory see <a href=\"/server/deusdata-codebase-memory-mcp.html\">codebase-memory-mcp</a> (79, dev tools)."),
"other":("Other MCP servers: Blender, Unity, Godot, KiCAD, Windows","<b>mcp-for-blender</b> (79), <b>unity-mcp</b> (78), <b>Windows-MCP</b> (78) and <b>KiCAD-MCP-Server</b> (77) are healthy; Godot and Unreal servers are stale.")}
def cat_faq(k,n,ss):
    nn=n.replace("&amp;","and"); best=ss[0]; act=[s for s in ss if not s["archived"]]
    arch=[s["repo"] for s in ss if s["archived"]]
    qa=[(f"What is the best {nn} MCP server right now?",f"As of the 2026-10-15 check, {best['repo']} has the highest health score in this category ({best['score']}/100, {best['label']})."),
        (f"How many {nn} MCP servers are tracked?",f"{len(ss)} servers: {sum(s['label']=='Healthy' for s in ss)} Healthy, {sum(s['label']=='Stale' for s in ss)} Stale, {len(arch)} Archived."),
        (f"Which {nn} MCP servers are archived?",("Archived on GitHub: "+", ".join(arch)+".") if arch else "None of the tracked servers in this category are archived as of 2026-10-15."),
        ("How is the health score calculated?","Repo exists 25, not archived 20, last push within 30/90/365 days 25/15/5, verified npm or PyPI package 20, stars up to 10 on a log scale.")]
    ld={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in qa]}
    return '<h2>FAQ</h2>'+"".join(f'<h3>{q}</h3><p>{a}</p>' for q,a in qa)+'<script type="application/ld+json">'+json.dumps(ld)+'</script>\n'
for k,n in CATS:
    t,lead=LEAD[k]; ss=[s for s in srv if s["category"]==k]
    c=head(t+" (Oct 2026, health-ranked)",f"Health-ranked {n.replace('&amp;','and')} MCP servers with dated checks and archived/stale flags.",f"/category/{k}.html")
    c+=f'<h1>{t}</h1><p class="lead"><b>Short answer (2026-10-15):</b> {lead}</p>\n<table><thead><tr><th>Server</th><th>Health</th><th>Stars</th><th>Last push</th></tr></thead><tbody>\n'
    for s in ss: c+=f'<tr><td><a href="/server/{slug(s["repo"])}.html">{s["repo"]}</a>{note(s)}</td><td>{badge(s)}</td><td>{s["stars"]:,}</td><td>{PL[s["push"]]}</td></tr>\n'
    c+='</tbody></table>\n'+cat_faq(k,n,ss)+'<p><a href="/">← All servers</a></p>\n'
    open(f"category/{k}.html","w").write(c+FOOT)
arch=[s for s in srv if s["archived"]]; old=[s for s in srv if s["push"]==">365d" and not s["archived"]]
st=head("MCP server status: archived &amp; stale flags (2026-10-15) — MCP Status","Archived and stale MCP servers flagged from dated GitHub checks.","/status.html")
st+=f'<h1>Status &amp; flags</h1><p class="lead">Check run <b>2026-10-15 06:50 UTC</b> · {len(srv)} servers · {cnt["Healthy"]} Healthy · {cnt["Stale"]} Stale · {cnt["Archived"]} Archived · {cnt["Broken"]} Broken.</p>\n<h2>Archived repositories</h2><ul>'+"".join(f'<li><a href="/server/{slug(s["repo"])}.html">{s["repo"]}</a> — {s["stars"]:,}★</li>' for s in arch)+'</ul>\n'
st+='<h2>Maintenance warnings</h2><ul><li><a href="/server/makenotion-notion-mcp-server.html">makenotion/notion-mcp-server</a> — package README says this self-hosted server is “no longer actively maintained or supported”; Notion recommends its hosted Remote Notion MCP.</li></ul>\n'
st+='<h2>No push in over a year</h2><ul>'+"".join(f'<li><a href="/server/{slug(s["repo"])}.html">{s["repo"]}</a></li>' for s in old)+'</ul>\n'
st+='<h2>Check log</h2><table><thead><tr><th>When (UTC)</th><th>Check</th><th>Result</th></tr></thead><tbody><tr><td>2026-10-15 06:50</td><td>GitHub repo metadata (stars, archived)</td><td>73 exist, 5 archived</td></tr><tr><td>2026-10-15 06:50</td><td>Push recency (30d / 90d / 365d buckets)</td><td>28 ≤30d in healthy set, 9 &gt;1 year</td></tr><tr><td>2026-10-15 06:50</td><td>Package resolves on npm / PyPI</td><td>6 verified, 67 not yet checked</td></tr></tbody></table>\n'
open("status.html","w").write(st+FOOT)
faq={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"How is the MCP Status health score calculated?","acceptedAnswer":{"@type":"Answer","text":"Repo exists 25, not archived 20, last push within 30 days 25 (90 days 15, 365 days 5), package verified on npm or PyPI 20, stars up to 10 on a log scale. Healthy is 75+, Stale 40-74, Broken below 40; archived repos are always labelled Archived."}},{"@type":"Question","name":"How often is data refreshed?","acceptedAnswer":{"@type":"Answer","text":"Every listing shows its check date. The first full check ran 2026-10-15; daily automated refreshes are being set up."}}]}
m=head("How MCP Status scores MCP servers — Methodology","Exact formula behind the MCP Status health score.","/methodology.html",'<script type="application/ld+json">'+json.dumps(faq)+'</script>')
m+='''<h1>Methodology</h1><p class="lead">Every score is computed only from public, verifiable signals. Nothing is estimated; unknown values are shown as “unchecked” and score zero.</p>
<table><thead><tr><th>Signal</th><th>Points</th><th>Source</th></tr></thead><tbody>
<tr><td>Repository exists</td><td>25</td><td>GitHub API</td></tr><tr><td>Not archived</td><td>20</td><td>GitHub <code>archived</code> flag</td></tr>
<tr><td>Last push ≤30 / ≤90 / ≤365 days</td><td>25 / 15 / 5</td><td>GitHub search <code>pushed:&lt;date</code> buckets</td></tr>
<tr><td>Published package resolves</td><td>20</td><td>registry.npmjs.org or pypi.org (verified fetch only)</td></tr>
<tr><td>Stars</td><td>0–10</td><td>round(10 × log10(stars) / 5)</td></tr></tbody></table>
<h2>Labels</h2><p><span class="b h">Healthy</span> ≥75 · <span class="b s">Stale</span> 40–74 · <span class="b a">Broken</span> &lt;40 · <span class="b a">Archived</span> whenever GitHub marks the repo archived, regardless of score.</p>
<h2>Known limits (v1)</h2><ul><li>Package checks done for 6 servers so far; the rest are pending, which caps them at 80.</li><li>Eight lower-star repos are confirmed pushed within 90 days but the 30-day bucket is unverified (marked *).</li><li>Live MCP handshake tests are on the roadmap.</li><li>Maintainer notes (e.g. “no longer maintained” in a README) are flagged manually.</li></ul>
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
open("sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"".join(f"<url><loc>{S}{u}</loc><lastmod>2026-10-15</lastmod></url>\n" for u in urls)+"</urlset>\n")
open("robots.txt","w").write(f"User-agent: *\nAllow: /\n\nSitemap: {S}/sitemap.xml\n")
open("netlify.toml","w").write('[build]\n  publish = "."\n  command = ""\n\n[[headers]]\n  for = "/data/*"\n  [headers.values]\n    Access-Control-Allow-Origin = "*"\n')
open(".gitignore","w").write(".netlify\n")
llm=f"""# MCP Status

> MCP Status ({S}) is a health-ranked directory of Model Context Protocol (MCP) servers. Every listing carries a dated, evidence-based health score (0-100) from public signals: GitHub repo exists, archived flag, last push recency, whether the npm/PyPI package resolves, and stars. Archived and stale servers are flagged explicitly.

Last full check: 2026-10-15T06:50Z. {len(srv)} servers: {cnt['Healthy']} Healthy, {cnt['Stale']} Stale, {cnt['Archived']} Archived.

## Key pages
- [Ranked list of all servers]({S}/)
- [Status / archived & stale flags]({S}/status.html)
- [Methodology]({S}/methodology.html)
- [Raw data JSON]({S}/data/servers.json)

## Best MCP servers by use case (healthiest first, as of 2026-10-15)
- Browser automation: ChromeDevTools/chrome-devtools-mcp (99), microsoft/playwright-mcp (99)
- Web scraping: firecrawl/firecrawl-mcp-server (98), apify/apify-mcp-server (78)
- Web search: exa-labs/exa-mcp-server (97), blazickjp/arxiv-mcp-server (77, papers)
- Databases: googleapis/mcp-toolbox (78); crystaldba/postgres-mcp (67, stale)
- Git / GitHub: github/github-mcp-server (79)
- Files / office: haris-musa/excel-mcp-server (97), wonderwhy-er/DesktopCommanderMCP (78)
- Cloud / infra: awslabs/mcp (78), cloudflare/mcp-server-cloudflare (77)
- Productivity: makenotion/notion-mcp-server (97, but README says no longer actively maintained; Notion recommends its hosted Remote Notion MCP), czlonkowski/n8n-mcp (79)
- Design: GLips/Figma-Context-MCP (78)

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

## Data (check of 2026-10-15T06:50Z)
{len(srv)} servers: {cnt['Healthy']} Healthy, {cnt['Stale']} Stale, {cnt['Archived']} Archived. Sources: GitHub search API and direct npm/PyPI lookups (6 packages verified; others marked unchecked). No data is invented.

## Score (0–100)
Repo exists 25 · not archived 20 · last push ≤30d 25 / ≤90d 15 / ≤365d 5 · verified package 20 · stars round(10·log10(stars)/5). Healthy ≥75, Stale 40–74, Broken <40; archived repos always labelled Archived.
""")
exec(open("gen_seo.py").read())
print(cnt, len(srv))
