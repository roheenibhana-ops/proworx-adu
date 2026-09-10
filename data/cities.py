CITIES = [
    # (name, slug, county). Matches the real Pro-Worx Construction site's
    # service-area taxonomy (bright-airy-home-build/src/data/locations.ts),
    # plus Provo added per Roh's request.
    ("Alpine", "alpine", "Utah"),
    ("Highland", "highland", "Utah"),
    ("Lehi", "lehi", "Utah"),
    ("Lindon", "lindon", "Utah"),
    ("Mapleton", "mapleton", "Utah"),
    ("Provo", "provo", "Utah"),
    ("Spanish Fork", "spanish-fork", "Utah"),
    ("Vineyard", "vineyard", "Utah"),
    ("Bluffdale", "bluffdale", "Salt Lake"),
    ("Cottonwood Heights", "cottonwood-heights", "Salt Lake"),
    ("Draper", "draper", "Salt Lake"),
    ("Herriman", "herriman", "Salt Lake"),
    ("Riverton", "riverton", "Salt Lake"),
    ("Salt Lake City", "salt-lake-city", "Salt Lake"),
    ("Sandy", "sandy", "Salt Lake"),
    ("South Jordan", "south-jordan", "Salt Lake"),
    ("West Jordan", "west-jordan", "Salt Lake"),
    ("Bountiful", "bountiful", "Davis"),
    ("Heber City", "heber-city", "Summit"),
    ("Park City", "park-city", "Summit"),
]

