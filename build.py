#!/usr/bin/env python3
"""Generates the full Pro-Worx ADU microsite: homepage, 19 city pages, blog scaffold."""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'data'))
from cities import CITIES, TESTIMONIALS, FAQS, LOCAL_FOCUS, NEIGHBORHOODS, HILLSIDE_TERRAIN, HOA_HEAVY, WELL_SEPTIC, DEEP_HEADLINES

ROOT = os.path.dirname(__file__)

# Update this the moment a custom domain is live (e.g. https://proworxadu.com)
# — canonical tags, sitemap.xml, robots.txt and JSON-LD all key off it, so
# this one line is the whole migration.
BASE_URL = "https://proworxadu.roheeni-bhana.workers.dev"

# Tracks every page we generate (path, changefreq, priority) so sitemap.xml
# stays in sync with whatever build_* functions actually write to disk.
SITEMAP_ENTRIES = []

def _register(path, changefreq="monthly", priority="0.6"):
    SITEMAP_ENTRIES.append((path, changefreq, priority))

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
    <a href="/index.html" class="wordmark">PRO-WORX ADU</a>
    <nav class="desktop-nav">
      <a href="/index.html#what-is-adu">What's an ADU?</a>
      <a href="/index.html#plans">Plans &amp; Pricing</a>
      <a href="/index.html#portfolio">Portfolio</a>
      <a href="/index.html#areas">Service Areas</a>
      <div class="nav-dropdown">
        <button class="nav-dropdown-trigger" type="button" aria-haspopup="true">Resources {CHEVRON_SVG}</button>
        <div class="nav-dropdown-menu">
          <a href="/blog/index.html">Blog</a>
          <a href="/adu-rules-2026.html">2026 ADU Law</a>
          <a href="/index.html#faq">FAQ</a>
        </div>
      </div>
    </nav>
    <div style="display:flex; align-items:center; gap:12px;">
      <a href="tel:8018884282" class="nav-cta btn btn-outline">(801) 888-4282</a>
      <a href="/index.html#contact" class="nav-cta btn btn-primary" style="text-transform:none; letter-spacing:normal;">Free Estimate</a>
      <button class="menu-btn" id="menuBtn" aria-label="Toggle menu">{MENU_SVG}</button>
    </div>
  </div>
  <div class="mobile-menu" id="mobileMenu">
    <a href="/index.html#what-is-adu">What's an ADU?</a>
    <a href="/index.html#plans">Plans &amp; Pricing</a>
    <a href="/index.html#portfolio">Portfolio</a>
    <a href="/index.html#areas">Service Areas</a>
    <a href="/blog/index.html">Blog</a>
    <a href="/adu-rules-2026.html">2026 ADU Law</a>
    <a href="/index.html#faq">FAQ</a>
    <a href="tel:8018884282" class="btn btn-outline">(801) 888-4282</a>
    <a href="/index.html#contact" class="btn btn-primary" style="text-transform:none; letter-spacing:normal;">Free Estimate</a>
  </div>
</header>"""

FOOTER = """<footer>
  <div class="container">
    <div class="footer-grid">
      <div class="footer-col">
        <a href="/index.html" class="wordmark">PRO-WORX ADU</a>
        <p class="footer-desc">A <a href="https://proworxconstruction.com" target="_blank" rel="noopener">Pro-Worx Construction</a> company. 20 years building in Utah. Utah's fixed-price ADU builder. Permits, design and construction, handled. <a href="https://proworxconstruction.com/adu-builders-utah/" target="_blank" rel="noopener" style="text-decoration:underline;">See our full ADU services on the main site &rarr;</a></p>
      </div>
      <div class="footer-col">
        <h4>Explore</h4>
        <a href="/index.html#what-is-adu">What's an ADU?</a>
        <a href="/index.html#plans">Plans &amp; Pricing</a>
        <a href="/index.html#portfolio">Portfolio</a>
        <a href="/index.html#areas">Service Areas</a>
      </div>
      <div class="footer-col">
        <h4>Resources</h4>
        <a href="/blog/index.html">Blog</a>
        <a href="/adu-rules-2026.html">2026 ADU Law Changes</a>
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
      <p>Licensed &amp; insured Utah general contractor &middot; License #11334534-5501</p>
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
        <p class="lede" style="margin-bottom:32px;">Tell us about your property and we'll follow up with next steps. Usually within one business day.</p>
        <div class="contact-row">{PHONE_SVG}<div><p class="label">Call us</p><p class="value">(801) 888-4282</p></div></div>
        <div class="contact-row">{MAIL_SVG}<div><p class="label">Email</p><p class="value">info@proworxconstruction.com</p></div></div>
        <div class="contact-row">{PIN_SVG}<div><p class="label">Service area</p><p class="value">Salt Lake, Utah, Davis &amp; Summit counties</p></div></div>
        <div class="contact-row">{CLOCK2_SVG}<div><p class="label">Hours</p><p class="value">Mon&ndash;Fri: 8AM&ndash;6PM</p></div></div>
      </div>
      {estimate_form(prefill_city)}
    </div>
  </div>
</section>"""

def page_shell(title, description, body, canonical_path, json_ld=None):
    canonical_url = f"{BASE_URL}{canonical_path}"
    json_ld_tags = ""
    if json_ld:
        for block in json_ld:
            json_ld_tags += f'<script type="application/ld+json">{block}</script>\n'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical_url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical_url}">
<meta name="twitter:card" content="summary">
{HEAD_COMMON}
{json_ld_tags}</head>
<body>

{header_nav()}

<div id="top"></div>

{body}

{FOOTER}

</body>
</html>
"""

def deep_content_section(name, slug, county):
    """Long-form, hyper-local ADU content block for a city page: cost/ROI
    table, terrain/permit/inspection detail, optional HOA section, and a
    quote-evaluation checklist. Modeled on the depth of the main site's
    Alpine renovation page. National benchmark figures are sourced and
    disclaimed rather than presented as confirmed local numbers."""

    neighborhoods = NEIGHBORHOODS.get(slug)
    neighborhood_intro = ""
    if neighborhoods:
        tags = "".join(f'<span class="neighborhood-tag">{n}</span>' for n in neighborhoods)
        neighborhood_intro = f"""    <div class="content-block">
      <p>We've worked on ADU projects across {name}, including {', '.join(neighborhoods[:-1])} and {neighborhoods[-1]}, and lot conditions, HOA layers and permit timelines can differ block to block, not just neighborhood to neighborhood.</p>
      <div class="neighborhood-tags">{tags}</div>
    </div>
"""

    geotechnical = ""
    if slug in HILLSIDE_TERRAIN:
        geotechnical = f"""    <div class="content-block">
      <h3>Why {name} Lots Sometimes Need Engineering a Flat-Lot ADU Quote Won't Include</h3>
      <p>{name}'s hillside and bench terrain means some lots need a soils or geotechnical review before a detached ADU's foundation gets designed, a step flatter Utah cities often skip entirely. If a contractor is pricing your {name} ADU the same way they'd price one a few miles away on flat ground, that's usually where the budget goes sideways once excavation starts.</p>
      <div class="table-wrap">
        <table class="data-table">
          <tr><th>Item</th><th>Typical Range</th></tr>
          <tr><td>Geotechnical/soils review</td><td>$1,000&ndash;$5,000</td></tr>
          <tr><td>Standard single-family soils report</td><td>~$2,700 average</td></tr>
          <tr><td>Licensed engineer labor</td><td>$100&ndash;$250 per hour</td></tr>
        </table>
      </div>
      <p class="source-note">Source: <a href="https://www.homeadvisor.com/cost/architects-and-engineers/geotechnical-report" target="_blank" rel="noopener">HomeAdvisor geotechnical report cost data</a>, national averages, not confirmed against {name}-specific pricing. We'll tell you during your free estimate whether your lot needs this step at all.</p>
    </div>
"""

    hoa_section = ""
    if slug in HOA_HEAVY:
        hoa_name = neighborhoods[0] if neighborhoods else f"{name}'s master-planned communities"
        hoa_section = f"""    <div class="content-block">
      <h3>Do I Need HOA Approval in Addition to a {name} City Permit?</h3>
      <p>If your property is in one of {name}'s HOA-governed communities like {hoa_name}, clearing your city permit doesn't automatically clear your HOA's architectural review. They're separate approvals, and homeowners sometimes assume one covers the other. Most HOA design boards in these communities focus on exterior massing, materials and placement more than interior layout, but they still need to sign off before you build.</p>
      <p>We submit both in parallel from the start of your project, which is usually where an ADU either saves a few weeks or loses them.</p>
    </div>
"""

    well_septic = ""
    if slug in WELL_SEPTIC:
        well_septic = f"""    <div class="content-block">
      <h3>Well &amp; Septic Capacity Matters More Than Lot Size in {name}</h3>
      <p>Some {name} properties, especially on the outlying and foothill lots, are still on well water or a septic system rather than full city utilities. A detached ADU adds real load to both. Before we talk floor plans, we confirm your well's capacity and your septic system's rating can support a second living unit, since that's a harder constraint than anything in the zoning code.</p>
    </div>
"""

    headline, headline_lede = DEEP_HEADLINES.get(
        slug,
        (f"What Actually Goes Into an ADU Project in {name}",
         f"The permitting, engineering and cost questions that come up specifically for {name} homeowners. Not a generic statewide answer.")
    )

    body = f"""<!-- HYPER-LOCAL DEEP CONTENT -->
<section>
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">THE {name.upper()} DETAILS</p>
      <h2>{headline}</h2>
      <p class="lede">{headline_lede}</p>
    </div>
    <div class="blog-post-body reveal">
{neighborhood_intro}    <div class="content-block">
      <h3>What Does an ADU Cost in {name}?</h3>
      <p>Every ADU quote should scale with the scope of work, not just square footage. For context on how similar home-investment categories perform, <a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener" class="link-arrow">Zonda's 2025 Cost vs. Value Report</a> tracks return-on-investment for comparable projects nationally:</p>
      <div class="table-wrap">
        <table class="data-table">
          <tr><th>Project Type</th><th>Typical Cost</th><th>Typical ROI</th></tr>
          <tr><td>Basement remodel (comparable scope to an ADU conversion)</td><td>$65K&ndash;$120K+</td><td>~70&ndash;75%</td></tr>
          <tr><td>Home addition (comparable scope to a detached ADU)</td><td>$225&ndash;$375 / sq ft</td><td>~50&ndash;60%</td></tr>
        </table>
      </div>
      <p class="source-note">Source: <a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener">Zonda 2025 Cost vs. Value Report</a>, national data for comparable remodel categories. Your {name} ADU quote will reflect your specific lot, structure and finish level, not this table.</p>
      <p>Pro-Worx ADU pricing in {name} typically lands at $100K&ndash;$200K for a garage or basement conversion, and $200K&ndash;$300K for a full detached, ground-up build.</p>
    </div>
{geotechnical}{well_septic}    <div class="content-block">
      <h3>What Actually Triggers a Building Permit for an ADU in {name}?</h3>
      <p>Not every part of an ADU conversion needs a separate permit review, but most of the ones that matter do:</p>
      <div class="check-list" style="margin-bottom:20px;">
        <div class="check-item">{CHECK_SVG}<span>New footings, framing or any change to the structure's footprint</span></div>
        <div class="check-item">{CHECK_SVG}<span>New or relocated plumbing and electrical circuits</span></div>
        <div class="check-item">{CHECK_SVG}<span>Basement egress windows for any bedroom</span></div>
        <div class="check-item">{CHECK_SVG}<span>Separate utility metering, where the ADU is metered independently</span></div>
      </div>
      <div class="table-wrap">
        <table class="data-table">
          <tr><th>Permit Type</th><th>Typical Fee</th></tr>
          <tr><td>Bathroom addition</td><td>$100&ndash;$800</td></tr>
          <tr><td>Kitchen/kitchenette addition</td><td>$150&ndash;$1,000</td></tr>
          <tr><td>Room addition / detached structure</td><td>$500&ndash;$5,000+</td></tr>
          <tr><td>Electrical (new circuit/panel work)</td><td>$50&ndash;$500</td></tr>
        </table>
      </div>
      <p class="source-note">Source: <a href="https://permitmint.com/reports.php" target="_blank" rel="noopener">PermitMint national building permit data</a>, based on municipal fee schedules across 1,500+ US cities. National ranges only, not confirmed against {name}'s specific fee schedule. We confirm your exact fees with the {name} building department as part of your free estimate.</p>
    </div>
    <div class="content-block">
      <h3>What Gets Inspected During an ADU Build in {name}, and When?</h3>
      <p>Every ADU we build in {name} goes through the same three inspection stages: framing (before drywall goes up), rough electrical and plumbing (before walls close), and a final inspection before move-in. Egress windows get inspected specifically for size and clearance. A common point where unpermitted basement conversions fail if a homeowner tries to sell or refinance later.</p>
    </div>
{hoa_section}    <div class="content-block">
      <h3>What Should a Real {name} ADU Quote Include?</h3>
      <p>A quote that doesn't account for {name}'s specific conditions isn't necessarily wrong on purpose. It's usually just based on a generic countywide template. Before you sign anything, make sure your quote itemizes:</p>
      <div class="check-list">
        <div class="check-item">{CHECK_SVG}<span>Soils or engineering review, if your lot needs one</span></div>
        <div class="check-item">{CHECK_SVG}<span>HOA submission time priced into the schedule, not just build time</span></div>
        <div class="check-item">{CHECK_SVG}<span>Permit fees itemized by category, not bundled into a lump sum</span></div>
        <div class="check-item">{CHECK_SVG}<span>Utility separation costs, if you're metering the ADU independently</span></div>
      </div>
    </div>
    </div>
  </div>
</section>

"""
    return body


def deep_content_alpine():
    """Bespoke, research-backed deep-content section for Alpine. Real
    neighborhoods, real zoning code citations, real city hall address.
    Built by hand rather than through the generic per-city template."""
    return f"""<!-- HYPER-LOCAL DEEP CONTENT: ALPINE (bespoke) -->
<section>
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">THE ALPINE DETAILS</p>
      <h2>Can You Build an ADU in Alpine, and What Does Grading or HOA Review Add to It?</h2>
      <p class="lede">Alpine's large, sloped lots and conditional-use zoning make an ADU here a different conversation than it is a few miles away in flatter Utah County cities like Lehi or Lindon.</p>
    </div>

    <img class="deep-image reveal" src="https://images.unsplash.com/photo-1601918774946-25832a4be0d6?q=80&w=1800&auto=format&fit=crop" alt="Foothill homes on a sloped lot in Alpine, Utah, with mountain views">

    <div class="spec-cards reveal" style="max-width:900px; margin-left:auto; margin-right:auto; margin-bottom:56px;">
      <div class="spec-card"><div class="spec-value">10,251</div><div class="spec-label">Population (2020 Census)</div></div>
      <div class="spec-card"><div class="spec-value">5,049 ft</div><div class="spec-label">Elevation</div></div>
      <div class="spec-card"><div class="spec-value">1850</div><div class="spec-label">Settled (as "Mountainville")</div></div>
      <div class="spec-card"><div class="spec-value">Alpine School District</div><div class="spec-label">Serves the city</div></div>
    </div>

    <div class="deep-layout reveal">
      <nav class="deep-jumpnav">
        <a href="#alpine-neighborhoods">Neighborhoods</a>
        <a href="#alpine-zoning">Zoning &amp; Permits</a>
        <a href="#alpine-cost">Cost</a>
        <a href="#alpine-terrain">Terrain &amp; Engineering</a>
        <a href="#alpine-hoa">HOA Approval</a>
        <a href="#alpine-sources">Sources</a>
      </nav>
      <div class="blog-post-body" style="margin:0; max-width:none;">

        <div class="content-block" id="alpine-neighborhoods">
          <h3>{PIN_SVG} Alpine's Neighborhoods Aren't All Built the Same</h3>
          <p>We've scoped ADU projects across Alpine's east-bench and foothill neighborhoods, and grading conditions can differ block to block, not just neighborhood to neighborhood:</p>
          <div class="neighborhood-cards">
            <div class="neighborhood-card"><h4>Heritage Hills</h4><p>Mature east-bench subdivision with an active HOA architectural review board. Most homes built late 1990s&ndash;early 2000s.</p></div>
            <div class="neighborhood-card"><h4>Alpine Cove</h4><p>Planned community on Alpine's north end with a uniform design feel and its own covenants. Lots run slightly smaller than the Alpine average.</p></div>
            <div class="neighborhood-card"><h4>Willow Canyon</h4><p>East foothill custom-home lots with direct trail access and generous acreage. Grading and drainage engineering come up often here.</p></div>
            <div class="neighborhood-card"><h4>Box Elder Area</h4><p>Upper east-bench lots, frequently an acre or more, with sweeping valley views and mountain-adjacent terrain.</p></div>
            <div class="neighborhood-card"><h4>Lambert Park Area</h4><p>Homes near Alpine's 250-acre Lambert Park open space and its Fort Canyon trail system. A popular draw for families considering an ADU for extended family.</p></div>
            <div class="neighborhood-card"><h4>Three Falls</h4><p>A platted custom-lot subdivision on Alpine's east side, developed in phases. Larger parcels with the same soils-review considerations as neighboring Willow Canyon.</p></div>
          </div>
          <p style="margin-top:8px;">Alpine sits on the slopes of the Wasatch Range at 5,049 feet, with American Fork Canyon, Tibble Fork Reservoir and Mount Timpanogos all accessible from the city. That's part of why lot terrain here varies so much even within a single subdivision.</p>
        </div>

        <div class="content-block" id="alpine-zoning">
          <h3>{CLIPBOARD_SVG} What Does Alpine's Zoning Code Actually Say About ADUs?</h3>
          <p>Alpine City's Development Code lists accessory dwelling units as a <strong>conditional use</strong>, not an automatic right, in three residential zones, each with its own minimum lot size:</p>
          <div class="spec-cards">
            <div class="spec-card"><div class="spec-value">10,000 sq ft</div><div class="spec-label">TR-10,000 Zone</div></div>
            <div class="spec-card"><div class="spec-value">20,000 sq ft</div><div class="spec-label">CR-20,000 Zone</div></div>
            <div class="spec-card"><div class="spec-value">40,000 sq ft</div><div class="spec-label">CR-40,000 Zone</div></div>
          </div>
          <p>Because ADUs are a conditional use here, your project goes through Alpine's conditional-use review process, not just an over-the-counter permit, on top of whatever SB284 changes for detached ADUs specifically as of October 1, 2026. We confirm which zone your lot sits in and what that means for your timeline before you commit to anything.</p>
          <div class="office-callout">
            {PIN_SVG}
            <p><strong>Alpine City Hall &amp; Building Department</strong><br>20 North Main Street, Alpine, UT 84004. Where conditional-use applications and building permits for Alpine ADU projects are filed and reviewed.</p>
          </div>
        </div>

        <div class="content-block" id="alpine-cost">
          <h3>{SHIELD_SVG} What Does an ADU Cost in Alpine?</h3>
          <p>Alpine's larger lots and grading requirements push most quotes toward the higher end of the range, so it helps to see how comparable home-investment categories perform nationally, per <a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener" class="link-arrow">Zonda's 2025 Cost vs. Value Report</a>:</p>
          <div class="table-wrap">
            <table class="data-table">
              <tr><th>Project Type</th><th>Typical Cost</th><th>Typical ROI</th></tr>
              <tr><td>Basement remodel (comparable scope to an ADU conversion)</td><td>$65K&ndash;$120K+</td><td>~70&ndash;75%</td></tr>
              <tr><td>Home addition (comparable scope to a detached ADU)</td><td>$225&ndash;$375 / sq ft</td><td>~50&ndash;60%</td></tr>
            </table>
          </div>
          <p class="source-note">Source: <a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener">Zonda 2025 Cost vs. Value Report</a>, national data; your Alpine quote reflects your lot, zone and finish level, not this table.</p>
          <p>Pro-Worx ADU pricing in Alpine typically lands at $100K&ndash;$200K for a garage or basement conversion, and $200K&ndash;$300K for a full detached, ground-up build, often toward the higher end here given Alpine's larger lots and grading requirements.</p>
        </div>

        <div class="content-block" id="alpine-terrain">
          <h3>{HAMMER_SVG} Why Alpine Lots Sometimes Need Engineering a Flat-Lot Quote Won't Include</h3>
          <p>Alpine's hillside and bench terrain means many lots need a soils or geotechnical review before a detached ADU's foundation gets designed, a step flatter Utah County cities often skip entirely. If a contractor is pricing your Alpine ADU the same way they'd price one a few miles away on flat ground, that's usually where the budget goes sideways once excavation starts.</p>
          <div class="table-wrap">
            <table class="data-table">
              <tr><th>Item</th><th>Typical Range</th></tr>
              <tr><td>Geotechnical/soils review</td><td>$1,000&ndash;$5,000</td></tr>
              <tr><td>Standard single-family soils report</td><td>~$2,700 average</td></tr>
              <tr><td>Licensed engineer labor</td><td>$100&ndash;$250 per hour</td></tr>
            </table>
          </div>
          <p class="source-note">Source: <a href="https://www.homeadvisor.com/cost/architects-and-engineers/geotechnical-report" target="_blank" rel="noopener">HomeAdvisor geotechnical report cost data</a>, national averages, not confirmed against Alpine-specific pricing.</p>
        </div>

        <div class="content-block" id="alpine-hoa">
          <h3>{CLOCK_SVG} Do I Need HOA Approval Too?</h3>
          <p>If you're in Heritage Hills, Alpine Cove, or another HOA-governed subdivision, clearing your conditional-use permit with the city doesn't clear your HOA's architectural review. They're separate approvals. These design boards tend to focus on exterior massing and materials more than interior layout, but they still need to sign off. We submit both in parallel from the start, which is usually where a project either saves weeks or loses them.</p>
        </div>

        <div class="content-block" id="alpine-sources">
          <h3>Sources</h3>
          <ul class="sources-list">
            <li><a href="https://cdn.sqhk.co/alpinecity/jela7oF/AlpineCityDevelopmentCodeCurrent.pdf" target="_blank" rel="noopener">Alpine City Development Code</a>: zoning districts and conditional-use ADU provisions</li>
            <li><a href="https://www.alpineut.gov/157/Building-Department" target="_blank" rel="noopener">Alpine City Building Department</a>: permit process</li>
            <li><a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener">Zonda 2025 Cost vs. Value Report</a>: national remodel ROI benchmarks</li>
            <li><a href="https://www.homeadvisor.com/cost/architects-and-engineers/geotechnical-report" target="_blank" rel="noopener">HomeAdvisor</a>: geotechnical report cost data</li>
            <li><a href="/adu-rules-2026.html" class="link-arrow">Utah SB284: what changes October 1, 2026 &rarr;</a></li>
          </ul>
        </div>

      </div>
    </div>
  </div>
</section>

"""


