#!/usr/bin/env python3
"""Generates the full Pro-Worx ADU microsite: homepage, 19 city pages, blog scaffold."""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'data'))
from cities import CITIES, TESTIMONIALS, FAQS

ROOT = os.path.dirname(__file__)

HEAD_COMMON = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,500&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' rx='20' fill='%23132030'/%3E%3Ctext x='50' y='68' font-family='Georgia,serif' font-weight='700' font-size='58' fill='%232a5d99' text-anchor='middle'%3EP%3C/text%3E%3C/svg%3E">
<link rel="stylesheet" href="/assets/style.css">"""

CHECK_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>'
CHEVRON_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>'
PIN_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>'
STAR_SVG = '<svg viewBox="0 0 24 24"><polygon points="12 2 15 9 22 9 16.5 13.5 18.5 21 12 17 5.5 21 7.5 13.5 2 9 9 9"/></svg>'
SHIELD_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2 4 6v6c0 5 3.5 8.5 8 10 4.5-1.5 8-5 8-10V6z"/></svg>'
CLOCK_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>'
CLIPBOARD_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="8" y="2" width="8" height="4" rx="1"/><path d="M9 4H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2h-3"/><line x1="9" y1="12" x2="15" y2="12"/><line x1="9" y1="16" x2="15" y2="16"/></svg>'
HAMMER_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 12l-8.5 8.5a2.12 2.12 0 1 1-3-3L12 9"/><path d="M17.64 15 22 10.64"/><path d="m20.91 11.7-1.25-1.25c-.6-.6-.93-1.4-.93-2.25v-.86L16.01 4.6a5.56 5.56 0 0 0-3.94-1.64H9l.92.82A6.18 6.18 0 0 1 12 8.4v1.56l2 2h2.47l2.26 1.91"/></svg>'

MENU_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>'
PHONE_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.362 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.338 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'
MAIL_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16v16H4z"/><path d="M22 6l-10 7L2 6"/></svg>'
CLOCK2_SVG = CLOCK_SVG

CITY_IMAGES = [
    "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?q=80&w=1600&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1600566752355-35792bedcfea?q=80&w=1600&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?q=80&w=1600&auto=format&fit=crop",
]

def header_nav(active_areas=False):
    return f"""<header>
  <div class="container">
    <a href="/index.html" class="wordmark">PRO-WORX ADU<span>PRO-WORX CONSTRUCTION</span></a>
    <nav class="desktop-nav">
      <a href="/index.html#what-is-adu">What's an ADU?</a>
      <a href="/index.html#plans">Plans &amp; Pricing</a>
      <a href="/index.html#process">Our Process</a>
      <a href="/index.html#portfolio">Portfolio</a>
      <a href="/index.html#areas">Service Areas</a>
      <a href="/blog/index.html">Blog</a>
      <a href="/index.html#faq">FAQ</a>
    </nav>
    <div style="display:flex; align-items:center; gap:12px;">
      <a href="tel:8018884282" class="nav-cta btn btn-outline">(801) 888-4282</a>
      <a href="/index.html#contact" class="nav-cta btn btn-primary">GET FREE ESTIMATE</a>
      <button class="menu-btn" id="menuBtn" aria-label="Toggle menu">{MENU_SVG}</button>
    </div>
  </div>
  <div class="mobile-menu" id="mobileMenu">
    <a href="/index.html#what-is-adu">What's an ADU?</a>
    <a href="/index.html#plans">Plans &amp; Pricing</a>
    <a href="/index.html#process">Our Process</a>
    <a href="/index.html#portfolio">Portfolio</a>
    <a href="/index.html#areas">Service Areas</a>
    <a href="/blog/index.html">Blog</a>
    <a href="/index.html#faq">FAQ</a>
    <a href="tel:8018884282" class="btn btn-outline">(801) 888-4282</a>
    <a href="/index.html#contact" class="btn btn-primary">GET FREE ESTIMATE</a>
  </div>
