# -*- coding: utf-8 -*-
"""Static site generator for b-economics.com.

Usage:  python3 tools/build.py
Writes every page into the repository root (folders with index.html),
so GitHub Pages can serve the existing URLs unchanged.
"""
import os, json, html, datetime
from urllib.parse import quote
from content import *

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = datetime.date.today().isoformat()
PAGES = []  # for sitemap
E = html.escape

def url(path):
    return SITE["domain"] + quote(path)

def case_path(key):
    return "/client/" + CASES[key]["slug"] + "/"

def article_path(a):
    return "/" + a["slug"] + "/"

NAV = [
    ("/service/behavior/", "כלכלה התנהגותית"),
    ("/service/financial-advice-service/", "ייעוץ כלכלי"),
    ("/service/economic-opinion/", "חוות דעת"),
    ("/לקוחות/", "פרויקטים"),
    ("/מרכז-ידע/", "מרכז ידע"),
    ("/about-us/", "אודות"),
]
NAV_GROUPS = {  # which top item is "current" for sub pages
    "/service/התאמת-מוצר-לשוק/": "/service/behavior/",
    "/service/אפיון-ui-ux/": "/service/behavior/",
    "/service/הרצאות-וסדנאות/": "/service/behavior/",
    "/שאלות-ותשובות/": "/about-us/",
}

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700&family=Frank+Ruhl+Libre:wght@500;700&display=swap" rel="stylesheet">')

WA_SVG = '<svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="currentColor" style="vertical-align:-3px;margin-inline-end:6px"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.8-1.3a.5.5 0 0 0 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.1 5.1 0 0 0 1.1 2.7 11.6 11.6 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.6 2.6 0 0 0 1.7-1.2 2.1 2.1 0 0 0 .2-1.2c-.1-.1-.3-.2-.5-.3z"/></svg>'


def header(path):
    cur = NAV_GROUPS.get(path, path)
    if path.startswith("/client/"):
        cur = "/לקוחות/"
    if any(path == article_path(a) for a in ARTICLES):
        cur = "/מרכז-ידע/"
    links = "".join(
        f'<a href="{p}"{" aria-current=\"page\"" if p == cur else ""}>{E(t)}</a>' for p, t in NAV)
    return f"""<a class="skip" href="#main">דילוג לתוכן</a>
<header class="site-header"><div class="wrap">
<a class="brand" href="/" aria-label="BEconomics, עמוד הבית"><img src="/assets/img/logo.svg" alt="BEconomics" width="176" height="44"></a>
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="site-nav">תפריט</button>
<nav class="nav" id="site-nav" aria-label="ראשי">{links}<a class="nav-cta" href="#contact">יצירת קשר</a></nav>
</div></header>"""


def contact_section():
    return f"""<section class="contact section" id="contact" aria-labelledby="contact-title"><div class="wrap">
<div>
<h2 id="contact-title">בואו נדבר</h2>
<p>ספרו לנו בקצרה מה האתגר. נחזור אליכם כדי לקבוע שיחת היכרות קצרה, בלי התחייבות.</p>
<ul class="contact-lines">
<li><a href="mailto:{SITE['email']}">{SITE['email']}</a><span>אימייל</span></li>
<li><a href="https://wa.me/{SITE['whatsapp']}" rel="noopener">{WA_SVG}{SITE['whatsapp_display']}</a><span>וואטסאפ</span></li>
<li><a href="{SITE['linkedin']}" rel="noopener">ד"ר טיראן רוטמן ב-LinkedIn</a><span>LinkedIn</span></li>
</ul>
</div>
<form id="contact-form" action="https://formsubmit.co/ajax/{SITE['email']}" method="POST" novalidate>
<input type="hidden" name="_subject" value="פנייה חדשה מאתר BEconomics">
<input type="hidden" name="_template" value="table">
<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
<div class="form-row">
<div class="field"><label for="f-name">שם</label><input id="f-name" name="שם" autocomplete="name" required></div>
<div class="field"><label for="f-phone">טלפון</label><input id="f-phone" name="טלפון" type="tel" autocomplete="tel" dir="ltr"></div>
</div>
<div class="field"><label for="f-email">אימייל</label><input id="f-email" name="email" type="email" autocomplete="email" dir="ltr" required></div>
<div class="field"><label for="f-msg">במה נוכל לעזור?</label><textarea id="f-msg" name="הודעה" required></textarea></div>
<button class="btn btn-primary" type="submit">שליחת ההודעה</button>
<p class="form-status" role="status" aria-live="polite"></p>
</form>
</div></section>"""


