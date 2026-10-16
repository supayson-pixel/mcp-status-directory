# SEO extension, exec'd at end of gen.py (shares its globals: srv,S,head,FOOT,badge,slug,PL,CATS,cnt,llm)
import math, html as H
PP={"<=30d":25,"30-90d":15,"90-365d":5,">365d":0}
CN=dict(CATS)
# install snippets verified from the package README on npm/PyPI (2026-10-15); others omitted
INST={
"ChromeDevTools/chrome-devtools-mcp":('{"mcpServers":{"chrome-devtools":{"command":"npx","args":["-y","chrome-devtools-mcp@latest"]}}}',"npm README"),
"microsoft/playwright-mcp":('{"mcpServers":{"playwright":{"command":"npx","args":["@playwright/mcp@latest"]}}}',"npm README"),
"firecrawl/firecrawl-mcp-server":('{"mcpServers":{"firecrawl":{"command":"npx","args":["-y","firecrawl-mcp"],"env":{"FIRECRAWL_API_KEY":"YOUR_KEY"}}}}',"npm README"),
"exa-labs/exa-mcp-server":('{"mcpServers":{"exa":{"url":"https://mcp.exa.ai/mcp"}}}',"npm README (hosted remote endpoint)"),
"makenotion/notion-mcp-server":('{"mcpServers":{"notion":{"command":"npx","args":["-y","@notionhq/notion-mcp-server"]}}}',"npm README — note: no longer actively maintained"),
"haris-musa/excel-mcp-server":('uvx excel-mcp-server stdio',"PyPI README"),
}
def parts(s):
    st=round(10*math.log10(s["stars"])/5) if s["stars"]>0 else 0
    p=[("Repository exists",25,25),("Not archived",0 if s["archived"] else 20,20),("Last push recency ("+PL[s["push"]].replace("&gt;",">")+")",PP[s["push"]],25),("Package verified on npm/PyPI","20 ("+s["package"].split(":",1)[1]+")" if s["package"] else "0 (unchecked)",20),(f"Stars ({s['stars']:,})",st,10)]
    tot=0 if not s.get('exists',True) else 25+(0 if s["archived"] else 20)+PP[s["push"]]+(20 if s["package"] else 0)+st
    return p,tot
def summ(s):
    return f'{s["repo"]} MCP server: health {s["score"]}/100 ({s["label"]}), {s["stars"]:,} GitHub stars, last push {PL[s["push"]].replace("&gt;",">")}, '+("archived on GitHub" if s["archived"] else "not archived")+f'. Checked {CD}.'
os.makedirs("server",exist_ok=True); os.makedirs("compare",exist_ok=True)
pages=[]  # (path,title,summary)
for s in srv:
    sl=slug(s["repo"]); path=f"/server/{sl}.html"; name=s["repo"].split("/")[1]
    p,tot=parts(s); assert tot==s["score"],(s["repo"],tot,s["score"])
    alts=[a for a in srv if a["category"]==s["category"] and a is not s][:5]
    t=f'{name} MCP server: status, health score &amp; install'
    d=H.escape(summ(s))
    ld=[{"@context":"https://schema.org","@type":"SoftwareApplication","name":s["repo"],"applicationCategory":"DeveloperApplication","operatingSystem":"Cross-platform","url":S+path,"sameAs":"https://github.com/"+s["repo"],"description":summ(s),"dateModified":CD,"offers":{"@type":"Offer","price":"0","priceCurrency":"USD"}},
        {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"MCP Status","item":S+"/"},{"@type":"ListItem","position":2,"name":CN[s["category"]].replace("&amp;","&"),"item":f'{S}/category/{s["category"]}.html'},{"@type":"ListItem","position":3,"name":s["repo"],"item":S+path}]}]
    h=head(t,d,path,"".join('<script type="application/ld+json">'+json.dumps(x)+'</script>' for x in ld))
    h+=f'<p class="mut"><a href="/">MCP Status</a> › <a href="/category/{s["category"]}.html">{CN[s["category"]]}</a> › {s["repo"]}</p>'
    h+=f'<h1>{name} MCP server</h1><p class="lead">{H.escape(summ(s))} Source: <a href="https://github.com/{s["repo"]}">github.com/{s["repo"]}</a></p>\n'
    if "note" in s: h+=f'<div class="card"><b>⚠ Maintenance warning:</b> {s["note"]}</div>\n'
    if s["archived"]: h+='<div class="card"><b>⚠ Archived:</b> GitHub marks this repository archived (read-only). Consider an alternative below.</div>\n'
    h+=f'<h2>Latest check</h2><table><tbody><tr><td>Checked at</td><td>{CHECKED}</td></tr><tr><td>Health</td><td>{badge(s)}</td></tr><tr><td>Rank</td><td>#{s["rank"]} of {len(srv)}</td></tr><tr><td>Category</td><td><a href="/category/{s["category"]}.html">{CN[s["category"]]}</a></td></tr><tr><td>Stars</td><td>{s["stars"]:,}</td></tr><tr><td>Archived</td><td>{"yes" if s["archived"] else "no"}</td></tr><tr><td>Last push</td><td>{PL[s["push"]]}</td></tr><tr><td>Package</td><td>{H.escape(s["package"]) if s["package"] else "unchecked"}</td></tr></tbody></table>\n'
    h+='<h2>Score breakdown</h2><table><thead><tr><th>Signal</th><th>Points</th><th>Max</th></tr></thead><tbody>'+"".join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a,b,c in p)+f'<tr><td><b>Total</b></td><td><b>{tot}</b></td><td>100</td></tr></tbody></table>\n'
    h+='<h2>Install</h2>'
    if s["repo"] in INST:
        cfg,src=INST[s["repo"]]
        h+=f'<p class="mut">Verified from the {src} on 2026-10-15.</p><pre><code>{H.escape(cfg)}</code></pre>\n'
    else: h+=f'<p class="mut">No install snippet yet — we only publish commands verified against the package registry. See the <a href="https://github.com/{s["repo"]}#readme">project README</a>.</p>\n'
    if alts: h+=f'<h2>Alternatives in {CN[s["category"]]}</h2><ul>'+"".join(f'<li><a href="/server/{slug(a["repo"])}.html">{a["repo"]}</a> — {badge(a)}</li>' for a in alts)+'</ul>\n'
    open(f"server/{sl}.html","w").write(h+FOOT); pages.append((path,f'{s["repo"]} MCP server',summ(s)))
