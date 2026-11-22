#!/usr/bin/env python3
"""One-off generator for the Volan static site. Output is plain HTML committed to the repo."""
import json, os, sys, html, hashlib
OUT = sys.argv[1]
SITE = "https://volanpremiumtransfers.com"
PHONE = "+35799335570"; PHONE_H = "+357 99 335570"
EMAIL = "info@volanminibus.com"
WA = "https://wa.me/35799335570"
LASTMOD = "2026-11-20"
BIZ_ID = SITE + "/#business"
def ver(f): return hashlib.md5(open(os.path.join(OUT, f), "rb").read()).hexdigest()[:8]
CSS_V = ver("assets/css/site.css"); JS_V = ver("assets/js/site.js")

ICONS = {
 "plane": '<path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "shield": '<path d="M12 3 4 6v6c0 5 3.4 8.4 8 9 4.6-.6 8-4 8-9V6z"/><path d="m9 12 2 2 4-4"/>',
 "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.6-3.6 3.3-5.5 6.5-5.5s5.9 1.9 6.5 5.5"/><circle cx="17" cy="9" r="2.6"/><path d="M16.5 14.6c2.7.2 4.5 1.9 5 4.9"/>',
 "chat": '<path d="M21 12a8.5 8.5 0 0 1-12.6 7.4L3 21l1.6-5.2A8.5 8.5 0 1 1 21 12z"/><path d="M8.5 11h.01M12 11h.01M15.5 11h.01"/>',
 "check": '<path d="M20 6 9 17l-5-5"/>',
 "map": '<path d="M12 21s-7-6.1-7-11.5A7 7 0 0 1 19 9.5C19 14.9 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
 "brief": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M3 13h18"/>',
 "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
 "baby": '<circle cx="12" cy="6" r="3"/><path d="M8 21v-5l-2-3 3-3h6l3 3-2 3v5"/>',
 "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
 "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
 "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
 "bus": '<rect x="4" y="3" width="16" height="15" rx="3"/><path d="M4 11h16M8 18v3M16 18v3M8 14.5h.01M16 14.5h.01"/>',
 "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
 "wine": '<path d="M8 3h8l-.5 6a3.5 3.5 0 0 1-7 0zM12 12.5V20M8.5 20h7"/>',
 "star": '<path d="m12 3 2.8 5.7 6.2.9-4.5 4.4 1.1 6.2L12 17.3 6.4 20.2l1.1-6.2L3 9.6l6.2-.9z"/>',
}
def ic(name, cls="icon"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'

NAV = [
 ("/larnaca-airport-transfers/", "Larnaca Airport"),
 ("/paphos-airport-transfers/", "Paphos Airport"),
 ("/private-tours-cyprus/", "Private Tours"),
 ("/group-bus-hire-cyprus/", "Groups &amp; Buses"),
 ("/#faq", "FAQ"),
]
ALL_PAGES = [
 ("/larnaca-airport-transfers/", "Larnaca Airport transfers"),
 ("/paphos-airport-transfers/", "Paphos Airport transfers"),
 ("/ayia-napa-protaras-transfers/", "Ayia Napa &amp; Protaras transfers"),
 ("/limassol-transfers/", "Limassol transfers"),
 ("/private-tours-cyprus/", "Private minibus tours"),
 ("/group-bus-hire-cyprus/", "Group transfers &amp; bus hire"),
]

def head(title, desc, path, extra_ld, preload_hero=False):
    url = SITE + path
    pre = ('<link rel="preload" as="image" href="/assets/img/van-coast-960.webp" '
           'imagesrcset="/assets/img/van-coast-640.webp 640w, /assets/img/van-coast-960.webp 960w, /assets/img/van-coast-1536.webp 1536w" imagesizes="100vw" fetchpriority="high">') if preload_hero else ""
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False, indent=1)}</script>' for x in extra_ld)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#0b1f3a">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Volan Premium Transfers">
<meta property="og:locale" content="en_GB">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/img/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Volan Premium Transfers – airport and private minibus transfers in Cyprus">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE}/assets/img/og-image.jpg">
{pre}
<link rel="stylesheet" href="/assets/css/site.css?v={CSS_V}">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-36GFT8VNKB"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-36GFT8VNKB');</script>
{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
'''

def header(path):
    links = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if h == path else ""}>{t}</a>' for h, t in NAV)
    return f'''<header class="site-header">
 <div class="wrap nav">
  <a class="brand" href="/">
   <picture><source srcset="/assets/img/logo-96.webp" type="image/webp"><img src="/assets/img/logo-96.png" width="44" height="44" alt=""></picture>
   <span><b>Volan</b><small>Premium Transfers</small></span>
  </a>
  <button class="menu-toggle" type="button" aria-controls="menu" aria-expanded="false" aria-label="Open menu">{ic("menu")}</button>
  <nav id="menu" class="menu" aria-label="Main">
   {links}
   <a class="btn btn-primary" href="/#quote">Get a quote</a>
  </nav>
 </div>
</header>
'''

def quote_section(heading="Get your instant quote", sub="Tell us where and when. We reply on WhatsApp with a fixed price, usually within minutes – day or night."):
    places = ["Larnaca Airport (LCA)", "Paphos Airport (PFO)", "Ayia Napa", "Protaras", "Larnaca", "Limassol", "Nicosia", "Paphos", "Coral Bay", "Polis / Latchi", "Troodos"]
    dl = "".join(f'<option value="{p}">' for p in places)
    return f'''<section id="quote" class="section quote">
 <div class="wrap split">
  <div>
   <span class="eyebrow">Book in 1 minute</span>
   <h2>{heading}</h2>
   <p class="lead">{sub}</p>
   <ul class="contact-list">
    <li><span class="ico">{ic("chat")}</span><span><small>WhatsApp – fastest reply</small><a href="{WA}" target="_blank" rel="noopener" data-loc="quote">{PHONE_H}</a></span></li>
    <li><span class="ico">{ic("phone")}</span><span><small>Call us 24/7</small><a href="tel:{PHONE}" data-loc="quote">{PHONE_H}</a></span></li>
    <li><span class="ico">{ic("mail")}</span><span><small>Email</small><a href="mailto:{EMAIL}" data-loc="quote">{EMAIL}</a></span></li>
    <li><span class="ico">{ic("clock")}</span><span><small>Hours</small><b>Open 24 hours, 7 days a week</b></span></li>
   </ul>
  </div>
  <form id="quote-form" class="form">
   <h3>Request a fixed price</h3>
   <div class="field full"><label for="q-name">Full name</label><input id="q-name" name="name" autocomplete="name" required></div>
   <div class="field"><label for="q-phone">Phone / WhatsApp</label><input id="q-phone" name="phone" type="tel" autocomplete="tel" placeholder="+44 7…" required></div>
   <div class="field"><label for="q-pax">Passengers</label><input id="q-pax" name="pax" type="number" min="1" inputmode="numeric" placeholder="e.g. 6"></div>
   <div class="field"><label for="q-pickup">From</label><input id="q-pickup" name="pickup" list="places" placeholder="Airport, hotel or address" required></div>
   <div class="field"><label for="q-dropoff">To</label><input id="q-dropoff" name="dropoff" list="places" placeholder="Hotel, villa or address" required></div>
   <div class="field"><label for="q-date">Date</label><input id="q-date" name="date" type="date" required></div>
   <div class="field"><label for="q-time">Time</label><input id="q-time" name="time" type="time" required></div>
   <div class="field full"><label for="q-flight">Flight number (optional)</label><input id="q-flight" name="flight" placeholder="e.g. BA662 – we track it for delays"></div>
   <div class="field full"><label for="q-notes">Luggage, child seats, extra stops</label><textarea id="q-notes" name="notes" rows="3"></textarea></div>
   <datalist id="places">{dl}</datalist>
   <button class="btn btn-wa" type="submit">{ic("chat")} Get my price on WhatsApp</button>
   <p class="fine">No payment needed to book. Opens WhatsApp with your details filled in.</p>
  </form>
 </div>
</section>
'''

def footer():
    pages = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in ALL_PAGES)
    return f'''<footer class="site-footer">
 <div class="wrap">
  <div class="foot-grid">
   <div>
    <a class="brand" href="/"><picture><source srcset="/assets/img/logo-96.webp" type="image/webp"><img src="/assets/img/logo-96.png" width="44" height="44" alt="" loading="lazy"></picture><span><b>Volan</b><small>Premium Transfers</small></span></a>
    <p>Private airport transfers, minibus and bus hire with professional drivers across Cyprus. Available 24/7.</p>
   </div>
   <div><h2>Transfers</h2><ul>{pages}</ul></div>
   <div><h2>Company</h2><ul><li><a href="/#about">About us</a></li><li><a href="/#fleet">Our vehicles</a></li><li><a href="/#routes">Routes &amp; journey times</a></li><li><a href="/#faq">FAQ</a></li><li><a href="/#quote">Get a quote</a></li></ul></div>
   <div><h2>Contact</h2><ul>
    <li><a href="tel:{PHONE}" data-loc="footer">{PHONE_H}</a></li>
    <li><a href="{WA}" target="_blank" rel="noopener" data-loc="footer">WhatsApp {PHONE_H}</a></li>
    <li><a href="mailto:{EMAIL}" data-loc="footer">{EMAIL}</a></li>
    <li>Island-wide service, Cyprus</li>
    <li>Open 24 hours, 7 days</li>
   </ul></div>
  </div>
  <div class="foot-bottom"><span>© <span id="year">2026</span> Volan Premium Transfers. All rights reserved.</span><span>Larnaca · Paphos · Limassol · Nicosia · Ayia Napa · Protaras</span></div>
 </div>
</footer>
<a class="wa-float" href="{WA}" target="_blank" rel="noopener" aria-label="Chat with us on WhatsApp" data-loc="float"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.2A9.7 9.7 0 0 0 3.6 16.8L2.3 21.7l5-1.3A9.7 9.7 0 1 0 12 2.2zm0 17.7a8 8 0 0 1-4.1-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8 8 0 1 1 12 19.9zm4.4-6c-.2-.1-1.4-.7-1.7-.8-.2-.1-.4-.1-.5.1l-.8 1c-.1.2-.3.2-.5.1a6.6 6.6 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.5-.4h-.5a.9.9 0 0 0-.7.3 2.8 2.8 0 0 0-.9 2.1 4.9 4.9 0 0 0 1 2.6 11.2 11.2 0 0 0 4.3 3.8c1.6.7 2.2.7 3 .6.5-.1 1.4-.6 1.6-1.1.2-.6.2-1 .1-1.1l-.5-.3z"/></svg></a>
<script src="/assets/js/site.js?v={JS_V}" defer></script>
</body>
</html>
'''

def crumbs(items):
    lis = "".join(f'<li><a href="{h}">{t}</a></li>' if h else f'<li aria-current="page">{t}</li>' for h, t in items)
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": html.unescape(t), **({"item": SITE + h} if h else {})} for i, (h, t) in enumerate(items)]}
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{lis}</ol></nav>', ld

def faq_html(faqs):
    return '<div class="faq">' + "".join(
        f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in faqs) + '</div>'

def faq_ld(faqs):
    import re
    strip = lambda s: html.unescape(re.sub(r"<[^>]+>", "", s))
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in faqs]}

def routes_table(rows, caption):
    trs = "".join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>' for a, b, c, d in rows)
    return f'''<div class="table-wrap"><table><caption>{caption}</caption>
<thead><tr><th scope="col">From</th><th scope="col">To</th><th scope="col">Distance</th><th scope="col">Typical time</th></tr></thead>
<tbody>{trs}</tbody></table></div>
<p class="note">Distances and times are approximate and depend on traffic and the exact pickup or drop-off address. Prices are fixed and confirmed before you travel.</p>'''

LCA, PFO = "Larnaca Airport (LCA)", "Paphos Airport (PFO)"
R = {
 "lca-larnaca": (LCA, "Larnaca city &amp; Mackenzie", "≈ 7 km", "10–15 min"),
 "lca-napa": (LCA, '<a href="/ayia-napa-protaras-transfers/">Ayia Napa</a>', "≈ 48 km", "40–45 min"),
 "lca-protaras": (LCA, '<a href="/ayia-napa-protaras-transfers/">Protaras</a>', "≈ 58 km", "45–55 min"),
 "lca-nicosia": (LCA, "Nicosia", "≈ 50 km", "40–45 min"),
 "lca-limassol": (LCA, '<a href="/limassol-transfers/">Limassol</a>', "≈ 70 km", "50–60 min"),
 "lca-paphos": (LCA, "Paphos", "≈ 140 km", "1 h 40 – 1 h 50"),
 "pfo-paphos": (PFO, "Paphos town &amp; Kato Paphos", "≈ 15 km", "20 min"),
 "pfo-coral": (PFO, "Coral Bay &amp; Peyia", "≈ 25 km", "25–30 min"),
 "pfo-polis": (PFO, "Polis &amp; Latchi", "≈ 50 km", "50–60 min"),
 "pfo-limassol": (PFO, '<a href="/limassol-transfers/">Limassol</a>', "≈ 60 km", "45–55 min"),
 "pfo-nicosia": (PFO, "Nicosia", "≈ 150 km", "1 h 40 – 1 h 50"),
 "pfo-napa": (PFO, '<a href="/ayia-napa-protaras-transfers/">Ayia Napa</a>', "≈ 190 km", "2 h 10 – 2 h 20"),
}

BUSINESS = {
 "@context": "https://schema.org",
 "@graph": [
  {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "Volan Premium Transfers", "inLanguage": "en", "publisher": {"@id": BIZ_ID}},
  {"@type": "LocalBusiness", "@id": BIZ_ID, "name": "Volan Premium Transfers", "alternateName": "Volan Minibus",
   "description": "Private airport transfers, minibus and bus hire with professional drivers across Cyprus. Larnaca and Paphos airport pickups, hotel transfers, private tours and group transport, 24/7.",
   "url": SITE + "/", "logo": SITE + "/assets/img/logo-512.png",
   "image": [SITE + "/assets/img/van-coast-1536.jpg", SITE + "/assets/img/og-image.jpg"],
   "telephone": PHONE, "email": EMAIL, "priceRange": "€€", "currenciesAccepted": "EUR",
   "address": {"@type": "PostalAddress", "addressCountry": "CY"},
   "areaServed": [{"@type": "Country", "name": "Cyprus"}] + [{"@type": "City", "name": c} for c in ["Larnaca", "Paphos", "Limassol", "Nicosia", "Ayia Napa", "Protaras", "Coral Bay", "Polis"]],
   "knowsLanguage": ["en", "el"],
   "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"], "opens": "00:00", "closes": "23:59"}],
   "contactPoint": [{"@type": "ContactPoint", "contactType": "reservations", "telephone": PHONE, "email": EMAIL, "availableLanguage": ["English", "Greek"], "hoursAvailable": "Mo-Su 00:00-23:59"}],
   "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Transfers and transport services", "itemListElement": [
     {"@type": "Offer", "itemOffered": {"@type": "Service", "name": html.unescape(t), "url": SITE + h}} for h, t in ALL_PAGES]}
  }
 ]}

def service_ld(name, path, desc, areas):
    return {"@context": "https://schema.org", "@type": "Service", "@id": SITE + path + "#service",
            "name": html.unescape(name), "serviceType": "Private transfer", "description": html.unescape(desc), "url": SITE + path,
            "provider": {"@id": BIZ_ID}, "areaServed": [{"@type": "Place", "name": a} for a in areas],
            "availableChannel": {"@type": "ServiceChannel", "servicePhone": PHONE, "serviceUrl": SITE + "/#quote"}}

def write(path, content):
    fp = os.path.join(OUT, path.strip("/"), "index.html") if path != "/" else os.path.join(OUT, "index.html")
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, "w").write(content)

def cta_band(title="Ready when you land.", text="Send your flight number and destination – we confirm a fixed price on WhatsApp."):
    return f'''<section class="section" style="padding-top:0"><div class="wrap"><div class="cta-band"><div><h2>{title}</h2><p>{text}</p></div>
<div class="actions"><a class="btn btn-wa" href="{WA}" target="_blank" rel="noopener" data-loc="cta">{ic("chat")} WhatsApp us</a><a class="btn btn-outline" href="tel:{PHONE}" data-loc="cta">{ic("phone")} {PHONE_H}</a></div></div></div></section>'''

# ---------------------------------------------------------------- inner pages
def inner(path, title, desc, h1, lead, crumb_name, body, facts, faqs, svc_name, areas, related):
    crumb_html, crumb_ld = crumbs([("/", "Home"), (None, crumb_name)])
    lds = [crumb_ld, service_ld(svc_name, path, desc, areas), faq_ld(faqs)]
    fact_li = "".join(f'<li><span>{k}</span><span>{v}</span></li>' for k, v in facts)
    rel = "".join(f'<li><a href="{h}">{t} {ic("arrow","icon")}</a></li>' for h, t in ALL_PAGES if h != path)
    out = head(title, desc, path, lds) + header(path) + f'''<main id="main">
<section class="page-hero"><div class="wrap">{crumb_html}
 <span class="eyebrow">Volan Premium Transfers</span>
 <h1>{h1}</h1>
 <p class="lead">{lead}</p>
 <div class="hero-ctas"><a class="btn btn-gold" href="#quote">Get a fixed price</a><a class="btn btn-ghost" href="{WA}" target="_blank" rel="noopener" data-loc="hero">{ic("chat")} WhatsApp {PHONE_H}</a></div>
</div></section>
<section class="section"><div class="wrap layout">
 <article class="prose">{body}
  <h2>Frequently asked questions</h2>
  {faq_html(faqs)}
 </article>
 <aside class="aside">
  <div class="card"><h3>At a glance</h3><ul class="facts">{fact_li}</ul>
   <a class="btn btn-primary" href="#quote">Get a fixed price</a>
   <a class="btn btn-outline" href="tel:{PHONE}" data-loc="aside">{ic("phone")} Call {PHONE_H}</a></div>
  <div class="card"><h3>Other transfers</h3><ul class="links">{rel}</ul></div>
 </aside>
</div></section>
{quote_section()}
</main>
''' + footer()
    write(path, out)

STD_FACTS = [("Passengers", "Any group size"), ("Availability", "24/7, every day"), ("Child seats", "Free on request"), ("Drivers", "English &amp; Greek speaking"), ("Booking", "WhatsApp, phone or email"), ("Payment", "Nothing to pay to book")]

inner("/larnaca-airport-transfers/",
 "Larnaca Airport Transfers (LCA) | Private Minibus 24/7 | Volan",
 "Private Larnaca Airport (LCA) transfers to Ayia Napa, Protaras, Limassol &amp; Nicosia. Meet &amp; greet, flight tracking, free child seats, any group size. 24/7.",
 "Larnaca Airport Transfers",
 "Private minibus and bus transfers from Larnaca International Airport (LCA) to any hotel, villa or address in Cyprus. Your driver tracks your flight and meets you in arrivals with a name sign.",
 "Larnaca Airport transfers",
 f'''<h2>Private transfers from Larnaca Airport</h2>
<p>Larnaca International Airport (IATA: LCA) is the main gateway to Cyprus and the closest airport to Ayia Napa, Protaras, Nicosia and Larnaca's beaches. Volan Premium Transfers runs private, door-to-door transfers from LCA around the clock – you never share the vehicle and never wait for other passengers.</p>
<p>Every booking includes flight tracking, so if your flight lands early or late your driver adjusts automatically. You'll be met inside the arrivals hall with a name sign, helped with your luggage and taken straight to your accommodation.</p>
<h2>Popular routes and journey times from LCA</h2>
{routes_table([R[k] for k in ["lca-larnaca","lca-napa","lca-protaras","lca-nicosia","lca-limassol","lca-paphos"]], "Larnaca Airport transfer times")}
<h2>What's included</h2>
<ul>
<li><strong>Meet &amp; greet</strong> in the arrivals hall with a name sign</li>
<li><strong>Flight tracking</strong> – no extra cost if your flight is delayed</li>
<li><strong>Baby and child seats</strong> free of charge on request</li>
<li><strong>Space for luggage</strong>, golf bags, strollers and sports equipment</li>
<li><strong>Fixed price</strong> agreed before you travel – no meter, no hidden fees</li>
<li>Professional, licensed and insured drivers who speak English and Greek</li>
</ul>
<h2>Vehicles for every group size</h2>
<p>Couples and families travel in a spacious private minibus; our fleet has minibuses with 8, 13, 17, 21 and 30 passengers, plus 55-seater buses, all with room for luggage. For bigger groups, weddings, conferences and sports teams we send several vehicles together – there is no limit on group size – see <a href="/group-bus-hire-cyprus/">group transfers and bus hire</a>.</p>
<h2>How to book your Larnaca Airport transfer</h2>
<p>Send your flight number, arrival time, number of passengers and destination using the form below or directly on <a href="{WA}" target="_blank" rel="noopener">WhatsApp ({PHONE_H})</a>. We reply with a fixed price, usually within minutes, and confirm your driver's details before you fly.</p>''',
 STD_FACTS,
 [("How do I find my driver at Larnaca Airport?", "Your driver waits in the arrivals hall of Larnaca International Airport holding a sign with your name. You also receive the driver's phone number on WhatsApp before you land."),
  ("What happens if my flight to Larnaca is delayed?", "We track every flight, so your driver adjusts to the actual landing time. There is no extra charge for flight delays."),
  ("How long is the transfer from Larnaca Airport to Ayia Napa?", "About 40–45 minutes for roughly 48 km, depending on traffic and your hotel's location."),
  ("How long is the transfer from Larnaca Airport to Limassol?", "About 50–60 minutes for roughly 70 km via the A1/A5 motorway."),
  ("Do you provide child seats for airport transfers?", "Yes. Baby seats, child seats and boosters are free of charge – just tell us the children's ages when you book."),
  ("How much is a taxi or private transfer from Larnaca Airport?", "The price depends on the destination, number of passengers, luggage and time of day. Send your details on WhatsApp and we confirm a fixed price within minutes – the price you're quoted is the price you pay.")],
 "Larnaca Airport transfers", ["Larnaca International Airport", "Larnaca", "Ayia Napa", "Protaras", "Nicosia", "Limassol", "Paphos"], None)

