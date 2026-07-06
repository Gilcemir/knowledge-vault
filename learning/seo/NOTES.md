# Teaching Notes — SEO workspace

## Mission interview (answered 2026-07-02)
- Goal: **both** tool discovery and transferable SEO skill, equally.
- Live at **https://omml2mathml.com/** (custom domain ✅ — Search Console lessons unblocked).
- Audience: **PT-BR and ES mainly**; site also supports EN. Repo confirms three locales: `SharedResources.resx` (EN default), `.pt-BR.resx`, `.es.resx`.
- Time budget: **30 minutes/week** — the binding constraint. Lesson ≤15 min + one tiny applied change (~15 min). One concept, one commit, per session.
- Prior knowledge: **zero SEO knowledge** (see learning-records/0001). Developer background is strong (.NET, built the site) — explain SEO concepts, not web tech.

## Baseline SEO audit (repo 2026-07-02, confirmed against live site same day)
Stack: ASP.NET Core Razor Pages (.NET 9), server-rendered ✅, localized EN/pt-BR/es, Bootstrap.

Live-site checks (curl, 2026-07-02):
- ❌ `https://omml2mathml.com/robots.txt` → **404**
- ❌ `https://omml2mathml.com/sitemap.xml` → **404**
- ⚠️ Homepage `<title>` renders as **"OMML2MathML - OMML2MathML"** — Index.cshtml sets `ViewData["Title"] = "OMML2MathML"` and the layout appends `- AppName`, duplicating the brand. Easy first fix, high visibility.
- ⚠️ `lang="pt"` served (culture-derived) — fine, but no hreflang siblings.

From repo (`_Layout.cshtml`, `wwwroot/`):
- ✅ `<html lang>` dynamic, ✅ title pattern, ✅ h1/h2 structure, ✅ viewport
- ❌ No `<meta name="description">`
- ❌ No canonical `<link>`
- ❌ No Open Graph / Twitter Card tags
- ❌ No hreflang alternate links despite 3 locales
- ❌ No structured data (JSON-LD `WebApplication` fits)
- ⚠️ Login/Register/Admin/Profile pages: noindex candidates

Each ❌/⚠️ = one future lesson + one small commit, ordered by impact:
1. ✅ Fix duplicated title + add meta description — DONE (live 2026-07-06, keyword-rich PT title + SciELO mention)
2. ✅ robots.txt — DONE (200; noindex on account/admin pages not yet verified)
3. ✅ Canonical URLs — DONE
4. ✅ hreflang — DONE (pt-BR root, es under /es/, x-default → root; **no EN variant** — /en/ 404s; confirm EN was deliberately dropped)
5. ✅ sitemap.xml (8 URLs) + Search Console verified + submitted — DONE (lesson 0002 complete 2026-07-06; pages indexed and ranking)
6. ✅ JSON-LD shipped (2 blocks live) — not yet validated; review in a future lesson
7. Keyword research: what do PT/ES searchers actually type? (Keyword Planner) ← NEXT

## Status after lesson 0002 (2026-07-06 — see learning-records/0002)
Technical foundation is DONE and live. Site is indexed and ranking. Gil implemented the entire audit himself, ahead of the lesson sequence — implement-first pattern confirmed again.
Next session (lesson 0003 candidates, demand side now):
- **Reading the Search Console Performance report** (impressions/clicks/CTR/position) — directly serves the mission's success criterion about PT/ES query impressions; data will have accumulated by next session.
- PT/ES keyword research (roadmap item 7), fed by the real queries from the Performance report.
- Smaller follow-ups: validate JSON-LD (Rich Results Test), confirm noindex on account/admin pages, confirm EN dropped intentionally.

## Indexing baseline (site: search by Gil, 2026-07-02)
`site:omml2mathml.com` returns **1 result: the homepage only**. `/converter` (the core page!), Contribuir, Privacy are NOT indexed. Duplicated title confirmed in the SERP; snippet is auto-generated from body text (mentions "SciELO Markup" — useful keyword signal: real users prepare Word docs for SciELO). Gil completed the Lesson 1 exercise ✅.
→ Lesson 2 = Search Console verification + URL Inspection of /converter to find out WHY it isn't indexed (no sitemap + weak internal linking are suspects, but inspect first, don't guess).

## Teaching preferences
- Absolute beginner in SEO: define every term at first use, expand every acronym.
- Keep lessons ≤15 min. One tangible win per session.
- **Implement-first learner** (2026-07-02): Gil chose to implement the audit fixes himself before proceeding to Lesson 2. Adapt: lessons become just-in-time deep-dives paired to whatever he's implementing next, plus review of what he shipped (check his commits in the MathFlow repo for evidence of understanding). Don't push Lesson 2's content until he starts Search Console work.