def deep_content_lehi():
    """Bespoke, research-backed deep-content section for Lehi. Real
    neighborhoods, real ordinance history (Lehi already allowed detached
    ADUs before SB284), real city hall/permit details. Built by hand
    rather than through the generic per-city template."""
    return f"""<!-- HYPER-LOCAL DEEP CONTENT: LEHI (bespoke) -->
<section>
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">THE LEHI DETAILS</p>
      <h2>Did Lehi Already Allow Detached ADUs Before SB284?</h2>
      <p class="lede">Unlike cities writing an ADU ordinance from scratch for October 1, 2026, Lehi has allowed detached ADUs for years. The city just updated its existing rule, and city staff estimate roughly 20% more Lehi properties are now newly eligible.</p>
    </div>

    <img class="deep-image reveal" src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?q=80&w=1800&auto=format&fit=crop" alt="New-construction homes in a Lehi, Utah subdivision near Traverse Mountain">

    <div class="spec-cards reveal" style="max-width:900px; margin-left:auto; margin-right:auto; margin-bottom:56px;">
      <div class="spec-card"><div class="spec-value">~99,366</div><div class="spec-label">Population (2026 est.)</div></div>
      <div class="spec-card"><div class="spec-value">4,561 ft</div><div class="spec-label">Elevation</div></div>
      <div class="spec-card"><div class="spec-value">"Silicon Slopes"</div><div class="spec-label">Adobe, Ancestry &amp; tech HQs</div></div>
      <div class="spec-card"><div class="spec-value">Alpine School District</div><div class="spec-label">Serves the city</div></div>
    </div>

    <div class="deep-layout reveal">
      <nav class="deep-jumpnav">
        <a href="#lehi-neighborhoods">Neighborhoods</a>
        <a href="#lehi-zoning">Zoning &amp; Permits</a>
        <a href="#lehi-cost">Cost</a>
        <a href="#lehi-hoa">HOA Approval</a>
        <a href="#lehi-sources">Sources</a>
      </nav>
      <div class="blog-post-body" style="margin:0; max-width:none;">

        <div class="content-block" id="lehi-neighborhoods">
          <h3>{PIN_SVG} Lehi's Neighborhoods Range From Historic Lots to Brand-New Subdivisions</h3>
          <p>Lehi has grown roughly 9x since 1990, and that shows up in how differently ADU-eligible lots look from one part of the city to another:</p>
          <div class="neighborhood-cards">
            <div class="neighborhood-card"><h4>Traverse Mountain</h4><p>Master-planned hillside community at the Point of the Mountain with sloped lots and mountain views. Comes with its own HOA design-review layer on top of city permits.</p></div>
            <div class="neighborhood-card"><h4>Thanksgiving Point Area</h4><p>Established neighborhoods near the Thanksgiving Point attractions and gardens, mostly flat lots on standard city utilities.</p></div>
            <div class="neighborhood-card"><h4>Holbrook Farms</h4><p>Newer Ivory Homes subdivision in central/north Lehi, still building out in phases. Lots tend to run at or near the city's minimum ADU-eligible size.</p></div>
            <div class="neighborhood-card"><h4>Ivory Ridge</h4><p>North Lehi subdivision with a mix of home ages and lot sizes, close to I-15 access.</p></div>
            <div class="neighborhood-card"><h4>Cold Spring Ranch</h4><p>D.R. Horton-built north Lehi community with more uniform, newer-construction lot layouts.</p></div>
            <div class="neighborhood-card"><h4>Historic Downtown Lehi</h4><p>The original Main Street townsite. Smaller, older lots where a garage or basement conversion is often the more realistic ADU path than a detached build.</p></div>
          </div>
          <p style="margin-top:8px;">Lehi anchors what's become known as "Silicon Slopes," with Adobe's campus, Ancestry's headquarters and a Texas Instruments chip fab all in the city. That tech-worker population is part of why rental demand for a well-built ADU here tends to run strong.</p>
        </div>

        <div class="content-block" id="lehi-zoning">
          <h3>{CLIPBOARD_SVG} What Changed in Lehi's ADU Ordinance?</h3>
          <p>Lehi's council approved a Development Code Amendment on <strong>July 14, 2026</strong> to bring its long-standing detached-ADU rule in line with SB284. Here's the before and after:</p>
          <div class="table-wrap">
            <table class="data-table">
              <tr><th>Requirement</th><th>Old Lehi Rule</th><th>Updated Rule (SB284-aligned)</th></tr>
              <tr><td>Minimum lot size</td><td>14,520 sq ft</td><td>11,000 sq ft</td></tr>
              <tr><td>ADU size cap</td><td>1,300 sq ft flat cap</td><td>Must be smaller than the primary home</td></tr>
              <tr><td>Setback from primary home</td><td>&mdash;</td><td>6 feet</td></tr>
              <tr><td>Owner-occupancy</td><td>&mdash;</td><td>Owner must live in either the main house or the ADU</td></tr>
            </table>
          </div>
          <p>The practical effect: city staff estimate roughly 20% more Lehi properties are now newly eligible for a detached ADU. If your lot was turned down under the old 14,520-sq-ft threshold, it may qualify now. Height for new detached construction tops out around 35 feet, and a detached ADU over 650 sq ft typically needs 2 off-street parking spaces. We confirm your lot's exact status with Lehi's Planning Division before you commit to anything.</p>
          <div class="office-callout">
            {PIN_SVG}
            <p><strong>Lehi City Hall</strong><br>131 N 100 E, Lehi, UT 84043. Building permits route through the Building and Inspections Department at 153 N 100 E; zoning eligibility questions go to the Planning Division.</p>
          </div>
        </div>

        <div class="content-block" id="lehi-cost">
          <h3>{SHIELD_SVG} What Does an ADU Cost in Lehi?</h3>
          <p>With Lehi's newer subdivisions largely on standard city utilities, most quotes here track closer to the national averages than in hillside cities. <a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener" class="link-arrow">Zonda's 2025 Cost vs. Value Report</a> is a useful benchmark for how comparable projects perform:</p>
          <div class="table-wrap">
            <table class="data-table">
              <tr><th>Project Type</th><th>Typical Cost</th><th>Typical ROI</th></tr>
              <tr><td>Basement remodel (comparable scope to an ADU conversion)</td><td>$65K&ndash;$120K+</td><td>~70&ndash;75%</td></tr>
              <tr><td>Home addition (comparable scope to a detached ADU)</td><td>$225&ndash;$375 / sq ft</td><td>~50&ndash;60%</td></tr>
            </table>
          </div>
          <p class="source-note">Source: <a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener">Zonda 2025 Cost vs. Value Report</a>, national data; your Lehi quote reflects your lot, zone and finish level, not this table.</p>
          <p>Pro-Worx ADU pricing in Lehi typically lands at $100K&ndash;$200K for a garage or basement conversion, and $200K&ndash;$300K for a full detached, ground-up build. Lehi's detached ADU impact fee currently runs $4,528, which we itemize separately in every quote rather than folding it into a vague lump sum.</p>
        </div>

        <div class="content-block" id="lehi-hoa">
          <h3>{CLOCK_SVG} Do I Need HOA Approval Too?</h3>
          <p>If you're in Traverse Mountain, your ADU needs sign-off from the Traverse Mountain Master Association's Architectural Review Committee in addition to your city permit. Newer Thanksgiving Point-area communities like Holbrook Farms and Cold Spring Ranch typically carry their own HOAs as well. City approval and HOA approval are separate processes, and we submit both in parallel from the start so one doesn't stall the other.</p>
        </div>

        <div class="content-block" id="lehi-sources">
          <h3>Sources</h3>
          <ul class="sources-list">
            <li><a href="https://www.lehi-ut.gov/media/a4jh0mwb/accessory-dwelling-units-faqs.pdf" target="_blank" rel="noopener">Lehi City ADU FAQ</a>: setback, occupancy and height rules</li>
            <li><a href="https://www.engagelehi.org/detached-adu-development-code-amendment-state-requirements" target="_blank" rel="noopener">Engage Lehi: Detached ADU Development Code Amendment</a>: what changed and why</li>
            <li><a href="https://www.lehi-ut.gov/departments/building-and-inspections/" target="_blank" rel="noopener">Lehi Building and Inspections Department</a>: permit process and fees</li>
            <li><a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener">Zonda 2025 Cost vs. Value Report</a>: national remodel ROI benchmarks</li>
            <li><a href="/adu-rules-2026.html" class="link-arrow">Utah SB284: what changes October 1, 2026 &rarr;</a></li>
          </ul>
        </div>

      </div>
    </div>
  </div>
</section>

"""


def deep_content_mapleton():
    """Bespoke, research-backed deep-content section for Mapleton. Real
    tiered floor-area ordinance, real well/septic and TDR-foothill context,
    real neighborhoods. Built by hand rather than the generic template."""
    return f"""<!-- HYPER-LOCAL DEEP CONTENT: MAPLETON (bespoke) -->
<section>
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">THE MAPLETON DETAILS</p>
      <h2>Can You Build an ADU in Mapleton, or Does Well and Septic Capacity Stop You First?</h2>
      <p class="lede">Mapleton's lots run large by Utah County standards, so almost every property clears the minimum size for an ADU. The real qualifying questions here are about well capacity, septic systems and foothill drainage.</p>
    </div>

    <img class="deep-image reveal" src="https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?q=80&w=1800&auto=format&fit=crop" alt="Large-lot foothill property near Maple Mountain in Mapleton, Utah">

    <div class="spec-cards reveal" style="max-width:900px; margin-left:auto; margin-right:auto; margin-bottom:56px;">
      <div class="spec-card"><div class="spec-value">16,275</div><div class="spec-label">Population (2025 est., +43% since 2020)</div></div>
      <div class="spec-card"><div class="spec-value">13.34 sq mi</div><div class="spec-label">City area</div></div>
      <div class="spec-card"><div class="spec-value">1850</div><div class="spec-label">Settled (as "Union Bench")</div></div>
      <div class="spec-card"><div class="spec-value">Nebo School District</div><div class="spec-label">Serves the city</div></div>
    </div>

    <div class="deep-layout reveal">
      <nav class="deep-jumpnav">
        <a href="#mapleton-neighborhoods">Neighborhoods</a>
        <a href="#mapleton-zoning">Zoning &amp; Permits</a>
        <a href="#mapleton-utilities">Well &amp; Septic</a>
        <a href="#mapleton-cost">Cost</a>
        <a href="#mapleton-sources">Sources</a>
      </nav>
      <div class="blog-post-body" style="margin:0; max-width:none;">

        <div class="content-block" id="mapleton-neighborhoods">
          <h3>{PIN_SVG} Mapleton's Bench and Foothill Lots Aren't All the Same</h3>
          <p>Mapleton has grown more than 40% since the 2020 census, but it's held onto a large-lot, semi-rural character on purpose:</p>
          <div class="neighborhood-cards">
            <div class="neighborhood-card"><h4>Maple Hills Estates</h4><p>Active new-home community on Mapleton's bench, with lots generally sized comfortably above the city's ADU minimum.</p></div>
            <div class="neighborhood-card"><h4>Foothill &amp; Ranch Estate Lots</h4><p>Mapleton's development code carries dedicated Ranch Estate and Hillside Estate zones with their own setback rules, a sign of how seriously the city treats sloped-lot construction.</p></div>
            <div class="neighborhood-card"><h4>Hobble Creek Corridor</h4><p>Properties along Mapleton's northern boundary near Hobble Creek, where older, larger parcels are common.</p></div>
          </div>
          <p style="margin-top:8px;">The city uses Transferable Development Rights specifically to preserve its foothills near Maple Canyon and Spanish Fork Peak, part of why most residential lots here run a third of an acre to two acres or more. That's good news for ADU eligibility on paper, but it also means grading and drainage engineering come up more often than they would on a standard subdivision lot.</p>
        </div>

        <div class="content-block" id="mapleton-zoning">
          <h3>{CLIPBOARD_SVG} How Big Can a Detached ADU Be on Your Mapleton Lot?</h3>
          <p>Mapleton's ordinance (Municipal Code &sect;18.84.410, last amended June 2026) is unusual in Utah County for tying a detached ADU's maximum size to how big your lot actually is, rather than applying one flat cap to everyone:</p>
          <div class="table-wrap">
            <table class="data-table">
              <tr><th>Lot Size</th><th>Max Detached ADU Size</th></tr>
              <tr><td>11,000 &ndash; 87,119 sq ft</td><td>1,000 sq ft</td></tr>
              <tr><td>87,120 &ndash; 130,679 sq ft (2&ndash;3 acres)</td><td>1,200 sq ft</td></tr>
              <tr><td>3+ acres</td><td>1,400 sq ft</td></tr>
            </table>
          </div>
          <p>A detached ADU also needs to sit at least 10 feet behind the front wall of your main house, and the city requires one dedicated off-street parking stall. Internal accessory apartments have a lower bar: a 6,000-sq-ft minimum lot, provided the home keeps its single-family appearance from the street. Either way, owner-occupancy of the main house or the ADU is required, and the rule doesn't apply in the SDP-1 or R-2-B zones. We confirm your lot's tier and zone with Mapleton's Community Development Department before pricing anything.</p>
        </div>

        <div class="content-block" id="mapleton-utilities">
          <h3>{HAMMER_SVG} Why Well and Septic Capacity Matters More Here Than Lot Size</h3>
          <p>Mapleton runs both a culinary water system and a separate pressurized irrigation system, and older or outlying parcels have historically relied on private wells rather than full city utilities. Adding an ADU means adding real demand to whatever water and waste system your property already has. Before we talk floor plans, we confirm whether your well can support a second living unit and whether your septic system (if you have one) has the rated capacity, since that's a harder constraint than anything in the zoning code.</p>
        </div>

        <div class="content-block" id="mapleton-cost">
          <h3>{SHIELD_SVG} What Does an ADU Cost in Mapleton?</h3>
          <p>Because Mapleton's lots run larger and its ADU sizes scale up with them, a Mapleton project can land on the higher end of the range compared to a flat-lot city with a fixed cap. <a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener" class="link-arrow">Zonda's 2025 Cost vs. Value Report</a> gives useful national context for comparable home-investment categories:</p>
          <div class="table-wrap">
            <table class="data-table">
              <tr><th>Project Type</th><th>Typical Cost</th><th>Typical ROI</th></tr>
              <tr><td>Basement remodel (comparable scope to an ADU conversion)</td><td>$65K&ndash;$120K+</td><td>~70&ndash;75%</td></tr>
              <tr><td>Home addition (comparable scope to a detached ADU)</td><td>$225&ndash;$375 / sq ft</td><td>~50&ndash;60%</td></tr>
            </table>
          </div>
          <p class="source-note">Source: <a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener">Zonda 2025 Cost vs. Value Report</a>, national data; your Mapleton quote reflects your lot tier, utility setup and finish level, not this table.</p>
          <p>Pro-Worx ADU pricing in Mapleton typically lands at $100K&ndash;$200K for a garage or basement conversion, and $200K&ndash;$300K for a full detached, ground-up build, with well or septic upgrades priced separately once we know what your property actually has.</p>
        </div>

        <div class="content-block" id="mapleton-sources">
          <h3>Sources</h3>
          <ul class="sources-list">
            <li><a href="https://codelibrary.amlegal.com/codes/mapletonut/latest/mapleton_ut/0-0-0-9585" target="_blank" rel="noopener">Mapleton Municipal Code &sect;18.84.410</a>: accessory apartment and detached ADU standards</li>
            <li><a href="https://www.mapleton.org/departments/community_development/building/index.php" target="_blank" rel="noopener">Mapleton Community Development, Building Division</a>: permit process</li>
            <li><a href="https://waterrights.utah.gov/asp_apps/viewEditPWS/pwsView.asp?SYSTEM_ID=1220" target="_blank" rel="noopener">Utah Division of Water Rights</a>: Mapleton public water system record</li>
            <li><a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener">Zonda 2025 Cost vs. Value Report</a>: national remodel ROI benchmarks</li>
            <li><a href="/adu-rules-2026.html" class="link-arrow">Utah SB284: what changes October 1, 2026 &rarr;</a></li>
          </ul>
        </div>

      </div>
    </div>
  </div>
</section>

"""


def deep_content_spanish_fork():
    """Bespoke, research-backed deep-content section for Spanish Fork. Real
    flat 1,000 sq ft cap, real zone exclusions, real parking rule, real
    registration fee, real history. Built by hand rather than the generic
    template. Deliberately avoids unverified neighborhood names."""
    return f"""<!-- HYPER-LOCAL DEEP CONTENT: SPANISH FORK (bespoke) -->
<section>
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">THE SPANISH FORK DETAILS</p>
      <h2>Can You Build an ADU in Spanish Fork, and Which Zones Are Excluded?</h2>
      <p class="lede">Spanish Fork keeps its detached ADU size cap the same for every qualifying lot in the city. The real work is confirming your property sits in a zone that allows one at all, and that your parking plan pencils out.</p>
    </div>

    <img class="deep-image reveal" src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?q=80&w=1800&auto=format&fit=crop" alt="Residential street in Spanish Fork, Utah near the historic downtown grid">

    <div class="spec-cards reveal" style="max-width:900px; margin-left:auto; margin-right:auto; margin-bottom:56px;">
      <div class="spec-card"><div class="spec-value">48,837</div><div class="spec-label">Population (2025 est., +14.6% since 2020)</div></div>
      <div class="spec-card"><div class="spec-value">1851</div><div class="spec-label">Founded &mdash; first permanent Icelandic settlement in the U.S.</div></div>
      <div class="spec-card"><div class="spec-value">1,000 sq ft</div><div class="spec-label">Flat detached ADU cap, citywide</div></div>
      <div class="spec-card"><div class="spec-value">Fiesta Days</div><div class="spec-label">Annual civic festival, since 1935</div></div>
    </div>

    <div class="deep-layout reveal">
      <nav class="deep-jumpnav">
        <a href="#spanishfork-neighborhoods">Downtown &amp; Grid</a>
        <a href="#spanishfork-zoning">Zoning &amp; Permits</a>
        <a href="#spanishfork-parking">Parking Rule</a>
        <a href="#spanishfork-cost">Cost</a>
        <a href="#spanishfork-sources">Sources</a>
      </nav>
      <div class="blog-post-body" style="margin:0; max-width:none;">

        <div class="content-block" id="spanishfork-neighborhoods">
          <h3>{PIN_SVG} Old Grid, River Bottoms, or the Foothill Subdivisions &mdash; Your Lot Depends on Where You Sit</h3>
          <p>Spanish Fork is one of Utah County's oldest cities, settled in 1851 and known for the Palmyra and old Fort St. Luke history that anchors its historic downtown. But the city isn't one uniform lot pattern &mdash; it's really three:</p>
          <div class="neighborhood-cards">
            <div class="neighborhood-card"><h4>Downtown Spanish Fork</h4><p>The original historic grid centered on Main Street, where lot sizes and platting can vary block by block since these parcels predate modern subdivision rules.</p></div>
            <div class="neighborhood-card"><h4>Maple Park &amp; Canyon Vista Estates</h4><p>Newer platted subdivisions near Maple Mountain High School on the city's east side, built to standard R-1-12 lot sizes &mdash; more predictable for ADU planning than the older grid.</p></div>
            <div class="neighborhood-card"><h4>The River Bottoms</h4><p>The city's own designated growth-and-preservation area along the Spanish Fork River, historically agricultural and now facing annexation and development pressure &mdash; still largely flat, semi-rural parcels.</p></div>
          </div>
          <p style="margin-top:8px;">Because lot sizes and platting vary so much between the historic grid, the newer east-side subdivisions and the River Bottoms, we don't quote an ADU from an address alone. We confirm your zone and lot size with the city before pricing anything, the same way we do in every city we build in.</p>
        </div>

        <div class="content-block" id="spanishfork-zoning">
          <h3>{CLIPBOARD_SVG} What Size ADU Can You Build in Spanish Fork, and Which Zones Don't Allow One?</h3>
          <p>Spanish Fork's accessory dwelling ordinance sets a single, flat maximum for a detached ADU rather than scaling it to lot size the way a city like Mapleton does:</p>
          <div class="table-wrap">
            <table class="data-table">
              <tr><th>Requirement</th><th>Spanish Fork Standard</th></tr>
              <tr><td>Minimum lot size</td><td>6,000 sq ft</td></tr>
              <tr><td>Max detached ADU size</td><td>1,000 sq ft (flat, regardless of lot size)</td></tr>
              <tr><td>Annual ADU registration fee</td><td>$60</td></tr>
            </table>
          </div>
          <p>The catch is that this rule doesn't apply everywhere in the city. Spanish Fork excludes several zones from ADUs entirely, including its A-E agricultural-estate zones and the R-4, R-5 and R-O residential zones. One more quirk worth knowing up front: the city doesn't treat an ADU's address as a separate, USPS-recognized mailing address, which can matter for mail and some utility accounts. We confirm your parcel's zone with Spanish Fork's Community Development Department before we talk size or budget.</p>
        </div>

        <div class="content-block" id="spanishfork-parking">
          <h3>{HAMMER_SVG} The Parking Count Rules Out Tandem Spaces</h3>
          <p>Spanish Fork requires dedicated off-street parking for an ADU, and it's stricter about how those spaces count than some neighboring cities: attached ADUs need 3 total off-street spaces on the property, detached ADUs need 4, and the city does not allow tandem spaces (one car parked behind another) to satisfy the requirement. On a smaller in-fill lot near the historic downtown grid, that parking math can be the deciding factor in whether a detached ADU fits at all &mdash; which is why we walk the site and lay out parking before we finalize a floor plan.</p>
        </div>

        <div class="content-block" id="spanishfork-cost">
          <h3>{SHIELD_SVG} What Does an ADU Cost in Spanish Fork?</h3>
          <p>Spanish Fork's flat 1,000-sq-ft cap and strict parking rule tend to keep detached projects closer to a standard footprint than a tiered-cap city like Mapleton allows, which helps keep budgets more predictable. For comparable home-investment categories, <a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener" class="link-arrow">Zonda's 2025 Cost vs. Value Report</a> is a useful national benchmark:</p>
          <div class="table-wrap">
            <table class="data-table">
              <tr><th>Project Type</th><th>Typical Cost</th><th>Typical ROI</th></tr>
              <tr><td>Basement remodel (comparable scope to an ADU conversion)</td><td>$65K&ndash;$120K+</td><td>~70&ndash;75%</td></tr>
              <tr><td>Home addition (comparable scope to a detached ADU)</td><td>$225&ndash;$375 / sq ft</td><td>~50&ndash;60%</td></tr>
            </table>
          </div>
          <p class="source-note">Source: <a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener">Zonda 2025 Cost vs. Value Report</a>, national data; your Spanish Fork quote reflects your zone, parking layout and finish level, not this table.</p>
          <p>Pro-Worx ADU pricing in Spanish Fork typically lands at $100K&ndash;$180K for a garage or basement conversion, and $190K&ndash;$280K for a full detached, ground-up build within the city's 1,000-sq-ft cap, with the $60 annual registration fee handled as part of your permit paperwork.</p>
        </div>

        <div class="content-block" id="spanishfork-sources">
          <h3>Sources</h3>
          <ul class="sources-list">
            <li><a href="https://www.spanishfork.org/departments/community_development/index.php" target="_blank" rel="noopener">Spanish Fork Community Development Department</a>: ADU zoning, parking and permit standards</li>
            <li><a href="https://www.spanishfork.org/" target="_blank" rel="noopener">City of Spanish Fork</a>: City Hall, 40 S Main St, Spanish Fork, UT 84660</li>
            <li><a href="https://www.spanishfork.gov/departments/community_development/riverbottoms.php" target="_blank" rel="noopener">Spanish Fork River Bottoms Vision Plan</a>: designated growth/preservation area along the Spanish Fork River</li>
            <li><a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener">Zonda 2025 Cost vs. Value Report</a>: national remodel ROI benchmarks</li>
            <li><a href="/adu-rules-2026.html" class="link-arrow">Utah SB284: what changes October 1, 2026 &rarr;</a></li>
          </ul>
        </div>

      </div>
    </div>
  </div>
</section>

"""