inner("/paphos-airport-transfers/",
 "Paphos Airport Transfers (PFO) | Private Minibus 24/7 | Volan",
 "Private Paphos Airport (PFO) transfers to Paphos, Coral Bay, Polis &amp; Limassol. Meet &amp; greet, flight tracking, free child seats, fixed prices. 24/7.",
 "Paphos Airport Transfers",
 "Private minibus and bus transfers from Paphos International Airport (PFO) to Kato Paphos, Coral Bay, Peyia, Polis, Latchi, Limassol and anywhere in Cyprus – with meet &amp; greet and flight tracking.",
 "Paphos Airport transfers",
 f'''<h2>Private transfers from Paphos Airport</h2>
<p>Paphos International Airport (IATA: PFO) serves the west of Cyprus – Paphos town, Kato Paphos, Coral Bay, Peyia, the Akamas peninsula, Polis and Latchi. Volan Premium Transfers provides private, door-to-door transfers from PFO 24 hours a day, so whether you land at noon or 3 a.m. a driver is waiting for you.</p>
<p>Your driver monitors your flight, meets you in arrivals with a name sign and takes you directly to your hotel or villa – no shared shuttles and no stops for other passengers.</p>
<h2>Popular routes and journey times from PFO</h2>
{routes_table([R[k] for k in ["pfo-paphos","pfo-coral","pfo-polis","pfo-limassol","pfo-nicosia","pfo-napa"]], "Paphos Airport transfer times")}
<h2>What's included</h2>
<ul>
<li><strong>Meet &amp; greet</strong> inside the arrivals hall</li>
<li><strong>Flight tracking</strong> with no charge for delays</li>
<li><strong>Free baby and child seats</strong> on request</li>
<li>Room for suitcases, golf bags, bikes and strollers</li>
<li><strong>Fixed, all-inclusive price</strong> confirmed before travel</li>
<li>Licensed, insured, English and Greek speaking drivers</li>
</ul>
<h2>Villa holidays, weddings and golf groups</h2>
<p>The Paphos area is popular for villa holidays, destination weddings and golf breaks. We have minibuses for 8, 13, 17, 21 and 30 passengers, plus 55-seater buses, and for larger parties we send as many vehicles as you need. See <a href="/group-bus-hire-cyprus/">group transfers and bus hire</a>, or plan a day out with a <a href="/private-tours-cyprus/">private minibus tour</a> to Akamas, the Troodos mountains or local wineries.</p>
<h2>How to book</h2>
<p>Fill in the form below or message us on <a href="{WA}" target="_blank" rel="noopener">WhatsApp ({PHONE_H})</a> with your flight number, arrival time, passengers and destination. We reply with a fixed price and confirm your driver before you fly.</p>''',
 STD_FACTS,
 [("Where will my driver meet me at Paphos Airport?", "Inside the arrivals hall at Paphos International Airport, holding a sign with your name. You receive the driver's contact number on WhatsApp in advance."),
  ("How long is the transfer from Paphos Airport to Coral Bay?", "About 25–30 minutes for roughly 25 km."),
  ("How long is the transfer from Paphos Airport to Limassol?", "About 45–55 minutes for roughly 60 km via the A6 motorway."),
  ("Is there a charge if my flight is delayed?", "No. We track your flight and the driver waits for your actual arrival time at no extra cost."),
  ("Can you transfer us from Paphos Airport to Ayia Napa or Protaras?", "Yes. The journey is about 2 h 10 – 2 h 20 for roughly 190 km. We can add a comfort stop on the way."),
  ("Do you have vehicles for large groups from Paphos Airport?", "Yes. We transport groups of any size – minibuses and buses for 8 to 55 passengers, and several vehicles together for larger groups such as wedding guests and golf groups.")],
 "Paphos Airport transfers", ["Paphos International Airport", "Paphos", "Coral Bay", "Peyia", "Polis", "Latchi", "Limassol"], None)

