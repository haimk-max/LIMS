#!/usr/bin/env python3
"""Regenerate the rule-catalog section of ICP_RULE_ENGINE_WORKBOOK_he.html
from ICP_LIMS_RULE_CATALOG_he.csv (the machine-readable source of truth).

Usage:  python3 tools/build_catalog_section.py
Run from docs/lims-icp/. Rewrites the block between the CATALOG:BEGIN and
CATALOG:END markers in place; everything else in the workbook is untouched.
"""
import csv
import html
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
CSV_PATH = BASE / "ICP_LIMS_RULE_CATALOG_he.csv"
HTML_PATH = BASE / "ICP_RULE_ENGINE_WORKBOOK_he.html"

STATUS_CHIP = {
    "SOP_CONFIRMED": ('sop', 'מעוגן SOP'),
    "WORKING_DECISION": ('work', 'החלטת עבודה'),
    "OPEN_DECISION": ('open', 'הכרעה פתוחה'),
}

# rule id -> decision-card anchor (open rules and open parameters)
DECISION_REF = {
    "ING-002": "d01", "CLS-001": "d01",
    "QC-008": "d02", "QC-009": "d02",
    "QC-004": "d03",
    "CAL-006": "d04", "CAL-007": "d04",
    "LIN-004": "d05", "LIN-005": "d05",
    "REP-003": "d06",
    "CON-006": "d07",
    "CON-002": "d08",
    "INT-001": "d09",  # rule is SOP-confirmed; its scope parameter is open
}

LATIN_RUN = re.compile(
    r'[A-Za-z0-9±%²<>≤≥×½]+(?:[ _/\.\-–][A-Za-z0-9±%²<>≤≥×½]+)*'
)


def bdi_wrap(text: str) -> str:
    """HTML-escape and wrap Latin-containing token runs in <bdi>."""
    out, last = [], 0
    for m in LATIN_RUN.finditer(text):
        if not re.search(r'[A-Za-z]', m.group(0)):
            continue  # pure numbers stay unwrapped
        out.append(html.escape(text[last:m.start()]))
        out.append('<bdi>' + html.escape(m.group(0)) + '</bdi>')
        last = m.end()
    out.append(html.escape(text[last:]))
    return ''.join(out)


def build_section(rows):
    families = {}
    order = []
    for r in rows:
        fam = r['family'].strip()
        if fam not in families:
            families[fam] = []
            order.append(fam)
        families[fam].append(r)

    parts = []
    for fam in order:
        rules = families[fam]
        parts.append(f'<div class="famblock"><h3>{html.escape(fam)} '
                     f'<span style="color:var(--soft);font-weight:400">({len(rules)} כללים)</span></h3>')
        parts.append('<table class="data-table"><thead><tr>'
                     '<th class="rid">מזהה</th><th style="width:30%">הכלל</th>'
                     '<th style="width:26%">פעולת המערכת</th><th>מעמד</th>'
                     '<th>מקור / הערה</th><th>בעלים</th><th>הכרעה</th>'
                     '</tr></thead><tbody>')
        for r in rules:
            rid = r['rule_id'].strip()
            status = r['normalized_status'].strip()
            cls, label = STATUS_CHIP.get(status, ('comp', status))
            owner = r.get('professional_owner', '').strip() or '—'
            src = r.get('source_or_open_note', '').strip()
            ref = DECISION_REF.get(rid)
            if ref:
                tag = 'פרמטר פתוח' if status == 'SOP_CONFIRMED' else 'חוסם'
                refcell = (f'<a class="dref" href="#{ref}">{ref.upper().replace("D", "D-")}'
                           f' ({tag})</a>')
            else:
                refcell = ''
            parts.append(
                f'<tr data-status="{status}">'
                f'<td class="rid">{html.escape(rid)}</td>'
                f'<td>{bdi_wrap(r["rule_text"].strip())}</td>'
                f'<td>{bdi_wrap(r["system_action"].strip())}</td>'
                f'<td><span class="chip {cls}">{label}</span></td>'
                f'<td>{bdi_wrap(src)}</td>'
                f'<td class="own">{html.escape(owner)}</td>'
                f'<td>{refcell}</td>'
                f'</tr>')
        parts.append('</tbody></table></div>')
    return '\n'.join(parts)


def main():
    with open(CSV_PATH, encoding='utf-8-sig') as f:
        rows = [r for r in csv.DictReader(f) if r.get('rule_id')]
    section = build_section(rows)
    doc = HTML_PATH.read_text(encoding='utf-8')
    begin = '<!-- CATALOG:BEGIN — נוצר אוטומטית מ-ICP_LIMS_RULE_CATALOG_he.csv; אין לערוך ידנית -->'
    end = '<!-- CATALOG:END -->'
    i, j = doc.find(begin), doc.find(end)
    if i < 0 or j < 0:
        sys.exit('CATALOG markers not found in workbook HTML')
    new = doc[:i + len(begin)] + '\n' + section + '\n  ' + doc[j:]
    HTML_PATH.write_text(new, encoding='utf-8')
    statuses = {}
    for r in rows:
        statuses[r['normalized_status']] = statuses.get(r['normalized_status'], 0) + 1
    print(f'OK: {len(rows)} rules -> {HTML_PATH.name}; by status: {statuses}')


if __name__ == '__main__':
    main()