def deep_content_highland():
    """Bespoke, research-backed deep-content section for Highland. Real
    large-lot zoning character, real ADU ordinance provisions (owner-
    occupancy, no detached ADUs, disguised-entrance rule), real neighborhoods
    where verifiable. Built by hand rather than the generic template."""
    return f"""<!-- HYPER-LOCAL DEEP CONTENT: HIGHLAND (bespoke) -->
<section>
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">THE HIGHLAND DETAILS</p>
      <h2>Can You Build a Detached ADU in Highland, Utah?</h2>
      <p class="lede">Highland's large lots make room for an ADU on paper, but the city's own ordinance is built around an internal, attached unit that doesn't read as a second home from the street &mdash; not a standalone building in the backyard.</p>
    </div>

    <img class="deep-image reveal" src="https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?q=80&w=1800&auto=format&fit=crop" alt="Large-lot home in Highland, Utah with a view toward Mount Timpanogos">

    <div class="spec-cards reveal" style="max-width:900px; margin-left:auto; margin-right:auto; margin-bottom:56px;">
      <div class="spec-card"><div class="spec-value">21,571</div><div class="spec-label">Population (2025 est.)</div></div>
      <div class="spec-card"><div class="spec-value">1977</div><div class="spec-label">Incorporated</div></div>
      <div class="spec-card"><div class="spec-value">6,000 sq ft</div><div class="spec-label">Minimum lot size for an ADU</div></div>
      <div class="spec-card"><div class="spec-value">Alpine School District</div><div class="spec-label">Serves the city</div></div>
    </div>

    <div class="deep-layout reveal">
      <nav class="deep-jumpnav">
        <a href="#highland-neighborhoods">Neighborhoods</a>
        <a href="#highland-zoning">Zoning &amp; Permits</a>
        <a href="#highland-design">Design Rule</a>
        <a href="#highland-cost">Cost</a>
        <a href="#highland-sources">Sources</a>
      </nav>
      <div class="blog-post-body" style="margin:0; max-width:none;">

        <div class="content-block" id="highland-neighborhoods">
          <h3>{PIN_SVG} Highland's Reputation Is Large Lots &mdash; Not Named Master-Planned Communities</h3>
          <p>Highland was settled by Scottish Mormon homesteaders in the 1870s and incorporated in 1977, and it's built its identity since then around larger residential lots than most of its Utah County neighbors, several zones running a half-acre or more. That means fewer branded subdivisions and more custom and semi-custom lots spread across the city:</p>
          <div class="neighborhood-cards">
            <div class="neighborhood-card"><h4>Hidden Oaks</h4><p>An established single-family area on Highland's residential side, part of the city's broader large-lot character.</p></div>
            <div class="neighborhood-card"><h4>Toscana</h4><p>A townhome community, one of the few attached-housing developments in a city otherwise dominated by single-family lots.</p></div>
          </div>
          <p style="margin-top:8px;">Outside those developments, most of Highland is larger, individually built lots rather than tract subdivisions, which is part of why an ADU project here is usually priced lot-by-lot rather than off a subdivision template.</p>
        </div>

        <div class="content-block" id="highland-zoning">
          <h3>{CLIPBOARD_SVG} What Does Highland's ADU Ordinance Actually Require?</h3>
          <p>Highland City's Development Code already addressed accessory dwelling units before Utah's SB284 changes take effect October 1, 2026, through its Supplementary Regulations, referenced in the R-1-20 and R-1-30 residential zones:</p>
          <div class="table-wrap">
            <table class="data-table">
              <tr><th>Requirement</th><th>Highland Standard</th></tr>
              <tr><td>Minimum lot size</td><td>6,000 sq ft</td></tr>
              <tr><td>Owner-occupancy</td><td>Required &mdash; the primary home must be owner-occupied</td></tr>
              <tr><td>Unit type allowed</td><td>Internal, attached unit only &mdash; not a detached backyard structure</td></tr>
              <tr><td>Parking</td><td>1 additional off-street space; any garage space lost to the ADU must be replaced</td></tr>
            </table>
          </div>
          <p>Because Highland's rule is written around an attached unit rather than a detached one, how SB284's detached-ADU mandate interacts with this existing ordinance is genuinely something we confirm with Highland's Community Development Department before pricing your project, not something we assume from the code alone.</p>
        </div>

        <div class="content-block" id="highland-design">
          <h3>{HAMMER_SVG} The "Doesn't Look Like Two Homes" Rule</h3>
          <p>Highland's ordinance is specific about street appearance: an ADU can't present as a separate unit when viewed from the street, and its entrance has to come from the rear of the home or a side entrance designed to blend in rather than read as a second front door. On a large Highland lot that's usually workable, but it does shape where in the house an ADU makes sense and how we frame the entrance and any exterior stairs.</p>
        </div>

        <div class="content-block" id="highland-cost">
          <h3>{SHIELD_SVG} What Does an ADU Cost in Highland?</h3>
          <p>Because Highland's ordinance points toward an internal, attached conversion rather than a ground-up detached build, most Highland projects land in the conversion range rather than the full-build range. <a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener" class="link-arrow">Zonda's 2025 Cost vs. Value Report</a> is a useful national benchmark for comparable scopes:</p>
          <div class="table-wrap">
            <table class="data-table">
              <tr><th>Project Type</th><th>Typical Cost</th><th>Typical ROI</th></tr>
              <tr><td>Basement remodel (comparable scope to an ADU conversion)</td><td>$65K&ndash;$120K+</td><td>~70&ndash;75%</td></tr>
              <tr><td>Home addition (comparable scope to a detached ADU)</td><td>$225&ndash;$375 / sq ft</td><td>~50&ndash;60%</td></tr>
            </table>
          </div>
          <p class="source-note">Source: <a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener">Zonda 2025 Cost vs. Value Report</a>, national data; your Highland quote reflects your home's layout and finish level, not this table.</p>
          <p>Pro-Worx ADU pricing in Highland typically lands at $90K&ndash;$170K for an internal or basement conversion that meets the city's attached-unit and design rules, with a detached option priced separately once we've confirmed how SB284 applies to your specific lot.</p>
        </div>

        <div class="content-block" id="highland-sources">
          <h3>Sources</h3>
          <ul class="sources-list">
            <li><a href="https://www.highlandut.gov/" target="_blank" rel="noopener">City of Highland</a>: Highland City Hall, 5400 W Civic Center Drive, Highland, UT 84003</li>
            <li>Highland City Development Code, Article 6 Supplementary Regulations (accessory dwelling unit provisions referenced from the R-1-20 and R-1-30 zones)</li>
            <li><a href="https://www.census.gov/quickfacts/fact/table/highlandcityutah" target="_blank" rel="noopener">U.S. Census Bureau QuickFacts</a>: Highland city population estimate</li>
            <li><a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener">Zonda 2025 Cost vs. Value Report</a>: national remodel ROI benchmarks</li>
            <li><a href="/adu-rules-2026.html" class="link-arrow">Utah SB284: what changes October 1, 2026 &rarr;</a></li>
          </ul>
        </div>

      </div>
    </div>
  </div>
</section>

"""


def deep_content_lindon():
    """Bespoke, research-backed deep-content section for Lindon. Real
    ordinance citation (Sec. 17.46.100), real detached-size formula, real
    setback offset rule, real parking counts. Built by hand rather than
    the generic template."""
    return f"""<!-- HYPER-LOCAL DEEP CONTENT: LINDON (bespoke) -->
<section>
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">THE LINDON DETAILS</p>
      <h2>How Big Can Your ADU Be in Lindon, Utah?</h2>
      <p class="lede">Lindon doesn't just give you a square-footage ceiling for a detached ADU. The city caps it against a percentage of your existing home, which means the same detached ADU can be a different allowed size on two lots right next to each other.</p>
    </div>

    <img class="deep-image reveal" src="https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde?q=80&w=1800&auto=format&fit=crop" alt="Single-family neighborhood street in Lindon, Utah">

    <div class="spec-cards reveal" style="max-width:900px; margin-left:auto; margin-right:auto; margin-bottom:56px;">
      <div class="spec-card"><div class="spec-value">12,015</div><div class="spec-label">Population (2025 est.)</div></div>
      <div class="spec-card"><div class="spec-value">1924</div><div class="spec-label">Incorporated (settled 1861)</div></div>
      <div class="spec-card"><div class="spec-value">6,000 sq ft</div><div class="spec-label">Minimum lot size for an ADU</div></div>
      <div class="spec-card"><div class="spec-value">Alpine School District</div><div class="spec-label">Serves the city</div></div>
    </div>

    <div class="deep-layout reveal">
      <nav class="deep-jumpnav">
        <a href="#lindon-character">Local Character</a>
        <a href="#lindon-zoning">Zoning &amp; Permits</a>
        <a href="#lindon-setbacks">Setbacks &amp; Parking</a>
        <a href="#lindon-cost">Cost</a>
        <a href="#lindon-sources">Sources</a>
      </nav>
      <div class="blog-post-body" style="margin:0; max-width:none;">

        <div class="content-block" id="lindon-character">
          <h3>{PIN_SVG} A Small City Squeezed Between a Growing Tech Corridor and the Lake</h3>
          <p>Lindon punches above its size for a city of just over 12,000 people. Along I-15 and State Street, it's become one of Utah County's busier commercial and industrial stretches &mdash; the Salt Lake Tribune has covered Lindon's tech-driven growth boom directly, and developments like the Gateway Industrial Complex and Lindon Tech Center sit right along that corridor. On the other side of town, Lindon Marina sits at the north end of Utah Lake State Park, historically associated with Lindon even though its official address falls just across the line in neighboring Vineyard.</p>
          <p style="margin-top:8px;">What Lindon doesn't have is a set of branded, marketed subdivisions the way some newer Utah County cities do &mdash; most of its residential streets are older, individually built lots rather than a tract-home master plan, which is part of why an ADU conversion here usually comes down to your specific home's layout and size rather than a subdivision template.</p>
        </div>

        <div class="content-block" id="lindon-zoning">
          <h3>{CLIPBOARD_SVG} How Does Lindon Actually Size a Detached ADU?</h3>
          <p>Lindon City's accessory apartment ordinance (Municipal Code &sect;17.46.100, adopted under Ordinance 2026-12) sets a min lot size of 6,000 sq ft, and it isn't allowed on lots below that or in areas marked on the city's own Accessory Apartment Map. Beyond that, the size math is formula-based rather than one flat number for everyone:</p>
          <div class="table-wrap">
            <table class="data-table">
              <tr><th>Unit Type</th><th>Max Size</th></tr>
              <tr><td>Internal accessory apartment</td><td>No stated size cap</td></tr>
              <tr><td>Detached ADU</td><td>Lesser of 1,500 sq ft or 40% of the primary home's size</td></tr>
              <tr><td>Substantially attached ADU</td><td>Lesser of 1,200 sq ft or 60% of the primary home's livable area</td></tr>
            </table>
          </div>
          <p>That "lesser of" language matters: on a smaller Lindon home, the 40% or 60% figure can cap your ADU well below the flat maximum, while a larger home unlocks closer to the full 1,500 or 1,200 sq ft. Owner-occupancy is required &mdash; the ordinance defines an eligible owner as holding at least 50% recorded deed ownership and living in the home as a primary residence. We run your specific home's size against this formula before we ever talk floor plans.</p>
        </div>

        <div class="content-block" id="lindon-setbacks">
          <h3>{HAMMER_SVG} Lindon's Setback Rule Pushes a Detached ADU Behind the House</h3>
          <p>A detached ADU in Lindon has to meet the underlying zone's setback and then sit at least 10 feet further back than your home's front-facing wall &mdash; and the same 10-foot offset applies to the street-facing side yard on a corner lot. On a deep lot (over 250 feet), the city allows an exception: a detached unit can sit in the front yard if it's at least 60 feet from the primary home. Parking is also spelled out precisely: an internal apartment needs 3 total stalls on the property (2 for the house, 1 for the apartment, none in the front setback), while a detached or attached ADU needs 4 total stalls, with at most one allowed in the front setback.</p>
        </div>

        <div class="content-block" id="lindon-cost">
          <h3>{SHIELD_SVG} What Does an ADU Cost in Lindon?</h3>
          <p>Because Lindon's detached-ADU cap scales with your existing home's size rather than a flat number, the final allowed square footage &mdash; and the budget that goes with it &mdash; can only be pinned down once we've measured your house. Here's what <a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener" class="link-arrow">Zonda's 2025 Cost vs. Value Report</a> shows nationally for comparable home-investment projects:</p>
          <div class="table-wrap">
            <table class="data-table">
              <tr><th>Project Type</th><th>Typical Cost</th><th>Typical ROI</th></tr>
              <tr><td>Basement remodel (comparable scope to an ADU conversion)</td><td>$65K&ndash;$120K+</td><td>~70&ndash;75%</td></tr>
              <tr><td>Home addition (comparable scope to a detached ADU)</td><td>$225&ndash;$375 / sq ft</td><td>~50&ndash;60%</td></tr>
            </table>
          </div>
          <p class="source-note">Source: <a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener">Zonda 2025 Cost vs. Value Report</a>, national data; your Lindon quote reflects your home's size under the 40%/60% formula and your finish level, not this table.</p>
          <p>Pro-Worx ADU pricing in Lindon typically lands at $95K&ndash;$180K for an internal or attached conversion, and $180K&ndash;$280K for a detached, ground-up build sized to whatever your home's formula allows.</p>
        </div>

        <div class="content-block" id="lindon-sources">
          <h3>Sources</h3>
          <ul class="sources-list">
            <li><a href="https://lindon.municipal.codes/" target="_blank" rel="noopener">Lindon Municipal Code &sect;17.46.100</a>: accessory apartment standards</li>
            <li><a href="https://www.lindon.gov/" target="_blank" rel="noopener">City of Lindon</a>: Lindon City Center, 100 North State Street, Lindon, UT 84042</li>
            <li><a href="https://www.sltrib.com/news/business/2018/02/10/we-expect-the-skyline-to-change-utah-countys-tech-boom-is-fueling-new-growth-in-lindon/" target="_blank" rel="noopener">Salt Lake Tribune</a>: Lindon's tech-driven industrial growth along I-15</li>
            <li><a href="https://utahlake.gov/launch-into-summer-at-one-of-five-utah-lake-marinas/" target="_blank" rel="noopener">Utah Lake State Park</a>: Lindon Marina at the north end of Utah Lake</li>
            <li><a href="https://www.census.gov/quickfacts/fact/table/lindoncityutah" target="_blank" rel="noopener">U.S. Census Bureau QuickFacts</a>: Lindon city population estimate</li>
            <li><a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener">Zonda 2025 Cost vs. Value Report</a>: national remodel ROI benchmarks</li>
            <li><a href="/adu-rules-2026.html" class="link-arrow">Utah SB284: what changes October 1, 2026 &rarr;</a></li>
          </ul>
        </div>

      </div>
    </div>
  </div>
</section>

"""


def deep_content_provo():
    """Bespoke, research-backed deep-content section for Provo. Real
    Title 14.30 accessory-apartment code, real 5-district neighborhood
    program, real named neighborhoods (Homes.com-verified), honest note
    on Provo's still-pending SB284 ordinance as of Sept 2026. Built by
    hand rather than the generic template."""
    return f"""<!-- HYPER-LOCAL DEEP CONTENT: PROVO (bespoke) -->
<section>
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">THE PROVO DETAILS</p>
      <h2>Can You Build an ADU in Provo, or Rent It Out to Students?</h2>
      <p class="lede">Provo's accessory apartment ordinance predates SB284 by years, and it reads that way: owner-occupancy is required, occupancy is capped, and a rental license is mandatory. If your goal is extended family or rental income from an owner-occupied home, this works in your favor &mdash; but the rules are built to prevent a pure student-rental play.</p>
    </div>

    <img class="deep-image reveal" src="https://images.unsplash.com/photo-1600585154526-990dced4db0d?q=80&w=1800&auto=format&fit=crop" alt="Residential neighborhood in Provo, Utah with mountains in the background">

    <div class="spec-cards reveal" style="max-width:900px; margin-left:auto; margin-right:auto; margin-bottom:56px;">
      <div class="spec-card"><div class="spec-value">114,527</div><div class="spec-label">Population (2025 est.)</div></div>
      <div class="spec-card"><div class="spec-value">1850</div><div class="spec-label">Incorporated (settled 1849)</div></div>
      <div class="spec-card"><div class="spec-value">5</div><div class="spec-label">Official Neighborhood Districts</div></div>
      <div class="spec-card"><div class="spec-value">Provo City School District</div><div class="spec-label">Serves the city</div></div>
    </div>

    <div class="deep-layout reveal">
      <nav class="deep-jumpnav">
        <a href="#provo-neighborhoods">Neighborhoods</a>
        <a href="#provo-zoning">Zoning &amp; Permits</a>
        <a href="#provo-sb284">SB284 Status</a>
        <a href="#provo-cost">Cost</a>
        <a href="#provo-sources">Sources</a>
      </nav>
      <div class="blog-post-body" style="margin:0; max-width:none;">

        <div class="content-block" id="provo-neighborhoods">
          <h3>{PIN_SVG} Provo Runs on Five Official Districts &mdash; And a Different Feel Block to Block</h3>
          <p>As Utah County's largest city and home to BYU, Provo is organized into five official Neighborhood Districts (North, East, West, Northwest and Central) under the city's Neighborhood District Program &mdash; a formal structure most Utah County cities this size don't have. Inside those districts, several long-established named areas shape how an ADU project actually looks:</p>
          <div class="neighborhood-cards">
            <div class="neighborhood-card"><h4>Joaquin</h4><p>A named neighborhood with its own city-adopted Joaquin Neighborhood Plan, closer to downtown and BYU.</p></div>
            <div class="neighborhood-card"><h4>Franklin</h4><p>An established residential area within Provo's district system.</p></div>
            <div class="neighborhood-card"><h4>Rock Canyon</h4><p>East-bench homes near the Rock Canyon trailhead and foothills, part of Provo's east side.</p></div>
            <div class="neighborhood-card"><h4>Grandview</h4><p>Split into North and South areas, a long-established residential part of the city.</p></div>
            <div class="neighborhood-card"><h4>Foothill</h4><p>Higher-elevation homes on Provo's eastern edge, with the terrain considerations that come with bench and foothill lots.</p></div>
          </div>
          <p style="margin-top:8px;">Because Provo has such a mix of century-old in-fill lots, BYU-adjacent rental-heavy blocks and newer bench subdivisions, we confirm your zone and district before pricing anything &mdash; a Joaquin in-fill lot and a Foothill bench lot can call for genuinely different ADU approaches.</p>
        </div>

        <div class="content-block" id="provo-zoning">
          <h3>{CLIPBOARD_SVG} What Does Provo's Accessory Apartment Code Actually Require?</h3>
          <p>Provo City Code Title 14.30 governs accessory apartments, and it's noticeably stricter on occupancy than a lot of Utah County ordinances, which makes sense in a city with a huge student rental market to manage:</p>
          <div class="table-wrap">
            <table class="data-table">
              <tr><th>Requirement</th><th>Provo Standard</th></tr>
              <tr><td>Owner-occupancy</td><td>Required for the primary one-family dwelling</td></tr>
              <tr><td>Occupancy cap</td><td>Maximum 3 unrelated adults</td></tr>
              <tr><td>Minimum detached ADU size</td><td>200 sq ft</td></tr>
              <tr><td>Detached ADU height/footprint</td><td>Must stay below the primary dwelling</td></tr>
              <tr><td>Parking</td><td>4 spaces required (up to 2 may be tandem)</td></tr>
              <tr><td>Utilities</td><td>Separate meter required for a detached unit</td></tr>
            </table>
          </div>
          <p>A rental dwelling license is also required, and ADUs are prohibited outright in several of Provo's higher-density zones (including PRO, R2PD, RM and the R16&ndash;R19 and R110 zones) &mdash; the zones where BYU-area student housing is concentrated. They're generally allowed in residential zones west of I-15, with some SDP-5/R2PD exceptions. We confirm your specific zone, and the exact permit fee from the city's current fee schedule, before pricing your project.</p>
        </div>

        <div class="content-block" id="provo-sb284">
          <h3>{HAMMER_SVG} Has Provo Adopted Its SB284 Ordinance Yet?</h3>
          <p>Unlike some Utah County cities that already had a detached-ADU rule in place, Provo was still working through its response to Utah's statewide SB284 mandate as of early September 2026. City staff proposed a 40%-of-parcel accessory-structure limit for detached ADUs, but as of the most recent reporting, that proposal hadn't yet gone through Planning Commission or a council vote &mdash; with the state's October 1, 2026 compliance deadline just weeks away. Because this is actively moving, we check the current status with Provo's Community Development Department at the time we scope your project rather than quoting a rule that may have changed.</p>
        </div>

        <div class="content-block" id="provo-cost">
          <h3>{SHIELD_SVG} What Does an ADU Cost in Provo?</h3>
          <p>Provo's occupancy caps and rental-license requirement mean most projects here are sized for a genuine second household rather than maximum rentable bedrooms, which keeps scope more in line with national averages rather than a maxed-out student-rental build-out. <a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener" class="link-arrow">Zonda's 2025 Cost vs. Value Report</a> puts comparable home-investment categories in perspective:</p>
          <div class="table-wrap">
            <table class="data-table">
              <tr><th>Project Type</th><th>Typical Cost</th><th>Typical ROI</th></tr>
              <tr><td>Basement remodel (comparable scope to an ADU conversion)</td><td>$65K&ndash;$120K+</td><td>~70&ndash;75%</td></tr>
              <tr><td>Home addition (comparable scope to a detached ADU)</td><td>$225&ndash;$375 / sq ft</td><td>~50&ndash;60%</td></tr>
            </table>
          </div>
          <p class="source-note">Source: <a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener">Zonda 2025 Cost vs. Value Report</a>, national data; your Provo quote reflects your zone, district and finish level, not this table.</p>
          <p>Pro-Worx ADU pricing in Provo typically lands at $95K&ndash;$180K for an internal or basement conversion, and $190K&ndash;$290K for a detached, ground-up build once the city's final SB284 standards are in place.</p>
        </div>

        <div class="content-block" id="provo-sources">
          <h3>Sources</h3>
          <ul class="sources-list">
            <li><a href="https://provo.municipal.codes/Code/14.30.020" target="_blank" rel="noopener">Provo City Code Title 14.30</a>: accessory apartment standards</li>
            <li><a href="https://www.provo.gov/180/Contact-Us" target="_blank" rel="noopener">City of Provo</a>: Provo City Hall, 445 W Center Street, Provo, UT 84601</li>
            <li><a href="https://www.provo.gov/282/Neighborhood-District-Program" target="_blank" rel="noopener">Provo Neighborhood District Program</a>: the city's 5 official districts</li>
            <li><a href="https://provo.com/news/detached-adu-sb284-october-1-provo/" target="_blank" rel="noopener">Provo.com</a>: Provo's pending SB284 ordinance status, September 2026</li>
            <li><a href="https://www.census.gov/quickfacts/provocityutah" target="_blank" rel="noopener">U.S. Census Bureau QuickFacts</a>: Provo city population estimate</li>
            <li><a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener">Zonda 2025 Cost vs. Value Report</a>: national remodel ROI benchmarks</li>
            <li><a href="/adu-rules-2026.html" class="link-arrow">Utah SB284: what changes October 1, 2026 &rarr;</a></li>
          </ul>
        </div>

      </div>
    </div>
  </div>
</section>

"""