inner("/ayia-napa-protaras-transfers/",
 "Larnaca Airport to Ayia Napa &amp; Protaras Transfers | Volan",
 "Private transfers from Larnaca Airport to Ayia Napa (≈45 min) and Protaras (≈50 min). One minibus for your whole group, free child seats, 24/7 fixed prices.",
 "Ayia Napa &amp; Protaras Transfers",
 "Our most-requested routes: private transfers from Larnaca Airport to Ayia Napa, Protaras, Cape Greco and Paralimni – for families, friends, stag and hen groups and weddings.",
 "Ayia Napa &amp; Protaras transfers",
 f'''<h2>Larnaca Airport to Ayia Napa and Protaras</h2>
<p>Ayia Napa and Protaras sit on the south-east coast of Cyprus, roughly 45–60 km from Larnaca International Airport. The drive runs along the A3 motorway and takes about 40–55 minutes. Paphos Airport is much further – around 190 km – so most visitors to this area fly into Larnaca.</p>
<p>Volan's private transfers pick you up in the arrivals hall and take you straight to your hotel, apartment or villa in Ayia Napa, Protaras, Pernera, Kapparis, Paralimni or Cape Greco.</p>
<h2>Journey times</h2>
{routes_table([R["lca-napa"], R["lca-protaras"], (LCA, "Paralimni &amp; Kapparis", "≈ 55 km", "45–50 min"), R["pfo-napa"]], "Transfer times to Ayia Napa and Protaras")}
<h2>Perfect for groups</h2>
<p>Ayia Napa is one of the most popular destinations in Cyprus for groups of friends, stag and hen parties and big family holidays. Instead of splitting into several taxis, your whole group travels together in one private minibus with all the luggage – we have minibuses for 8, 13, 17, 21 and 30 passengers, plus 55-seater buses. For larger parties and wedding guests we send several vehicles together.</p>
<h2>Beyond the airport run</h2>
<ul>
<li>Nights out and returns between Ayia Napa, Protaras and Larnaca</li>
<li>Day trips to Cape Greco, Nissi Beach and Konnos Bay</li>
<li><a href="/private-tours-cyprus/">Private tours</a> to Nicosia, Lefkara village and the Troodos mountains</li>
<li>Return transfers to Larnaca Airport timed to your flight</li>
</ul>''',
 STD_FACTS,
 [("How long is the transfer from Larnaca Airport to Ayia Napa?", "About 40–45 minutes for roughly 48 km via the A3 motorway."),
  ("How long is the transfer from Larnaca Airport to Protaras?", "About 45–55 minutes for roughly 58 km, depending on traffic and your hotel's exact location."),
  ("Which airport is closest to Ayia Napa?", "Larnaca International Airport (LCA) is closest – about 48 km. Paphos Airport is around 190 km away."),
  ("Can a group of 10 travel together to Ayia Napa?", "Yes. We have minibuses for 8, 13, 17, 21 and 30 passengers, plus 55-seater buses, so the whole group arrives together with all the luggage."),
  ("Do you offer return transfers from Ayia Napa to Larnaca Airport?", "Yes. We schedule the pickup from your hotel based on your flight time, 24 hours a day.")],
 "Ayia Napa and Protaras transfers", ["Ayia Napa", "Protaras", "Paralimni", "Cape Greco", "Larnaca International Airport"], None)