def footer():
    beh = "".join(f'<li><a href="{SERVICES[k]["path"]}">{E(SERVICES[k]["title"])}</a></li>' for k in BEHAVIOR_SERVICES)
    fin = (f'<li><a href="{SERVICES["finance"]["path"]}">{E(SERVICES["finance"]["title"])}</a></li>'
           f'<li><a href="{OPINION["path"]}">חוות דעת כלכלית</a></li>')
    more = ('<li><a href="/לקוחות/">פרויקטים</a></li><li><a href="/מרכז-ידע/">מרכז ידע</a></li>'
            '<li><a href="/שאלות-ותשובות/">שאלות ותשובות</a></li><li><a href="/about-us/">אודות</a></li>'
            '<li><a href="/הצהרת-נגישות/">הצהרת נגישות</a></li>')
    year = datetime.date.today().year
    return f"""<footer class="site-footer"><div class="wrap">
<div class="footer-grid">
<div><a class="brand" href="/"><img src="/assets/img/logo.svg" alt="BEconomics" width="152" height="38"></a>
<p>כלכלה התנהגותית, ייעוץ כלכלי וחוות דעת מומחה. משלבים כלכלה, פסיכולוגיה, נוירוכלכלה ועיצוב מוצר, במגזר העסקי ובמשרדי ממשלה.</p></div>
<div><h2>כלכלה התנהגותית</h2><ul>{beh}</ul></div>
<div><h2>ייעוץ כלכלי</h2><ul>{fin}</ul></div>
<div><h2>עוד באתר</h2><ul>{more}</ul></div>
</div>
<div class="footer-bottom"><span>© {year} BEconomics. כל הזכויות שמורות.</span><span>האתר האישי של ד"ר טיראן רוטמן: <a href="{SITE['personal']}">tiranrothman.com</a></span></div>
</div></footer>"""