def deep_content_vineyard():
    """Bespoke, research-backed deep-content section for Vineyard. Real
    licensing/fee requirements, real min lot sizes, real named new-build
    communities, honest HOA-vs-zoning framing. Built by hand rather than
    the generic template."""
    return f"""<!-- HYPER-LOCAL DEEP CONTENT: VINEYARD (bespoke) -->
<section>
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">THE VINEYARD DETAILS</p>
      <h2>In Vineyard, City Zoning May Say Yes &mdash; But Has Your HOA?</h2>
      <p class="lede">Vineyard is one of the fastest-growing cities in Utah, built almost entirely on new master-planned subdivisions since the old Geneva Steel mill closed. That means the city's ADU rule is clear and licensed &mdash; but nearly every lot also sits inside an HOA whose covenants haven't necessarily caught up.</p>
    </div>

    <img class="deep-image reveal" src="https://images.unsplash.com/photo-1600585154526-990dced4db0d?q=80&w=1800&auto=format&fit=crop" alt="New master-planned subdivision homes in Vineyard, Utah near Utah Lake">

    <div class="spec-cards reveal" style="max-width:900px; margin-left:auto; margin-right:auto; margin-bottom:56px;">
      <div class="spec-card"><div class="spec-value">16,092</div><div class="spec-label">Population (2025 est.)</div></div>
      <div class="spec-card"><div class="spec-value">1989</div><div class="spec-label">Incorporated (growth began ~2012)</div></div>
      <div class="spec-card"><div class="spec-value">12,000 sq ft</div><div class="spec-label">Minimum lot size for a detached ADU</div></div>
      <div class="spec-card"><div class="spec-value">Alpine School District</div><div class="spec-label">Serves the city (currently)</div></div>
    </div>

    <div class="deep-layout reveal">
      <nav class="deep-jumpnav">
        <a href="#vineyard-neighborhoods">Neighborhoods</a>
        <a href="#vineyard-zoning">Zoning &amp; Licensing</a>
        <a href="#vineyard-hoa">HOA Reality Check</a>
        <a href="#vineyard-cost">Cost</a>
        <a href="#vineyard-sources">Sources</a>
      </nav>
      <div class="blog-post-body" style="margin:0; max-width:none;">

        <div class="content-block" id="vineyard-neighborhoods">
          <h3>{PIN_SVG} A City Built From Scratch on the Old Geneva Steel Site</h3>
          <p>Vineyard had fewer than 200 residents as recently as 2010. Redevelopment of the former Geneva Steel mill site on Utah Lake, plus the arrival of UVU's Vineyard campus and the FrontRunner Vineyard Station in 2022, turned it into one of Utah's fastest-growing cities almost overnight. That means the city is made up almost entirely of active new-construction communities rather than older, established neighborhoods:</p>
          <div class="neighborhood-cards">
            <div class="neighborhood-card"><h4>Holdaway Fields</h4><p>An active new-home community with Estate and Cottage sections, built by Goodboro Homes.</p></div>
            <div class="neighborhood-card"><h4>The Villas at Waters Edge</h4><p>A newer development by Leisure Villas, part of Vineyard's ongoing build-out near the lake.</p></div>
            <div class="neighborhood-card"><h4>The Maples</h4><p>A Home Center Construction community among Vineyard's current active subdivisions.</p></div>
          </div>
          <p style="margin-top:8px;">Because Vineyard is still actively building, the specific HOA and lot-plat details of a brand-new phase can differ from the phase built two years earlier in the same community. We confirm your exact subdivision and phase before pricing anything.</p>
        </div>

        <div class="content-block" id="vineyard-zoning">
          <h3>{CLIPBOARD_SVG} Vineyard's ADU Rule Comes With a Licensing Requirement, Not Just a Permit</h3>
          <p>Vineyard requires an ADU license, not just a building permit, and treats it as an ongoing city-tracked use rather than a one-time approval:</p>
          <div class="table-wrap">
            <table class="data-table">
              <tr><th>Requirement</th><th>Vineyard Standard</th></tr>
              <tr><td>Minimum lot size, internal/attached ADU</td><td>5,200 sq ft</td></tr>
              <tr><td>Minimum lot size, detached ADU</td><td>12,000 sq ft</td></tr>
              <tr><td>Parking</td><td>4 on-site spaces, minimum 8&prime;&times;18&prime; each, no tandem owner/tenant parking</td></tr>
              <tr><td>License fee</td><td>$50, renewed every 2 years with a code-enforcement inspection</td></tr>
            </table>
          </div>
          <p>Vineyard's 12,000-sq-ft detached-ADU minimum is actually stricter than the 11,000-sq-ft statewide floor set by Utah's SB284, which takes effect October 1, 2026 &mdash; how the city reconciles that difference is exactly what we confirm with Vineyard's Community Development Department before pricing your project, rather than assuming.</p>
        </div>

        <div class="content-block" id="vineyard-hoa">
          <h3>{HAMMER_SVG} The City Says Yes. Your HOA Still Gets a Vote.</h3>
          <p>Because nearly every lot in Vineyard sits inside a homeowners association tied to a specific master-planned community, the city's ADU license is often only half the approval you need. HOA design review, architectural standards and, in some cases, outright restrictions on secondary units can apply on top of whatever the city allows. We treat this as a real, separate step in every Vineyard project &mdash; not a formality &mdash; and confirm your specific HOA's covenants before finalizing a design.</p>
        </div>

        <div class="content-block" id="vineyard-cost">
          <h3>{SHIELD_SVG} What Does an ADU Cost in Vineyard?</h3>
          <p>Because Vineyard's building stock is almost entirely new construction, most ADU work here is a ground-up detached build rather than a garage or basement conversion of an older home. <a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener" class="link-arrow">Zonda's 2025 Cost vs. Value Report</a> gives useful national context for comparable home-investment categories:</p>
          <div class="table-wrap">
            <table class="data-table">
              <tr><th>Project Type</th><th>Typical Cost</th><th>Typical ROI</th></tr>
              <tr><td>Basement remodel (comparable scope to an ADU conversion)</td><td>$65K&ndash;$120K+</td><td>~70&ndash;75%</td></tr>
              <tr><td>Home addition (comparable scope to a detached ADU)</td><td>$225&ndash;$375 / sq ft</td><td>~50&ndash;60%</td></tr>
            </table>
          </div>
          <p class="source-note">Source: <a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener">Zonda 2025 Cost vs. Value Report</a>, national data; your Vineyard quote reflects your subdivision, HOA requirements and finish level, not this table.</p>
          <p>Pro-Worx ADU pricing in Vineyard typically lands at $190K&ndash;$290K for a full detached, ground-up build within the city's 1,200-sq-ft cap, with HOA-driven design upgrades (matching exterior materials, roofline, etc.) priced separately once we know your community's standards.</p>
        </div>

        <div class="content-block" id="vineyard-sources">
          <h3>Sources</h3>
          <ul class="sources-list">
            <li><a href="https://www.vineyardutah.gov/government/accessory_dwelling_unit_licensing.php" target="_blank" rel="noopener">City of Vineyard</a>: ADU licensing requirements and fee</li>
            <li><a href="https://www.vineyardutah.gov/contact/index.php" target="_blank" rel="noopener">Vineyard City Hall</a>: 125 S Main St, Vineyard, UT 84059</li>
            <li><a href="https://www.census.gov/quickfacts/fact/table/vineyardtownutah" target="_blank" rel="noopener">U.S. Census Bureau QuickFacts</a>: Vineyard population estimate</li>
            <li><a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener">Zonda 2025 Cost vs. Value Report</a>: national remodel ROI benchmarks</li>
            <li><a href="/adu-rules-2026.html" class="link-arrow">Utah SB284: what changes October 1, 2026 &rarr;</a></li>
          </ul>
        </div>

      </div>
    </div>
  </div>
</section>

"""


def deep_content_bluffdale():
    """Bespoke, research-backed deep-content section for Bluffdale. Real
    50%-of-primary-home size cap, real no-short-term-rental rule, real
    verified communities. Built by hand rather than the generic template."""
    return f"""<!-- HYPER-LOCAL DEEP CONTENT: BLUFFDALE (bespoke) -->
<section>
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">THE BLUFFDALE DETAILS</p>
      <h2>Bluffdale Caps Your ADU at Half Your Home's Size &mdash; And Bans Airbnb-Style Rentals</h2>
      <p class="lede">Bluffdale's ADU ordinance is refreshingly permissive on lot size, but it's specific about what an ADU is for: a real second household, not a short-term rental. The size cap ties directly to your existing home, not a flat number.</p>
    </div>

    <img class="deep-image reveal" src="https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde?q=80&w=1800&auto=format&fit=crop" alt="Semi-rural residential property in Bluffdale, Utah near the Salt Lake County equestrian trails">

    <div class="spec-cards reveal" style="max-width:900px; margin-left:auto; margin-right:auto; margin-bottom:56px;">
      <div class="spec-card"><div class="spec-value">19,506</div><div class="spec-label">Population (2025 est.)</div></div>
      <div class="spec-card"><div class="spec-value">1978</div><div class="spec-label">Incorporated (settled 1848&ndash;49)</div></div>
      <div class="spec-card"><div class="spec-value">6,000 sq ft</div><div class="spec-label">Minimum lot size for an ADU</div></div>
      <div class="spec-card"><div class="spec-value">Jordan School District</div><div class="spec-label">Serves the city</div></div>
    </div>

    <div class="deep-layout reveal">
      <nav class="deep-jumpnav">
        <a href="#bluffdale-neighborhoods">Neighborhoods</a>
        <a href="#bluffdale-zoning">Zoning &amp; Permits</a>
        <a href="#bluffdale-rentals">No Short-Term Rentals</a>
        <a href="#bluffdale-cost">Cost</a>
        <a href="#bluffdale-sources">Sources</a>
      </nav>
      <div class="blog-post-body" style="margin:0; max-width:none;">

        <div class="content-block" id="bluffdale-neighborhoods">
          <h3>{PIN_SVG} Bluffdale Still Feels Rural in Places &mdash; And Newer in Others</h3>
          <p>Salt Lake County's southernmost city has held onto a semi-rural, equestrian character even as growth pushes north from Utah County and south from Draper. That mix shows up block by block:</p>
          <div class="neighborhood-cards">
            <div class="neighborhood-card"><h4>Day Ranch</h4><p>A townhome community reflecting Bluffdale's newer, denser development.</p></div>
            <div class="neighborhood-card"><h4>Independence at the Point</h4><p>A detached single-family community on the newer end of Bluffdale's housing stock.</p></div>
            <div class="neighborhood-card"><h4>Bringhurst Station</h4><p>Another of Bluffdale's active newer-construction communities.</p></div>
          </div>
          <p style="margin-top:8px;">Outside these newer communities, much of Bluffdale still carries larger, older agricultural-heritage lots &mdash; part of why the city's ADU ordinance is written to work across both without carving out separate rules by zone.</p>
        </div>

        <div class="content-block" id="bluffdale-zoning">
          <h3>{CLIPBOARD_SVG} How Bluffdale Actually Sizes an ADU</h3>
          <p>Bluffdale City Code Chapter 11.340 allows both internal (I-ADU) and detached (D-ADU) accessory dwelling units in residential, mixed-use and special-district zones, with the size cap tied directly to your existing home:</p>
          <div class="table-wrap">
            <table class="data-table">
              <tr><th>Requirement</th><th>Bluffdale Standard</th></tr>
              <tr><td>Minimum lot size</td><td>6,000 sq ft</td></tr>
              <tr><td>Max ADU size</td><td>50% of the primary home's gross square footage</td></tr>
              <tr><td>Parking, detached ADU</td><td>2 additional off-street spaces</td></tr>
              <tr><td>Parking, internal ADU</td><td>1 additional off-street space</td></tr>
              <tr><td>Units per property</td><td>One ADU maximum</td></tr>
            </table>
          </div>
          <p>Owner-occupancy is required in either the main home or the ADU, a detached unit needs a permanent foundation (no trailers or manufactured units used as a workaround), and Bluffdale doesn't allow a separate utility meter or street address for the ADU. Bluffdale's 6,000-sq-ft minimum is already more permissive than the 11,000-sq-ft floor set by Utah's SB284, effective October 1, 2026, but we confirm the city's current compliance status with Community Development before pricing your project.</p>
        </div>

        <div class="content-block" id="bluffdale-rentals">
          <h3>{HAMMER_SVG} Thinking Airbnb? Bluffdale's Ordinance Says No.</h3>
          <p>Bluffdale requires a minimum 30-day occupancy for an ADU, which rules out nightly or short-term rental platforms entirely. If your goal is extended family housing or a genuine long-term tenant, that's not a problem &mdash; but if you were planning a short-term rental income stream, Bluffdale's ordinance is built specifically to prevent that use.</p>
        </div>

        <div class="content-block" id="bluffdale-cost">
          <h3>{SHIELD_SVG} What Does an ADU Cost in Bluffdale?</h3>
          <p>Because Bluffdale's size cap scales with your home rather than a flat number, and the city permits both internal and detached units on the same 6,000-sq-ft threshold, project scope here varies more than in a single-formula city. <a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener" class="link-arrow">Zonda's 2025 Cost vs. Value Report</a> gives useful national context for comparable home-investment categories:</p>
          <div class="table-wrap">
            <table class="data-table">
              <tr><th>Project Type</th><th>Typical Cost</th><th>Typical ROI</th></tr>
              <tr><td>Basement remodel (comparable scope to an ADU conversion)</td><td>$65K&ndash;$120K+</td><td>~70&ndash;75%</td></tr>
              <tr><td>Home addition (comparable scope to a detached ADU)</td><td>$225&ndash;$375 / sq ft</td><td>~50&ndash;60%</td></tr>
            </table>
          </div>
          <p class="source-note">Source: <a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener">Zonda 2025 Cost vs. Value Report</a>, national data; your Bluffdale quote reflects your home's size under the 50% cap and your finish level, not this table.</p>
          <p>Pro-Worx ADU pricing in Bluffdale typically lands at $95K&ndash;$180K for an internal or attached conversion, and $190K&ndash;$290K for a detached, ground-up build sized to whatever your home's 50% cap allows.</p>
        </div>

        <div class="content-block" id="bluffdale-sources">
          <h3>Sources</h3>
          <ul class="sources-list">
            <li><a href="https://www.bluffdale.gov/271/Land-Use-Ordinances" target="_blank" rel="noopener">Bluffdale City Code Ch. 11.340</a>: accessory dwelling unit standards</li>
            <li><a href="https://www.bluffdale.gov/580/Contact-Us" target="_blank" rel="noopener">City of Bluffdale</a>: Bluffdale City Hall, 2222 W 14400 S, Bluffdale, UT 84065</li>
            <li><a href="https://www.census.gov/quickfacts/fact/table/bluffdalecityutah" target="_blank" rel="noopener">U.S. Census Bureau QuickFacts</a>: Bluffdale population estimate</li>
            <li><a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener">Zonda 2025 Cost vs. Value Report</a>: national remodel ROI benchmarks</li>
            <li><a href="/adu-rules-2026.html" class="link-arrow">Utah SB284: what changes October 1, 2026 &rarr;</a></li>
          </ul>
        </div>

      </div>
    </div>
  </div>
</section>

"""


def deep_content_draper():
    """Bespoke, research-backed deep-content section for Draper. Real
    Sec. 9-5-210 ordinance, real 50%-of-home cap, real The Point mega-
    project context, honest hedge on hillside-specific ADU review (not
    verified to exist). Built by hand rather than the generic template."""
    return f"""<!-- HYPER-LOCAL DEEP CONTENT: DRAPER (bespoke) -->
<section>
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">THE DRAPER DETAILS</p>
      <h2>Draper's ADU Rule Is the Same From Suncrest to The Point &mdash; The Terrain Isn't</h2>
      <p class="lede">Draper's accessory dwelling ordinance doesn't carve out separate rules for its hillside neighborhoods, but a lot on Suncrest's slopes and a lot near a flat new-build in South Draper are two very different construction jobs even under the same code.</p>
    </div>

    <img class="deep-image reveal" src="https://images.unsplash.com/photo-1601918774946-25832a4be0d6?q=80&w=1800&auto=format&fit=crop" alt="Hillside homes in Draper, Utah near Corner Canyon">

    <div class="spec-cards reveal" style="max-width:900px; margin-left:auto; margin-right:auto; margin-bottom:56px;">
      <div class="spec-card"><div class="spec-value">50,652</div><div class="spec-label">Population (2025 est.)</div></div>
      <div class="spec-card"><div class="spec-value">1978</div><div class="spec-label">Incorporated (settled 1849 as "Draperville")</div></div>
      <div class="spec-card"><div class="spec-value">12,000 sq ft</div><div class="spec-label">Minimum lot size for a detached ADU</div></div>
      <div class="spec-card"><div class="spec-value">Canyons School District</div><div class="spec-label">Serves the city</div></div>
    </div>

    <div class="deep-layout reveal">
      <nav class="deep-jumpnav">
        <a href="#draper-neighborhoods">Neighborhoods</a>
        <a href="#draper-zoning">Zoning &amp; Permits</a>
        <a href="#draper-terrain">Hillside Terrain</a>
        <a href="#draper-cost">Cost</a>
        <a href="#draper-sources">Sources</a>
      </nav>
      <div class="blog-post-body" style="margin:0; max-width:none;">

        <div class="content-block" id="draper-neighborhoods">
          <h3>{PIN_SVG} From Suncrest's Slopes to The Point's Mega-Development</h3>
          <p>Draper spans both Salt Lake and Utah counties and covers some of the most varied terrain of any city we build in:</p>
          <div class="neighborhood-cards">
            <div class="neighborhood-card"><h4>Suncrest</h4><p>A hillside master-planned community that actually straddles the Draper/Highland line, with steep-slope lots and mountain views.</p></div>
            <div class="neighborhood-card"><h4>Corner Canyon</h4><p>The area around Corner Canyon High School, part of Draper's east-bench foothill terrain.</p></div>
            <div class="neighborhood-card"><h4>The Point</h4><p>The former Utah State Prison site, now a massive mixed-use redevelopment reported in the billions of dollars &mdash; a distinctly Draper-specific landmark project reshaping the city's north end.</p></div>
          </div>
          <p style="margin-top:8px;">Because Draper genuinely runs from flat valley-floor lots to steep hillside parcels within the same city limits, we never quote an ADU here without walking the specific property first.</p>
        </div>

        <div class="content-block" id="draper-zoning">
          <h3>{CLIPBOARD_SVG} What Draper's Ordinance Actually Requires</h3>
          <p>Draper City Code &sect;9-5-210 covers two ADU types &mdash; detached (D-ADU) and internal (I-ADU) &mdash; each with its own standards:</p>
          <div class="table-wrap">
            <table class="data-table">
              <tr><th>Requirement</th><th>Draper Standard</th></tr>
              <tr><td>Minimum lot size, detached ADU</td><td>12,000 sq ft</td></tr>
              <tr><td>Minimum lot size, internal ADU</td><td>6,000 sq ft, fronting a public street</td></tr>
              <tr><td>Max ADU size</td><td>50% of the primary home's square footage</td></tr>
              <tr><td>Height limit, detached ADU</td><td>35 ft, matching the primary home's materials and color</td></tr>
              <tr><td>Parking</td><td>1 additional on-site space, no tandem or blocked spaces</td></tr>
              <tr><td>Lease term</td><td>Minimum 30 days &mdash; no short-term rentals</td></tr>
            </table>
          </div>
          <p>Owner-occupancy is required and re-verified annually at renewal, only one ADU is allowed per lot, and both ADU types share utility meters with the main house rather than getting a separate connection. We confirm the exact permit fee and your specific zone with Draper's Planning and Development Department before pricing your project, since that figure isn't published in the general code.</p>
        </div>

        <div class="content-block" id="draper-terrain">
          <h3>{HAMMER_SVG} Draper's Code Doesn't Single Out Hillside Lots &mdash; But Your Site Work Will</h3>
          <p>Unlike Alpine, Draper's ordinance doesn't carry a distinct hillside or sensitive-lands review specifically for ADUs. That doesn't mean the terrain stops mattering: a Suncrest or Corner Canyon lot on real slope still needs the same grading, drainage and foundation engineering any steep-lot build requires, it just isn't triggered by an ADU-specific code section. We scope that engineering the same way we would for any hillside project in Draper, separate from the standard permit review.</p>
        </div>

        <div class="content-block" id="draper-cost">
          <h3>{SHIELD_SVG} What Does an ADU Cost in Draper?</h3>
          <p>Because Draper's terrain varies so much from lot to lot, project cost here swings more than in a flatter, single-character city. <a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener" class="link-arrow">Zonda's 2025 Cost vs. Value Report</a> gives useful national context for comparable home-investment categories:</p>
          <div class="table-wrap">
            <table class="data-table">
              <tr><th>Project Type</th><th>Typical Cost</th><th>Typical ROI</th></tr>
              <tr><td>Basement remodel (comparable scope to an ADU conversion)</td><td>$65K&ndash;$120K+</td><td>~70&ndash;75%</td></tr>
              <tr><td>Home addition (comparable scope to a detached ADU)</td><td>$225&ndash;$375 / sq ft</td><td>~50&ndash;60%</td></tr>
            </table>
          </div>
          <p class="source-note">Source: <a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener">Zonda 2025 Cost vs. Value Report</a>, national data; your Draper quote reflects your lot's terrain, your home's size under the 50% cap, and your finish level, not this table.</p>
          <p>Pro-Worx ADU pricing in Draper typically lands at $100K&ndash;$190K for an internal conversion on a flatter lot, and $210K&ndash;$320K for a detached, ground-up build on hillside terrain once grading and drainage are factored in.</p>
        </div>

        <div class="content-block" id="draper-sources">
          <h3>Sources</h3>
          <ul class="sources-list">
            <li><a href="https://codelibrary.amlegal.com/codes/draperut/latest/draper_ut/0-0-0-43100" target="_blank" rel="noopener">Draper City Code &sect;9-5-210</a>: accessory dwelling unit standards</li>
            <li><a href="https://www.draperutah.gov/business-development/planning-and-development/accessory-dwelling-units-permits/" target="_blank" rel="noopener">City of Draper</a>: ADU permitting overview; City Hall, 1020 E Pioneer Rd, Draper, UT</li>
            <li><a href="https://www.census.gov/quickfacts/fact/table/drapercityutah" target="_blank" rel="noopener">U.S. Census Bureau QuickFacts</a>: Draper population estimate</li>
            <li><a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener">Zonda 2025 Cost vs. Value Report</a>: national remodel ROI benchmarks</li>
            <li><a href="/adu-rules-2026.html" class="link-arrow">Utah SB284: what changes October 1, 2026 &rarr;</a></li>
          </ul>
        </div>

      </div>
    </div>
  </div>
</section>

"""