inner("/limassol-transfers/",
 "Limassol Transfers from Larnaca &amp; Paphos Airport | Volan",
 "Private transfers to Limassol from Larnaca and Paphos airports – hotels, marina, cruise port and business travel. Any group size, 24/7.",
 "Limassol Transfers",
 "Private transfers to Limassol hotels, Limassol Marina, the cruise port and business districts – from Larnaca Airport, Paphos Airport or anywhere in Cyprus.",
 "Limassol transfers",
 f'''<h2>Airport transfers to Limassol</h2>
<p>Limassol is roughly halfway between Cyprus's two international airports. Larnaca Airport is about 70 km away (around 50–60 minutes on the A1/A5) and Paphos Airport about 60 km away (around 45–55 minutes on the A6). We collect you from either airport and drive you directly to your hotel, apartment, office or the port.</p>
<h2>Journey times</h2>
{routes_table([R["lca-limassol"], R["pfo-limassol"], ("Limassol", "Nicosia", "≈ 85 km", "1 h"), ("Limassol", "Troodos (Platres)", "≈ 45 km", "50–60 min")], "Transfer times to and from Limassol")}
<h2>Business, cruise and event travel</h2>
<ul>
<li><strong>Corporate travel</strong> – punctual, discreet transfers for executives and teams, with flexible waiting time</li>
<li><strong>Cruise passengers</strong> – transfers between Limassol port, the airports and hotels</li>
<li><strong>Conferences and events</strong> – shuttles for delegates with minibuses and buses for 8 to 55 passengers</li>
<li><strong>Hotel and Airbnb guests</strong> – door-to-door transfers to any address in Limassol</li>
</ul>
<p>Need a full day? Combine your transfer with a <a href="/private-tours-cyprus/">private tour</a> to the Troodos mountains, Kourion or local wineries.</p>''',
 STD_FACTS,
 [("Which airport is closer to Limassol?", "Both are similar. Paphos Airport is about 60 km (45–55 min) and Larnaca Airport about 70 km (50–60 min). Larnaca has more flights."),
  ("Do you provide transfers for cruise passengers in Limassol?", "Yes. We transfer cruise passengers between Limassol port, both airports and hotels across Cyprus."),
  ("Can you provide corporate transport in Limassol?", "Yes. We provide point-to-point corporate transfers and shuttles for teams, clients and conference delegates."),
  ("Are your Limassol transfers available at night?", "Yes, we operate 24/7 including early-morning and late-night flights.")],
 "Limassol transfers", ["Limassol", "Limassol Marina", "Limassol Port", "Larnaca International Airport", "Paphos International Airport"], None)