# One genuinely distinct local-angle paragraph per city, plus a distinct
# "what to watch for" note tied to SB284 (Utah's Oct 1, 2026 detached-ADU
# law). These describe real, verifiable geographic/zoning *patterns* for
# each area rather than asserting exact ordinance numbers we haven't
# confirmed with each city. Lehi and Provo include specifics that were
# confirmed via reporting (see /adu-rules-2026.html for sourcing).
LOCAL_FOCUS = {
    "alpine": (
        "Alpine's lots skew large and semi-rural, with several foothill "
        "and equestrian-zoned subdivisions carrying their own architectural "
        "covenants on top of city code.",
        "Most Alpine lots comfortably clear SB284's 11,000-sq-ft detached-ADU "
        "threshold. The bigger question is usually HOA design review, not "
        "lot size."
    ),
    "highland": (
        "Highland's newer master-planned neighborhoods tend to have larger, "
        "more uniform lots than older Utah County cities, and many families "
        "here are looking at an ADU for multigenerational living rather "
        "than a rental.",
        "Because Highland's HOAs often pre-date SB284, expect city zoning "
        "and your HOA's covenants to both weigh in on setbacks and exterior "
        "finish."
    ),
    "lehi": (
        "Lehi already allowed detached ADUs before the statewide law "
        "changed. The city's existing rule set a 14,520-sq-ft minimum lot "
        "and a 1,300-sq-ft size cap, and Lehi's council has since added "
        "6-foot setbacks from the primary home and an owner-occupancy "
        "requirement to bring its ordinance in line with SB284.",
        "City staff estimate the update could make roughly 20% more Lehi "
        "properties newly eligible for a detached ADU. Worth a fresh look "
        "even if you were told no a few years ago."
    ),
    "lindon": (
        "Lindon mixes older agricultural-heritage lots. Often larger than "
        "typical suburban parcels. With newer infill development, which "
        "means eligibility can vary block to block more than in a uniformly "
        "platted city.",
        "Older, larger Lindon lots are strong SB284 candidates; newer, "
        "tighter infill lots are more likely to fall under the 11,000-sq-ft "
        "line and need an internal ADU instead."
    ),
    "mapleton": (
        "Mapleton's bench-and-foothill lots are among the largest in Utah "
        "County, with some properties on well or septic systems rather than "
        "full city utilities.",
        "Lot size usually isn't the constraint in Mapleton. Utility "
        "capacity and foothill drainage engineering are the details worth "
        "confirming early."
    ),
    "provo": (
        "Provo's ADU market is unusually driven by BYU's student-rental "
        "demand, and the city is still finalizing its SB284 compliance "
        "ordinance. A draft proposal would cap all accessory structures at "
        "40% of total parcel area, with published maps showing which "
        "neighborhoods gain new eligibility.",
        "Provo's east-bench neighborhoods generally have larger lots that "
        "clear the 11,000-sq-ft threshold; older, smaller downtown-adjacent "
        "lots near campus are more likely to need an internal conversion."
    ),
    "spanish-fork": (
        "Spanish Fork has some of the more affordable land in Utah County, "
        "and we're seeing steady interest in ADUs both for rental income "
        "and for housing extended family as the city grows.",
        "A mix of older grid-platted lots and newer subdivisions means "
        "SB284 eligibility should be checked lot-by-lot rather than assumed "
        "city-wide."
    ),
    "vineyard": (
        "Vineyard is Utah's newest planned city, built almost entirely on "
        "former Geneva Steel land. Nearly every lot is recent construction "
        "under a single HOA-governed design standard.",
        "Vineyard's uniform, modern lot sizing makes SB284 eligibility "
        "unusually easy to determine. The HOA's architectural guidelines "
        "are typically the bigger factor in what an ADU can look like."
    ),
    "bluffdale": (
        "Bluffdale still has a rural-transition feel in parts of the city, "
        "with larger lots than its denser Salt Lake County neighbors and "
        "room for detached construction without tight side-yard clearances.",
        "Bluffdale's larger average lot size makes it one of the stronger "
        "SB284 candidates in Salt Lake County."
    ),
    "cottonwood-heights": (
        "Cottonwood Heights sits right up against the canyons, so snow "
        "load, slope grading and drainage engineering matter more here than "
        "in flatter valley cities, and HOA aesthetic standards run higher "
        "than average.",
        "Foothill lots here can be larger than they look on a plat map, "
        "but canyon-adjacent parcels sometimes carry additional geotechnical "
        "review before a detached ADU gets approved."
    ),
    "draper": (
        "Draper's hillside neighborhoods around Suncrest and Corner Canyon "
        "bring steep-slope lots into play, which usually means more "
        "engineering for grading and drainage than a flat-lot build "
        "elsewhere in the valley.",
        "Draper's HOA-governed hillside communities often have stricter "
        "architectural review than city code alone. Plan for both "
        "approvals, not just one."
    ),
    "herriman": (
        "Herriman is one of the fastest-growing cities in the valley, with "
        "master-planned communities built on larger modern lots. A good "
        "match for SB284's detached-ADU rules.",
        "New-build Herriman subdivisions are generally well above the "
        "11,000-sq-ft threshold, though individual HOAs may still restrict "
        "exterior style or placement."
    ),
    "riverton": (
        "Riverton has a mix of older agricultural-heritage lots and newer "
        "growth, so lot sizes vary more than in a purely master-planned "
        "city. Some of the older parcels are genuinely large.",
        "Check your specific lot rather than assuming. Riverton's range of "
        "lot sizes means SB284 eligibility isn't uniform across the city."
    ),
    "salt-lake-city": (
        "Salt Lake City's older, denser neighborhoods often sit on lots "
        "well under SB284's 11,000-sq-ft detached-ADU threshold, which "
        "means an internal ADU. A basement or attic conversion. Is the "
        "realistic path for many downtown-adjacent homeowners, even as "
        "rental demand near downtown and the University stays strong.",
        "If your lot doesn't clear the detached-ADU threshold, a basement "
        "or garage conversion is usually still fully permittable under the "
        "city's long-standing internal-ADU rules."
    ),
    "sandy": (
        "Sandy's established mid-size lots are common across the city, and "
        "several newer developments carry HOA design guidelines on top of "
        "city zoning. Plus foothill lots near the mountains that call for "
        "proper snow-load design.",
        "Sandy has had internal-ADU rules for years, so the main change "
        "from SB284 is opening up detached backyard units on qualifying "
        "lots."
    ),
    "south-jordan": (
        "South Jordan's Daybreak community runs under its own detailed HOA "
        "design guidelines that can be more restrictive than city code, "
        "while older South Jordan neighborhoods follow standard city "
        "zoning.",
        "If you're in Daybreak, budget time for HOA architectural review in "
        "addition to the city's SB284-compliant permitting process."
    ),
    "west-jordan": (
        "West Jordan has some of the more varied lot sizes in Salt Lake "
        "County, with older neighborhoods on larger parcels seeing strong "
        "interest in ADUs for multigenerational living and rental income.",
        "Many of West Jordan's older, larger-lot neighborhoods clear the "
        "SB284 threshold comfortably. Newer, tighter subdivisions are more "
        "likely to need an internal ADU."
    ),
    "bountiful": (
        "Bountiful's bench and hillside neighborhoods along the Wasatch "
        "Front often sit on older, larger lots than newer Davis County "
        "development, with a mix of historic and mid-century housing stock.",
        "Bountiful's established bench lots are frequently large enough for "
        "a detached ADU under SB284. Older utility connections are the "
        "detail worth checking early."
    ),
    "heber-city": (
        "Heber City is one of the fastest-growing cities on the Wasatch "
        "Back, with larger rural-residential lots common and strong "
        "interest in ADUs tied to nearby Park City's tourism and workforce "
        "housing needs.",
        "Heber's larger rural-residential lots are generally well-suited to "
        "SB284's detached-ADU rules, though well/septic capacity should be "
        "confirmed on outlying parcels."
    ),
    "park-city": (
        "Park City is its own case: strict historic-district and design-"
        "review overlays apply in Old Town, short-term-rental rules can "
        "limit how an ADU is used, and lot sizes swing from tiny Old Town "
        "parcels to large lots in outlying neighborhoods.",
        "Park City's local overlays and nightly-rental restrictions matter "
        "as much as SB284 itself. Confirm both before assuming a detached "
        "ADU is rentable the way you're picturing it."
    ),
}

