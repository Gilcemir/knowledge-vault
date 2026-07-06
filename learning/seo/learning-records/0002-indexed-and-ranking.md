# MathFlow is indexed and ranking — technical foundation complete

Gil reported (2026-07-06) that lesson 0002 is done: the site was verified in Google Search Console, the sitemap submitted, the missing pages indexed, and the site now **ranks** for its queries. Live checks the same day confirmed the shipped state goes well beyond the lesson scope — essentially the entire baseline audit from NOTES.md is resolved:

- ✅ `robots.txt` and `sitemap.xml` both return 200 (sitemap lists 8 URLs: pt-BR root + `/es/` variants of home, converter, contribute, privacy)
- ✅ Title fixed and keyword-rich: "Converta equações do Word para MathML — grátis e online - OMML2MathML"
- ✅ Meta description present, mentions SciELO Markup (the keyword signal spotted in lesson 1)
- ✅ Canonical link present
- ✅ hreflang: `pt-BR` (root), `es` (`/es/`), `x-default` → root
- ✅ Two JSON-LD blocks present

**Site structure decision (his own, not from a lesson):** root now serves pt-BR, Spanish lives under `/es/`, and there is no separate English URL (`/en/` → 404, no `hreflang="en"`). x-default points at the pt-BR root. Consistent with the PT-BR/ES priority audience, but the original mission text mentions EN — worth confirming whether EN was deliberately dropped.

**What this proves about understanding:** Gil can now execute the full crawl → index pipeline end-to-end (verify property, submit sitemap, inspect URLs, request indexing) and translate an audit checklist into shipped fixes independently. The implement-first pattern from NOTES.md held strongly — he outran the lesson sequence.

**Zone of proximal development moves to the demand side:** the technical/supply side is done. Next frontier is *what people actually search for and how the site performs against it* — Search Console Performance report (impressions, clicks, CTR, position) and PT/ES keyword research (roadmap item 7), plus validating the JSON-LD he shipped.