inner("/private-tours-cyprus/",
 "Private Minibus Tours in Cyprus with Driver | Volan",
 "Private minibus tours in Cyprus with your own driver: Troodos villages, wineries, Lefkara, Nicosia, Kourion, Akamas &amp; Cape Greco. Custom routes.",
 "Private Minibus Tours in Cyprus",
 "Explore Cyprus at your own pace with a private minibus and a local driver. You choose the stops – we handle the driving, parking and timing.",
 "Private tours",
 '''<h2>Your own minibus and driver for the day</h2>
<p>A private tour lets your family or group see the best of Cyprus without renting cars, navigating mountain roads or worrying about parking. Your driver picks you up from your hotel, follows the itinerary you choose and brings you back whenever you're ready. Tours are fully private and can start from Larnaca, Ayia Napa, Protaras, Limassol, Paphos or Nicosia.</p>
<h2>Popular private tour ideas</h2>
<h3>Troodos mountains &amp; villages</h3>
<p>Mountain villages such as Omodos and Kakopetria, painted Byzantine churches, waterfalls and cooler air in summer.</p>
<h3>Wine route</h3>
<p>Visit family wineries in the Limassol wine villages and taste local varieties such as Xynisteri and Commandaria – everyone can taste, nobody has to drive.</p>
<h3>Lefkara &amp; Nicosia</h3>
<p>The lace-making village of Lefkara, then Nicosia's old town, the Venetian walls and the Ledra Street crossing.</p>
<h3>Kourion &amp; Aphrodite's Rock</h3>
<p>The ancient theatre of Kourion above the sea and the legendary birthplace of Aphrodite on the coast road to Paphos.</p>
<h3>Cape Greco &amp; the east coast</h3>
<p>Sea caves, cliffs and beaches around Cape Greco, Konnos Bay and Ayia Napa.</p>
<h3>Akamas &amp; Latchi</h3>
<p>The wild west of Cyprus – the Baths of Aphrodite, Latchi harbour and Polis.</p>
<h2>How private tours work</h2>
<ul>
<li>Tell us your group size, pickup area and the places you want to see</li>
<li>We suggest a realistic route and give you a fixed price for the day</li>
<li>Your driver follows your pace – extra stops for photos, lunch and swims</li>
<li>Child seats free on request; any group size, from couples to large groups</li>
</ul>
<p>Our drivers are professional chauffeurs who know the island well. Entrance tickets, meals and tastings are not included unless agreed.</p>''',
 [("Group size", "Any group size"), ("Duration", "Half or full day"), ("Pickup", "Any hotel in Cyprus"), ("Itinerary", "Fully custom"), ("Child seats", "Free on request"), ("Booking", "WhatsApp, phone or email")],
 [("Can we create our own tour itinerary?", "Yes. All our tours are private and fully custom. Tell us what you'd like to see and we'll suggest a route that fits the day."),
  ("Is the driver a licensed tour guide?", "Our drivers are professional chauffeurs who know Cyprus well and can recommend stops. If you need an official licensed guide, ask us and we'll arrange one."),
  ("Are entrance fees and wine tastings included?", "No, the price covers the vehicle, driver and fuel. Entrance tickets, tastings and meals are paid separately unless agreed in advance."),
  ("Where do private tours start?", "We pick you up from your hotel or villa anywhere in Cyprus, including Ayia Napa, Protaras, Larnaca, Limassol, Paphos and Nicosia.")],
 "Private minibus tours in Cyprus", ["Cyprus", "Troodos", "Nicosia", "Lefkara", "Kourion", "Akamas", "Cape Greco"], None)