</header>"""

FOOTER = """<footer>
  <div class="container">
    <div class="footer-grid">
      <div class="footer-col">
        <a href="/index.html" class="wordmark">PRO-WORX ADU</a>
        <p class="footer-desc">A Pro-Worx Construction company. Utah's fixed-price ADU builder — permits, design and construction, handled.</p>
      </div>
      <div class="footer-col">
        <h4>Explore</h4>
        <a href="/index.html#what-is-adu">What's an ADU?</a>
        <a href="/index.html#plans">Plans &amp; Pricing</a>
        <a href="/index.html#process">Our Process</a>
        <a href="/index.html#portfolio">Portfolio</a>
        <a href="/blog/index.html">Blog</a>
      </div>
      <div class="footer-col">
        <h4>Company</h4>
        <a href="/index.html#areas">Service Areas</a>
        <a href="/index.html#faq">FAQ</a>
        <a href="/index.html#contact">Get an Estimate</a>
      </div>
      <div class="footer-col">
        <h4>Contact</h4>
        <p>(801) 888-4282</p>
        <p>info@proworxconstruction.com</p>
        <p>Mon&ndash;Fri: 8AM&ndash;6PM</p>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; <span id="year"></span> Pro-Worx Construction. All rights reserved.</p>
      <p>Licensed &amp; insured Utah general contractor.</p>
    </div>
  </div>
</footer>

<div class="sticky-cta">
  <a href="/index.html#contact" class="btn btn-primary">GET FREE ESTIMATE</a>
</div>

<script src="/assets/main.js"></script>"""

def estimate_form(prefill_city=""):
    options = ""
    for name, slug, county in CITIES:
        sel = " selected" if name == prefill_city else ""
        options += f'<option{sel}>{name}</option>\n              '
    return f"""<div class="light-card">
        <form id="estimateForm">
          <div class="field-row">
            <div class="field"><label for="fname">First Name</label><input type="text" id="fname" name="fname" required></div>
            <div class="field"><label for="lname">Last Name</label><input type="text" id="lname" name="lname" required></div>
          </div>
          <div class="field-row">
            <div class="field"><label for="phone">Phone</label><input type="tel" id="phone" name="phone" required></div>
            <div class="field"><label for="email">Email</label><input type="email" id="email" name="email" required></div>
          </div>
          <div class="field">
            <label for="city">City</label>
            <select id="city" name="city" required>
              <option value="">Select your city</option>
              {options}<option>Other</option>
            </select>
          </div>
          <div class="field">
            <label for="adutype">ADU Type of Interest</label>
            <select id="adutype" name="adutype">
              <option value="">Not sure yet</option>
              <option>Detached Backyard ADU</option>
              <option>Garage Conversion</option>
              <option>Basement Conversion</option>
            </select>
          </div>
          <div class="field">
            <label for="message">Tell us about your project</label>
            <textarea id="message" name="message" placeholder="Lot size, goals, timeline..."></textarea>
          </div>
          <button type="submit" class="btn btn-primary" style="width:100%;">REQUEST FREE ESTIMATE</button>
          <p class="form-note">By submitting, you agree to be contacted about your ADU project. No spam, ever.</p>
          <div class="form-success" id="formSuccess">
            <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
            <span>Thanks! We'll be in touch within one business day.</span>
          </div>
        </form>
      </div>"""

def contact_section(prefill_city=""):
    return f"""<section class="bg-secondary" id="contact">
  <div class="container">
    <div class="contact-wrap reveal">
      <div>
        <p class="eyebrow">GET STARTED</p>
        <h2 style="font-size:32px; margin-bottom:16px;">Request a Free ADU Estimate</h2>
        <p class="lede" style="margin-bottom:32px;">Tell us about your property and we'll follow up with next steps &mdash; usually within one business day.</p>
        <div class="contact-row">{PHONE_SVG}<div><p class="label">Call us</p><p class="value">(801) 888-4282</p></div></div>
        <div class="contact-row">{MAIL_SVG}<div><p class="label">Email</p><p class="value">info@proworxconstruction.com</p></div></div>
        <div class="contact-row">{PIN_SVG}<div><p class="label">Service area</p><p class="value">Salt Lake, Utah, Davis &amp; Summit counties</p></div></div>
        <div class="contact-row">{CLOCK2_SVG}<div><p class="label">Hours</p><p class="value">Mon&ndash;Fri: 8AM&ndash;6PM</p></div></div>
      </div>
      {estimate_form(prefill_city)}
    </div>
  </div>
</section>"""

def page_shell(title, description, body, canonical_path):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
{HEAD_COMMON}
</head>
<body>

{header_nav()}

<div id="top"></div>

{body}

{FOOTER}

</body>
</html>
"""

