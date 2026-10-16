"""Daily data refresh: re-checks every listed server with real API data only.
GitHub repo metadata (exists, archived, stars, pushed_at) + npm/PyPI package resolution
(package name read from the repo's own package.json / pyproject.toml, accepted only if the
registry entry resolves and links back to the same GitHub repo). Writes data/servers.json and
appends a dated entry to data/changes.json."""
import json, math, os, re, subprocess, sys, urllib.request, urllib.error, datetime as dt, base64
try: import tomllib
except ImportError: tomllib=None
TOK=subprocess.run(["gh","auth","token"],capture_output=True,text=True).stdout.strip()
NOW=dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
def get(url,gh=False):
    h={"User-Agent":"mcp-status-refresh"}
    if gh: h.update({"Authorization":"token "+TOK,"Accept":"application/vnd.github+json"})
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers=h),timeout=30) as r: return r.status,json.loads(r.read())
    except urllib.error.HTTPError as e: return e.code,None
    except Exception as e: return -1,str(e)
def ghfile(repo,path):
    c,d=get(f"https://api.github.com/repos/{repo}/contents/{path}",True)
    if c==200 and isinstance(d,dict) and d.get("content"): return base64.b64decode(d["content"]).decode("utf-8","replace")
    return None
def links_back(text,repo): return repo.lower() in json.dumps(text).lower()
def npm(name,repo):
    c,d=get("https://registry.npmjs.org/"+name.replace("/","%2f"))
    if c!=200 or not d or "dist-tags" not in d: return None
    v=d["dist-tags"].get("latest"); meta=d.get("versions",{}).get(v,{})
    if not links_back([meta.get("repository"),meta.get("homepage"),meta.get("bugs"),d.get("repository")],repo): return None
    return f"npm:{name}@{v}"
def pypi(name,repo):
    c,d=get(f"https://pypi.org/pypi/{name}/json")
    if c!=200 or not d: return None
    i=d["info"]
    if not links_back([i.get("project_urls"),i.get("home_page"),i.get("description","")[:20000]],repo): return None
    return f"pypi:{i['name']}@{i['version']}"
def find_pkg(repo,old):
    if old:  # re-resolve the known package at its latest version
        reg,rest=old.split(":",1); name=rest.rsplit("@",1)[0]
        r=(npm if reg=="npm" else pypi)(name,repo)
        if r: return r,"re-resolved"
    pj=ghfile(repo,"package.json")
    if pj:
        try:
            j=json.loads(pj)
            if j.get("name") and not j.get("private"):
                r=npm(j["name"],repo)
                if r: return r,"package.json"
        except Exception: pass
    pt=ghfile(repo,"pyproject.toml")
    if pt:
        name=None
        try: name=tomllib.loads(pt).get("project",{}).get("name") if tomllib else None
        except Exception: pass
        if not name:
            m=re.search(r'^\[project\][^\[]*?^name\s*=\s*["\']([^"\']+)',pt,re.M|re.S); name=m and m.group(1)
        if name:
            r=pypi(name,repo)
            if r: return r,"pyproject.toml"
    return None,"none found"
PP={"<=30d":25,"30-90d":15,"90-365d":5,">365d":0}
def bucket(p):
    if not p: return ">365d"
    d=(NOW-dt.datetime.fromisoformat(p.replace("Z","+00:00"))).days
    return "<=30d" if d<=30 else "30-90d" if d<=90 else "90-365d" if d<=365 else ">365d"
def score(s):
    if not s["exists"]: return 0
    st=round(10*math.log10(s["stars"])/5) if s["stars"]>0 else 0
    return 25+(0 if s["archived"] else 20)+PP[s["push"]]+(20 if s["package"] else 0)+st
def label(s):
    if not s["exists"]: return "Broken"
    return "Archived" if s["archived"] else "Healthy" if s["score"]>=75 else "Stale" if s["score"]>=40 else "Broken"
