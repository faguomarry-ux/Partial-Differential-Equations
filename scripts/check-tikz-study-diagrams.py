"""Validate native TikZ diagrams, margin text and chapter/full-book agreement.

Run after latexmk for main.tex and chapter-01.tex ... chapter-12.tex.
Requires PyMuPDF. Validation does not replace mathematical or visual review.
"""
from pathlib import Path
import re,json,hashlib
import pymupdf as fitz

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"tmp/pdfs/tikz-qa"
REPORT.mkdir(parents=True,exist_ok=True)
items=json.loads((ROOT/"figures/tikz/manifest.json").read_text(encoding="utf-8"))
assert len(items)==60
assert len({i["id"] for i in items})==60
for ch in range(1,13):
    group=[i for i in items if i["chapter"]==ch]
    assert len(group)==5
    assert sum(i["placement"]=="body" for i in group)==4
    assert sum(i["placement"]=="margin" for i in group)==1
for i in items:
    p=ROOT/i["drawing"];s=p.read_text(encoding="utf-8")
    assert s.count(r"\begin{tikzpicture}")==1 and s.count(r"\end{tikzpicture}")==1,p
    assert r"\includegraphics" not in s,p
    assert "\t" not in s,p
    macro="PDEMarginDiagram" if i["placement"]=="margin" else "PDEBodyDiagram"
    call="\\"+macro+"{"+i["id"][1:]+"}"
    assert (ROOT/i["source"]).read_text(encoding="utf-8").count(call)==1,i
for stem in ["main"]+[f"chapter-{i:02d}" for i in range(1,13)]:
    s=(ROOT/f"build/{stem}.log").read_text(encoding="utf-8",errors="replace")
    for bad in ["Overfull","Missing character","undefined","multiply defined","Missing diagram"]:
        assert bad not in s,(stem,bad)

doc=fitz.open(ROOT/"build/main.pdf")
aux=(ROOT/"build/main.aux").read_text(encoding="utf-8")
names=doc.resolve_names()
positions=[]
for item in items:
    id=item["id"][1:]
    m=re.search(r"\\newlabel\{fig:tikz-"+re.escape(id)+r"\}\{\{[^}]+\}\{[^}]+\}\{[^}]*\}\{([^}]+)\}",aux)
    assert m,item["id"]
    dest=names[m[1]]
    p=doc[dest["page"]]
    if item["placement"]=="body":
        assert p.search_for("Diagram "+item["id"]+"."),item["id"]
    positions.append(dict(id=item["id"],physical_page=dest["page"]+1,
                          printed_page=p.get_label()))

# Trace the literal input graph; dynamic file arguments are checked via manifest.
seen=set()
def visit(p):
    p=p.resolve()
    if p in seen:return
    assert p.exists(),p
    seen.add(p)
    s=re.sub(r"(?<!\\)%.*","",p.read_text(encoding="utf-8"))
    for name in re.findall(r"\\input\{([^}]+)\}",s):
        if "#" in name:continue
        child=ROOT/(name if Path(name).suffix else name+".tex")
        visit(child)
visit(ROOT/"main.tex")
for item in items:visit(ROOT/item["drawing"])
labels=[];refs=[]
for p in seen:
    s=re.sub(r"(?<!\\)%.*","",p.read_text(encoding="utf-8"))
    labels.extend(v for v in re.findall(r"\\label\{([^}]+)\}",s) if "#" not in v)
    refs.extend(v for v in re.findall(r"\\(?:ref|eqref|pageref)\{([^}]+)\}",s) if "#" not in v)
assert len(set(labels))==len(labels)
assert not set(refs)-set(labels)-{"fig:tikz-"+i["id"][1:] for i in items}

def args_at(s,pos,count=2):
    args=[]
    for _ in range(count):
        while pos<len(s) and s[pos].isspace():pos+=1
        assert s[pos]=="{",(pos,s[pos:pos+20])
        pos+=1;start=pos;depth=1
        while depth:
            if s[pos]=="{" and s[pos-1]!="\\":depth+=1
            if s[pos]=="}" and s[pos-1]!="\\":depth-=1
            pos+=1
        args.append(s[start:pos-1])
    return args,pos
cjk=lambda s:"".join(re.findall(r"[\u4e00-\u9fff]",s))
margin_text=[];low=[];bottoms=[]
for n,p in enumerate(doc):
    spans=[s for b in p.get_text("dict")["blocks"] if "lines" in b
           for l in b["lines"] for s in l["spans"]]
    ss=[s for s in spans if s["bbox"][0]>443]
    margin_text.append(cjk("".join(s["text"] for s in ss)))
    chinese=[s for s in ss if cjk(s["text"])]
    if chinese:
        bottom=max(s["bbox"][3] for s in chinese)
        bottoms.append(bottom)
        if bottom>774:low.append([n+1,bottom])
missing=[];note_count=0
for p in seen:
    if "chapters" not in p.parts and "frontmatter" not in p.parts:continue
    s=p.read_text(encoding="utf-8")
    for match in re.finditer(r"\\PDEAnnotation(?=\{)",s):
        args,_=args_at(s,match.end())
        wanted=cjk("".join(args))
        note_count+=1
        if not any(wanted in t for t in margin_text):missing.append([str(p.relative_to(ROOT)),args[0]])
for item in items:
    if item["placement"]=="margin":
        wanted=cjk("图"+item["title"]+item["caption"])
        if not any(wanted in t for t in margin_text):missing.append([item["id"],"margin diagram caption"])
assert not missing,missing
assert not low,low

titles={1:"1 Introduction",2:"2 Four Important Linear Partial Differential Equations",
        3:"3 Nonlinear First-Order PDE",4:"4 Other Ways to Represent Solutions",
        5:"5 Sobolev Spaces",6:"6 Second-Order Elliptic Equations",7:"7 Linear Evolution Equations",8:"8 The Calculus of Variations",9:"9 Nonvariational Techniques",10:"10 Hamilton-Jacobi Equations",11:"11 Systems of Conservation Laws",12:"12 Nonlinear Wave Equations"}
chapters=[]
clip=fitz.Rect(0,0,595,785)
for ch,title in titles.items():
    start=next(r[2]-1 for r in doc.get_toc() if r[1]==title)
    study=fitz.open(ROOT/f"build/chapter-{ch:02d}.pdf")
    for j,page in enumerate(study):
        a=page.get_text("words",clip=clip)
        b=doc[start+j].get_text("words",clip=clip)
        assert [w[4] for w in a]==[w[4] for w in b],(ch,j+1,"text mismatch")
        for x,y in zip(a,b):
            assert max(abs(x[k]-y[k]) for k in range(4))<.03,(ch,j+1,x,y)
    chapters.append(dict(chapter=ch,pages=len(study),bookmarks=len(study.get_toc()),
                         physical_range=[start+1,start+len(study)],
                         printed_range=[doc[start].get_label(),doc[start+len(study)-1].get_label()]))
summary=dict(total_diagrams=60,body_diagrams=48,margin_diagrams=12,all_drawings_native_tikz=True,
             book_pages=len(doc),book_bookmarks=len(doc.get_toc()),
             book_links=sum(len(p.get_links()) for p in doc),
             reachable_tex=len(seen),static_labels=len(labels),
             diagram_labels=len(items),explicit_references=len(refs),
             existing_text_notes=note_count,missing_notes=missing,low_margins=low,
             maximum_margin_text_bottom=round(max(bottoms),2),
             all_twelve_chapters_identical_to_full_book=True,
             chapters=chapters,diagram_positions=positions)
(REPORT/"final-validation.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(summary,ensure_ascii=True,indent=2))