COMP=[("playwright-mcp-vs-chrome-devtools-mcp-vs-browser-tools-mcp",["microsoft/playwright-mcp","ChromeDevTools/chrome-devtools-mcp","AgentDeskAI/browser-tools-mcp"]),
("playwright-mcp-vs-executeautomation-mcp-playwright",["microsoft/playwright-mcp","executeautomation/mcp-playwright"]),
("firecrawl-mcp-vs-apify-mcp",["firecrawl/firecrawl-mcp-server","apify/apify-mcp-server"]),
("browsermcp-vs-mcp-chrome",["BrowserMCP/mcp","hangwin/mcp-chrome"]),
("kubernetes-mcp-server-comparison",["containers/kubernetes-mcp-server","Flux159/mcp-server-kubernetes"]),
("n8n-mcp-vs-n8n-mcp-server",["czlonkowski/n8n-mcp","leonardsellem/n8n-mcp-server"]),
("database-mcp-toolbox-vs-postgres-mcp-vs-mysql",["googleapis/mcp-toolbox","crystaldba/postgres-mcp","benborla/mcp-server-mysql"]),
("figma-context-mcp-vs-cursor-talk-to-figma",["GLips/Figma-Context-MCP","grab/cursor-talk-to-figma-mcp"])]
BY={s["repo"]:s for s in srv}
for cs,rs in COMP:
    ss=[BY[r] for r in rs]; assert len({s["category"] for s in ss})==1
    nm=" vs ".join(r.split("/")[1] for r in rs); path=f"/compare/{cs}.html"; w=max(ss,key=lambda s:s["score"])
    tie=[s for s in ss if s["score"]==w["score"]]
    verdict=("Tie on health score: "+" and ".join(s["repo"] for s in tie) if len(tie)>1 else f'{w["repo"]} has the highest health score') + f' ({w["score"]}/100) as of {CD}.'
    t=f'{nm}: MCP server comparison (health, stars, maintenance)'
    h=head(t,H.escape(f"Side-by-side {nm} comparison from dated checks. {verdict}"),path)
    h+=f'<p class="mut"><a href="/">MCP Status</a> › <a href="/category/{ss[0]["category"]}.html">{CN[ss[0]["category"]]}</a> › Compare</p><h1>{nm}</h1><p class="lead"><b>Verdict:</b> {verdict} Data checked {CHECKED}.</p>\n'
    rows=[("Health score",lambda s:badge(s)),("Stars",lambda s:f'{s["stars"]:,}'),("Last push",lambda s:PL[s["push"]]),("Archived",lambda s:"yes" if s["archived"] else "no"),("Package",lambda s:H.escape(s["package"]) if s["package"] else "unchecked"),("Verified install snippet",lambda s:"yes" if s["repo"] in INST else "no"),("Rank (of %d)"%len(srv),lambda s:f'#{s["rank"]}')]
    h+='<table><thead><tr><th></th>'+"".join(f'<th><a href="/server/{slug(s["repo"])}.html">{s["repo"]}</a></th>' for s in ss)+'</tr></thead><tbody>'+"".join(f'<tr><td>{a}</td>'+"".join(f'<td>{f(s)}</td>' for s in ss)+'</tr>' for a,f in rows)+'</tbody></table>\n'
    for s in ss:
        if "note" in s: h+=f'<p>⚠ {s["repo"]}: {s["note"]}</p>'
    h+='<p class="mut">Comparison covers maintenance health only, not features. <a href="/methodology.html">Methodology</a>.</p>\n'
    open(f"compare/{cs}.html","w").write(h+FOOT); pages.append((path,nm+" comparison",verdict))