prev=json.load(open("data/servers.json"))
out=[]; errors=[]
for o in prev["servers"]:
    repo=o["repo"]; s=dict(repo=repo,category=o["category"])
    for k in ("note",): 
        if k in o: s[k]=o[k]
    c,d=get(f"https://api.github.com/repos/{repo}",True)
    if c==200:
        s.update(exists=True,stars=d["stargazers_count"],archived=bool(d["archived"]),pushed_at=d["pushed_at"])
        if d["full_name"].lower()!=repo.lower(): s["renamed_to"]=d["full_name"]
    elif c==404:
        s.update(exists=False,stars=o.get("stars",0),archived=o.get("archived",False),pushed_at=o.get("pushed_at"))
    else:
        errors.append((repo,c,d)); s.update({k:o.get(k) for k in ("exists","stars","archived","pushed_at")}); s["exists"]=s["exists"] if s["exists"] is not None else True; s["stale_data"]=True
    s["push"]=bucket(s.get("pushed_at")) if s.get("pushed_at") else o["push"].replace("<=90d*","30-90d")
    if s["exists"]:
        pk,how=find_pkg(d["full_name"] if c==200 else repo,o.get("package")); s["package"]=pk; s["package_source"]=how
    else: s["package"]=None
    s["score"]=score(s); s["label"]=label(s); out.append(s)
    print(f'{repo:50} {s["stars"]:>6} arch={s["archived"]} {s["push"]:8} {s["package"]} {s["score"]} {s["label"]}',flush=True)
if errors and len(errors)>len(out)//4: sys.exit(f"too many API errors: {errors[:5]}")
out.sort(key=lambda s:(s["label"] in ("Archived","Broken"),-s["score"],-s["stars"]))
for i,s in enumerate(out): s["rank"]=i+1
P={s["repo"]:s for s in prev["servers"]}
ch=[]
for s in out:
    p=P[s["repo"]]
    if not s["exists"]: ch.append(f'{s["repo"]}: repository not found (404)')
    if s["archived"] and not p["archived"]: ch.append(f'{s["repo"]}: newly archived on GitHub')
    if p["archived"] and not s["archived"]: ch.append(f'{s["repo"]}: un-archived')
    if s["label"]!=p["label"]: ch.append(f'{s["repo"]}: {p["label"]} → {s["label"]} ({p["score"]} → {s["score"]})')
    elif s["score"]!=p["score"]: ch.append(f'{s["repo"]}: score {p["score"]} → {s["score"]}')
    if s["package"] and not p.get("package"): ch.append(f'{s["repo"]}: package verified ({s["package"]})')
    if p.get("package") and not s["package"] and s["exists"]: ch.append(f'{s["repo"]}: package no longer resolves ({p["package"]})')
    if s.get("renamed_to"): ch.append(f'{s["repo"]}: GitHub redirects to {s["renamed_to"]}')
chk=NOW.isoformat().replace("+00:00","Z")
json.dump({"checked_at":chk,"site":prev["site"],"scoring":"repo 25 + not archived 20 + push(<=30d 25,<=90d 15,<=365d 5) + verified package 20 + round(10*log10(stars)/5)","push_note":"push bucket from the GitHub API pushed_at timestamp at check time","servers":out},open("data/servers.json","w"),indent=1)
cnt={k:sum(1 for s in out if s["label"]==k) for k in ["Healthy","Stale","Archived","Broken"]}
cl=json.load(open("data/changes.json")) if os.path.exists("data/changes.json") else []
cl.insert(0,{"checked_at":chk,"counts":cnt,"packages_verified":sum(1 for s in out if s["package"]),"api_errors":len(errors),"changes":ch})
json.dump(cl[:60],open("data/changes.json","w"),indent=1)
print("COUNTS",cnt,"PKG",sum(1 for s in out if s["package"]),"ERR",errors); print("CHANGES"); print("\n".join(ch))