def page(path, title, description, main, *, show_contact=True, jsonld=None, og_type="website"):
    full_title = f"{title} | BEconomics" if path != "/" else f"BEconomics | {SITE['tagline']}"
    ld = ""
    if jsonld:
        ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>'
    canonical = url(path)
    doc = f"""<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(full_title)}</title>
<meta name="description" content="{E(description)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="he_IL">
<meta property="og:site_name" content="BEconomics">
<meta property="og:title" content="{E(full_title)}">
<meta property="og:description" content="{E(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE['domain']}/assets/img/social-card.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#12303a">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.png" sizes="192x192">
{FONTS}
<link rel="stylesheet" href="/assets/site.css">
{ld}
</head>
<body>
{header(path)}
<main id="main">
{main}
</main>
{contact_section() if show_contact else ""}
{footer()}
<script src="/assets/site.js" defer></script>
</body>
</html>
"""
    out = os.path.join(ROOT, path.strip("/"), "index.html") if path != "/" else os.path.join(ROOT, "index.html")
    if path == "/404/":
        out = os.path.join(ROOT, "404.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)
    if path != "/404/":
        PAGES.append(path)


def page_head(title, lead, crumbs, extra=""):
    c = " / ".join(f'<a href="{p}">{E(t)}</a>' for p, t in crumbs)
    return f"""<div class="page-head"><div class="wrap">
<p class="crumbs"><a href="/">ראשי</a>{" / " + c if c else ""}</p>
<h1>{E(title)}</h1>
{f'<p class="lead">{E(lead)}</p>' if lead else ""}{extra}
</div></div>"""


def ledger(keys):
    rows = []
    for k in keys:
        c = CASES[k]
        kind = "חוות דעת מומחה" if c["kind"] == "opinion" else "כלכלה התנהגותית"
        rows.append(f"""<a class="ledger-row" href="{case_path(k)}">
<span class="ledger-client">{E(c['client'])}<span class="ledger-kind">{kind}</span></span>
<span class="ledger-title">{E(c['title'])}</span>
<span class="ledger-result">{E(c['result_short'])}<small>{E(c['result_note'])}</small></span>
</a>""")
    return '<div class="ledger">' + "".join(rows) + "</div>"


def case_tiles(keys):
    out = []
    for k in keys:
        c = CASES[k]
        out.append(f"""<li><a class="tile" href="{case_path(k)}">
<span class="logo-slot"><img src="/assets/img/{c['logo']}" alt="" loading="lazy"></span>
<span class="kind">{E(c['client'])}</span>
<h3>{E(c['title'])}</h3>
<p>{E(c['summary'])}</p>
</a></li>""")
    return '<ul class="grid-list">' + "".join(out) + "</ul>"


def aside_services(current):
    items = []
    for k in BEHAVIOR_SERVICES + ["finance"]:
        s = SERVICES[k]
        cur = ' aria-current="page"' if s["path"] == current else ""
        items.append(f'<li><a href="{s["path"]}"{cur}>{E(s["title"])}</a></li>')
    cur = ' aria-current="page"' if OPINION["path"] == current else ""
    items.append(f'<li><a href="{OPINION["path"]}"{cur}>חוות דעת כלכלית</a></li>')
    return f'<aside class="aside" aria-label="שירותים"><h2>השירותים שלנו</h2><ul>{"".join(items)}</ul></aside>'


ORG_LD = {
    "@context": "https://schema.org",
    "@type": "ProfessionalService",
    "name": "BEconomics",
    "url": SITE["domain"] + "/",
    "logo": SITE["domain"] + "/assets/img/logo.png",
    "description": "כלכלה התנהגותית יישומית, ייעוץ כלכלי ופיננסי וחוות דעת כלכליות לבתי משפט.",
    "email": SITE["email"],
    "areaServed": "IL",
    "founder": {"@type": "Person", "name": "Dr. Tiran Rothman", "alternateName": "ד\"ר טיראן רוטמן",
                "url": SITE["personal"], "sameAs": [SITE["linkedin"]]},
}

# ================================================================ HOME
def build_home():
    beh_links = "".join(
        f'<li><a href="{SERVICES[k]["path"]}">{E(SERVICES[k]["title"])}<span>{E(SERVICES[k]["short"])}</span></a></li>'
        for k in BEHAVIOR_SERVICES)
    fin_links = (f'<li><a href="{SERVICES["finance"]["path"]}">תוכניות עסקיות והערכות שווי<span>{E(SERVICES["finance"]["short"])}</span></a></li>'
                 f'<li><a href="{OPINION["path"]}">חוות דעת כלכלית לבית משפט<span>{E(OPINION["short"])}</span></a></li>')
    steps = "".join(f"<li><h3>{E(t)}</h3><p>{E(d)}</p></li>" for t, d in PROCESS)
    logos = "".join(f'<li><img src="/assets/img/{f}" alt="{E(n)}" loading="lazy"></li>' for f, n in CLIENT_LOGOS)
    facts = "".join(f"<li>{E(x)}</li>" for x in ABOUT["facts"][:4])
    main = f"""
<section class="hero" aria-labelledby="hero-title"><div class="wrap">
<div>
<h1 id="hero-title">{E(SITE['tagline'])}</h1>
<p class="lead">בודקים איך אנשים מחליטים בפועל, מעצבים התערבות ומודדים אותה בשטח מול קבוצת ביקורת. אותה משמעת מחקרית עומדת גם מאחורי חוות הדעת הכלכליות שלנו לבתי משפט ומאחורי הערכות השווי.</p>
<div class="hero-actions"><a class="btn btn-primary" href="#contact">לתיאום שיחת היכרות</a><a class="btn btn-ghost" href="/לקוחות/">לפרויקטים</a></div>
</div>
<figure class="readout" aria-labelledby="readout-title">
<p class="readout-title" id="readout-title">ניסוי שטח: נטישת לקוחות בבנק</p>
<p class="readout-sub">64 בנקאים, חודש אחד. מדד נטישה, תקופת ההשוואה = 100</p>
<div class="bar"><div class="bar-label"><span>תקופה מקבילה, לפני הניסוי</span><b>100</b></div><div class="bar-track"><div class="bar-fill" style="--w:100%"></div></div></div>
<div class="bar"><div class="bar-label"><span>חודש הניסוי</span><b>פחות מ-80</b></div><div class="bar-track"><div class="bar-fill is-treat" style="--w:79%"></div></div></div>
<div class="bar"><div class="bar-label"><span>החודשים שאחרי, מול הממוצע השנתי</span><b>69</b></div><div class="bar-track"><div class="bar-fill is-treat" style="--w:69%"></div></div></div>
<figcaption class="readout-note">ירידה של יותר מ-20% בנטישה בחודש הניסוי, ו-31% מתחת לממוצע השנתי אחריו. <a href="{case_path('leumi')}">למקרה המלא</a></figcaption>
</figure>
</div></section>

<section class="section" aria-labelledby="what-title"><div class="wrap">
<div class="section-head"><h2 id="what-title">שני תחומים, שיטה אחת</h2>
<p>בשני התחומים אנחנו עובדים מנתונים, מנסחים הנחות במפורש ובודקים אותן. ההבדל הוא בשאלה: בצד אחד, איך לשנות החלטות של אנשים. בצד השני, כמה משהו שווה, ומה גרם לנזק.</p></div>
<div class="pillars">
<div class="pillar"><h3>כלכלה התנהגותית יישומית</h3><p>ניסויי שטח, עיצוב מוצר ותקשורת שמבוססים על האופן שבו לקוחות, משתמשים ואזרחים מחליטים בפועל.</p><ul class="link-list">{beh_links}</ul></div>
<div class="pillar"><h3>ייעוץ כלכלי ופיננסי</h3><p>תוכניות עסקיות, בדיקות כדאיות, הערכות שווי וחוות דעת מומחה בהליכים משפטיים, כולל תביעות ייצוגיות.</p><ul class="link-list">{fin_links}</ul></div>
</div>
</div></section>

<section class="section section-alt" aria-labelledby="process-title"><div class="wrap">
<div class="section-head"><h2 id="process-title">איך עובד פרויקט התנהגותי</h2></div>
<ol class="steps">{steps}</ol>
</div></section>

<section class="section" aria-labelledby="results-title"><div class="wrap">
<div class="section-head"><h2 id="results-title">מה יצא מזה</h2><p>חלק מהפרויקטים האחרונים, בחוות דעת מומחה ובכלכלה התנהגותית.</p></div>
{ledger(HOME_LEDGER)}
<p style="margin-top:24px"><a href="/לקוחות/">לכל הפרויקטים</a></p>
</div></section>

<section class="section-tight" aria-labelledby="clients-title"><div class="wrap">
<h2 id="clients-title" style="font-size:1.5rem">עבדנו עם</h2>
<ul class="logos" style="padding:0">{logos}</ul>
<p class="logos-note">ארגונים שעבדנו עבורם או איתם. השמות מוצגים לשם הקשר בלבד.</p>
</div></section>

<section class="section section-alt" aria-labelledby="about-title"><div class="wrap person">
<img src="/assets/img/tiran-rothman.jpg" alt="ד&quot;ר טיראן רוטמן" width="720" height="840" loading="lazy">
<div>
<h2 id="about-title">ד"ר טיראן רוטמן</h2>
<p class="lead" style="font-size:1.1rem">מייסד BEconomics. כלכלן, חוקר כלכלה התנהגותית ומחבר הספר Valuations of Early-Stage Companies and Disruptive Technologies (Palgrave Macmillan, 2020).</p>
<ul class="facts">{facts}</ul>
<p><a href="/about-us/">עוד על ד"ר רוטמן ועל רשת המומחים</a></p>
</div>
</div></section>
"""
    page("/", SITE["tagline"],
         "BEconomics: כלכלה התנהגותית יישומית, ניסויי שטח, ייעוץ כלכלי, הערכות שווי וחוות דעת כלכליות לבתי משפט. בהובלת ד\"ר טיראן רוטמן.",
         main, jsonld=ORG_LD)


# ================================================================ SERVICES
def build_services():
    for key, s in SERVICES.items():
        crumbs = [("/service/behavior/", "כלכלה התנהגותית")] if key in BEHAVIOR_SERVICES and key != "behavior" else []
        if key == "talks":
            body = ""
            for t in TALKS:
                meta = "".join(f"<div><dt>{E(a)}:</dt><dd>{E(b)}</dd></div>" for a, b in t["meta"])
                body += f'<div class="talk"><h2 style="font-size:1.5rem">{E(t["title"])}</h2><dl>{meta}</dl><p>{E(t["text"])}</p></div>'
            body += '<p style="margin-top:24px">להזמנת הרצאה, כתבו לנו את סוג הקהל, מספר המשתתפים והמועד המבוקש, בטופס למטה.</p>'
        else:
            body = s["body"]
        cases = ""
        if s["cases"]:
            cases = f'<h2 class="group-title" style="margin-top:56px">פרויקטים לדוגמה</h2>{case_tiles(s["cases"])}'
        main = page_head(s["title"], s["lead"], crumbs) + f"""
<div class="section"><div class="wrap cols">
<div><div class="prose">{body}</div>{cases}</div>
{aside_services(s['path'])}
</div></div>"""
        page(s["path"], s["title"], s["lead"], main)

    # behavioral hub gets an extra overview list of the four services at top of body: already in aside


# ================================================================ EXPERT OPINION
def build_opinion():
    o = OPINION
    areas = [
        ("אומדן נזק בחברות ציבוריות", "ניתוח אירוע (Event Study) לבחינת ההשפעה של הודעה או פעולה על מחיר המניה, ואמידת הנזק לבעלי המניות."),
        ("הערכות שווי לחברות טכנולוגיה", "חברות הייטק צעירות ובוגרות, כולל בתחומי מדעי החיים, סייבר, תחבורה חכמה ואנרגיה."),
        ("סכסוכי שותפים ומשקיעים", "מחלוקות על גיוסי הון, על שווי ועל זכויות משקיעים, כולל מכשירים כמו SAFE ואג\"ח להמרה."),
        ("מדעי החיים", "פיתוח תרופות ומכשור רפואי, השפעות של רגולציה רפואית ושל הודעות FDA על הפעילות הכלכלית ועל גיוסי הון."),
        ("מימון התנהגותי", "פסיכולוגיה של משקיעים בשוק ההון וציפיות משקיעים, כשהשאלה המשפטית תלויה באופן שבו משקיעים מגיבים למידע."),
    ]
    area_html = "".join(f"<li><strong>{E(a)}.</strong> {E(b)}</li>" for a, b in areas)
    body = f"""
<p>ד"ר טיראן רוטמן מכין חוות דעת כלכליות ופיננסיות מטעם הצדדים, ומשמש גם מומחה מטעם בית המשפט, ברשימת המומחים של בית המשפט המחוזי.</p>
<h2>תחומי מומחיות</h2>
<ul>{area_html}</ul>

<h2>ניתוח אירוע (Event Study): איך אומדים נזק</h2>
<p>בעל מניות בחברה נסחרת שטוען שהחזקה שלו נפגעה בגלל פעולה או הודעה של החברה, צריך להראות שתי עובדות: שמחיר המניה זז בגלל האירוע, ולא בגלל השוק או הענף, ובכמה. ניתוח אירוע הוא השיטה המקובלת לכך.</p>
<div class="method">
<dl>
<dt>חלון האומדן</dt><dd>תקופה לפני האירוע, שבה לומדים איך המניה מתנהגת בדרך כלל ביחס לשוק.</dd>
<dt>חלון האירוע</dt><dd>הימים שסביב ההודעה או הפעולה, שבהם בודקים אם המניה סטתה מההתנהגות הרגילה שלה.</dd>
<dt>תשואה חריגה (AR)</dt><dd>ההפרש בין התשואה בפועל (לוגריתמית) לבין התשואה שהייתה צפויה בלי האירוע.</dd>
</dl>
<p style="margin:16px 0 4px">את התשואה הצפויה אומדים בשתי שיטות, כבדיקת חוסן:</p>
<ul>
<li><strong>מודל מתואם שוק:</strong> התשואה הצפויה שווה לתשואת מדד הייחוס. זו גישה פשוטה, ש"מניחה" שהמניה זזה אחד לאחד עם השוק.</li>
<li><strong>מודל השוק:</strong> אומדים ברגרסיה ליניארית בחלון האומדן את הפרמטרים α ו-β של המניה ביחס למדד, ומהם גוזרים את התשואה הצפויה. כך מביאים בחשבון שמניה מסוכנת יותר זזה בעוצמה רבה יותר מהשוק.</li>
</ul>
<p class="formula">AR<sub>t</sub> = R<sub>t</sub> − (α̂ + β̂·R<sub>m,t</sub>)</p>
<p style="margin:0">כל שיטה מורצת גם מול מדד השוק הכללי וגם מול מדד הענף, כלומר ארבעה אומדנים בסך הכל. המובהקות נבחנת ביחס לתנודתיות הרגילה של המניה בחלון האומדן, כדי להפריד בין תגובה לאירוע לבין רעש רגיל, ולוודא שאין אירוע מקביל שמסביר את התנועה.</p>
</div>
<p>מספר מובהק לבדו לא מספיק. חוות דעת טובה מסבירה גם את ההיגיון הכלכלי: למה האירוע היה אמור להשפיע, ואיך משקיעים מגיבים בפועל למידע מסוגו. כאן נכנס הצד ההתנהגותי. השאלה אם משקיעים "הבינו" הודעה, הגיבו אליה בעוצמה רבה מדי או לאט מדי, היא לעיתים קרובות לב המחלוקת.</p>

<h2>הערכות שווי בהליכים משפטיים</h2>
<p>הערכת שווי לצורכי הליך משפטי, או ביקורת על הערכת שווי של הצד שכנגד, נבחנת לפי שאלה אחת: האם ההנחות מוצגות במפורש ואפשר לבדוק אותן. בתחזיות של הנהלות יש לרוב שתי הטיות חוזרות: אופטימיות יתר ועיגון למחיר של סבב קודם או של עסקה קודמת. חוות הדעת מראה כמה השווי רגיש להן.</p>
"""
    main = page_head(o["title"], o["lead"], [("/service/financial-advice-service/", "ייעוץ כלכלי")]) + f"""
<div class="section"><div class="wrap cols">
<div><div class="prose">{body}</div>
<h2 class="group-title" style="margin-top:56px">חוות דעת לדוגמה</h2>{case_tiles(OPINION_CASES)}</div>
{aside_services(o['path'])}
</div></div>"""
    page(o["path"], o["title"], o["lead"], main)


# ================================================================ CASES
def build_cases():
    for k, c in CASES.items():
        meta = "".join(f"<li>{E(a)}: <b>{E(b)}</b></li>" for a, b in c["meta"])
        blocks = "".join(f'<div class="case-block"><h2>{E(h)}</h2><p>{E(t)}</p></div>' for h, t in c["blocks"])
        blocks += f'<div class="case-block"><h2>התוצאה</h2><div class="result-box"><p>{E(c["result"])}</p></div></div>'
        group = OPINION_CASES if c["kind"] == "opinion" else BEHAVIOR_CASES
        others = [x for x in group if x != k][:3]
        svc = (OPINION["path"], "חוות דעת כלכלית") if c["kind"] == "opinion" else ("/service/behavior/", "שינוי התנהגות צרכנית")
        main = page_head(c["title"], c["summary"], [("/לקוחות/", "פרויקטים")],
                         extra=f'<ul class="case-meta">{meta}</ul>') + f"""
<div class="section"><div class="wrap cols">
<div class="prose">{blocks}</div>
<aside class="aside" aria-label="קשור"><h2>שירות</h2><ul><li><a href="{svc[0]}">{E(svc[1])}</a></li></ul>
<h2 style="margin-top:22px">פרויקטים נוספים</h2><ul>{"".join(f'<li><a href="{case_path(x)}">{E(CASES[x]["title"])}</a></li>' for x in others)}</ul></aside>
</div></div>"""
        page(case_path(k), c["title"], c["summary"] + " " + c["result"][:120], main, og_type="article")

    # projects index
    main = page_head("פרויקטים", "חלק מהעבודה שלנו בשני התחומים. בחלק מחוות הדעת שם הלקוח לא מוצג, מטעמי חיסיון.", []) + f"""
<div class="section"><div class="wrap">
<h2 class="group-title">חוות דעת כלכליות לבתי משפט</h2>{case_tiles(OPINION_CASES)}
<h2 class="group-title">כלכלה התנהגותית יישומית</h2>{case_tiles(BEHAVIOR_CASES)}
</div></div>"""
    page("/לקוחות/", "פרויקטים", "חוות דעת כלכליות לבתי משפט ופרויקטים בכלכלה התנהגותית: בנק לאומי, בנק ישראל, המשרד להגנת הסביבה, רשות המים, כללית ועוד.", main)


# ================================================================ ABOUT, FAQ
def build_about():
    facts = "".join(f"<li>{E(x)}</li>" for x in ABOUT["facts"])
    intro = "".join(f"<p>{E(p)}</p>" for p in ABOUT["intro"])
    experts = "".join(f"""<div class="expert"><img src="/assets/img/{x['img']}" alt="{E(x['name'])}" width="96" height="96" loading="lazy">
<div><h3>{E(x['name'])}</h3><p class="role">{E(x['role'])}</p><p>{E(x['text'])}</p></div></div>""" for x in EXPERTS)
    main = page_head("אודות", "BEconomics נוסדה כדי לחבר בין ייעוץ אסטרטגי ופיננסי לבין מחקר מדעי.", []) + f"""
<section class="section"><div class="wrap person">
<img src="/assets/img/tiran-rothman.jpg" alt="ד&quot;ר טיראן רוטמן" width="720" height="840">
<div class="prose"><h2>ד"ר טיראן רוטמן, PhD, MBA</h2>{intro}<ul class="facts">{facts}</ul>
<p>{E(ABOUT['book'])} <a href="https://link.springer.com/book/10.1007/978-3-030-38847-8" rel="noopener">לעמוד הספר</a></p>
<p>עוד על המחקר וההרצאות: <a href="{SITE['personal']}">tiranrothman.com</a></p></div>
</div></section>
<section class="section section-alt" aria-labelledby="experts-title"><div class="wrap">
<div class="section-head"><h2 id="experts-title">רשת המומחים</h2><p>חוקרים מהאקדמיה שמצטרפים לפרויקטים לפי הצורך, כדי לבנות פתרונות מבוססי ניסוי לחברות ולגופים ממשלתיים.</p></div>
<div class="experts">{experts}</div>
</div></section>"""
    person = {"@context": "https://schema.org", "@type": "Person", "name": "Dr. Tiran Rothman", "alternateName": "ד\"ר טיראן רוטמן",
              "jobTitle": "Economist, founder of BEconomics", "url": SITE["personal"], "worksFor": {"@type": "Organization", "name": "BEconomics"},
              "sameAs": [SITE["linkedin"], SITE["personal"]]}
    page("/about-us/", "אודות", "ד\"ר טיראן רוטמן, מייסד BEconomics, ורשת המומחים: פרופ' אייל פאר, פרופ' מוסי רוזנבוים, ד\"ר דייבי דישטניק וד\"ר גלית ולנר.", main, jsonld=person)


def build_faq():
    items = "".join(f'<details><summary>{E(q)}</summary><div class="answer">{a}</div></details>' for q, a in FAQ)
    main = page_head("שאלות ותשובות", "מה זה כלכלה התנהגותית יישומית, כמה זה עולה וכמה זמן לוקח.", []) + f"""
<div class="section"><div class="wrap"><div class="faq">{items}</div></div></div>"""
    import re
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in FAQ]}
    page("/שאלות-ותשובות/", "שאלות ותשובות", "שאלות נפוצות על כלכלה התנהגותית יישומית: ההבדל משיווק, עלות, משך ותוצאות.", main, jsonld=ld)


