# SEO Resources

All URLs verified live 2026-07-02. Google Search Central docs are the primary source of truth; courses/guides are the conceptual on-ramp.

## Knowledge

### Official Google docs (source of truth)
- [Google SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)
  The canonical "start here" doc (last updated 2025-12). Use for: fundamentals — titles, snippets, site organization, images. **Essential.**
- [How Google Search works (in-depth)](https://developers.google.com/search/docs/fundamentals/how-search-works)
  The three stages: crawling → indexing → serving, and why pages fail at each. Use for: the conceptual backbone of every technical-SEO lesson. **Essential.**
- [Get started with Google Search Console](https://developers.google.com/search/docs/monitor-debug/search-console-start)
  Verify the site, submit a sitemap, inspect URLs, monitor queries. Use for: all measurement — the first practical action once MathFlow is live. **Essential.**
- [Localized versions of your page (hreflang)](https://developers.google.com/search/docs/specialty/international/localized-versions)
  hreflang via HTML tags/headers/sitemap, bidirectional requirement, `x-default`. Use for: MathFlow's EN/pt-BR/es localization. **Essential.**
- [Intro to structured data](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data)
  Why JSON-LD, schema.org vocabulary, Rich Results Test. Use for: structured-data lessons.
- [Software App structured data](https://developers.google.com/search/docs/appearance/structured-data/software-app)
  `SoftwareApplication`/`WebApplication` markup — exactly what a free web tool should emit (price can be 0). Use for: MathFlow's JSON-LD.
- [Sitemaps overview](https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview)
  When a sitemap matters (and when it doesn't). Use for: building MathFlow's sitemap (also one of the 3 hreflang methods).
- [robots.txt introduction](https://developers.google.com/search/docs/crawling-indexing/robots/intro)
  Manages crawler traffic; does NOT hide pages (that's `noindex`). Use for: robots.txt + noindex decisions on login/admin pages.

### Reference specs
- [schema.org: WebApplication](https://schema.org/WebApplication)
  Full property list (`applicationCategory`, `featureList`, `screenshot`, …). Companion to the Google Software App doc.

### Courses & guides
- [Ahrefs SEO Course for Beginners](https://ahrefs.com/academy/seo-training-course)
  Free, no sign-up, ~2h of video across 5 modules (basics, keyword research, on-page, links, technical). Use for: the conceptual on-ramp; pairs with Google docs. Follow-up: [Ahrefs Technical SEO Course](https://ahrefs.com/academy/technical-seo-course). **Essential.**
- [Moz Beginner's Guide to SEO](https://moz.com/beginners-guide-to-seo)
  Classic 7-chapter guide; overlaps heavily with the Ahrefs course — pick one. Optional.

### Tools
- [Google Keyword Planner](https://ads.google.com/home/tools/keyword-planner/)
  Google's own volume/idea data; needs a free Ads account, no spend. Use for: checking PT-BR + ES + EN query volume ("converter equação word mathml", "convertir ecuación word a mathml", "omml to mathml").
- [Ahrefs Free Keyword Generator](https://ahrefs.com/keyword-generator)
  No-account keyword ideas + difficulty. Use for: quick checks on low-volume niche terms. Optional.

### ASP.NET Core specific
- [SeoTags library](https://mjebrahimi.github.io/SeoTags/) ([repo](https://github.com/mjebrahimi/SeoTags))
  NuGet package that generates meta description/canonical/OG/Twitter/JSON-LD tags. Optional — hand-written tags in `_Layout.cshtml` per the Google docs are equally valid; check repo activity before adopting.

## Wisdom (Communities)

- [Google Search Central Help Community](https://support.google.com/webmasters/community)
  Google's official forum, monitored by Product Experts. Use for: "why isn't my page indexed" questions with specifics.
- [r/TechSEO](https://www.reddit.com/r/TechSEO/)
  ~35–40k members, developer-flavored, high signal-to-noise (Ahrefs' Patrick Stox is active). Use for: rendering, markup, server-config questions. The larger [r/SEO](https://www.reddit.com/r/SEO/) is noisier — general questions only.

## Gaps
- No good resource found for "SEO for niche web tools/utilities" specifically — the niche is blog spam. Strategy questions (what pages to build around a converter tool) will be reasoned from first principles + community feedback.
- web.dev has no dedicated SEO course (its Learn series is performance/HTML).