inner("/group-bus-hire-cyprus/",
 "Group Transfers &amp; Bus Hire with Driver in Cyprus | Volan",
 "Minibus and bus hire with driver in Cyprus – 8 to 55 passengers, any group size: weddings, conferences, sports teams and events. Group airport transfers 24/7.",
 "Group Transfers &amp; Bus Hire in Cyprus",
 "Minibuses with 8, 13, 17, 21 and 30 passengers, plus 55-seater buses, and several vehicles together for any number of passengers – always with professional drivers. Ideal for weddings, events, conferences, sports teams and large families.",
 "Group transfers &amp; bus hire",
 '''<h2>Transport for any group size</h2>
<p>Moving a group around Cyprus is much simpler with one vehicle and one driver than with a convoy of taxis. Volan Premium Transfers moves groups of any size: private minibuses with 8, 13, 17, 21 and 30 passengers, plus 55-seater buses, and several vehicles together for the biggest groups – from a single airport run to multi-day event transport.</p>
<h2>What we transport</h2>
<ul>
<li><strong>Weddings</strong> – guest shuttles between hotels, the ceremony and the reception venue</li>
<li><strong>Conferences and corporate events</strong> – delegate transfers, team outings and incentive trips</li>
<li><strong>Sports teams and clubs</strong> – training camps, matches and tournaments, with room for kit</li>
<li><strong>Schools and organised groups</strong> – excursions and educational trips</li>
<li><strong>Large families and friends</strong> – everyone arrives together with all the luggage</li>
<li><strong>Airport group transfers</strong> from Larnaca and Paphos airports</li>
</ul>
<h2>Why groups choose Volan</h2>
<ul>
<li>One point of contact on WhatsApp for planning and changes</li>
<li>Fixed quotes agreed in advance – no hidden fees</li>
<li>Licensed and insured vehicles with professional drivers</li>
<li>Available 24/7 for early flights and late events</li>
<li>Island-wide: Larnaca, Ayia Napa, Protaras, Nicosia, Limassol and Paphos</li>
</ul>
<h2>Get a group quote</h2>
<p>Send the number of passengers, dates, pickup and drop-off points and a rough schedule. For multi-day events, a list of transfers is perfect – we'll return one fixed price for everything.</p>''',
 [("Group size", "Any number of passengers"), ("Vehicles", "8 · 13 · 17 · 21 · 30 · 55 seats"), ("Availability", "24/7"), ("Coverage", "All of Cyprus"), ("Quotes", "Fixed, in advance"), ("Booking", "WhatsApp, phone or email")],
 [("What is the largest group you can transport?", "There is no limit. Our largest bus takes 55 passengers, and we combine several vehicles so any number of people can travel together."),
  ("Can you provide wedding guest shuttles in Cyprus?", "Yes. We run shuttles between hotels, ceremony and reception venues, including late-night returns."),
  ("Do you provide airport transfers for groups?", "Yes. We collect groups from Larnaca and Paphos airports with minibuses and buses for 8 to 55 passengers – and several vehicles for bigger groups – with room for luggage."),
  ("How far in advance should we book group transport?", "As early as possible, especially for the larger minibuses in the summer season and for weddings. Short-notice requests are welcome – message us and we'll check availability.")],
 "Group transfers and bus hire in Cyprus", ["Cyprus", "Larnaca", "Paphos", "Limassol", "Nicosia", "Ayia Napa", "Protaras"], None)