# ================================================================ KNOWLEDGE
def build_knowledge():
    tiles = "".join(f"""<li><a class="tile" href="{article_path(a)}"><h3>{E(a['title'])}</h3><p>{E(a['summary'])}</p></a></li>""" for a in ARTICLES)
    main = page_head("מרכז ידע", "מבוא לכלכלה התנהגותית, לעקרונות שלה וליישומים שלה, ורשימת קריאה למי שרוצה להעמיק.", []) + f"""
<div class="section"><div class="wrap"><ul class="grid-list">{tiles}</ul></div></div>"""
    page("/מרכז-ידע/", "מרכז ידע", "מאמרים על כלכלה התנהגותית: מהי, העקרונות, תיאוריית הדחיפה, מימון התנהגותי ותובנות מחיי היומיום.", main)

    for a in ARTICLES:
        if a["body"] is None:
            body = "<p>מאמרים וספרים שעיצבו את הכלכלה ההתנהגותית, למי שרוצה לקרוא את המקורות.</p>" + \
                   '<ol class="refs" lang="en">' + "".join(f"<li>{r}</li>" for r in REFERENCES) + "</ol>"
        else:
            body = a["body"]
        others = [x for x in ARTICLES if x is not a][:4]
        main = page_head(a["title"], a["summary"], [("/מרכז-ידע/", "מרכז ידע")]) + f"""
<div class="section"><div class="wrap cols">
<article class="prose">{body}</article>
<aside class="aside" aria-label="מאמרים נוספים"><h2>עוד במרכז הידע</h2><ul>{"".join(f'<li><a href="{article_path(x)}">{E(x["title"])}</a></li>' for x in others)}</ul></aside>
</div></div>"""
        ld = {"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "inLanguage": "he",
              "author": {"@type": "Person", "name": "Dr. Tiran Rothman"}, "publisher": {"@type": "Organization", "name": "BEconomics"}}
        page(article_path(a), a["title"], a["summary"], main, jsonld=ld, og_type="article")