def build_city_page(name, slug, county, index):
    n_t = len(TESTIMONIALS)
    rotated_testimonials = [TESTIMONIALS[(index + i) % n_t] for i in range(n_t)]
    hero_img = CITY_IMAGES[index % len(CITY_IMAGES)]
    others = [c for c in CITIES if c[2] == county and c[1] != slug]
    if len(others) < 3:
        others = others + [c for c in CITIES if c[1] != slug and c not in others]
    nearby = others[:4]

    nearby_chips = "\n      ".join(
        f'<a href="/locations/{s}.html" class="city-chip">{PIN_SVG}{n}</a>' for n, s, c in nearby
    )

    faq_html = ""
    for q, a in FAQS:
        q_f = q.format(city=name, county=county)
        a_f = a.format(city=name, county=county)
        faq_html += f"""      <div class="accordion-item">
        <button class="accordion-trigger">{q_f}
          {CHEVRON_SVG}
        </button>
        <div class="accordion-panel"><p>{a_f}</p></div>
      </div>
"""

    testimonial_cards = ""
    for t in rotated_testimonials:
        testimonial_cards += f"""      <div class="testimonial-card">
        <div class="stars">{STAR_SVG}{STAR_SVG}{STAR_SVG}{STAR_SVG}{STAR_SVG}</div>
        <p class="quote">&ldquo;{t['quote']}&rdquo;</p>
        <p class="testimonial-author">{t['author']}</p>
        <p class="testimonial-role">{t['role']}</p>
      </div>
"""

    body = f"""<div class="container">
  <div class="breadcrumb">
    <a href="/index.html">Home</a><span>/</span>
    <a href="/index.html#areas">Service Areas</a><span>/</span>
    <span class="current">{name}</span>
  </div>
</div>

<!-- CITY HERO -->
<section class="page-hero" style="--page-hero-img:url('{hero_img}');">
  <div class="page-hero-bg"></div>
  <div class="container">
    <p class="eyebrow fade-up d1">{county.upper()} COUNTY &middot; UTAH ADU SPECIALISTS</p>
    <h1 class="fade-up d2">Thinking About Building an ADU in {name}?</h1>
    <p class="lede fade-up d3">Pro-Worx Construction designs, permits and builds custom Accessory Dwelling Units for {name} homeowners &mdash; fixed pricing, licensed &amp; insured, 3&ndash;5 week builds on garage and basement conversions.</p>
    <div class="hero-ctas fade-up d4" style="margin-top:32px;">
      <a href="#contact" class="btn btn-primary">GET FREE ESTIMATE</a>
      <a href="/index.html#plans" class="btn btn-light">SEE ADU PLANS &amp; PRICING</a>
    </div>
  </div>
</section>

<div class="container">
  <div class="stats-bar" id="statsBar">
    <div class="stat"><div class="num" data-count="1100" data-suffix="+">0</div><div class="label">Projects Completed</div></div>
    <div class="stat"><div class="num" data-count="15" data-suffix="+">0</div><div class="label">Years of Excellence</div></div>
    <div class="stat"><div class="num">5&#9733;</div><div class="label">Google Rating</div></div>
    <div class="stat"><div class="num" data-count="19" data-suffix="">0</div><div class="label">Utah Cities Served</div></div>
  </div>
</div>

<!-- OVERVIEW -->
<section>
  <div class="container">
    <div class="whatis reveal">
      <div>
        <p class="eyebrow">ADUs IN {name.upper()}</p>
        <h2>Add a Second Home to Your {name} Property</h2>
        <p class="lede">Whether you're looking to house family, add rental income, or increase your property's value, an Accessory Dwelling Unit is one of the fastest-growing home additions in {county} County. Pro-Worx handles design, permitting and construction for {name} homeowners from first estimate to final walkthrough.</p>
        <div class="check-list">
          <div class="check-item">{CHECK_SVG}<span>Detached, attached and basement/garage-conversion ADUs</span></div>
          <div class="check-item">{CHECK_SVG}<span>Full permitting handled with the {name} building department</span></div>
          <div class="check-item">{CHECK_SVG}<span>Fixed-price plan tiers so there are no surprises on cost</span></div>
          <div class="check-item">{CHECK_SVG}<span>Built by the same licensed &amp; insured team behind Pro-Worx Construction</span></div>
        </div>
      </div>
      <img src="https://images.unsplash.com/photo-1449844908441-8829872d2607?q=80&w=1200&auto=format&fit=crop" alt="Backyard ADU cottage in {name}, Utah">
    </div>
  </div>
</section>

<!-- SERVICES -->
<section class="bg-secondary">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">OUR SERVICES</p>
      <h2>Which ADU Is Right for Your {name} Lot?</h2>
      <p class="lede">Every property is different &mdash; we'll walk your site and recommend the configuration that fits your space, budget and goals.</p>
    </div>
    <div class="grid grid-3 reveal">
      <div class="image-tile">
        <img src="https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?q=80&w=800&auto=format&fit=crop" alt="Detached backyard ADU">
        <div class="scrim"></div>
        <div class="tile-content">
          <h3>Detached Backyard ADU</h3>
          <p>A standalone cottage with its own entrance, kitchen and bath.</p>
        </div>
      </div>
      <div class="image-tile">
        <img src="https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?q=80&w=800&auto=format&fit=crop" alt="Garage conversion ADU">
        <div class="scrim"></div>
        <div class="tile-content">
          <h3>Garage Conversion</h3>
          <p>Turn an underused garage into a fully permitted living space.</p>
        </div>
      </div>
      <div class="image-tile">
        <img src="https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?q=80&w=800&auto=format&fit=crop" alt="Basement conversion ADU">
        <div class="scrim"></div>
        <div class="tile-content">
          <h3>Basement Conversion</h3>
          <p>Leverage the same basement-finishing expertise Pro-Worx is known for.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- PERMIT CALLOUT + SEASONAL -->
<section>
  <div class="container">
    <div class="grid grid-2 reveal">
      <div class="permit-callout">
        {CLIPBOARD_SVG}
        <div>
          <h3>Permits &amp; {name} Zoning</h3>
          <p>Most ADU permits in {county} County are processed through the {name} building and planning department. We handle intake, plan review coordination and inspection scheduling for you from start to finish, so you never have to deal with the city directly.</p>
        </div>
      </div>
      <div class="seasonal-band">
        {HAMMER_SVG}
        <p><strong>Built for Utah's climate.</strong> Freeze-thaw winters make proper foundation insulation and drainage critical for a comfortable, durable ADU year-round &mdash; every Pro-Worx build is engineered to code for our climate, not a generic template.</p>
      </div>
    </div>
  </div>
</section>

<!-- PROCESS -->
<section class="bg-secondary">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">HOW IT WORKS</p>
      <h2>Your {name} ADU, Four Steps From Now</h2>
    </div>
    <div class="grid grid-4 reveal">
      <div class="process-step"><div class="medallion">1</div><h3>Free Estimate</h3><p>We walk your property and talk through what's possible for your lot and budget.</p></div>
      <div class="process-step"><div class="medallion">2</div><h3>Design &amp; Permits</h3><p>We handle plans and permitting with {name} from start to finish.</p></div>
      <div class="process-step"><div class="medallion">3</div><h3>Construction</h3><p>Our crews build on schedule with weekly updates, start to finish.</p></div>
      <div class="process-step"><div class="medallion">4</div><h3>Move-In Ready</h3><p>Final walkthrough, final inspection, and the keys are yours.</p></div>
    </div>
  </div>
</section>

<!-- WHY CHOOSE US -->
<section>
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">WHY {name.upper()} HOMEOWNERS CHOOSE US</p>
      <h2>What Sets Pro-Worx Apart</h2>
    </div>
    <div class="grid grid-4 reveal">
      <div class="light-card static"><div class="icon-circle">{SHIELD_SVG}</div><h3 style="margin-top:16px; font-size:18px;">Licensed &amp; Insured</h3><p style="font-size:14px; color:var(--muted-foreground); margin-top:8px;">Full Utah general contractor license, on every job.</p></div>
      <div class="light-card static"><div class="icon-circle">{CLOCK_SVG}</div><h3 style="margin-top:16px; font-size:18px;">On Time, On Budget</h3><p style="font-size:14px; color:var(--muted-foreground); margin-top:8px;">Fixed pricing with no hidden fees, ever.</p></div>
      <div class="light-card static"><div class="icon-circle">{CLIPBOARD_SVG}</div><h3 style="margin-top:16px; font-size:18px;">Permits Handled</h3><p style="font-size:14px; color:var(--muted-foreground); margin-top:8px;">We manage the entire {name} approval process.</p></div>
      <div class="light-card static"><div class="icon-circle">{HAMMER_SVG}</div><h3 style="margin-top:16px; font-size:18px;">1,100+ Projects</h3><p style="font-size:14px; color:var(--muted-foreground); margin-top:8px;">15+ years building across Utah.</p></div>
    </div>
  </div>
</section>

<!-- TESTIMONIAL -->
<section class="bg-secondary">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">TESTIMONIALS</p>
      <h2>What Homeowners Are Saying</h2>
    </div>
    <div class="grid grid-3 reveal">
{testimonial_cards}    </div>
  </div>
</section>

<!-- NEARBY AREAS -->
<section>
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">ALSO SERVING</p>
      <h2>Nearby {county} County Areas</h2>
    </div>
    <div class="nearby-list reveal" style="justify-content:center;">
      {nearby_chips}
    </div>
  </div>
</section>

<!-- FAQ -->
<section class="bg-secondary">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">FREQUENTLY ASKED QUESTIONS</p>
      <h2>ADU Questions from {name} Homeowners</h2>
    </div>
    <div class="accordion reveal">
{faq_html}    </div>
  </div>
</section>

{contact_section(name)}"""

    title = f"ADU Builder in {name}, UT | Pro-Worx ADU"
    desc = f"Pro-Worx builds custom Accessory Dwelling Units in {name}, Utah. Fixed pricing, full permitting with the {name} building department, licensed & insured. Get a free ADU estimate."
    return page_shell(title, desc, body, f"/locations/{slug}.html")


