# irfanismailm.com

Personal site for **Irfan Ismail M** (@irfanismailm) — personal notes on tech, facts
and social good. It's the *personal* corner; the video/production work lives at
**Irfan & Co** (irfanco.com). Static site (HTML/CSS/JS), no build step, hosted on GitHub Pages.

## Files
- `index.html` — the page
- `styles.css` — all styles
- `main.js` — mobile menu, scroll reveals, year
- `favicon.svg`, `favicon-16.png`, `favicon-32.png`, `apple-touch-icon.png`, `favicon.ico` — the signature "I" + coral underline
- `og-image.png` — social share preview (1200×630)
- `signature.svg` / `signature.png` — the logo lockup as an asset
- `site.webmanifest`, `robots.txt`, `sitemap.xml`
- `CNAME` — custom domain (irfanismailm.com)
- `.nojekyll` — tells GitHub Pages to serve files as-is

## Before you publish
1. **WhatsApp link** — in `index.html`, find `wa.me/971500000000` and replace the number
   with yours in international format (no `+`, spaces or dashes), e.g. `971501234567`.
2. Optional: tweak the hero copy, the "What I share" cards, or the status line.

## Deploy on GitHub Pages
1. Create a repo (e.g. `irfanismailm.github.io` for a user site, or any repo for a project site).
2. Upload **all files in this folder to the repo root** (keep them flat — don't nest them).
3. Repo → **Settings → Pages → Build and deployment → Source: Deploy from a branch**,
   pick `main` and `/ (root)`. Save.
4. Wait ~1 minute; your site appears at the URL shown on that Pages screen.

## Custom domain (irfanismailm.com)
1. The included `CNAME` file already sets the domain.
2. At your registrar, add DNS records:
   - Four **A** records for the apex `@` → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - One **CNAME** for `www` → `<your-username>.github.io`
3. In **Settings → Pages → Custom domain**, confirm `irfanismailm.com`, then tick **Enforce HTTPS**.

Pushing to the branch redeploys automatically.

## Credits
Brand icons from [Simple Icons](https://simpleicons.org) (CC0). Fonts: Bricolage Grotesque,
Hanken Grotesk, Space Mono, Kaushan Script (Google Fonts, OFL).