# ================================================================ ACCESSIBILITY, 404
def build_misc():
    main = page_head("הצהרת נגישות", "", []) + f"""
<div class="section"><div class="wrap prose">
<p>אנחנו רואים חשיבות בכך שהאתר יהיה נגיש לכל אדם, כולל אנשים עם מוגבלות. האתר נבנה בהתאם להנחיות WCAG 2.1 ברמה AA ולתקן הישראלי 5568, ככל שהדבר ניתן.</p>
<h2>מה עשינו</h2>
<ul>
<li>מבנה כותרות היררכי וסימון סמנטי של אזורי העמוד.</li>
<li>ניווט מלא במקלדת, עם סימון בולט של הרכיב המסומן וקישור לדילוג לתוכן.</li>
<li>טקסט חלופי לתמונות בעלות משמעות.</li>
<li>ניגודיות צבעים מספקת, ותמיכה בהגדלת טקסט בדפדפן עד 200% בלי אובדן תוכן.</li>
<li>כיבוי אנימציות למי שהגדיר זאת במערכת ההפעלה, ותמיכה במצב כהה.</li>
<li>טופס יצירת קשר עם תוויות לכל שדה והודעות מצב שקוראי מסך מקריאים.</li>
</ul>
<h2>נתקלתם בבעיה?</h2>
<p>אם משהו באתר לא נגיש לכם, נשמח לדעת ולתקן. כתבו ל-<a href="mailto:{SITE['email']}">{SITE['email']}</a> או בוואטסאפ ל-{SITE['whatsapp_display']}, ופרטו את העמוד והבעיה.</p>
<p>ההצהרה עודכנה בתאריך {datetime.date.today().strftime('%d.%m.%Y')}.</p>
</div></div>"""
    page("/הצהרת-נגישות/", "הצהרת נגישות", "הצהרת הנגישות של אתר BEconomics.", main)

    main = page_head("העמוד לא נמצא", "ייתכן שהכתובת השתנתה כשהאתר עודכן.", []) + """
<div class="section"><div class="wrap prose">
<p>אפשר לחזור ל<a href="/">עמוד הבית</a>, לעבור ל<a href="/לקוחות/">פרויקטים</a> או ל<a href="/מרכז-ידע/">מרכז הידע</a>, או לכתוב לנו בטופס למטה ונעזור למצוא את מה שחיפשתם.</p>
</div></div>"""
    page("/404/", "העמוד לא נמצא", "העמוד לא נמצא.", main)