# Real neighborhood names, confirmed via public real-estate/city sources,
# for cities where we've done the research. Cities not listed here don't
# get invented neighborhood names. LOCAL_FOCUS above still gives each of
# them a genuinely distinct angle without fabricating specifics.
NEIGHBORHOODS = {
    "salt-lake-city": ["Sugar House", "The Avenues", "Rose Park", "Sunnyside", "Highland Park"],
    "sandy": ["Hidden Valley", "Willow Creek", "Granite", "Granite Oaks"],
    "draper": ["Suncrest", "Corner Canyon", "Hidden Valley"],
    "bountiful": ["South Bountiful", "East Bountiful", "the Bountiful Bench"],
    "park-city": ["Old Town", "Prospector", "Thaynes Canyon", "the Deer Valley area"],
    "lehi": ["Traverse Mountain", "Thanksgiving Point area"],
    "provo": ["East Bench", "Edgemont", "the BYU-adjacent grid"],
}

# Cities where hillside/canyon terrain makes soils/geotechnical review a
# real, recurring factor. Not universal, so we don't apply this section
# to flat-lot cities where it wouldn't be an honest differentiator.
HILLSIDE_TERRAIN = {
    "draper", "cottonwood-heights", "alpine", "park-city", "bountiful",
    "heber-city", "highland",
}

# Cities where master-planned HOA communities are common enough that HOA
# coordination is a genuine, recurring part of the ADU process there.
HOA_HEAVY = {
    "highland", "vineyard", "south-jordan", "draper", "herriman",
    "cottonwood-heights", "alpine",
}

# Cities where well/septic capacity is a genuine, recurring factor for
# detached ADU utility hookups (outlying/semi-rural lots).
WELL_SEPTIC = {"mapleton", "heber-city", "alpine"}