def deep_content_riverton():
    """Bespoke, research-backed deep-content section for Riverton. Real
    Municipal Code 18.225.080, real 2x-footprint/10%-of-lot size cap, real
    $175 registration fee, real Redfin-verified neighborhoods. Built by
    hand rather than the generic template."""
    return f"""<!-- HYPER-LOCAL DEEP CONTENT: RIVERTON (bespoke) -->
<section>
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">THE RIVERTON DETAILS</p>
      <h2>Riverton Sizes Your ADU Off Your Lot, Not a Flat Number</h2>
      <p class="lede">Riverton already had a working detached-ADU ordinance well before SB284, and it ties the size cap to your specific lot and home rather than handing every property the same ceiling.</p>
    </div>

    <img class="deep-image reveal" src="https://images.unsplash.com/photo-1600566752355-35792bedcfea?q=80&w=1800&auto=format&fit=crop" alt="Residential neighborhood in Riverton, Utah near the Jordan River">

    <div class="spec-cards reveal" style="max-width:900px; margin-left:auto; margin-right:auto; margin-bottom:56px;">
      <div class="spec-card"><div class="spec-value">47,395</div><div class="spec-label">Population (2025 est.)</div></div>
      <div class="spec-card"><div class="spec-value">1948</div><div class="spec-label">Incorporated (settled 1850s as "Gardnerville")</div></div>
      <div class="spec-card"><div class="spec-value">$175</div><div class="spec-label">ADU registration fee</div></div>
      <div class="spec-card"><div class="spec-value">Jordan School District</div><div class="spec-label">Serves the city</div></div>
    </div>

    <div class="deep-layout reveal">
      <nav class="deep-jumpnav">
        <a href="#riverton-neighborhoods">Neighborhoods</a>
        <a href="#riverton-zoning">Zoning &amp; Permits</a>
        <a href="#riverton-setbacks">Setbacks &amp; Parking</a>
        <a href="#riverton-cost">Cost</a>
        <a href="#riverton-sources">Sources</a>
      </nav>
      <div class="blog-post-body" style="margin:0; max-width:none;">

        <div class="content-block" id="riverton-neighborhoods">
          <h3>{PIN_SVG} Riverton Runs From Its Agricultural Roots to Newer Growth Along the Jordan River</h3>
          <p>Named for its position along the Jordan River, Riverton grew from 1850s farmland into a full Salt Lake County city by the time it incorporated in 1948. Its residential character today spans several distinct, real-mapped areas:</p>
          <div class="neighborhood-cards">
            <div class="neighborhood-card"><h4>Riverton South</h4><p>A defined residential area on the city's south side.</p></div>
            <div class="neighborhood-card"><h4>Central Riverton</h4><p>The older, more established core of the city.</p></div>
            <div class="neighborhood-card"><h4>Western Springs</h4><p>A named residential area on Riverton's west side.</p></div>
            <div class="neighborhood-card"><h4>Summerhill</h4><p>Another of Riverton's distinct, mapped residential areas.</p></div>
          </div>
          <p style="margin-top:8px;">Because Riverton mixes older agricultural-heritage parcels with newer subdivisions across these areas, lot size and layout vary enough that we check your specific property against the code before pricing anything.</p>
        </div>

        <div class="content-block" id="riverton-zoning">
          <h3>{CLIPBOARD_SVG} How Riverton Actually Sizes a Detached ADU</h3>
          <p>Riverton Municipal Code &sect;18.225.080 already allowed detached ADUs in single-family zones well before Utah's SB284 mandate, and it ties the size limit to your existing property rather than a flat cap:</p>
          <div class="table-wrap">
            <table class="data-table">
              <tr><th>Requirement</th><th>Riverton Standard</th></tr>
              <tr><td>Max detached ADU size</td><td>Lesser of 2&times; the principal home's footprint, or 10% of the lot area</td></tr>
              <tr><td>Registration fee</td><td>$175, including required inspections</td></tr>
              <tr><td>Owner-occupancy</td><td>Required (main house or ADU) &mdash; with exceptions for military deployment, medical need or sabbatical up to 3 years</td></tr>
              <tr><td>Re-registration</td><td>Required when the property changes owners</td></tr>
            </table>
          </div>
          <p>A building permit and certificate of occupancy are both required on top of the registration fee. Because the size formula depends on your specific home's footprint and lot area, we run the actual numbers on your property before we ever talk floor plans.</p>
        </div>

        <div class="content-block" id="riverton-setbacks">
          <h3>{HAMMER_SVG} Riverton's Setback Rules Are Detailed &mdash; Especially Around Entrances</h3>
          <p>Riverton spells out setbacks more precisely than most cities we build in. An ADU's entrance and any exterior stairs need to sit at least 10 feet from the side or rear property line (or face an alley, street, or the rear of the main house instead). General accessory-structure setbacks run 5 feet at the rear and between structures, 10 feet from the main dwelling, and a side setback that scales from 1 to 15 feet depending on the structure's size and placement. Parking requires one dedicated on-site space, though an existing driveway at least 20 by 8 feet can satisfy that requirement without adding new pavement.</p>
        </div>

        <div class="content-block" id="riverton-cost">
          <h3>{SHIELD_SVG} What Does an ADU Cost in Riverton?</h3>
          <p>Because Riverton's size cap scales with your specific home and lot rather than a flat number, the final allowed footprint &mdash; and the budget behind it &mdash; comes down to your property's actual measurements. <a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener" class="link-arrow">Zonda's 2025 Cost vs. Value Report</a> gives useful national context for comparable home-investment categories:</p>
          <div class="table-wrap">
            <table class="data-table">
              <tr><th>Project Type</th><th>Typical Cost</th><th>Typical ROI</th></tr>
              <tr><td>Basement remodel (comparable scope to an ADU conversion)</td><td>$65K&ndash;$120K+</td><td>~70&ndash;75%</td></tr>
              <tr><td>Home addition (comparable scope to a detached ADU)</td><td>$225&ndash;$375 / sq ft</td><td>~50&ndash;60%</td></tr>
            </table>
          </div>
          <p class="source-note">Source: <a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener">Zonda 2025 Cost vs. Value Report</a>, national data; your Riverton quote reflects your lot and home's size under the 2x/10% formula, and your finish level, not this table.</p>
          <p>Pro-Worx ADU pricing in Riverton typically lands at $95K&ndash;$180K for an internal conversion, and $190K&ndash;$290K for a detached, ground-up build sized to whatever your property's formula allows.</p>
        </div>

        <div class="content-block" id="riverton-sources">
          <h3>Sources</h3>
          <ul class="sources-list">
            <li><a href="https://ecode360.com/47630284" target="_blank" rel="noopener">Riverton Municipal Code &sect;18.225.080</a>: accessory dwelling unit standards</li>
            <li><a href="https://www.rivertonutah.gov/contact" target="_blank" rel="noopener">City of Riverton</a>: Riverton City Hall, 12830 S Redwood Road, Riverton, UT 84065</li>
            <li><a href="https://www.rivertonutah.gov/about/history" target="_blank" rel="noopener">City of Riverton</a>: incorporation history</li>
            <li><a href="https://www.census.gov/quickfacts/fact/table/rivertoncityutah" target="_blank" rel="noopener">U.S. Census Bureau QuickFacts</a>: Riverton population estimate</li>
            <li><a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener">Zonda 2025 Cost vs. Value Report</a>: national remodel ROI benchmarks</li>
            <li><a href="/adu-rules-2026.html" class="link-arrow">Utah SB284: what changes October 1, 2026 &rarr;</a></li>
          </ul>
        </div>

      </div>
    </div>
  </div>
</section>

"""


def deep_content_sandy():
    """Bespoke, research-backed deep-content section for Sandy. Real
    internal-only accessory apartment rule (no detached ADU under this
    provision, separate guesthouse rule for detached), real proof-of-
    occupancy requirement. Honest about unverified figures (lot size,
    fee, setbacks) rather than inventing them. Built by hand rather
    than the generic template."""
    return f"""<!-- HYPER-LOCAL DEEP CONTENT: SANDY (bespoke) -->
<section>
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">THE SANDY DETAILS</p>
      <h2>Sandy's Existing Ordinance Only Covers Attached Units &mdash; Detached Is a Different Rule</h2>
      <p class="lede">Sandy's accessory apartment code was written around a unit inside your existing home, not a standalone structure in the backyard. If you want a detached ADU, you're looking at a separate provision and, likely, the new SB284 mandate rather than the accessory apartment rule itself.</p>
    </div>

    <img class="deep-image reveal" src="https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?q=80&w=1800&auto=format&fit=crop" alt="Established residential neighborhood in Sandy, Utah near the Wasatch foothills">

    <div class="spec-cards reveal" style="max-width:900px; margin-left:auto; margin-right:auto; margin-bottom:56px;">
      <div class="spec-card"><div class="spec-value">92,386</div><div class="spec-label">Population (2025 est.)</div></div>
      <div class="spec-card"><div class="spec-value">1893</div><div class="spec-label">Incorporated (settled 1871, mining roots)</div></div>
      <div class="spec-card"><div class="spec-value">1</div><div class="spec-label">Accessory apartment allowed per single-family home</div></div>
      <div class="spec-card"><div class="spec-value">Canyons School District</div><div class="spec-label">Serves the city</div></div>
    </div>

    <div class="deep-layout reveal">
      <nav class="deep-jumpnav">
        <a href="#sandy-neighborhoods">Neighborhoods</a>
        <a href="#sandy-zoning">Zoning &amp; Permits</a>
        <a href="#sandy-proof">Proof of Occupancy</a>
        <a href="#sandy-cost">Cost</a>
        <a href="#sandy-sources">Sources</a>
      </nav>
      <div class="blog-post-body" style="margin:0; max-width:none;">

        <div class="content-block" id="sandy-neighborhoods">
          <h3>{PIN_SVG} From Historic Mining Roots to Foothill Growth Near Little Cottonwood Canyon</h3>
          <p>Sandy grew out of the silver-mining and smelting boom tied to Little Cottonwood Canyon in the 1870s before incorporating in 1893, and today it's one of the larger, more established cities in Salt Lake County. Its residential character ranges from older, flatter neighborhoods near the historic Main Street core to newer development toward the foothills:</p>
          <div class="neighborhood-cards">
            <div class="neighborhood-card"><h4>Dimple Dell Oaks</h4><p>A subdivision near Dimple Dell Regional Park, one of Sandy's signature natural landmarks.</p></div>
            <div class="neighborhood-card"><h4>The Dell</h4><p>A residential area associated with the Dimple Dell park corridor.</p></div>
          </div>
          <p style="margin-top:8px;">Because Sandy spans everything from century-old lots to newer foothill-adjacent construction, we confirm your specific zone and lot history before pricing anything &mdash; an older Sandy lot and a newer one can fall under genuinely different practical constraints even under the same code.</p>
        </div>

        <div class="content-block" id="sandy-zoning">
          <h3>{CLIPBOARD_SVG} Sandy's Accessory Apartment Rule Is Attached-Only</h3>
          <p>Sandy City's accessory apartment ordinance is specific about what it covers: an accessory apartment "shall not occupy any accessory buildings," meaning it's written for a unit inside your existing single-family home, not a detached structure. A separate "guesthouse" provision covers detached structures, with its own setback rules apart from the accessory apartment code:</p>
          <div class="table-wrap">
            <table class="data-table">
              <tr><th>Requirement</th><th>Sandy Standard</th></tr>
              <tr><td>Unit type covered</td><td>Internal/attached only (no accessory buildings)</td></tr>
              <tr><td>Units per property</td><td>One accessory apartment per single-family structure</td></tr>
              <tr><td>Parking</td><td>1 additional off-street space, beyond standard household parking</td></tr>
              <tr><td>Permit</td><td>Administrative special use permit plus an accessory apartment business license</td></tr>
            </table>
          </div>
          <p>Sandy hasn't published a specific minimum lot size, square-footage cap or setback figure for the accessory apartment provision itself in what we could verify, and we didn't want to guess at numbers that could be wrong. If you're set on a detached ADU, that likely falls under Utah's SB284 mandate (effective October 1, 2026) rather than this existing ordinance &mdash; we confirm the current, exact standards with Sandy's Community Development Department as the first step on every project here.</p>
        </div>

        <div class="content-block" id="sandy-proof">
          <h3>{HAMMER_SVG} Sandy Actually Requires Proof You Live There</h3>
          <p>Most Utah cities state an owner-occupancy requirement in a sentence. Sandy spells out exactly how you prove it: a deed, tax return, government ID, or notarized affidavit showing the primary dwelling is your primary residence. It's a small detail, but it's worth knowing before you apply &mdash; have that documentation ready rather than finding out about it mid-application.</p>
        </div>

        <div class="content-block" id="sandy-cost">
          <h3>{SHIELD_SVG} What Does an ADU Cost in Sandy?</h3>
          <p>Because Sandy's existing ordinance points toward an internal conversion, and a detached unit runs through a separate process entirely, project scope here depends heavily on which path fits your property and goals. <a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener" class="link-arrow">Zonda's 2025 Cost vs. Value Report</a> gives useful national context for comparable home-investment categories:</p>
          <div class="table-wrap">
            <table class="data-table">
              <tr><th>Project Type</th><th>Typical Cost</th><th>Typical ROI</th></tr>
              <tr><td>Basement remodel (comparable scope to an ADU conversion)</td><td>$65K&ndash;$120K+</td><td>~70&ndash;75%</td></tr>
              <tr><td>Home addition (comparable scope to a detached ADU)</td><td>$225&ndash;$375 / sq ft</td><td>~50&ndash;60%</td></tr>
            </table>
          </div>
          <p class="source-note">Source: <a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener">Zonda 2025 Cost vs. Value Report</a>, national data; your Sandy quote reflects which path (internal apartment vs. detached ADU) fits your property, and your finish level, not this table.</p>
          <p>Pro-Worx ADU pricing in Sandy typically lands at $90K&ndash;$170K for an internal accessory apartment conversion, with a detached ADU priced separately once we've confirmed how the city is applying SB284 to your specific lot.</p>
        </div>

        <div class="content-block" id="sandy-sources">
          <h3>Sources</h3>
          <ul class="sources-list">
            <li><a href="https://sandyutah.legistar.com/View.ashx?GUID=1221E71F-91D9-41B9-99DF-73367A5D7E57&amp;ID=9806732&amp;M=F" target="_blank" rel="noopener">Sandy City Council</a>: accessory apartment ordinance language</li>
            <li><a href="https://sandy.utah.gov/2353/Accessory-Apartments" target="_blank" rel="noopener">City of Sandy</a>: accessory apartment permitting overview; City Hall, 10000 S Centennial Parkway, Sandy, UT 84070</li>
            <li><a href="https://www.census.gov/quickfacts/fact/table/sandycityutah" target="_blank" rel="noopener">U.S. Census Bureau QuickFacts</a>: Sandy population estimate</li>
            <li><a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener">Zonda 2025 Cost vs. Value Report</a>: national remodel ROI benchmarks</li>
            <li><a href="/adu-rules-2026.html" class="link-arrow">Utah SB284: what changes October 1, 2026 &rarr;</a></li>
          </ul>
        </div>

      </div>
    </div>
  </div>
</section>

"""


def deep_content_west_jordan():
    """Bespoke, research-backed deep-content section for West Jordan. Real
    Ordinance 21-18, real 10,000 sq ft detached threshold tied to specific
    zones (PC/LSFR/VLSFR), real rental-license-not-owner-occupancy rule,
    Redfin/Homes.com-verified neighborhoods. Built by hand rather than
    the generic template."""
    return f"""<!-- HYPER-LOCAL DEEP CONTENT: WEST JORDAN (bespoke) -->
<section>
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">THE WEST JORDAN DETAILS</p>
      <h2>West Jordan's Detached-ADU Rule Only Applies in Certain Zones</h2>
      <p class="lede">West Jordan already allowed detached ADUs years before SB284, but only on larger lots in specific zones. An internal ADU has a much lower bar &mdash; and West Jordan cares less about who lives where than most cities, and more about whether you've got a rental license.</p>
    </div>

    <img class="deep-image reveal" src="https://images.unsplash.com/photo-1600566752355-35792bedcfea?q=80&w=1800&auto=format&fit=crop" alt="Residential neighborhood in West Jordan, Utah near the Jordan River">

    <div class="spec-cards reveal" style="max-width:900px; margin-left:auto; margin-right:auto; margin-bottom:56px;">
      <div class="spec-card"><div class="spec-value">116,812</div><div class="spec-label">Population (2025 est.)</div></div>
      <div class="spec-card"><div class="spec-value">1941</div><div class="spec-label">Incorporated (settled 1848)</div></div>
      <div class="spec-card"><div class="spec-value">10,000 sq ft</div><div class="spec-label">Minimum lot size for a detached ADU</div></div>
      <div class="spec-card"><div class="spec-value">Jordan School District</div><div class="spec-label">Serves most of the city</div></div>
    </div>

    <div class="deep-layout reveal">
      <nav class="deep-jumpnav">
        <a href="#westjordan-neighborhoods">Neighborhoods</a>
        <a href="#westjordan-zoning">Zoning &amp; Permits</a>
        <a href="#westjordan-rental">Rental License, Not Occupancy</a>
        <a href="#westjordan-cost">Cost</a>
        <a href="#westjordan-sources">Sources</a>
      </nav>
      <div class="blog-post-body" style="margin:0; max-width:none;">

        <div class="content-block" id="westjordan-neighborhoods">
          <h3>{PIN_SVG} From Jordan Landing's Growth Corridor to Older River-Adjacent Lots</h3>
          <p>One of Utah's largest cities by population, West Jordan grew from 1848 farmland along the Jordan River into a major Salt Lake County hub anchored by Jordan Landing, a large mixed-use retail development, and a UTA TRAX line with six stops in the city. Its residential character spans real, distinct areas:</p>
          <div class="neighborhood-cards">
            <div class="neighborhood-card"><h4>Jordan Hills</h4><p>A defined residential neighborhood in West Jordan.</p></div>
            <div class="neighborhood-card"><h4>Copper Hills</h4><p>A named area toward the Oquirrh Mountains side of the city, newer growth territory.</p></div>
            <div class="neighborhood-card"><h4>Jordan Oaks &amp; Cobble Creek</h4><p>Additional mapped residential areas reflecting West Jordan's mix of older and newer construction.</p></div>
          </div>
          <p style="margin-top:8px;">Because West Jordan genuinely mixes century-old agricultural-heritage lots with newer, tighter subdivisions toward the Oquirrh foothills, the zone your specific lot sits in matters more here than in a more uniform city.</p>
        </div>

        <div class="content-block" id="westjordan-zoning">
          <h3>{CLIPBOARD_SVG} Internal vs. Detached: Two Very Different Bars to Clear</h3>
          <p>West Jordan's ADU ordinance (adopted under Ordinance No. 21-18, years ahead of SB284) treats internal and detached units very differently:</p>
          <div class="table-wrap">
            <table class="data-table">
              <tr><th>Requirement</th><th>West Jordan Standard</th></tr>
              <tr><td>Internal ADU</td><td>Allowed in all R-1 zones, no stated minimum lot size</td></tr>
              <tr><td>Detached ADU</td><td>Only on lots 10,000 sq ft or larger, and only in PC, LSFR, and VLSFR zones</td></tr>
              <tr><td>Detached ADU size</td><td>Smaller than the main house, capped at 20% of combined rear and side yard area</td></tr>
              <tr><td>Setbacks (detached)</td><td>6 ft from the primary dwelling, 15 ft rear, 8 ft interior side, 20 ft corner side</td></tr>
              <tr><td>Parking</td><td>1 additional paved, non-tandem space, 9&prime;&times;18&prime; minimum</td></tr>
            </table>
          </div>
          <p>A detached ADU also isn't allowed on a lot with a failing septic system, and it can't be paired with multi-family, mobile-home or attached/townhome-style housing. Because the detached path only works in specific zones, we confirm your exact zone designation with West Jordan's Community Development Department before we tell you what's possible.</p>
        </div>

        <div class="content-block" id="westjordan-rental">
          <h3>{HAMMER_SVG} West Jordan Cares About a Rental License, Not Who Lives Where</h3>
          <p>Unlike most Utah cities we build in, West Jordan's ordinance doesn't hinge on an owner-occupancy requirement. Instead, the trigger is simpler: if either the main house or the ADU is rented out, you need a valid business license for that rental. That's a meaningfully different compliance path than a city like Provo or Highland, where owner-occupancy of the main home is the rule itself.</p>
        </div>

        <div class="content-block" id="westjordan-cost">
          <h3>{SHIELD_SVG} What Does an ADU Cost in West Jordan?</h3>
          <p>Because West Jordan's detached-ADU path is zone-restricted while internal conversions are allowed almost everywhere, most projects here split cleanly into one of two very different budgets. <a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener" class="link-arrow">Zonda's 2025 Cost vs. Value Report</a> gives useful national context for comparable home-investment categories:</p>
          <div class="table-wrap">
            <table class="data-table">
              <tr><th>Project Type</th><th>Typical Cost</th><th>Typical ROI</th></tr>
              <tr><td>Basement remodel (comparable scope to an ADU conversion)</td><td>$65K&ndash;$120K+</td><td>~70&ndash;75%</td></tr>
              <tr><td>Home addition (comparable scope to a detached ADU)</td><td>$225&ndash;$375 / sq ft</td><td>~50&ndash;60%</td></tr>
            </table>
          </div>
          <p class="source-note">Source: <a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener">Zonda 2025 Cost vs. Value Report</a>, national data; your West Jordan quote reflects which zone and unit type fits your property, and your finish level, not this table.</p>
          <p>Pro-Worx ADU pricing in West Jordan typically lands at $90K&ndash;$170K for an internal conversion, and $190K&ndash;$290K for a detached, ground-up build on a qualifying lot and zone.</p>
        </div>

        <div class="content-block" id="westjordan-sources">
          <h3>Sources</h3>
          <ul class="sources-list">
            <li><a href="https://www.westjordanutah.gov/" target="_blank" rel="noopener">West Jordan Ordinance No. 21-18</a>: accessory dwelling unit standards</li>
            <li><a href="https://www.westjordanutah.gov/" target="_blank" rel="noopener">City of West Jordan</a>: City Hall, 8000 South Redwood Road, West Jordan, UT 84088</li>
            <li><a href="https://www.census.gov/quickfacts/fact/table/westjordancityutah" target="_blank" rel="noopener">U.S. Census Bureau QuickFacts</a>: West Jordan population estimate</li>
            <li><a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener">Zonda 2025 Cost vs. Value Report</a>: national remodel ROI benchmarks</li>
            <li><a href="/adu-rules-2026.html" class="link-arrow">Utah SB284: what changes October 1, 2026 &rarr;</a></li>
          </ul>
        </div>

      </div>
    </div>
  </div>
</section>

"""