# compare index
ci=head("MCP server comparisons — MCP Status","Side-by-side health comparisons of popular MCP servers in the same category.","/compare/")
ci+='<h1>MCP server comparisons</h1><ul>'+"".join(f'<li><a href="{p}">{n}</a> — {v}</li>' for p,n,v in pages if p.startswith("/compare/"))+'</ul>\n'
open("compare/index.html","w").write(ci+FOOT)
core=[("/","Ranked list of all servers",f"All {len(srv)} servers ranked by health score."),("/status.html","Status & flags","Archived, stale and maintenance warnings."),("/methodology.html","Methodology","Exact scoring formula and limits."),("/submit.html","Submit a server","Free listing via GitHub issue."),("/compare/","Comparisons index","All head-to-head comparison pages."),("/data/servers.json","Raw data JSON","Machine-readable data for every server.")]
catp=[(f"/category/{k}.html",n.replace("&amp;","&")+" MCP servers",LEAD[k][0].replace("&amp;","&")) for k,n in CATS]
allp=core+catp+pages
llm2=llm+"\n## Comparisons\n"+"".join(f"- [{n}]({S}{p}): {v}\n" for p,n,v in pages if p.startswith("/compare/"))
llm2+="\n## Server pages\n"+"".join(f"- [{n}]({S}{p}): {v}\n" for p,n,v in pages if p.startswith("/server/"))
llm2+=f"\n## Optional\n- [llms-full.txt]({S}/llms-full.txt): full per-server data in one file\n"
open("llms.txt","w").write(llm2)
full=f"# MCP Status — full data (checked {CHECKED})\n\nSource: {S}. Score = repo exists 25 + not archived 20 + push(<=30d 25, <=90d 15, <=365d 5) + verified package 20 + round(10*log10(stars)/5). Healthy >=75, Stale 40-74, Broken <40, Archived if GitHub-archived.\n\n## All pages\n"+"".join(f"- {S}{p} — {n}: {v}\n" for p,n,v in allp)+"\n## Servers\n"
for s in srv:
    full+=f"\n### {s['repo']}\n- Page: {S}/server/{slug(s['repo'])}.html\n- GitHub: https://github.com/{s['repo']}\n- Category: {s['category']}\n- Health: {s['score']}/100 ({s['label']}), rank #{s['rank']}\n- Stars: {s['stars']}\n- Archived: {'yes' if s['archived'] else 'no'}\n- Last push: {s['push']}\n- Package: {s['package'] or 'unchecked'}\n"+(f"- Install (verified): {INST[s['repo']][0]}\n" if s['repo'] in INST else "")+(f"- Warning: {s['note']}\n" if 'note' in s else "")
open("llms-full.txt","w").write(full)
urls=[p for p,_,_ in core if not p.endswith(".json")]+[p for p,_,_ in catp]+[p for p,_,_ in pages]
open("sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"".join(f"<url><loc>{S}{u}</loc><lastmod>{CHECKED[:10]}</lastmod></url>\n" for u in urls)+"</urlset>\n")
bots=["GPTBot","OAI-SearchBot","ChatGPT-User","ClaudeBot","Claude-User","Claude-SearchBot","anthropic-ai","PerplexityBot","Perplexity-User","Google-Extended","Applebot-Extended","CCBot","Bytespider","Amazonbot","meta-externalagent","DuckAssistBot","cohere-ai","MistralAI-User"]
open("robots.txt","w").write("User-agent: *\nAllow: /\nDisallow: /thanks.html\n\n"+"".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots)+f"Sitemap: {S}/sitemap.xml\n")
print("seo pages:",len(pages),"sitemap urls:",len(urls))