# A distinct headline + lede for the deep-content section on each city
# page, so the section reads as "this city's specific issue" rather than
# a name-swapped template. Mirrors how the main site's Alpine page leads
# with "grading, permits and HOA review" instead of a generic ADU pitch.
DEEP_HEADLINES = {
    "alpine": (
        "Why Does an ADU in Alpine Mean Dealing With Grading, Soils and HOA Review?",
        "Alpine's large, sloped lots make an ADU foundation a different conversation than it is a few miles away in flatter Utah County cities."
    ),
    "highland": (
        "Why HOA Design Review Matters as Much as City Permits in Highland",
        "Highland's newer master-planned subdivisions often have HOA architectural standards that predate SB284, and they don't disappear just because the city says yes."
    ),
    "lehi": (
        "Lehi Already Allowed Detached ADUs. Here's What Changed on October 1, 2026",
        "Lehi updated its existing detached-ADU ordinance to comply with SB284, and city staff estimate roughly 20% more properties are now newly eligible."
    ),
    "lindon": (
        "Why Lot Size Varies More in Lindon Than in a Uniformly Platted City",
        "Lindon's mix of older, larger agricultural-heritage lots and newer infill means SB284 eligibility has to be checked lot-by-lot, not assumed citywide."
    ),
    "mapleton": (
        "The Real Constraint on a Mapleton ADU Usually Isn't Lot Size. It's Utilities",
        "Mapleton's bench-and-foothill lots are large enough for most detached ADUs, but well and septic capacity needs to be confirmed before anything else."
    ),
    "provo": (
        "Provo Is Still Finalizing Its SB284 Ordinance. Here's Where Things Stand",
        "A draft proposal would cap accessory structures at 40% of parcel area, and eligibility splits sharply between Provo's east bench and its smaller, campus-adjacent lots."
    ),
    "spanish-fork": (
        "Why Spanish Fork's Mixed Lot Sizes Mean Checking Your Address, Not Assuming",
        "A mix of older grid-platted lots and newer subdivisions means SB284 eligibility varies more within Spanish Fork than in a single-era-built city."
    ),
    "vineyard": (
        "Vineyard's Uniform New-Build Lots Make SB284 Eligibility the Easy Part",
        "Nearly every lot in Vineyard sits under the same HOA design standard. The real question is what the HOA will approve, not whether the city allows it."
    ),
    "bluffdale": (
        "Bluffdale's Larger, Rural-Transition Lots Are Ahead of the SB284 Curve",
        "Bluffdale carries a rural-transition feel with larger average lots than its denser Salt Lake County neighbors, making it one of the stronger SB284 candidates in the county."
    ),
    "cottonwood-heights": (
        "Why Canyon-Adjacent Lots in Cottonwood Heights Need a Different Engineering Conversation",
        "Snow load, slope grading and drainage matter more here than in flatter valley cities, and HOA aesthetic standards run higher than average."
    ),
    "draper": (
        "Why Draper's Hillside Neighborhoods Change the ADU Math",
        "Suncrest and Corner Canyon's steep-slope lots mean more grading and drainage engineering than a flat-lot build elsewhere in the valley, and HOA review runs on top of city permitting."
    ),
    "herriman": (
        "Herriman's New-Build Subdivisions Are a Strong Match for SB284",
        "Master-planned communities on larger modern lots mean most new Herriman subdivisions clear the detached-ADU threshold comfortably."
    ),
    "riverton": (
        "Riverton's Lot Sizes Vary Enough That You Should Check Yours Specifically",
        "A mix of older agricultural-heritage lots and newer growth means SB284 eligibility isn't uniform across the city. Some of the older parcels are genuinely large."
    ),
    "salt-lake-city": (
        "Why Most Salt Lake City ADUs Are Basement Conversions, Not Backyard Cottages",
        "Older, denser SLC lots often sit under SB284's 11,000-sq-ft detached-ADU threshold. For most homeowners here, an internal ADU is the realistic path, not a zoning failure."
    ),
    "sandy": (
        "What Sandy Homeowners Need to Know About Foothill Lots and HOA Layers",
        "Sandy's established mid-size lots are common, but several newer developments carry HOA design guidelines on top of city zoning, and foothill lots need proper snow-load design."
    ),
    "south-jordan": (
        "Daybreak's HOA Design Guidelines Can Be Stricter Than South Jordan's Own Code",
        "If you're in Daybreak, budget time for HOA architectural review in addition to the city's SB284-compliant permitting process. Older South Jordan neighborhoods follow standard city zoning instead."
    ),
    "west-jordan": (
        "West Jordan's Older, Larger-Lot Neighborhoods Are Where SB284 Opens the Most Doors",
        "West Jordan has some of the more varied lot sizes in Salt Lake County. Older neighborhoods on larger parcels clear the threshold; newer, tighter subdivisions are more likely to need an internal ADU."
    ),
    "bountiful": (
        "Why Bountiful's Bench Lots Are Well-Suited to a Detached ADU",
        "Older, larger lots along the Wasatch Front bench frequently clear the SB284 threshold. Aging utility connections are the detail worth checking early."
    ),
    "heber-city": (
        "Heber City's Rural-Residential Lots Meet Growing Wasatch Back Demand",
        "Larger lots are generally well-suited to SB284's detached-ADU rules, but well and septic capacity should be confirmed on outlying parcels."
    ),
    "park-city": (
        "Why Park City's Overlays Matter as Much as SB284 Itself",
        "Historic-district design review in Old Town and short-term-rental restrictions can limit how a Park City ADU gets used, regardless of what the state law allows."
    ),
}