def deep_content_cottonwood_heights():
    """Bespoke, research-backed deep-content section for Cottonwood
    Heights. Real $100 license fee, real $1,100 detached conditional-use
    fee, real short-term-rental ban, real egress rule. Honest about
    unverified max-size and setback figures. Built by hand rather than
    the generic template."""
    return f"""<!-- HYPER-LOCAL DEEP CONTENT: COTTONWOOD HEIGHTS (bespoke) -->
<section>
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">THE COTTONWOOD HEIGHTS DETAILS</p>
      <h2>Cottonwood Heights Requires a License and a Conditional-Use Permit &mdash; That's Two Different Fees</h2>
      <p class="lede">Cottonwood Heights legalized ADUs back in 2021, well ahead of SB284. An internal conversion is a relatively simple licensing process, but a detached ADU adds a conditional-use permit on top &mdash; and a separate fee for it.</p>
    </div>

    <img class="deep-image reveal" src="https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?q=80&w=1800&auto=format&fit=crop" alt="Residential neighborhood in Cottonwood Heights, Utah near the mouth of Big Cottonwood Canyon">

    <div class="spec-cards reveal" style="max-width:900px; margin-left:auto; margin-right:auto; margin-bottom:56px;">
      <div class="spec-card"><div class="spec-value">32,265</div><div class="spec-label">Population (2025 est.)</div></div>
      <div class="spec-card"><div class="spec-value">2005</div><div class="spec-label">Incorporated (after a 2004 referendum)</div></div>
      <div class="spec-card"><div class="spec-value">6,000 sq ft</div><div class="spec-label">Minimum lot size for an ADU</div></div>
      <div class="spec-card"><div class="spec-value">Canyons School District</div><div class="spec-label">Serves the city</div></div>
    </div>

    <div class="deep-layout reveal">
      <nav class="deep-jumpnav">
        <a href="#ch-neighborhoods">Neighborhoods</a>
        <a href="#ch-zoning">Zoning &amp; Permits</a>
        <a href="#ch-rentals">No Short-Term Rentals</a>
        <a href="#ch-cost">Cost</a>
        <a href="#ch-sources">Sources</a>
      </nav>
      <div class="blog-post-body" style="margin:0; max-width:none;">

        <div class="content-block" id="ch-neighborhoods">
          <h3>{PIN_SVG} A Canyon-Mouth City Built Around Established Neighborhoods</h3>
          <p>Cottonwood Heights sits at the mouth of both Big and Little Cottonwood Canyons, giving it direct access to some of Utah's best-known ski resorts. It's one of Salt Lake County's newer incorporated cities, becoming official in 2005 after decades as unincorporated county land, and its housing stock reflects that older, established suburban character:</p>
          <div class="neighborhood-cards">
            <div class="neighborhood-card"><h4>Old Mill</h4><p>A recognized area tied to the city's Old Mill Golf Course and surrounding development.</p></div>
            <div class="neighborhood-card"><h4>Butler &amp; Butler West</h4><p>Established residential neighborhoods on the ridge between Big and Little Cottonwood Creeks.</p></div>
          </div>
          <p style="margin-top:8px;">Because most of Cottonwood Heights was built out well before incorporation, lot sizes and layouts tend to follow older suburban patterns rather than newer subdivision standards &mdash; something we factor into every ADU conversion here.</p>
        </div>

        <div class="content-block" id="ch-zoning">
          <h3>{CLIPBOARD_SVG} What Cottonwood Heights' ADU Ordinance Actually Requires</h3>
          <p>Cottonwood Heights City Council legalized ADUs on September 21, 2021, years ahead of Utah's SB284 mandate. The city's official ADU checklists spell out two distinct paths:</p>
          <div class="table-wrap">
            <table class="data-table">
              <tr><th>Requirement</th><th>Cottonwood Heights Standard</th></tr>
              <tr><td>Minimum lot size</td><td>6,000 sq ft (R-1, RR-1, F-1 zones)</td></tr>
              <tr><td>Internal ADU parking</td><td>1 additional space beyond the 2 required for the main home, no tandem</td></tr>
              <tr><td>ADU license fee</td><td>$100</td></tr>
              <tr><td>Owner-occupancy</td><td>Required (main home or ADU), with proof required at application</td></tr>
              <tr><td>Units per property</td><td>One ADU maximum</td></tr>
            </table>
          </div>
          <p>A detached ADU adds a conditional-use permit on top of the standard license, which the internal path doesn't require. Cottonwood Heights' published checklists don't state a maximum ADU square footage or specific setback figures the way some cities do, so we confirm those details, along with the current conditional-use fee, directly with the city's Community Development Department before pricing any detached project.</p>
        </div>

        <div class="content-block" id="ch-rentals">
          <h3>{HAMMER_SVG} Long-Term Only &mdash; No Airbnb, and a Real Egress Rule</h3>
          <p>Cottonwood Heights requires a minimum 30 consecutive days for any ADU rental, and short-term rentals are explicitly prohibited under city code. If you're converting a basement or below-grade space, the city also requires a minimum 5.0-square-foot egress opening &mdash; a specific number worth knowing before you finalize a floor plan, since it affects where windows and stairwells can go.</p>
        </div>

        <div class="content-block" id="ch-cost">
          <h3>{SHIELD_SVG} What Does an ADU Cost in Cottonwood Heights?</h3>
          <p>Because a detached ADU here adds a conditional-use permit on top of the standard license fee, that path carries more upfront process than an internal conversion. <a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener" class="link-arrow">Zonda's 2025 Cost vs. Value Report</a> gives useful national context for comparable home-investment categories:</p>
          <div class="table-wrap">
            <table class="data-table">
              <tr><th>Project Type</th><th>Typical Cost</th><th>Typical ROI</th></tr>
              <tr><td>Basement remodel (comparable scope to an ADU conversion)</td><td>$65K&ndash;$120K+</td><td>~70&ndash;75%</td></tr>
              <tr><td>Home addition (comparable scope to a detached ADU)</td><td>$225&ndash;$375 / sq ft</td><td>~50&ndash;60%</td></tr>
            </table>
          </div>
          <p class="source-note">Source: <a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener">Zonda 2025 Cost vs. Value Report</a>, national data; your Cottonwood Heights quote reflects your home's layout, permit path and finish level, not this table.</p>
          <p>Pro-Worx ADU pricing in Cottonwood Heights typically lands at $95K&ndash;$180K for an internal conversion, and $200K&ndash;$300K for a detached, ground-up build once the conditional-use permit and its requirements are confirmed with the city.</p>
        </div>

        <div class="content-block" id="ch-sources">
          <h3>Sources</h3>
          <ul class="sources-list">
            <li><a href="https://www.cottonwoodheights.utah.gov/city-services/community-development/accessory-dwelling-units" target="_blank" rel="noopener">City of Cottonwood Heights</a>: ADU program overview and official Internal ADU checklist</li>
            <li><a href="https://www.cottonwoodheights.utah.gov/community/history/contact-us" target="_blank" rel="noopener">Cottonwood Heights City Hall</a>: 2277 Bengal Blvd, Cottonwood Heights, UT 84121</li>
            <li><a href="https://www.census.gov/quickfacts/fact/table/cottonwoodheightscityutah" target="_blank" rel="noopener">U.S. Census Bureau QuickFacts</a>: Cottonwood Heights population estimate</li>
            <li><a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener">Zonda 2025 Cost vs. Value Report</a>: national remodel ROI benchmarks</li>
            <li><a href="/adu-rules-2026.html" class="link-arrow">Utah SB284: what changes October 1, 2026 &rarr;</a></li>
          </ul>
        </div>

      </div>
    </div>
  </div>
</section>

"""


def deep_content_herriman():
    """Bespoke, research-backed deep-content section for Herriman. Real
    current I-ADU/DADU rules, real Jan 2026 staff proposal to rewrite the
    DADU ordinance (framed honestly as pending, not adopted), real HOA
    prevalence. Built by hand rather than the generic template."""
    return f"""<!-- HYPER-LOCAL DEEP CONTENT: HERRIMAN (bespoke) -->
<section>
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">THE HERRIMAN DETAILS</p>
      <h2>Herriman's Detached ADU Rule Is Being Rewritten Right Now</h2>
      <p class="lede">Herriman already allows detached ADUs, but the city's Planning Commission has a new, more permissive ordinance under review as of early 2026 &mdash; and almost every lot in this fast-growing city also sits inside an HOA with its own say.</p>
    </div>

    <img class="deep-image reveal" src="https://images.unsplash.com/photo-1600585154526-990dced4db0d?q=80&w=1800&auto=format&fit=crop" alt="New master-planned subdivision in Herriman, Utah near the Oquirrh Mountains">

    <div class="spec-cards reveal" style="max-width:900px; margin-left:auto; margin-right:auto; margin-bottom:56px;">
      <div class="spec-card"><div class="spec-value">63,282</div><div class="spec-label">Population (2025 est., +14.7% since 2020)</div></div>
      <div class="spec-card"><div class="spec-value">2001</div><div class="spec-label">Became a city (town since 1999)</div></div>
      <div class="spec-card"><div class="spec-value">$559</div><div class="spec-label">Current detached ADU application review fee</div></div>
      <div class="spec-card"><div class="spec-value">Jordan School District</div><div class="spec-label">Serves the city</div></div>
    </div>

    <div class="deep-layout reveal">
      <nav class="deep-jumpnav">
        <a href="#herriman-neighborhoods">Neighborhoods</a>
        <a href="#herriman-zoning">Current Zoning Rule</a>
        <a href="#herriman-proposed">Proposed Rewrite</a>
        <a href="#herriman-hoa">HOA Reality Check</a>
        <a href="#herriman-cost">Cost</a>
        <a href="#herriman-sources">Sources</a>
      </nav>
      <div class="blog-post-body" style="margin:0; max-width:none;">

        <div class="content-block" id="herriman-neighborhoods">
          <h3>{PIN_SVG} One of Utah's Fastest-Growing Cities, Almost Entirely New Construction</h3>
          <p>Herriman grew nearly 15% between 2020 and 2025 alone, expanding from a small settlement near the Oquirrh Mountains into a major Salt Lake County city built almost entirely on master-planned communities:</p>
          <div class="neighborhood-cards">
            <div class="neighborhood-card"><h4>Rosecrest</h4><p>A major Sorenson Companies master-planned community and one of Herriman's best-known developments.</p></div>
            <div class="neighborhood-card"><h4>Blackridge &amp; Silvercrest</h4><p>Established newer-build communities within the city.</p></div>
            <div class="neighborhood-card"><h4>Herriman Towne Center</h4><p>A mixed residential and commercial area with its own dedicated Master HOA.</p></div>
            <div class="neighborhood-card"><h4>Olympia</h4><p>A newer growth area added through a 933-acre annexation in 2022.</p></div>
          </div>
          <p style="margin-top:8px;">Because nearly every one of these communities is HOA-governed, we treat the HOA conversation as a real, separate step on every Herriman project &mdash; not an afterthought.</p>
        </div>

        <div class="content-block" id="herriman-zoning">
          <h3>{CLIPBOARD_SVG} What Herriman's Rule Requires Right Now</h3>
          <p>Herriman currently allows both internal (I-ADU) and detached (DADU) accessory dwelling units in residential and agricultural zones:</p>
          <div class="table-wrap">
            <table class="data-table">
              <tr><th>Requirement</th><th>Herriman Standard (Current)</th></tr>
              <tr><td>Minimum lot size, internal ADU</td><td>6,000 sq ft</td></tr>
              <tr><td>Minimum lot size, detached ADU</td><td>0.2295 acres (about 10,000 sq ft)</td></tr>
              <tr><td>Internal ADU structure rule</td><td>Must share a wall with the primary dwelling</td></tr>
              <tr><td>Parking</td><td>1 additional space beyond the 4 already required for the main home</td></tr>
              <tr><td>Detached ADU application fee</td><td>$559 review fee, plus standard building permit fees</td></tr>
              <tr><td>Units per lot</td><td>One ADU maximum</td></tr>
            </table>
          </div>
          <p>Owner-occupancy is required, backed by a recorded agreement on the property. We confirm your specific zone and lot size with Herriman's Planning Department before pricing anything, especially given the ordinance is actively changing (see next section).</p>
        </div>

        <div class="content-block" id="herriman-proposed">
          <h3>{HAMMER_SVG} A More Permissive Rule Is Already Under Review</h3>
          <p>As of a January 21, 2026 Planning Commission staff report, Herriman has a new detached ADU ordinance proposed &mdash; not yet adopted &mdash; that would meaningfully change the math: a lower 6,000-sq-ft lot minimum (matching the internal-ADU threshold), a size cap of 1,000 sq ft or 50% of the main dwelling, a 20-ft height limit, 10-ft rear and 8-ft side setbacks, and a requirement that the ADU match the primary home's materials and style. The proposal also explicitly prohibits short-term rentals. City staff cited anticipated state legislation, almost certainly Utah's SB284, as a driver for the rewrite. Because this hasn't been formally adopted as of this writing, we confirm the current, in-force version of the ordinance with the city before finalizing any detached ADU plan.</p>
        </div>

        <div class="content-block" id="herriman-hoa">
          <h3>{CLOCK_SVG} The City Might Say Yes. Your HOA Still Gets a Vote.</h3>
          <p>Herriman itself maintains a dedicated HOA map layer on its city GIS system, which tells you how prevalent HOA coverage is here &mdash; similar to what we see in Vineyard. Communities like Rosecrest and Herriman Towne Center have active, well-organized HOAs with their own architectural review. We treat HOA approval as a distinct step from city zoning on every Herriman project, and confirm your specific community's covenants before finalizing a design.</p>
        </div>

        <div class="content-block" id="herriman-cost">
          <h3>{SHIELD_SVG} What Does an ADU Cost in Herriman?</h3>
          <p>Because Herriman's building stock is almost entirely new construction and its detached-ADU rule is actively changing, most projects here are ground-up builds priced against the current ordinance, with a plan to confirm any new standard before permits are pulled. <a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener" class="link-arrow">Zonda's 2025 Cost vs. Value Report</a> gives useful national context for comparable home-investment categories:</p>
          <div class="table-wrap">
            <table class="data-table">
              <tr><th>Project Type</th><th>Typical Cost</th><th>Typical ROI</th></tr>
              <tr><td>Basement remodel (comparable scope to an ADU conversion)</td><td>$65K&ndash;$120K+</td><td>~70&ndash;75%</td></tr>
              <tr><td>Home addition (comparable scope to a detached ADU)</td><td>$225&ndash;$375 / sq ft</td><td>~50&ndash;60%</td></tr>
            </table>
          </div>
          <p class="source-note">Source: <a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener">Zonda 2025 Cost vs. Value Report</a>, national data; your Herriman quote reflects your community, HOA requirements and finish level, not this table.</p>
          <p>Pro-Worx ADU pricing in Herriman typically lands at $190K&ndash;$290K for a full detached, ground-up build, with HOA-driven design matching (exterior materials, rooflines) priced separately once we know your community's standards.</p>
        </div>

        <div class="content-block" id="herriman-sources">
          <h3>Sources</h3>
          <ul class="sources-list">
            <li><a href="https://www.herriman.org/uploads/files/2600/I-ADU-General-Requirements.pdf" target="_blank" rel="noopener">City of Herriman</a>: Internal ADU requirements</li>
            <li><a href="https://www.herriman.gov/dadu" target="_blank" rel="noopener">City of Herriman</a>: current Detached ADU standards and fees</li>
            <li><a href="https://herrimancity-meeting-files-pc.s3.us-west-1.amazonaws.com/1-21-26/Item+5.3+-+Staff+Report.pdf" target="_blank" rel="noopener">Herriman Planning Commission</a>: January 21, 2026 staff report on a proposed DADU ordinance rewrite</li>
            <li><a href="https://www.census.gov/quickfacts/fact/table/herrimancityutah" target="_blank" rel="noopener">U.S. Census Bureau QuickFacts</a>: Herriman population estimate</li>
            <li><a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener">Zonda 2025 Cost vs. Value Report</a>: national remodel ROI benchmarks</li>
            <li><a href="/adu-rules-2026.html" class="link-arrow">Utah SB284: what changes October 1, 2026 &rarr;</a></li>
          </ul>
        </div>

      </div>
    </div>
  </div>
</section>

"""


def deep_content_salt_lake_city():
    """Bespoke, research-backed deep-content section for Salt Lake City.
    Real Sec. 21A.40.200, real 1,000 sq ft detached cap with no size limit
    on internal units, real historic-district design review overlap, real
    neighborhood-by-neighborhood lot character. Built by hand rather than
    the generic template."""
    return f"""<!-- HYPER-LOCAL DEEP CONTENT: SALT LAKE CITY (bespoke) -->
<section>
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">THE SALT LAKE CITY DETAILS</p>
      <h2>In Salt Lake City, Your Neighborhood Decides More Than the Zoning Code Does</h2>
      <p class="lede">SLC's ADU ordinance is mature and citywide, with no minimum lot size at all. But whether that means an easy internal conversion or a Historic Landmark Commission review depends entirely on which neighborhood your home sits in.</p>
    </div>

    <img class="deep-image reveal" src="https://images.unsplash.com/photo-1600566752229-250ed79470f8?q=80&w=1800&auto=format&fit=crop" alt="Historic bungalow homes in a Salt Lake City neighborhood">

    <div class="spec-cards reveal" style="max-width:900px; margin-left:auto; margin-right:auto; margin-bottom:56px;">
      <div class="spec-card"><div class="spec-value">218,428</div><div class="spec-label">Population (2025 est.)</div></div>
      <div class="spec-card"><div class="spec-value">1847</div><div class="spec-label">Founded (Utah's capital &amp; largest city)</div></div>
      <div class="spec-card"><div class="spec-value">No minimum</div><div class="spec-label">Lot size required for an ADU</div></div>
      <div class="spec-card"><div class="spec-value">Salt Lake City School District</div><div class="spec-label">Serves the city</div></div>
    </div>

    <div class="deep-layout reveal">
      <nav class="deep-jumpnav">
        <a href="#slc-neighborhoods">Neighborhoods</a>
        <a href="#slc-zoning">Zoning &amp; Permits</a>
        <a href="#slc-historic">Historic Districts</a>
        <a href="#slc-cost">Cost</a>
        <a href="#slc-sources">Sources</a>
      </nav>
      <div class="blog-post-body" style="margin:0; max-width:none;">

        <div class="content-block" id="slc-neighborhoods">
          <h3>{PIN_SVG} From the Avenues' Tight Historic Grid to Rose Park's Post-War Lots</h3>
          <p>As Utah's capital and largest city, Salt Lake City covers more architectural and lot-size variety than any other city we build in:</p>
          <div class="neighborhood-cards">
            <div class="neighborhood-card"><h4>The Avenues</h4><p>Platted in the 1850s&ndash;1890s, a dense grid of small lots with mostly pre-1930 housing and its own local Historic Preservation Overlay District.</p></div>
            <div class="neighborhood-card"><h4>Capitol Hill</h4><p>A separate, distinct local Historic Preservation Overlay District, also listed on the National Register.</p></div>
            <div class="neighborhood-card"><h4>Yalecrest</h4><p>An east-bench National Historic District known for larger lots and architect-designed 1920s&ndash;40s homes.</p></div>
            <div class="neighborhood-card"><h4>Sugar House</h4><p>A commercial core surrounded by residential blocks of mixed vintage, from older bungalows to newer infill.</p></div>
            <div class="neighborhood-card"><h4>Rose Park &amp; Poplar Grove</h4><p>West-side neighborhoods with newer, post-WWII, more uniform suburban-style lots &mdash; generally more affordable and less design-restricted than the east-side historic districts.</p></div>
          </div>
          <p style="margin-top:8px;">The practical difference is real: an ADU in Rose Park and an ADU in the Avenues can involve completely different review processes even though they're in the same city.</p>
        </div>

        <div class="content-block" id="slc-zoning">
          <h3>{CLIPBOARD_SVG} SLC's ADU Code Has No Minimum Lot Size</h3>
          <p>Salt Lake City Code &sect;21A.40.200 governs ADUs citywide, and it's more permissive on lot size than almost any other city we build in:</p>
          <div class="table-wrap">
            <table class="data-table">
              <tr><th>Requirement</th><th>Salt Lake City Standard</th></tr>
              <tr><td>Minimum lot size</td><td>None required</td></tr>
              <tr><td>Max detached ADU size</td><td>1,000 sq ft gross floor area</td></tr>
              <tr><td>Max internal ADU size</td><td>No specific cap &mdash; just standard zone requirements</td></tr>
              <tr><td>Setbacks (detached)</td><td>3 ft rear, 3 ft side, corner-side 20% of lot width or 10 ft, whichever is less</td></tr>
              <tr><td>Parking</td><td>1 space, waived near transit, bike infrastructure, or with existing surplus parking</td></tr>
            </table>
          </div>
          <p>Owner-occupancy is required (deed holder, a blood or marriage relative, or a trust's trustor), with exceptions for duplex/multi-family lots, temporary absences up to 3 years, or medical care placement. A restrictive covenant gets recorded with the county, and renting the ADU requires enrolling in the city's landlord-tenant program. Because SLC's rule predates SB284 and is already citywide, we confirm the current standard and any recent updates with SLC Planning before pricing your project.</p>
        </div>

        <div class="content-block" id="slc-historic">
          <h3>{HAMMER_SVG} A Historic District Overlay Changes the Process, Not Just the Style</h3>
          <p>If your home sits in the Avenues or Capitol Hill's local Historic Preservation Overlay District, an ADU project isn't just a building-permit conversation &mdash; it typically means design review through the city's Historic Landmark Commission, on top of the standard zoning process. Yalecrest carries National Register status, which is a different (and generally lighter) form of recognition than a local overlay. We confirm which category your specific address falls under before we scope any design work, since it changes both the timeline and what exterior changes are realistic.</p>
        </div>

        <div class="content-block" id="slc-cost">
          <h3>{SHIELD_SVG} What Does an ADU Cost in Salt Lake City?</h3>
          <p>Because SLC's smaller historic lots often favor an internal conversion over a detached build, and historic-district design review can add both time and cost, project scope here varies more by neighborhood than by a single citywide number. <a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener" class="link-arrow">Zonda's 2025 Cost vs. Value Report</a> gives useful national context for comparable home-investment categories:</p>
          <div class="table-wrap">
            <table class="data-table">
              <tr><th>Project Type</th><th>Typical Cost</th><th>Typical ROI</th></tr>
              <tr><td>Basement remodel (comparable scope to an ADU conversion)</td><td>$65K&ndash;$120K+</td><td>~70&ndash;75%</td></tr>
              <tr><td>Home addition (comparable scope to a detached ADU)</td><td>$225&ndash;$375 / sq ft</td><td>~50&ndash;60%</td></tr>
            </table>
          </div>
          <p class="source-note">Source: <a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener">Zonda 2025 Cost vs. Value Report</a>, national data; your SLC quote reflects your neighborhood, historic-district status and finish level, not this table.</p>
          <p>Pro-Worx ADU pricing in Salt Lake City typically lands at $90K&ndash;$180K for an internal conversion, and $190K&ndash;$280K for a detached, ground-up build within the city's 1,000-sq-ft cap, with historic-district design review priced separately when it applies.</p>
        </div>

        <div class="content-block" id="slc-sources">
          <h3>Sources</h3>
          <ul class="sources-list">
            <li><a href="https://codelibrary.amlegal.com/codes/saltlakecityut/latest/saltlakecity_ut/0-0-0-68737" target="_blank" rel="noopener">Salt Lake City Code &sect;21A.40.200</a>: accessory dwelling unit standards</li>
            <li><a href="https://www.slcdocs.com/Planning/Guides/ADU_handbook.pdf" target="_blank" rel="noopener">SLC Planning Division</a>: ADU Handbook</li>
            <li><a href="https://www.slc.gov/historic-preservation/historic-districts-and-buildings/local-historic-districts/the-avenues/" target="_blank" rel="noopener">SLC Historic Preservation</a>: the Avenues local Historic District</li>
            <li><a href="https://www.slc.gov/historic-preservation/historic-districts-and-buildings/national-historic-districts/capitol-hill/" target="_blank" rel="noopener">SLC Historic Preservation</a>: Capitol Hill Historic District</li>
            <li><a href="https://www.census.gov/quickfacts/fact/table/saltlakecitycityutah" target="_blank" rel="noopener">U.S. Census Bureau QuickFacts</a>: Salt Lake City population estimate</li>
            <li><a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener">Zonda 2025 Cost vs. Value Report</a>: national remodel ROI benchmarks</li>
            <li><a href="/adu-rules-2026.html" class="link-arrow">Utah SB284: what changes October 1, 2026 &rarr;</a></li>
          </ul>
        </div>

      </div>
    </div>
  </div>
</section>

"""