# ---------------------------------------------------------------- home
HOME_FAQ = [
 ("How much is a private transfer from Larnaca Airport to Ayia Napa?", "The price depends on the number of passengers, luggage and time of day. Send your details on WhatsApp (+357 99 335570) and we confirm a fixed price within minutes – no meter and no hidden fees."),
 ("How long does it take from Larnaca Airport to Ayia Napa, Protaras or Limassol?", "Approximately 40–45 minutes to Ayia Napa, 45–55 minutes to Protaras and 50–60 minutes to Limassol, depending on traffic. See the <a href=\"#routes\">routes table</a> for more journey times."),
 ("Do you provide child seats?", "Yes. Baby seats, child seats and boosters are available free of charge on request for airport transfers and tours."),
 ("How big are your vehicles?", "We have minibuses for 8, 13, 17, 21 and 30 passengers, plus 55-seater buses, all with room for luggage. For larger groups we send several vehicles together, so we can transport any number of people."),
 ("Do you operate 24/7?", "Yes. We run airport transfers, hotel pickups and private hire 24 hours a day, 7 days a week, including early-morning and late-night flights."),
 ("What happens if my flight is delayed?", "We track your flight and your driver adjusts to the real landing time, at no extra cost."),
 ("Where will the driver meet me?", "Inside the arrivals hall at Larnaca or Paphos airport, holding a sign with your name. You receive the driver's contact details on WhatsApp before you land."),
 ("How do I book and pay?", "Book via the quote form, WhatsApp, phone or email. No payment is needed to make a booking; we confirm the fixed price and all details with you in advance."),
 ("Which areas of Cyprus do you cover?", "The whole island: Larnaca, Ayia Napa, Protaras, Paralimni, Nicosia, Limassol, Paphos, Coral Bay, Polis, Latchi and the Troodos mountains."),
]