TESTIMONIALS = [
    {
        "quote": "Pro-Worx converted our garage into a rental unit in under 5 weeks. Permits, design, everything. Handled.",
        "author": "Sarah M.",
        "role": "Sandy, UT",
    },
    {
        "quote": "We now have my mother-in-law living comfortably in her own backyard cottage. On time, on budget, exactly as quoted.",
        "author": "David R.",
        "role": "Bountiful, UT",
    },
    {
        "quote": "The fixed pricing meant no surprises. Our ADU is now generating steady rental income every month.",
        "author": "Jennifer K.",
        "role": "Herriman, UT",
    },
]

FAQS = [
    ("Can I legally build an ADU on my property in {city}?",
     "Most single-family lots in {city} qualify for an ADU, but rules vary by zoning district and, as of October 1, 2026, by the city's updated SB284 detached-ADU ordinance. We handle a full zoning and permit review as part of every free estimate, so you'll know exactly what's possible before committing to anything."),
    ("How much does an ADU cost in {city}?",
     "Typical investment runs $100K–$200K for a garage or basement conversion and $200K–$300K for a full detached build. Final pricing depends on your lot, utility access and finish level. We'll give you an exact number after a site walk."),
    ("How long does an ADU build take in {city}?",
     "Garage and basement conversions typically take 3–5 weeks. Detached, ground-up ADUs run longer once permitting and foundation work are factored in. We'll give you a realistic timeline before you sign anything."),
    ("Will an ADU increase my property value in {county} County?",
     "ADUs are one of the highest-return additions available to Utah homeowners, both through added square footage and rental income potential. Many owners recoup their investment through rent within a few years."),
    ("Do you handle permits and inspections with the {city} building department?",
     "Yes. Permitting, plan review and inspection scheduling are included in every ADU plan tier. You won't need to deal with the city directly at any point in the process."),
    ("Can I rent out my ADU in {city}?",
     "In most cases, yes. Most cities in {county} County allow long-term rental of a permitted ADU, though a handful of cities and HOAs restrict short-term/nightly rentals. We'll confirm exactly how {city} treats rentals as part of your free estimate."),
    ("Does an ADU in {city} need its own egress window?",
     "Yes. Any bedroom needs a code-compliant egress window or door for safety, standard on every basement conversion and detached build we do in {city}. It's factored into your quote from day one."),
    ("Is financing available for an ADU project in {city}?",
     "Many {city} homeowners finance an ADU through a home equity loan, HELOC, cash-out refinance, or a renovation/construction loan. We're not a lender, but we can help you scope the project so you can have that conversation with real numbers."),
]