def deep_content_south_jordan():
    """Bespoke, research-backed deep-content section for South Jordan.
    Real Municipal Code 17.130.030, real internal-vs-guesthouse split,
    real owner-occupancy verification method, real Daybreak master-planned
    community context (flagged as HOA-dependent, not asserted as fact).
    Built by hand rather than the generic template."""
    return f"""<!-- HYPER-LOCAL DEEP CONTENT: SOUTH JORDAN (bespoke) -->
<section>
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">THE SOUTH JORDAN DETAILS</p>
      <h2>In South Jordan, the City Code Is Only Half the Story</h2>
      <p class="lede">South Jordan's ADU ordinance draws a sharp line between an internal unit and a detached guesthouse &mdash; and if you're in Daybreak, your HOA may have its own opinion on top of the city's.</p>
    </div>

    <img class="deep-image reveal" src="https://images.unsplash.com/photo-1600585152220-90363fe7e115?q=80&w=1800&auto=format&fit=crop" alt="Suburban home in South Jordan, Utah near the Oquirrh Mountains">

    <div class="spec-cards reveal" style="max-width:900px; margin-left:auto; margin-right:auto; margin-bottom:56px;">
      <div class="spec-card"><div class="spec-value">~88,910</div><div class="spec-label">Population (2025 est.)</div></div>
      <div class="spec-card"><div class="spec-value">2</div><div class="spec-label">ADU types: internal &amp; detached guesthouse</div></div>
      <div class="spec-card"><div class="spec-value">1,500 sq ft</div><div class="spec-label">Max guesthouse size (or 35% of home)</div></div>
      <div class="spec-card"><div class="spec-value">14,520 sq ft</div><div class="spec-label">Min lot size for a detached guesthouse</div></div>
    </div>

    <div class="deep-layout reveal">
      <nav class="deep-jumpnav">
        <a href="#sj-neighborhoods">Neighborhoods</a>
        <a href="#sj-zoning">Zoning &amp; Permits</a>
        <a href="#sj-daybreak">Daybreak &amp; HOAs</a>
        <a href="#sj-cost">Cost</a>
        <a href="#sj-sources">Sources</a>
      </nav>
      <div class="blog-post-body" style="margin:0; max-width:none;">

        <div class="content-block" id="sj-neighborhoods">
          <h3>{PIN_SVG} From Daybreak's Master Plan to South Jordan's Older Established Streets</h3>
          <p>South Jordan splits roughly into two eras of development, and it shapes what an ADU project looks like:</p>
          <div class="neighborhood-cards">
            <div class="neighborhood-card"><h4>Daybreak</h4><p>A ~4,200-acre master-planned community built around Oquirrh Lake, with its own villages (Cascade Village, SpringHouse, Watermark, more) and a homeowners association layered on top of city zoning.</p></div>
            <div class="neighborhood-card"><h4>Glenmoor</h4><p>An established subdivision outside Daybreak's master plan, with older, more traditional single-family lots.</p></div>
            <div class="neighborhood-card"><h4>Sunstone Village</h4><p>Another pre-Daybreak South Jordan neighborhood with its own lot character, separate from the master-planned side of the city.</p></div>
          </div>
          <p style="margin-top:8px;">Whether you're in Daybreak or one of South Jordan's older neighborhoods changes more than the view &mdash; it can change who reviews your ADU plans before the city ever sees them.</p>
        </div>

        <div class="content-block" id="sj-zoning">
          <h3>{CLIPBOARD_SVG} South Jordan Splits ADUs Into Two Very Different Categories</h3>
          <p>South Jordan Municipal Code &sect;17.130.030 doesn't treat all ADUs the same way &mdash; an internal unit and a detached guesthouse have different lot, size and review requirements:</p>
          <div class="table-wrap">
            <table class="data-table">
              <tr><th>Requirement</th><th>Internal ADU</th><th>Detached Guesthouse</th></tr>
              <tr><td>Minimum lot size</td><td>6,000 sq ft</td><td>14,520 sq ft</td></tr>
              <tr><td>Max size</td><td>Standard zone limits</td><td>1,500 sq ft or 35% of primary home, whichever is less; max 3 bedrooms</td></tr>
              <tr><td>Review path</td><td>Planning Department review</td><td>Planning Commission review</td></tr>
              <tr><td>Allowed zones</td><td>A-5, A-1, R-1.8, R-2.5, R-3, R-4, R-5</td><td>A-5, A-1, R-1.8 only</td></tr>
            </table>
          </div>
          <p>Owner-occupancy is required for both types, verified through documentation like voter or vehicle registration, and each adds at least one off-street parking space beyond what the primary home already needs. We haven't been able to confirm current permit/review fee amounts directly from the city, so we always confirm those with South Jordan Planning before finalizing a quote &mdash; along with checking how the city's code interacts with Utah's SB284 detached-ADU mandate, effective October 1, 2026, on your specific lot.</p>
        </div>

        <div class="content-block" id="sj-daybreak">
          <h3>{HAMMER_SVG} In Daybreak, Check the HOA Before You Check the City Code</h3>
          <p>Daybreak covers a large share of South Jordan, and it operates under its own homeowners association architectural review in addition to city zoning &mdash; a common pattern for large master-planned communities, though we haven't independently verified Daybreak's current ADU-specific HOA rules against the city's ordinance. If your lot is in Daybreak, the practical first step isn't the building department, it's your village's HOA guidelines: an ADU design the city would approve outright can still need HOA sign-off, and the two reviews don't always move on the same timeline. We check both before we scope a Daybreak project.</p>
        </div>

        <div class="content-block" id="sj-cost">
          <h3>{SHIELD_SVG} What Does an ADU Cost in South Jordan?</h3>
          <p>South Jordan's split between internal conversions and ground-up detached guesthouses means project cost varies more by which path your lot qualifies for than almost anywhere else we build. <a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener" class="link-arrow">Zonda's 2025 Cost vs. Value Report</a> gives useful national context for comparable home-investment categories:</p>
          <div class="table-wrap">
            <table class="data-table">
              <tr><th>Project Type</th><th>Typical Cost</th><th>Typical ROI</th></tr>
              <tr><td>Basement remodel (comparable scope to an internal ADU)</td><td>$65K&ndash;$120K+</td><td>~70&ndash;75%</td></tr>
              <tr><td>Home addition (comparable scope to a detached guesthouse)</td><td>$225&ndash;$375 / sq ft</td><td>~50&ndash;60%</td></tr>
            </table>
          </div>
          <p class="source-note">Source: <a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener">Zonda 2025 Cost vs. Value Report</a>, national data; your South Jordan quote reflects your lot type, HOA requirements (if applicable) and finish level, not this table.</p>
          <p>Pro-Worx ADU pricing in South Jordan typically lands at $85K&ndash;$160K for an internal conversion, and $200K&ndash;$300K for a detached guesthouse within the city's size cap, with any Daybreak HOA design review handled as part of our planning process.</p>
        </div>

        <div class="content-block" id="sj-sources">
          <h3>Sources</h3>
          <ul class="sources-list">
            <li><a href="https://www.sjc.utah.gov/DocumentCenter/View/826/Accessory-Dwelling-Unit-ADU-PDF" target="_blank" rel="noopener">City of South Jordan</a>: Accessory Dwelling Unit (ADU) guide, Municipal Code &sect;17.130.030</li>
            <li><a href="https://en.wikipedia.org/wiki/South_Jordan,_Utah" target="_blank" rel="noopener">Wikipedia</a>: South Jordan population and geography</li>
            <li><a href="https://www.daybreakutah.com/villages-districts/" target="_blank" rel="noopener">Daybreak Utah</a>: villages and districts</li>
            <li><a href="https://www.census.gov/quickfacts/fact/table/southjordancityutah" target="_blank" rel="noopener">U.S. Census Bureau QuickFacts</a>: South Jordan population estimate</li>
            <li><a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener">Zonda 2025 Cost vs. Value Report</a>: national remodel ROI benchmarks</li>
            <li><a href="/adu-rules-2026.html" class="link-arrow">Utah SB284: what changes October 1, 2026 &rarr;</a></li>
          </ul>
        </div>

      </div>
    </div>
  </div>
</section>

"""


def deep_content_bountiful():
    """Bespoke, research-backed deep-content section for Bountiful.
    Real Land Use Code Sec. 14-14-124, real 8,000 sq ft buildable-land
    minimum for a detached ADU with a flat 350-1,250 sq ft size band,
    real internal-vs-detached approval split (staff review vs. Administrative
    Committee conditional use). Built by hand rather than the generic
    template."""
    return f"""<!-- HYPER-LOCAL DEEP CONTENT: BOUNTIFUL (bespoke) -->
<section>
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">THE BOUNTIFUL DETAILS</p>
      <h2>In Bountiful, an Internal ADU and a Backyard ADU Go Through Completely Different Doors</h2>
      <p class="lede">Bountiful's code treats an internal conversion as a simple staff-approved permitted use &mdash; but a detached backyard unit needs conditional-use approval from the city's Administrative Committee, on a lot with real buildable-land requirements.</p>
    </div>

    <img class="deep-image reveal" src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?q=80&w=1800&auto=format&fit=crop" alt="Home on the east bench of Bountiful, Utah with mountain slopes behind it">

    <div class="spec-cards reveal" style="max-width:900px; margin-left:auto; margin-right:auto; margin-bottom:56px;">
      <div class="spec-card"><div class="spec-value">~45,762</div><div class="spec-label">Population (2020 Census)</div></div>
      <div class="spec-card"><div class="spec-value">8,000 sq ft</div><div class="spec-label">Min buildable land for a detached ADU</div></div>
      <div class="spec-card"><div class="spec-value">350&ndash;1,250 sq ft</div><div class="spec-label">Detached ADU size band</div></div>
      <div class="spec-card"><div class="spec-value">1847</div><div class="spec-label">Founded &mdash; Utah's 2nd-oldest settlement</div></div>
    </div>

    <div class="deep-layout reveal">
      <nav class="deep-jumpnav">
        <a href="#bt-neighborhoods">Neighborhoods</a>
        <a href="#bt-zoning">Zoning &amp; Permits</a>
        <a href="#bt-sb284">SB284 Status</a>
        <a href="#bt-cost">Cost</a>
        <a href="#bt-sources">Sources</a>
      </nav>
      <div class="blog-post-body" style="margin:0; max-width:none;">

        <div class="content-block" id="bt-neighborhoods">
          <h3>{PIN_SVG} From the Historic Downtown Core to the Slopes of the East Bench</h3>
          <p>Bountiful was Utah's second permanent settlement after Salt Lake City, and its layout still shows it &mdash; an older downtown core at the base of the Wasatch Range, with residential zones climbing the mountain slopes to the east and flatter, newer development toward the west:</p>
          <div class="neighborhood-cards">
            <div class="neighborhood-card"><h4>Downtown Bountiful</h4><p>The city's original 1847 townsite and Downtown (DN) zone, sitting at the base of the Wasatch Range with the oldest housing stock in the city.</p></div>
            <div class="neighborhood-card"><h4>East Bench</h4><p>Homes climbing the mountain slopes on Bountiful's east side &mdash; a real, commonly used real-estate term for the area, though not an official city-defined boundary.</p></div>
            <div class="neighborhood-card"><h4>Val Verda</h4><p>A recognized neighborhood in southern Bountiful, tracked separately in census and real-estate data.</p></div>
          </div>
          <p style="margin-top:8px;">Older lots near downtown tend to favor an internal conversion, while larger east-bench and Val Verda lots are more likely to clear the buildable-land threshold for a detached unit &mdash; but we check your specific parcel either way.</p>
        </div>

        <div class="content-block" id="bt-zoning">
          <h3>{CLIPBOARD_SVG} Two ADU Types, Two Very Different Approval Paths</h3>
          <p>Bountiful City Land Use Code &sect;14-14-124 splits ADUs into an internal unit and a detached unit, and they don't go through the same process:</p>
          <div class="table-wrap">
            <table class="data-table">
              <tr><th>Requirement</th><th>Internal ADU</th><th>Detached ADU</th></tr>
              <tr><td>Approval path</td><td>Staff review &mdash; permitted use</td><td>Administrative Committee &mdash; conditional use</td></tr>
              <tr><td>Minimum buildable land</td><td>Standard zone requirements</td><td>8,000 sq ft</td></tr>
              <tr><td>Size</td><td>Standard zone requirements</td><td>350&ndash;1,250 sq ft</td></tr>
            </table>
          </div>
          <p>The city's own definition ties an ADU to an owner-occupied primary residence, and we haven't been able to find a published permit fee for either ADU type on the city's site &mdash; we confirm current fees directly with Bountiful Planning (801-298-6190) before finalizing a quote, along with how the city's existing conditional-use process interacts with Utah's SB284 detached-ADU mandate, effective October 1, 2026.</p>
        </div>

        <div class="content-block" id="bt-sb284">
          <h3>{HAMMER_SVG} Has Bountiful Updated Its Code for SB284?</h3>
          <p>We haven't found a public staff report, planning commission agenda, or city council record showing Bountiful has amended its ADU ordinance in response to SB284 as of this writing. That's not the same as saying the city won't &mdash; it's simply what's publicly available right now. Since Bountiful's detached-ADU rule is already a defined conditional-use path rather than an outright ban, we confirm with the city directly how SB284's October 1, 2026 mandate applies to your specific lot before we scope any design work.</p>
        </div>

        <div class="content-block" id="bt-cost">
          <h3>{SHIELD_SVG} What Does an ADU Cost in Bountiful?</h3>
          <p>Because Bountiful's older downtown lots often favor an internal conversion while larger east-bench and Val Verda lots can support a detached build, project scope here depends heavily on which path your property qualifies for. <a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener" class="link-arrow">Zonda's 2025 Cost vs. Value Report</a> gives useful national context for comparable home-investment categories:</p>
          <div class="table-wrap">
            <table class="data-table">
              <tr><th>Project Type</th><th>Typical Cost</th><th>Typical ROI</th></tr>
              <tr><td>Basement remodel (comparable scope to an internal ADU)</td><td>$65K&ndash;$120K+</td><td>~70&ndash;75%</td></tr>
              <tr><td>Home addition (comparable scope to a detached ADU)</td><td>$225&ndash;$375 / sq ft</td><td>~50&ndash;60%</td></tr>
            </table>
          </div>
          <p class="source-note">Source: <a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener">Zonda 2025 Cost vs. Value Report</a>, national data; your Bountiful quote reflects your lot, approval path and finish level, not this table.</p>
          <p>Pro-Worx ADU pricing in Bountiful typically lands at $80K&ndash;$150K for an internal conversion, and $190K&ndash;$270K for a detached build within the city's 1,250-sq-ft cap.</p>
        </div>

        <div class="content-block" id="bt-sources">
          <h3>Sources</h3>
          <ul class="sources-list">
            <li><a href="https://www.bountiful.gov/DocumentCenter/View/623/Chapter-14-Supplementary-Development-Standards-PDF" target="_blank" rel="noopener">Bountiful City Land Use Code</a> &sect;14-14-124: Accessory Dwelling Units</li>
            <li><a href="https://www.bountiful.gov/188/Accessory-Dwelling-Units" target="_blank" rel="noopener">Bountiful City Planning</a>: ADU program overview</li>
            <li><a href="https://en.wikipedia.org/wiki/Bountiful,_Utah" target="_blank" rel="noopener">Wikipedia</a>: Bountiful population, geography and settlement history</li>
            <li><a href="https://zondahome.com/2025-cost-vs-value-report/" target="_blank" rel="noopener">Zonda 2025 Cost vs. Value Report</a>: national remodel ROI benchmarks</li>
            <li><a href="/adu-rules-2026.html" class="link-arrow">Utah SB284: what changes October 1, 2026 &rarr;</a></li>
          </ul>
        </div>

      </div>
    </div>
  </div>
</section>

"""


def local_business_jsonld():
    import json
    data = {
        "@context": "https://schema.org",
        "@type": "GeneralContractor",
        "name": "Pro-Worx ADU",
        "url": BASE_URL,
        "telephone": "+18018884282",
        "email": "info@proworxconstruction.com",
        "parentOrganization": {
            "@type": "Organization",
            "name": "Pro-Worx Construction",
            "url": "https://proworxconstruction.com",
        },
        "areaServed": [
            {"@type": "AdministrativeArea", "name": f"{n}, Utah"} for n, s, c in CITIES
        ],
        "priceRange": "$100K-$300K",
        "openingHours": "Mo-Fr 08:00-18:00",
    }
    return json.dumps(data)


def breadcrumb_jsonld(crumbs):
    """crumbs: list of (name, path) tuples, path may be '' for the current page (no url)."""
    import json
    items = []
    for i, (name, path) in enumerate(crumbs, start=1):
        entry = {"@type": "ListItem", "position": i, "name": name}
        if path:
            entry["item"] = f"{BASE_URL}{path}"
        items.append(entry)
    data = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}
    return json.dumps(data)


def faq_jsonld(qa_pairs):
    """qa_pairs: list of (question, answer) plain-text tuples (HTML tags should already be stripped)."""
    import json
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in qa_pairs
        ],
    }
    return json.dumps(data)


# Custom, hook-specific H1s for the bespoke cities, tied to what actually
# makes each city's ADU rules distinct (rather than one template with the
# name swapped in). Generic-template cities rotate through HERO_H1_TEMPLATES
# instead, so even those don't all read identically.
CITY_HERO_H1 = {
    "alpine": "Can You Build an ADU in Alpine, Utah?",
    "lehi": "Can You Build a Detached ADU in Lehi After SB284?",
    "mapleton": "How Big of an ADU Can You Build in Mapleton, Utah?",
    "spanish-fork": "Can You Build an ADU in Spanish Fork, Utah?",
    "highland": "Can You Build an ADU in Highland, Utah?",
    "lindon": "How Big Can Your ADU Be in Lindon, Utah?",
    "provo": "Can You Build an ADU in Provo, Utah?",
    "vineyard": "Can You Build an ADU in Vineyard, or Does Your HOA Say No?",
    "bluffdale": "How Big of an ADU Can You Build in Bluffdale, Utah?",
    "draper": "Can You Build an ADU on a Hillside Lot in Draper, Utah?",
    "riverton": "How Big Can Your ADU Be in Riverton, Utah?",
    "sandy": "Can You Build a Detached ADU in Sandy, Utah?",
    "west-jordan": "Can You Build a Detached ADU in West Jordan, Utah?",
    "cottonwood-heights": "Do You Need a Permit for an ADU in Cottonwood Heights?",
    "herriman": "Can You Build an ADU in Herriman, or Does Your HOA Say No?",
    "salt-lake-city": "Can You Build an ADU in Salt Lake City?",
    "south-jordan": "Can You Build a Detached Guesthouse in South Jordan, Utah?",
    "bountiful": "Can You Build a Detached ADU in Bountiful, Utah?",
}

HERO_H1_TEMPLATES = [
    "Can You Build an ADU in {name}, Utah?",
    "How Much Does an ADU Cost in {name}?",
    "What Does It Take to Build an ADU in {name}?",
    "Is Your {name} Lot Big Enough for an ADU?",
    "Do You Need a Permit to Build an ADU in {name}?",
    "What Are the ADU Rules in {name}, {county} County?",
    "Can You Add a Rental Unit to Your {name} Property?",
    "How Do You Build an ADU in {name}, Utah?",
]


def hero_h1_for(name, slug, county, index):
    custom = CITY_HERO_H1.get(slug)
    if custom:
        return custom
    template = HERO_H1_TEMPLATES[index % len(HERO_H1_TEMPLATES)]
    return template.format(name=name, county=county)