def build_meta_files():
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in PAGES:
        sm.append(f"<url><loc>{url(p)}</loc><lastmod>{TODAY}</lastmod></url>")
    sm.append("</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(sm) + "\n")
    open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE['domain']}/sitemap.xml\n")
    open(os.path.join(ROOT, "CNAME"), "w").write("b-economics.com\n")
    open(os.path.join(ROOT, ".nojekyll"), "w").write("")
    lines = ["# BEconomics", "", "> כלכלה התנהגותית יישומית, ייעוץ כלכלי ופיננסי וחוות דעת כלכליות לבתי משפט, בהובלת ד\"ר טיראן רוטמן.", "",
             "## Services"]
    for k in BEHAVIOR_SERVICES + ["finance"]:
        lines.append(f"- [{SERVICES[k]['title']}]({url(SERVICES[k]['path'])}): {SERVICES[k]['short']}")
    lines.append(f"- [{OPINION['title']}]({url(OPINION['path'])}): {OPINION['short']}")
    lines += ["", "## Case studies"] + [f"- [{c['title']}]({url(case_path(k))}): {c['summary']}" for k, c in CASES.items()]
    lines += ["", "## Knowledge center"] + [f"- [{a['title']}]({url(article_path(a))}): {a['summary']}" for a in ARTICLES]
    lines += ["", "## About", f"- [About]({url('/about-us/')})", f"- Founder's personal site: {SITE['personal']}", ""]
    open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8").write("\n".join(lines))


if __name__ == "__main__":
    build_home(); build_services(); build_opinion(); build_cases()
    build_about(); build_faq(); build_knowledge(); build_misc(); build_meta_files()
    print(f"built {len(PAGES)} pages")