def build_locations():
    out_dir = os.path.join(ROOT, 'locations')
    os.makedirs(out_dir, exist_ok=True)
    for i, (name, slug, county) in enumerate(CITIES):
        html = build_city_page(name, slug, county, i)
        with open(os.path.join(out_dir, f"{slug}.html"), 'w') as f:
            f.write(html)
    print(f"Built {len(CITIES)} city pages")


def build_blog():
    posts = [
        {
            "slug": "how-much-does-an-adu-cost-in-utah",
            "title": "How Much Does an ADU Cost in Utah? A 2026 Pricing Breakdown",
            "cat": "Pricing",
            "excerpt": "A realistic look at what drives ADU pricing across Salt Lake, Utah, Davis and Summit counties &mdash; from garage conversions to detached cottages.",
            "img": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?q=80&w=1200&auto=format&fit=crop",
        },
        {
            "slug": "adu-permits-utah-what-to-know",
            "title": "ADU Permits in Utah: What Every Homeowner Should Know Before Building",
            "cat": "Permitting",
            "excerpt": "Zoning, setbacks, utility hookups and inspections &mdash; what actually happens between your first estimate and your first tenant.",
            "img": "https://images.unsplash.com/photo-1600566752355-35792bedcfea?q=80&w=1200&auto=format&fit=crop",
        },
        {
            "slug": "garage-conversion-vs-detached-adu",
            "title": "Garage Conversion vs. Detached ADU: Which Is Right for Your Lot?",
            "cat": "Planning",
            "excerpt": "The two most common ADU paths compared on cost, timeline and privacy, so you can pick the right fit for your property.",
            "img": "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?q=80&w=1200&auto=format&fit=crop",
        },
    ]

    cards = ""
    for p in posts:
        cards += f"""      <a href="/blog/{p['slug']}.html" class="blog-card" style="display:block;">
        <div class="blog-thumb"><img src="{p['img']}" alt="{p['title']}"></div>
        <div class="blog-body">
          <span class="blog-cat">{p['cat']}</span>
          <h3>{p['title']}</h3>
          <p>{p['excerpt']}</p>
          <p class="blog-meta">Pro-Worx ADU Team</p>
        </div>
      </a>
"""

    body = f"""<div class="container">
  <div class="breadcrumb">
    <a href="/index.html">Home</a><span>/</span>
    <span class="current">Blog</span>
  </div>
</div>

<section style="padding-top:24px;">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">THE ADU BLOG</p>
      <h2>Guides &amp; Advice for Utah Homeowners</h2>
      <p class="lede">Everything we've learned building Accessory Dwelling Units across Salt Lake, Utah, Davis and Summit counties.</p>
    </div>
    <div class="grid grid-3 reveal">
{cards}    </div>
  </div>
</section>

{contact_section()}"""

    html = page_shell(
        "The ADU Blog | Pro-Worx ADU",
        "Guides on ADU pricing, permitting and planning for Utah homeowners, from the Pro-Worx ADU team.",
        body,
        "/blog/index.html",
    )
    with open(os.path.join(ROOT, 'blog', 'index.html'), 'w') as f:
        f.write(html)

    # One real sample post to establish the template; the rest are linked but
    # can be written for real once Roh has content ready.
    post_body = f"""<div class="container">
  <div class="breadcrumb">
    <a href="/index.html">Home</a><span>/</span>
    <a href="/blog/index.html">Blog</a><span>/</span>
    <span class="current">Pricing</span>
  </div>
</div>

<section style="padding-top:24px;">
  <div class="container">
    <div class="blog-post-body">
      <p class="eyebrow">PRICING</p>
      <h1 style="font-size:36px; margin-bottom:12px;">How Much Does an ADU Cost in Utah?</h1>
      <p class="post-meta">Pro-Worx ADU Team &middot; Utah ADU Guides</p>
      <p>Accessory Dwelling Units have become one of the most popular ways for Utah homeowners to add living space, house family or generate rental income &mdash; but the first question everyone asks is the same: what does it actually cost?</p>
      <h2>The short answer</h2>
      <p>Across Salt Lake, Utah, Davis and Summit counties, Pro-Worx ADU pricing starts at $95K for a garage or basement conversion and runs to $210K+ for a detached, ground-up 2-bedroom residence. Where your project lands in that range depends mainly on three things: the structure you're starting from, the size of the finished unit, and your lot's utility access.</p>
      <h2>What drives the price up or down</h2>
      <p>A garage or basement conversion is almost always the most affordable path, since the foundation, framing and roof already exist &mdash; the work is mostly interior build-out, plumbing and electrical. A detached, ground-up ADU costs more because it includes excavation, foundation, framing and a full exterior envelope, but it also offers the most privacy and flexibility for renters or family members.</p>
      <p>Utility hookups are the other major swing factor. If your existing service panel and sewer line have capacity for a second unit, costs stay predictable. If they don't, expect an additional line item for upgrades &mdash; something we flag clearly during your free estimate, never after signing.</p>
      <h2>Why fixed pricing matters</h2>
      <p>Every Pro-Worx ADU plan tier is a fixed price once we've walked your property, not a rough estimate that grows during construction. That's the same transparent-pricing standard we've applied to over 1,100 projects across Utah in 15+ years.</p>
      <p>Ready to see what your specific lot would cost? <a href="/index.html#contact" class="link-arrow">Get a free ADU estimate &rarr;</a></p>
    </div>
  </div>
</section>

{contact_section()}"""

    post_html = page_shell(
        "How Much Does an ADU Cost in Utah? | Pro-Worx ADU",
        "A realistic breakdown of Accessory Dwelling Unit pricing across Salt Lake, Utah, Davis and Summit counties.",
        post_body,
        "/blog/how-much-does-an-adu-cost-in-utah.html",
    )
    with open(os.path.join(ROOT, 'blog', 'how-much-does-an-adu-cost-in-utah.html'), 'w') as f:
        f.write(post_html)

    # Placeholder pages for the other two linked posts so no link 404s.
    for p in posts[1:]:
        placeholder_body = f"""<div class="container">
  <div class="breadcrumb">
    <a href="/index.html">Home</a><span>/</span>
    <a href="/blog/index.html">Blog</a><span>/</span>
    <span class="current">{p['cat']}</span>
  </div>
</div>

<section style="padding-top:24px;">
  <div class="container">
    <div class="blog-post-body">
      <p class="eyebrow">{p['cat'].upper()}</p>
      <h1 style="font-size:36px; margin-bottom:12px;">{p['title']}</h1>
      <p class="post-meta">Pro-Worx ADU Team &middot; Coming soon</p>
      <p>{p['excerpt']} We're finishing this guide &mdash; check back soon, or <a href="/index.html#contact" class="link-arrow">get a free estimate &rarr;</a> in the meantime.</p>
    </div>
  </div>
</section>

{contact_section()}"""
        placeholder_html = page_shell(
            f"{p['title']} | Pro-Worx ADU",
            p['excerpt'].replace('&mdash;', '-'),
            placeholder_body,
            f"/blog/{p['slug']}.html",
        )
        with open(os.path.join(ROOT, 'blog', f"{p['slug']}.html"), 'w') as f:
            f.write(placeholder_html)

    print("Built blog index + 3 posts")


if __name__ == '__main__':
    build_locations()
    build_blog()