def home():
    lds = [BUSINESS, faq_ld(HOME_FAQ)]
    svc = [
     ("plane", "Larnaca Airport transfers", "Meet &amp; greet at LCA and a private ride to Ayia Napa, Protaras, Nicosia, Limassol or anywhere on the island.", "/larnaca-airport-transfers/"),
     ("plane", "Paphos Airport transfers", "Private pickups at PFO for Paphos, Coral Bay, Polis, Latchi and Limassol – day or night.", "/paphos-airport-transfers/"),
     ("sun", "Ayia Napa &amp; Protaras", "Our most popular routes. One minibus for the whole group – families, friends and weddings.", "/ayia-napa-protaras-transfers/"),
     ("brief", "Limassol &amp; corporate", "Punctual, discreet transfers for business travellers, cruise passengers and conferences.", "/limassol-transfers/"),
     ("wine", "Private tours", "Troodos villages, wineries, Lefkara, Kourion, Cape Greco and Akamas – at your own pace.", "/private-tours-cyprus/"),
     ("bus", "Groups &amp; bus hire", "Minibuses and buses for 8 to 55 passengers, and several vehicles together for any group size – weddings, teams and events.", "/group-bus-hire-cyprus/"),
    ]
    cards = "".join(f'<a class="card" href="{u}"><span class="ico">{ic(i)}</span><h3>{t}</h3><p>{d}</p><span class="more">Learn more {ic("arrow")}</span></a>' for i, t, d, u in svc)
    rows = [R[k] for k in ["lca-larnaca","lca-napa","lca-protaras","lca-nicosia","lca-limassol","lca-paphos","pfo-paphos","pfo-coral","pfo-limassol"]]
    out = head("Cyprus Airport Transfers &amp; Minibus Hire 24/7 | Volan",
 "Private airport transfers in Cyprus from Larnaca &amp; Paphos to Ayia Napa, Protaras, Limassol &amp; more. Any group size, free child seats, meet &amp; greet. 24/7.",
               "/", lds, preload_hero=True) + header("/") + f'''<main id="main">
<section class="hero">
 <picture>
  <source type="image/webp" srcset="/assets/img/van-coast-640.webp 640w, /assets/img/van-coast-960.webp 960w, /assets/img/van-coast-1536.webp 1536w" sizes="100vw">
  <img class="hero-img" src="/assets/img/van-coast-960.jpg" srcset="/assets/img/van-coast-640.jpg 640w, /assets/img/van-coast-960.jpg 960w, /assets/img/van-coast-1536.jpg 1536w" sizes="100vw" width="1536" height="508" alt="Volan Premium Transfers minibus on the Cyprus coast" fetchpriority="high">
 </picture>
 <div class="wrap"><div class="hero-inner">
  <span class="eyebrow">Larnaca &amp; Paphos airports · 24/7</span>
  <h1>Private airport transfers &amp; minibus hire in Cyprus</h1>
  <p class="lead">Your driver tracks your flight, meets you in arrivals and takes you straight to your hotel or villa – anywhere on the island, at a fixed price agreed in advance.</p>
  <div class="hero-ctas">
   <a class="btn btn-gold" href="#quote">Get a fixed price</a>
   <a class="btn btn-ghost" href="{WA}" target="_blank" rel="noopener" data-loc="hero">{ic("chat")} WhatsApp {PHONE_H}</a>
  </div>
  <ul class="hero-points">
   <li>{ic("check")} Meet &amp; greet</li><li>{ic("check")} Flight tracking</li><li>{ic("check")} Free child seats</li><li>{ic("check")} Any group size</li>
  </ul>
 </div></div>
</section>

<section class="trust" aria-label="Why travellers choose us"><div class="wrap"><ul>
 <li><span class="ico">{ic("shield")}</span><span><strong>Licensed &amp; insured</strong>Registered Cyprus operator</span></li>
 <li><span class="ico">{ic("clock")}</span><span><strong>24/7 service</strong>Every flight, day or night</span></li>
 <li><span class="ico">{ic("globe")}</span><span><strong>English &amp; Greek</strong>Professional drivers</span></li>
 <li><span class="ico">{ic("chat")}</span><span><strong>Reply in minutes</strong>Instant WhatsApp quotes</span></li>
</ul></div></section>

<section id="services" class="section"><div class="wrap">
 <div class="section-head center"><span class="eyebrow">Our services</span><h2>Transfers and private hire across Cyprus</h2>
 <p class="lead">From a 2 a.m. arrival at Larnaca to a 50-guest wedding in Paphos – one trusted local company, one fixed price.</p></div>
 <div class="grid g3">{cards}</div>
</div></section>

<section id="how" class="section section-alt"><div class="wrap">
 <div class="section-head center"><span class="eyebrow">How it works</span><h2>Booked in a minute, met at the gate</h2></div>
 <ol class="steps grid g3">
  <li><h3>Send your trip</h3><p>Use the quote form or WhatsApp: flight number, destination, passengers and luggage.</p></li>
  <li><h3>Get a fixed price</h3><p>We reply within minutes with an all-inclusive price. Nothing to pay to book.</p></li>
  <li><h3>Meet your driver</h3><p>Your driver tracks your flight and waits in arrivals with your name on a sign.</p></li>
 </ol>
</div></section>

<section id="about" class="section"><div class="wrap split">
 <div class="photo"><picture><source type="image/webp" srcset="/assets/img/van-paphos-castle-640.webp 640w, /assets/img/van-paphos-castle-960.webp 960w" sizes="(max-width:900px) 100vw, 560px"><img src="/assets/img/van-paphos-castle-960.jpg" width="960" height="317" loading="lazy" alt="Volan Premium Transfers minibus near Paphos harbour castle"></picture></div>
 <div>
  <span class="eyebrow">About Volan</span>
  <h2>A local Cyprus transfer company that answers the phone</h2>
  <p>Volan Premium Transfers is a licensed Cyprus transport operator offering private airport transfers, minibus hire with professional drivers. We serve both international airports – Larnaca (LCA) and Paphos (PFO) – and every resort on the island, 24 hours a day.</p>
  <p>You deal directly with us, not a booking platform: one WhatsApp conversation for your quote, your driver's details and any last-minute changes.</p>
  <ul class="checks">
   <li>{ic("check")} Private, door-to-door – never shared with other passengers</li>
   <li>{ic("check")} Fixed prices confirmed before you travel, no hidden fees</li>
   <li>{ic("check")} Free baby and child seats on request</li>
   <li>{ic("check")} English and Greek speaking drivers</li>
  </ul>
 </div>
</div></section>

<section id="fleet" class="section section-alt"><div class="wrap">
 <div class="section-head center"><span class="eyebrow">Our vehicles</span><h2>Minibuses and buses for 8 to 55 passengers</h2>
 <p class="lead">Every group gets the right size of vehicle – air-conditioned, with room for luggage and a professional driver. For bigger groups we send several vehicles together, so there is no limit on group size.</p></div>
 <ul class="seats">
  <li><b>8</b><span><strong>Up to 8 passengers</strong>Couples, families and small groups</span></li>
  <li><b>13</b><span><strong>Up to 13 passengers</strong>Large families and groups of friends</span></li>
  <li><b>17</b><span><strong>Up to 17 passengers</strong>Teams, golf groups and parties</span></li>
  <li><b>21</b><span><strong>Up to 21 passengers</strong>Weddings, events and corporate groups</span></li>
  <li><b>30</b><span><strong>Up to 30 passengers</strong>Large groups, tours and conferences</span></li>
  <li><b>55</b><span><strong>Up to 55 passengers</strong>55-seater bus for big groups and events</span></li>
 </ul>
 <p class="note center">Free child seats on request. Bigger group? We combine vehicles so everyone travels together.</p>
</div></section>

<section id="routes" class="section"><div class="wrap">
 <div class="section-head center"><span class="eyebrow">Routes</span><h2>Popular transfers and journey times</h2>
 <p class="lead">Private transfers from Larnaca and Paphos airports to every resort in Cyprus.</p></div>
 {routes_table(rows, "Cyprus airport transfer distances and times")}
</div></section>

<section id="faq" class="section section-alt"><div class="wrap">
 <div class="section-head center"><span class="eyebrow">FAQ</span><h2>Frequently asked questions</h2></div>
 {faq_html(HOME_FAQ)}
</div></section>

{quote_section()}
</main>
''' + footer()
    write("/", out)

home()

# 404
write404 = head("Page not found | Volan Premium Transfers", "This page could not be found.", "/404", []).replace('content="index, follow, max-image-preview:large"', 'content="noindex"') + header("") + f'''<main id="main"><section class="page-hero"><div class="wrap"><h1>Page not found</h1><p class="lead">The page you were looking for doesn't exist. Try one of our transfers below or message us on WhatsApp.</p>
<div class="hero-ctas"><a class="btn btn-gold" href="/">Go to homepage</a><a class="btn btn-ghost" href="{WA}" target="_blank" rel="noopener">{ic("chat")} WhatsApp {PHONE_H}</a></div></div></section>
<section class="section"><div class="wrap"><div class="grid g3">''' + "".join(f'<a class="card" href="{h}"><h3>{t}</h3><span class="more">View {ic("arrow")}</span></a>' for h, t in ALL_PAGES) + '</div></div></section></main>' + footer()
open(os.path.join(OUT, "404.html"), "w").write(write404)

# sitemap
urls = ["/"] + [h for h, _ in ALL_PAGES]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f'  <url><loc>{SITE}{u}</loc><lastmod>{LASTMOD}</lastmod></url>\n' for u in urls) + '</urlset>\n'
open(os.path.join(OUT, "sitemap.xml"), "w").write(sm)
print("ok", urls)
