#!/usr/bin/env python3
"""Convert a manual (typed) table of contents into a real Word TOC field.

The doc keeps displaying the same entries, but the TOC becomes a genuine
indexation: TOC \\o "1-2" \\h \\z \\u with bookmarks on every heading.
Word/LibreOffice regenerate it (with real page numbers and hyperlinks) via
F9 / Update Table; w:updateFields makes them refresh automatically on open.
"""
import sys, re
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def fld(par, kind, text=None):
    r = OxmlElement('w:r')
    if kind in ('begin', 'separate', 'end'):
        fc = OxmlElement('w:fldChar')
        fc.set(qn('w:fldCharType'), kind)
        if kind == 'begin':
            fc.set(qn('w:dirty'), 'true')
        r.append(fc)
    else:  # instr
        it = OxmlElement('w:instrText')
        it.set(qn('xml:space'), 'preserve')
        it.text = text
        r.append(it)
    par._p.append(r)

def add_bookmark(par, bid, name):
    start = OxmlElement('w:bookmarkStart')
    start.set(qn('w:id'), str(bid))
    start.set(qn('w:name'), name)
    end = OxmlElement('w:bookmarkEnd')
    end.set(qn('w:id'), str(bid))
    par._p.insert(0, start)
    par._p.append(end)

def fix(path):
    doc = Document(path)
    paras = doc.paragraphs
    ci = next((i for i, p in enumerate(paras) if p.text.strip() == 'Contents'), None)
    if ci is None:
        print(f'{path}: no Contents heading, skipped'); return

    # 1. collect the manual entries right after Contents
    entries, targets = [], []
    for p in paras[ci + 1:]:
        st = getattr(p.style, 'name', '') or ''
        if st.startswith('Heading') or not p.text.strip():
            break
        entries.append(p)
    if not entries:
        # maybe already converted
        xml = doc.element.xml
        if 'TOC \\o' in xml:
            print(f'{path}: already a TOC field'); return
        print(f'{path}: no entries found, skipped'); return

    # 2. collect body headings (level 1 and 2) to bookmark + rebuild entries
    bid = 1000
    for p in paras[ci + 1:]:
        st = getattr(p.style, 'name', '') or ''
        if not st.startswith('Heading') or not p.text.strip():
            continue
        lvl = 2 if '2' in st.split()[-1] else 1
        bid += 1
        name = f'_Toc{bid}'
        add_bookmark(p, bid, name)
        targets.append((lvl, p.text.strip(), name))

    # cached display: level-1 entries only (what the manual TOC listed),
    # page numbers stripped — Word fills them on update
    cached = []
    for lvl, text, name in targets:
        if lvl == 1:
            cached.append((re.sub(r'\s*\t?\s*\d+\s*$', '', text), name))

    # 3. build field paragraphs right after Contents
    new_pars = []
    for i, (text, name) in enumerate(cached):
        np = doc.add_paragraph()
        np.paragraph_format.space_after = doc.paragraphs[0].paragraph_format.space_after
        if i == 0:
            fld(np, 'begin')
            fld(np, 'instr', ' TOC \\o "1-2" \\h \\z \\u ')
            fld(np, 'separate')
        r = np.add_run(text)
        r.font.size = entries[0].runs[0].font.size if entries[0].runs else None
        if i == len(cached) - 1:
            fld(np, 'end')
        new_pars.append(np)

    # 4. drop the manual entries, move field paragraphs into place
    anchor = paras[ci]._p
    for p in entries:
        p._p.getparent().remove(p._p)
    for np in new_pars:
        anchor.addnext(np._p)
        anchor = np._p

    # 5. ask Word/LibreOffice to refresh fields on open
    settings = doc.settings.element
    if settings.find(qn('w:updateFields')) is None:
        uf = OxmlElement('w:updateFields')
        uf.set(qn('w:val'), 'true')
        settings.append(uf)

    doc.save(path)
    print(f'{path}: TOC field installed ({len(cached)} level-1 entries, '
          f'{len(targets)} headings bookmarked)')

for f in sys.argv[1:]:
    fix(f)