# Mid-page CTA banner copy, same variation logic as the H1s: custom wording
# tied to each bespoke city's real hook, a rotation pool for the rest.
CITY_CTA1 = {
    "alpine": ("Not sure what your Alpine lot's grading actually allows?", "We'll walk your property, check the slope and your zone, and tell you what's realistic before you commit to anything."),
    "lehi": ("Wondering how SB284 changed things for your Lehi lot?", "We'll check your lot against Lehi's updated ordinance and tell you exactly what's possible &mdash; free, no obligation."),
    "mapleton": ("Not sure your well or septic can handle a Mapleton ADU?", "We'll check your utilities and your lot's size tier before you spend a dollar on design."),
    "spanish-fork": ("Not sure your Spanish Fork lot is in an eligible zone?", "We'll confirm your zone and parking layout before you commit to a floor plan."),
    "highland": ("Wondering if your Highland home can fit an attached ADU?", "We'll walk your layout and confirm what Highland's ordinance actually allows."),
    "lindon": ("Not sure what size ADU your Lindon home qualifies for?", "We'll run your home's size against Lindon's formula and tell you the real number."),
    "provo": ("Not sure how Provo's rules apply to your rental plans?", "We'll walk your property and confirm your zone before you commit to anything."),
    "vineyard": ("Not sure if your Vineyard HOA allows an ADU?", "We'll check the city's rule and help you navigate your HOA's design standards."),
    "bluffdale": ("Not sure what size ADU your Bluffdale home qualifies for?", "We'll measure your home and confirm the 50% size cap before you spend a dollar on design."),
    "draper": ("Not sure what your Draper lot's terrain adds to the budget?", "We'll walk your property, check the slope, and give you a real number before you commit to anything."),
    "riverton": ("Not sure what size ADU your Riverton lot qualifies for?", "We'll run your home's footprint and lot area through the city's formula and tell you the real number."),
    "sandy": ("Not sure if your Sandy home needs an attached or detached ADU path?", "We'll confirm which rule applies to your property before you spend a dollar on design."),
    "west-jordan": ("Not sure if your West Jordan lot is in a detached-ADU zone?", "We'll confirm your zone and lot size before you spend a dollar on design."),
    "cottonwood-heights": ("Not sure if you need a conditional-use permit in Cottonwood Heights?", "We'll confirm which permit path applies to your project before you spend a dollar on design."),
    "herriman": ("Not sure how Herriman's changing ADU rule affects your lot?", "We'll confirm the current standard and your HOA's requirements before you spend a dollar on design."),
    "salt-lake-city": ("Not sure if your SLC home is in a historic district?", "We'll confirm your neighborhood's review requirements before you spend a dollar on design."),
    "south-jordan": ("Not sure if your South Jordan lot qualifies for a guesthouse?", "We'll check your lot size and zone against the city's two ADU categories before you spend a dollar on design."),
    "bountiful": ("Not sure if your Bountiful lot clears the 8,000 sq ft buildable-land minimum?", "We'll check your parcel and tell you which approval path applies before you spend a dollar on design."),
}
CTA1_TEMPLATES = [
    ("Not sure what your {name} lot actually allows?", "We'll walk your property, check it against {name}'s zoning, and tell you exactly what's possible &mdash; free, no obligation."),
    ("Wondering what an ADU would actually cost in {name}?", "We'll give you a real number based on your property, not a generic estimate."),
    ("Is your {name} property a good fit for an ADU?", "We'll check your lot against {name}'s current rules and tell you what's realistic."),
    ("Ready to find out what's possible on your {name} lot?", "A free on-site visit gets you a real answer, not a guess."),
    ("Still deciding if an ADU makes sense in {name}?", "We'll walk you through the numbers and the permitting timeline, free of charge."),
    ("Curious what {name}'s ADU rules mean for your property?", "We'll translate the zoning code into a straight answer for your specific lot."),
]

CITY_CTA2 = {
    "alpine": ("See ADU plans built for Alpine's larger, sloped lots", "Browse fixed-price plan tiers designed with grading and drainage in mind."),
    "lehi": ("See ADU plans and pricing updated for post-SB284 Lehi", "Browse fixed-price plan tiers, or book a free on-site estimate now."),
    "mapleton": ("See ADU plans sized for Mapleton's tiered lot rule", "Browse fixed-price plan tiers, or book a free on-site estimate now."),
    "spanish-fork": ("See ADU plans that fit Spanish Fork's 1,000 sq ft cap", "Browse fixed-price plan tiers, or book a free on-site estimate now."),
    "highland": ("See attached ADU plans built for Highland's ordinance", "Browse fixed-price plan tiers, or book a free on-site estimate now."),
    "lindon": ("See ADU plans sized to Lindon's formula-based cap", "Browse fixed-price plan tiers, or book a free on-site estimate now."),
    "provo": ("See ADU plans built around Provo's occupancy rules", "Browse fixed-price plan tiers, or book a free on-site estimate now."),
    "vineyard": ("See ADU plans that work with Vineyard's HOA standards", "Browse fixed-price plan tiers, or book a free on-site estimate now."),
    "bluffdale": ("See ADU plans sized to Bluffdale's 50% cap", "Browse fixed-price plan tiers, or book a free on-site estimate now."),
    "draper": ("See ADU plans built for Draper's hillside and flat lots alike", "Browse fixed-price plan tiers, or book a free on-site estimate now."),
    "riverton": ("See ADU plans sized to Riverton's lot-based formula", "Browse fixed-price plan tiers, or book a free on-site estimate now."),
    "sandy": ("See ADU plans for Sandy's attached and detached paths", "Browse fixed-price plan tiers, or book a free on-site estimate now."),
    "west-jordan": ("See ADU plans for West Jordan's internal and detached paths", "Browse fixed-price plan tiers, or book a free on-site estimate now."),
    "cottonwood-heights": ("See ADU plans for Cottonwood Heights' licensed and permitted paths", "Browse fixed-price plan tiers, or book a free on-site estimate now."),
    "herriman": ("See ADU plans that work with Herriman's HOA standards", "Browse fixed-price plan tiers, or book a free on-site estimate now."),
    "salt-lake-city": ("See ADU plans built for SLC's historic and newer lots alike", "Browse fixed-price plan tiers, or book a free on-site estimate now."),
    "south-jordan": ("See ADU plans built for Daybreak and older South Jordan lots alike", "Browse fixed-price plan tiers, or book a free on-site estimate now."),
    "bountiful": ("See ADU plans built for Bountiful's downtown and east-bench lots alike", "Browse fixed-price plan tiers, or book a free on-site estimate now."),
}
CTA2_TEMPLATES = [
    ("See ADU plans and pricing for {name}", "Browse fixed-price plan tiers before you talk to anyone, or book a free on-site estimate now."),
    ("Compare {name} ADU plan tiers before you decide", "Every plan is fixed-price, so you know your budget upfront."),
    ("Get a head start on your {name} ADU budget", "Browse our plan tiers, or skip straight to a free on-site estimate."),
    ("Explore what fits your {name} budget and lot", "Fixed-price plans mean no surprises once construction starts."),
    ("See what's already built for {name} homeowners", "Browse our plan tiers, or book a free estimate to get specific numbers."),
    ("Ready to put real numbers to your {name} project?", "Browse fixed-price plans, or get a free on-site estimate now."),
]


def cta1_for(name, slug, index):
    h, p = CITY_CTA1.get(slug) or CTA1_TEMPLATES[index % len(CTA1_TEMPLATES)]
    return h.format(name=name), p.format(name=name)


def cta2_for(name, slug, index):
    h, p = CITY_CTA2.get(slug) or CTA2_TEMPLATES[(index + 3) % len(CTA2_TEMPLATES)]
    return h.format(name=name), p.format(name=name)


def build_city_page(name, slug, county, index):
    local_context, local_sb284_note = LOCAL_FOCUS.get(
        slug,
        (
            f"Every {name} lot is different, which is why we walk the "
            f"property before quoting anything.",
            "We'll confirm exactly how the October 1, 2026 SB284 changes "
            "apply to your specific lot as part of your free estimate.",
        ),
    )
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
    faq_pairs = []
    for q, a in FAQS:
        q_f = q.format(city=name, county=county)
        a_f = a.format(city=name, county=county)
        faq_pairs.append((q_f, a_f))
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
    <h1 class="fade-up d2">{hero_h1_for(name, slug, county, index)}</h1>
    <p class="lede fade-up d3">Pro-Worx Construction designs, permits and builds custom Accessory Dwelling Units for {name} homeowners. Fixed pricing, licensed &amp; insured, 3&ndash;5 week builds on garage and basement conversions.</p>
    <div class="hero-ctas fade-up d4" style="margin-top:32px;">
      <a href="#contact" class="btn btn-primary">GET FREE ESTIMATE</a>
      <a href="/index.html#plans" class="btn btn-light">SEE ADU PLANS &amp; PRICING</a>
    </div>
  </div>
</section>

<div class="container">
  <div class="stats-bar" id="statsBar">
    <div class="stat"><div class="num" data-count="1100" data-suffix="+">0</div><div class="label">Projects Completed</div></div>
    <div class="stat"><div class="num" data-count="20" data-suffix="+">0</div><div class="label">Years of Excellence</div></div>
    <div class="stat"><div class="num">5&#9733;</div><div class="label">Google Rating</div></div>
    <div class="stat"><div class="num" data-count="{len(CITIES)}" data-suffix="">0</div><div class="label">Utah Cities Served</div></div>
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
      <p class="lede">Every property is different. We'll walk your site and recommend the configuration that fits your space, budget and goals.</p>
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
          <h3>Do I Need a Permit for an ADU in {name}?</h3>
          <p>Most ADU permits in {county} County are processed through the {name} building and planning department. We handle intake, plan review coordination and inspection scheduling for you from start to finish, so you never have to deal with the city directly.</p>
        </div>
      </div>
      <div class="seasonal-band">
        {HAMMER_SVG}
        <p><strong>What's different about ADUs in {name}.</strong> {local_context}</p>
      </div>
    </div>
    <div class="permit-callout reveal" style="margin-top:24px;">
      {CLIPBOARD_SVG}
      <div>
        <h3>What Does Utah's New ADU Law (SB284) Mean for {name} Homeowners?</h3>
        <p>Utah's SB284 now requires most cities to allow one detached ADU per qualifying lot statewide. {local_sb284_note} See the full breakdown on our <a href="/adu-rules-2026.html" class="link-arrow">2026 ADU law page &rarr;</a>.</p>
      </div>
    </div>
  </div>
</section>

<!-- MID-PAGE CTA 1 -->
<section class="bg-secondary" style="padding-top:48px; padding-bottom:48px;">
  <div class="container">
    <div class="inline-cta reveal">
      <div>
        <h3>{cta1_for(name, slug, index)[0]}</h3>
        <p>{cta1_for(name, slug, index)[1]}</p>
      </div>
      <a href="#contact" class="btn btn-primary">GET FREE ESTIMATE</a>
    </div>
  </div>
</section>

{deep_content_alpine() if slug == 'alpine' else deep_content_lehi() if slug == 'lehi' else deep_content_mapleton() if slug == 'mapleton' else deep_content_spanish_fork() if slug == 'spanish-fork' else deep_content_highland() if slug == 'highland' else deep_content_lindon() if slug == 'lindon' else deep_content_provo() if slug == 'provo' else deep_content_vineyard() if slug == 'vineyard' else deep_content_bluffdale() if slug == 'bluffdale' else deep_content_draper() if slug == 'draper' else deep_content_riverton() if slug == 'riverton' else deep_content_sandy() if slug == 'sandy' else deep_content_west_jordan() if slug == 'west-jordan' else deep_content_cottonwood_heights() if slug == 'cottonwood-heights' else deep_content_herriman() if slug == 'herriman' else deep_content_salt_lake_city() if slug == 'salt-lake-city' else deep_content_south_jordan() if slug == 'south-jordan' else deep_content_bountiful() if slug == 'bountiful' else deep_content_section(name, slug, county)}<!-- PROCESS -->
<!-- MID-PAGE CTA 2 -->
<section style="padding-top:8px; padding-bottom:8px;">
  <div class="container">
    <div class="inline-cta reveal" style="background:var(--card); border:1px solid var(--border);">
      <div>
        <h3>{cta2_for(name, slug, index)[0]}</h3>
        <p>{cta2_for(name, slug, index)[1]}</p>
      </div>
      <div style="display:flex; gap:12px; flex-wrap:wrap;">
        <a href="/index.html#plans" class="btn btn-light">SEE PLANS &amp; PRICING</a>
        <a href="#contact" class="btn btn-primary">GET FREE ESTIMATE</a>
      </div>
    </div>
  </div>
</section>

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
      <div class="light-card static"><div class="icon-circle">{HAMMER_SVG}</div><h3 style="margin-top:16px; font-size:18px;">1,100+ Projects</h3><p style="font-size:14px; color:var(--muted-foreground); margin-top:8px;">20 years building across Utah.</p></div>
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
    path = f"/locations/{slug}.html"
    crumbs = [("Home", "/index.html"), ("Service Areas", "/index.html#areas"), (name, "")]
    json_ld = [local_business_jsonld(), breadcrumb_jsonld(crumbs), faq_jsonld(faq_pairs)]
    _register(path, changefreq="monthly", priority="0.8")
    return page_shell(title, desc, body, path, json_ld=json_ld)


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
            "excerpt": "A realistic look at what drives ADU pricing across Salt Lake, Utah, Davis and Summit counties. From garage conversions to detached cottages.",
            "img": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?q=80&w=1200&auto=format&fit=crop",
        },
        {
            "slug": "adu-permits-utah-what-to-know",
            "title": "ADU Permits in Utah: What Every Homeowner Should Know Before Building",
            "cat": "Permitting",
            "excerpt": "Zoning, setbacks, utility hookups and inspections. What actually happens between your first estimate and your first tenant.",
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

    _register("/blog/index.html", changefreq="weekly", priority="0.7")
    html = page_shell(
        "The ADU Blog | Pro-Worx ADU",
        "Guides on ADU pricing, permitting and planning for Utah homeowners, from the Pro-Worx ADU team.",
        body,
        "/blog/index.html",
        json_ld=[breadcrumb_jsonld([("Home", "/index.html"), ("Blog", "")])],
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
      <p>Accessory Dwelling Units have become one of the most popular ways for Utah homeowners to add living space, house family or generate rental income. But the first question everyone asks is the same: what does it actually cost?</p>
      <h2>The short answer</h2>
      <p>Across Salt Lake, Utah, Davis and Summit counties, Pro-Worx ADU pricing typically runs $100K&ndash;$200K for a garage or basement conversion and $200K&ndash;$300K for a full detached, ground-up build. Where your project lands in that range depends mainly on three things: the structure you're starting from, the size of the finished unit, and your lot's utility access.</p>
      <h2>What drives the price up or down</h2>
      <p>A garage or basement conversion is almost always the most affordable path, since the foundation, framing and roof already exist. The work is mostly interior build-out, plumbing and electrical. A detached, ground-up ADU costs more because it includes excavation, foundation, framing and a full exterior envelope, but it also offers the most privacy and flexibility for renters or family members.</p>
      <p>Utility hookups are the other major swing factor. If your existing service panel and sewer line have capacity for a second unit, costs stay predictable. If they don't, expect an additional line item for upgrades. Something we flag clearly during your free estimate, never after signing.</p>
      <h2>Why fixed pricing matters</h2>
      <p>Every Pro-Worx ADU plan tier is a fixed price once we've walked your property, not a rough estimate that grows during construction. That's the same transparent-pricing standard we've applied to over 1,100 projects across Utah in 20 years.</p>
      <p>Ready to see what your specific lot would cost? <a href="/index.html#contact" class="link-arrow">Get a free ADU estimate &rarr;</a></p>
    </div>
  </div>
</section>

{contact_section()}"""

    _register("/blog/how-much-does-an-adu-cost-in-utah.html", changefreq="monthly", priority="0.6")
    post_html = page_shell(
        "How Much Does an ADU Cost in Utah? | Pro-Worx ADU",
        "A realistic breakdown of Accessory Dwelling Unit pricing across Salt Lake, Utah, Davis and Summit counties.",
        post_body,
        "/blog/how-much-does-an-adu-cost-in-utah.html",
        json_ld=[breadcrumb_jsonld([("Home", "/index.html"), ("Blog", "/blog/index.html"), ("Pricing", "")])],
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
      <p>{p['excerpt']} We're finishing this guide. Check back soon, or <a href="/index.html#contact" class="link-arrow">get a free estimate &rarr;</a> in the meantime.</p>
    </div>
  </div>
</section>

{contact_section()}"""
        _register(f"/blog/{p['slug']}.html", changefreq="monthly", priority="0.5")
        placeholder_html = page_shell(
            f"{p['title']} | Pro-Worx ADU",
            p['excerpt'].replace(' - ', '-'),
            placeholder_body,
            f"/blog/{p['slug']}.html",
            json_ld=[breadcrumb_jsonld([("Home", "/index.html"), ("Blog", "/blog/index.html"), (p['cat'], "")])],
        )
        with open(os.path.join(ROOT, 'blog', f"{p['slug']}.html"), 'w') as f:
            f.write(placeholder_html)

    print("Built blog index + 3 posts")


def build_law_page():
    body = """<div class="container">
  <div class="breadcrumb">
    <a href="/index.html">Home</a><span>/</span>
    <span class="current">2026 ADU Law Changes</span>
  </div>
</div>

<section style="padding-top:24px;">
  <div class="container">
    <div class="blog-post-body">
      <p class="eyebrow">UTAH LAW &middot; SB284</p>
      <h1 style="font-size:36px; margin-bottom:12px;">Utah's New Detached ADU Law: What Changes on October 1, 2026</h1>
      <p class="post-meta">Pro-Worx ADU Team &middot; Utah ADU Guides</p>

      <p>Starting <strong>October 1, 2026</strong>, a new state law. Senate Bill 284 (SB284). Changes how Utah cities are allowed to regulate detached backyard ADUs. If you were told "no" on a detached ADU by your city a few years ago, or you've just never checked, this is worth a fresh look.</p>

      <h2>What was true before SB284</h2>
      <p>Many Utah cities historically only permitted <em>internal</em> ADUs. A basement apartment or an addition attached to the existing home. While prohibiting standalone, detached backyard units outright, or requiring a discretionary conditional-use permit that made approval unpredictable.</p>

      <h2>What SB284 requires, starting October 1, 2026</h2>
      <p>Cities with a population of 5,000 or more must now allow at least one detached ADU on qualifying single-family lots. The core provisions reported so far include:</p>
      <ul>
        <li><strong>Lot size:</strong> Detached ADUs must be permitted on parcels of roughly 11,000 square feet or larger with an existing single-family home. Many cities also allow them on smaller lots, at their discretion.</li>
        <li><strong>One ADU per lot:</strong> A property gets one ADU. Either internal or detached, not both.</li>
        <li><strong>No conditional-use permits:</strong> Cities can no longer require a discretionary conditional-use review just to build a qualifying detached ADU.</li>
        <li><strong>Size caps limited:</strong> Cities cannot set arbitrary maximum sizes, though they may cap a detached ADU at the size of the primary home.</li>
        <li><strong>Parking:</strong> Up to two on-site parking spaces can be required for detached ADUs of 650 square feet or larger.</li>
        <li><strong>Local control remains on the details:</strong> Cities still set their own setbacks, height limits, and owner-occupancy requirements, and must meet standard building codes.</li>
      </ul>

      <h2>Cities are still finalizing their local ordinances</h2>
      <p>SB284 sets the floor, not the final word. Individual cities are amending their own zoning codes to comply by the October 1 deadline, and the details vary. A few examples from public reporting:</p>
      <ul>
        <li><strong>Lehi</strong> already allowed detached ADUs on lots of 14,520+ sq ft with a 1,300 sq ft size cap, and has added a 6-foot setback from the primary home plus an owner-occupancy requirement to align with SB284. City staff estimate this could make roughly 20% more properties newly eligible.</li>
        <li><strong>Orem</strong>, which previously prohibited detached ADUs entirely, is proposing rules that restrict them from front yards and prohibit short-term rental use.</li>
        <li><strong>Provo</strong> has proposed capping all accessory structures at 40% of total parcel area and has published maps showing which neighborhoods gain new eligibility.</li>
      </ul>
      <p>Because every city's final ordinance can differ on setbacks, height, and owner-occupancy rules, the only way to know exactly what your property qualifies for is to check with your specific city's building department. Which is exactly what we do for you as part of every free estimate.</p>

      <h2>What this means if you were told no before</h2>
      <p>If a detached backyard ADU wasn't an option on your lot in the past, SB284 is a real reason to check again. Between the new statewide floor and each city's updated local ordinance, a meaningful number of Utah properties are newly eligible for a detached unit as of October 1, 2026.</p>

      <p>Not sure where your property stands? <a href="/index.html#contact" class="link-arrow">Get a free ADU estimate &rarr;</a> and we'll walk you through exactly what's possible under your city's updated rules.</p>

      <p style="font-size:13px; color:var(--muted-foreground); margin-top:32px;">This page summarizes public reporting on SB284 as of September 2026 for general information. It isn't legal advice, and every city's final ordinance may differ in its specifics. Confirm current requirements with your city's building department or with us before making decisions based on this page.</p>
    </div>
  </div>
</section>

""" + contact_section()

    _register("/adu-rules-2026.html", changefreq="monthly", priority="0.8")
    html = page_shell(
        "Utah's New ADU Law: SB284 Explained (Effective October 1, 2026) | Pro-Worx ADU",
        "What Utah's SB284 detached-ADU law changes on October 1, 2026. Lot size rules, parking, permitting, and how it affects Utah homeowners.",
        body,
        "/adu-rules-2026.html",
        json_ld=[breadcrumb_jsonld([("Home", "/index.html"), ("2026 ADU Law Changes", "")])],
    )
    with open(os.path.join(ROOT, 'adu-rules-2026.html'), 'w') as f:
        f.write(html)
    print("Built adu-rules-2026.html")


def build_sitemap_and_robots():
    _register("/index.html", changefreq="weekly", priority="1.0")

    urls = ""
    for path, changefreq, priority in SITEMAP_ENTRIES:
        urls += f"""  <url>
    <loc>{BASE_URL}{path}</loc>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>
"""
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}</urlset>
"""
    with open(os.path.join(ROOT, 'sitemap.xml'), 'w') as f:
        f.write(sitemap)

    robots = f"""User-agent: *
Allow: /

Sitemap: {BASE_URL}/sitemap.xml
"""
    with open(os.path.join(ROOT, 'robots.txt'), 'w') as f:
        f.write(robots)

    print(f"Built sitemap.xml ({len(SITEMAP_ENTRIES)} URLs) + robots.txt")


if __name__ == '__main__':
    build_locations()
    build_blog()
    build_law_page()
    build_sitemap_and_robots()
