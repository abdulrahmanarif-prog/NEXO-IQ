# NEXO — English site content

Source of truth for every English string on `index.html`, in page order. Edit here first, then mirror into the HTML (the site has no build step, so the copy is duplicated by hand).

---

## Metadata

| Field | Value |
| --- | --- |
| Page title | NEXO \| Engineering & Contracting Company in Baghdad, Iraq |
| Meta description | NEXO Engineering & Contracting delivers architectural and structural design, general contracting, and BIM training across Iraq. Based in Baghdad. |
| OG / Twitter title | NEXO \| Engineering & Contracting Company in Baghdad, Iraq |
| OG / Twitter description | Architectural and structural design, general contracting, and BIM training across Iraq. |
| OG site name | NEXO Engineering & Contracting |
| OG image alt | The NEXO mark — two gold axes crossing — beside the company name. |
| Canonical | https://nexo-iq.com/ |
| Locale | `en`, alternate `ar_IQ` |

---

## Header

**Logo alt:** NEXO Engineering & Contracting - شركة نكسو للهندسة والمقاولات
**Brand link label:** NEXO Engineering & Contracting — home
**Menu toggle label:** Open menu / Close menu

**Nav:** About · Divisions · Clients · Academy · **Get in touch** (gold button)

---

## Hero

**Eyebrow:** Baghdad · Iraq

**H1:**
> Vision meets
> *structural* execution

*(second line's "structural" is italic/emphasised)*

**Lede:**
> NEXO Engineering & Contracting designs, builds, and teaches — architectural and structural modelling, heavy civil contracting, and the technical training that keeps both standing.

**Buttons:** See the divisions → · Request a consultation

**Discipline code strip** (parallel, not sequential — do not reorder):

| Code | Label |
| --- | --- |
| A— | Architectural & structural design |
| C— | General contracting |
| T— | Training academy |

**Axis figure**
- SVG alt: The NEXO mark drawn as two crossing structural axes: design and execution meeting at a node.
- Axis labels: `DESIGN` (left) · `EXECUTION` (right)
- Caption: Fig. 01 — Two axes, one node

---

## About — `#about`

**Figure**
- Image alt: A NEXO project under construction in Baghdad — reinforced concrete frame and structural steel on site.
- Caption: Fig. 02 — On site, Baghdad

**Eyebrow:** Who we are

**H2:** Next-Generation Engineering eXcellence Organization

**Body:**
> Rooted in Baghdad, NEXO closes the gap between the model and the site. We bring BIM-grade technical modelling, advanced construction chemistry, and local workforce development under one practice — so what gets drawn is what gets built.

**Spec list**

| Term | Definition |
| --- | --- |
| Vision | To be Iraq's leading multidisciplinary engineering practice, setting the benchmark for architectural modelling, structural durability, and technical education. |
| Mission | Deliver turnkey civil contracting, architectural precision, and practical software training by pairing international engineering standards with strategic industrial partnerships. |
| Where we work | Commercial, hospitality, petroleum, and urban development projects across Iraq — from concept package to handover. |

---

## Divisions — `#divisions`

**Eyebrow:** Capabilities
**H2:** Three divisions, one practice
**Intro:** Each runs its own discipline and its own crew. Open one to see the scope of work.

### A—01 · Architectural & Structural Design
**Sub:** Concept packages and detailed calculations to international code.
**Scope of work**
- Architectural spatial planning & 3D visualisation
- Structural calculations & BIM modelling
- Civil layout optimisation
- Exterior facade & interior engineering

### C—02 · General Contracting & Construction
**Sub:** Turnkey execution for commercial, petroleum, hospitality, and urban work.
**Scope of work**
- High-rise structural construction
- Petroleum & industrial infrastructure
- MEP systems integration
- Structural rehabilitation & retrofitting

### T—03 · Training & Capacity Academy
**Sub:** Industry-standard software and site expertise for engineers across Iraq.
**Scope of work**
- BIM — Revit, ETABS, AutoCAD, Primavera P6
- Site supervision & HSE standards
- Concrete testing & chemical application
- Technical masterclasses & certification

---

## Network — `#network`

**Eyebrow:** Network
**H2:** Who we build with
**Intro:** Developers, energy operators, and the construction-chemistry suppliers behind the work.

### Clients

| Name | Category | Footer | Link | Logo alt |
| --- | --- | --- | --- | --- |
| Rixos Baghdad | Luxury hospitality & residences | Client · Visit ↗ | https://rixosbaghdadresidences.com/ | Rixos Baghdad Hotel & Residences - فندق وشقق ريكسوس بغداد |
| EBS Petroleum | Energy & industrial | Client · Visit ↗ | https://www.ebspetroleum.com/ | EBS Petroleum Company Limited |
| Millennium Tower | Ramlah urban developments | Client · Visit ↗ | https://ramlah.co/millennium | TOWERS MILLENNIUM by RAMLAH - ابراج ميلينيوم من رملة |
| Future City | Modon developments | Client · Visit ↗ | https://modoniq.com/ar/future-city/ | Modon Future City - مدن |

### Partners & suppliers

| Name | Category | Footer | Logo alt |
| --- | --- | --- | --- |
| Sika | Construction chemicals | Supplier · Building Trust | Sika |
| Fosroc | Constructive solutions | Supplier · Saint-Gobain | Fosroc Saint-Gobain |
| DCP | Don Construction Products | Supplier · Specialty chemicals | DCP - Don Construction Products |
| Zamzam Land | Development partner | Partner · Joint project | Zamzam Land |

---

## Academy — `#academy`

**Eyebrow:** NEXO Academy
**H2:** Learn it where it gets built
**Body:**
> Workshops in BIM, structural engineering, and construction management — taught by the engineers running our sites, on the software the industry actually uses.

**Button:** Enrol or ask a question →

---

## Contact — `#contact`

**Eyebrow:** Get in touch
**H2:** Start a project with us
**Body:**
> Tender documents, an engineering question, or a place on the next workshop — reach the Baghdad office directly.

| Term | Value |
| --- | --- |
| Office | Baghdad, Iraq |
| Email | info@nexo-iq.com |
| Phone | +964 771 819 6242 — *`tel:` link; also in the JSON-LD `telephone` field* |

**CTA:** Email the office → *(mailto link; there is no contact form — the previous one had no backend and collected nothing)*

---

## Footer — title block

| Key | Value |
| --- | --- |
| *(logo cell)* | NEXO Engineering & Contracting - شركة نكسو للهندسة والمقاولات |
| Office | Baghdad, IQ |
| Divisions | A / C / T |
| Practice | Engineering & Contracting |

**Footer nav:** About · Divisions · Clients · Contact
**Copyright:** © 2026 NEXO Engineering & Contracting Co.

---

## Copy rules

- Spelling is British-leaning: *modelling*, *optimisation*, *visualisation*, *enrol*, *organisation* — but the brand expansion keeps its US spelling, **Next-Generation Engineering eXcellence Organization**.
- Em dashes are spaced ` — `; the discipline codes use an em dash with no space (`A—`, `A—01`).
- Ampersands in prose, not "and", inside titles and list items.
- Arabic company names live only in `alt` attributes — keep both languages when editing those images.
- Claim no project counts, years in business, headcount, street address, or founding date. None are known.
