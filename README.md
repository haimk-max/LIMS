# LIMS — בחינת מערכת LIMS למעבדה

ריפו ייעודי לבחינת מערכת ה-LIMS הקיימת של מעבדת כימיה למי שתייה וסביבה (רשות המים), דרך פיילוט ממוקד: אפיון מלא של תהליך הריצה האנליטית ב-**ICP-OES** ובחינתו מול הספק.

**מקור**: הריפו נפתח ב-2026-08-11 והכיל בעבר תיקיית `docs/lims-icp/` בריפו `water-knowledge-system` (שם פותח מ-2026-08-02; אימץ ב-2026-08-03 פרויקט מקביל שנוהל ב-ChatGPT). ראו תעודת המעבר ב-`CLAUDE.md` §0 ו-`docs/lims-icp/START_HERE_he.md` §0.

## מסמכי ניהול

| מסמך | תפקיד |
|---|---|
| [`CLAUDE.md`](CLAUDE.md) | כללי עבודה קבועים לפרויקט + תעודת המעבר מ-water-knowledge-system |
| [`PROCESS.md`](PROCESS.md) | SSOT לדרישות פתוחות/סגורות **של ריפו זה** |
| [`HANDOVER.md`](HANDOVER.md) | זיכרון בין-סשן |

## מסלול ה-ICP-OES (הליבה הפעילה)

| מסמך | תפקיד | מתי לקרוא |
|---|---|---|
| [`docs/lims-icp/START_HERE_he.md`](docs/lims-icp/START_HERE_he.md) | מסמך העוגן: מצב, החלטות, חסמים והמשך | **תחילת כל סשן** על מסלול זה |
| [`docs/lims-icp/ICP_RULE_ENGINE_WORKBOOK_he.html`](docs/lims-icp/ICP_RULE_ENGINE_WORKBOOK_he.html) — v0.3 | חוברת העבודה לצוות המעבדה: תהליך, 12 כרטיסי הכרעה עם טופסי החלטה (D-01…D-12, שישה חסמי-סף), קטלוג 51 הכללים בר-סינון, 7 כללים מועמדים, 9 נקודות התייחסות, נתוני אב | בעבודת הצוות על סגירת האפיון |
| [`docs/lims-icp/ICP_LIMS_RULE_CATALOG_he.csv`](docs/lims-icp/ICP_LIMS_RULE_CATALOG_he.csv) | מקור-האמת המכני לכללים (51 שורות: מזהה, משפחה, נוסח, פעולת מערכת, מעמד, בעלים, מקור) | בכל עדכון כלל — לפני הרצת המחולל |
| [`docs/lims-icp/tools/build_catalog_section.py`](docs/lims-icp/tools/build_catalog_section.py) | מחולל קטע-הקטלוג בחוברת מה-CSV (מונע סטייה בין עותקים). הרצה: `python3 tools/build_catalog_section.py` מתוך `docs/lims-icp/` | אחרי כל עדכון ל-CSV |
| [`docs/lims-icp/sources/SOP_05_ICPOES.docx`](docs/lims-icp/sources/SOP_05_ICPOES.docx) | המקור המקצועי המבוקר (הנוהל הרשמי) | אימות כלל/סף/סתירה |
| [`docs/lims-icp/sources/ICP_EXPORT_EXAMPLE.xlsx`](docs/lims-icp/sources/ICP_EXPORT_EXAMPLE.xlsx) | קובץ ייצוא אמיתי מהמכשיר (Mjr_Metals, 55 מדידות, 11 גיליונות) — הראיה של כרטיס D-01 | מיפוי שדות; אימות טענות על הייצוא |
| [`docs/lims-icp/sources/ICP_OES_lab_workflow_rule_engine_he_v0.2.html`](docs/lims-icp/sources/ICP_OES_lab_workflow_rule_engine_he_v0.2.html) | הגרסה שיובאה מ-ChatGPT — ארכיון | היסטוריה בלבד |
| [`docs/lims-icp/sources/ICP_LIMS_workflow_specification_he_v0.1.docx`](docs/lims-icp/sources/ICP_LIMS_workflow_specification_he_v0.1.docx) | אפיון מוקדם (מודל נתונים, BR-ICP-001…015, תרחישי קבלה) | רקע; ארכיטקטורה מוצעת שונה — ראו נקודת-תשומת-לב A4 בחוברת |

## תשתית תומכת לבחינת הספק

| מסמך | תפקיד |
|---|---|
| [`docs/LIMS_CAPABILITY_MAP.md`](docs/LIMS_CAPABILITY_MAP.md) | מפת יכולות מדורגת למקטע הריצה האנליטית: 47 שורות דרישה בארבע רמות יכולת (תיעוד/חישוב/ניהול/אכיפה), עמדת גבול LIMS⇄CDS, 9 תרחישי הדגמה מחייבים, 18 שאלות מפרט (v1.0, טיוטה לדיון) |
| [`docs/LIMS_VENDOR_FINDINGS.md`](docs/LIMS_VENDOR_FINDINGS.md) | ממצאי בחינת LabWare, LabVantage, SampleManager, STARLIMS ומחלקת המתמחות הסביבתיות: תיוג ראיות פר-טענה, סבב הפרכה אדברסרי, מלכודות רכש והצהרת חפיפה (v1.0, טיוטה לדיון) |

**קשר בין השכבות**: התהליך המאופיין ב-`lims-icp/` הוא ה"מטען" שממלא את תרחישי ההדגמה (D1–D9) ושאלות המפרט (S1–S18) שבמפת היכולות בתוכן אמיתי — לקראת חבילת בחינה מול הספק הקיים.
