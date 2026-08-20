# 🏛️ Technical Architecture & Design System Documentation
## Grupo Aylesva — Shopify Online Store 2.0 Theme

---

## 1. System Overview

The **Grupo Aylesva** platform is designed as an enterprise-grade e-commerce and corporate portal built natively on **Shopify Online Store 2.0**. It unifies multiple business verticals into a cohesive, high-performance web experience.

```text
┌─────────────────────────────────────────────────────────────┐
│                    Shopify OS 2.0 Core                      │
├──────────────────────────────┬──────────────────────────────┤
│    Gold & Ink Design System  │   Modular Section Engine     │
│   (Tokens, Typography, CSS)  │  (15+ Typed Liquid Sections) │
├──────────────────────────────┴──────────────────────────────┤
│               JSON Template Routing Engine                  │
│   (index.json, page.globalestates.json, page.direct.json…)  │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. "Gold & Ink" Design Tokens (`aylesva-corp-tokens.liquid`)

All design tokens are managed via CSS Custom Properties injected into `theme.liquid`:

| Token | Value | Purpose |
| :--- | :--- | :--- |
| `--ay-gold` | `#C5A47E` | Primary accent, interactive borders & badges |
| `--ay-gold-dark` | `#967448` | Hover states and deep metallic tones |
| `--ay-gold-text` | `#8C6839` | High-contrast accessible text gold |
| `--ay-ink-900` | `#020617` | Deep corporate background & headings |
| `--ay-ink-800` | `#0F172A` | Primary body typography |
| `--ay-stone` | `#F8F7F4` | Clean canvas background |
| `--ay-pad-x` | `clamp(20px, 4vw, 48px)` | Fluid horizontal container padding |
| `--ay-radius` | `8px` | Harmonious border radius across all cards |

### Typography Hierarchy
- **Headings & Display:** `Sora`, sans-serif (Geometric, high-end corporate tone).
- **Body & Editorial:** `Manrope`, sans-serif (Clean legibility at small & medium scales).
- **Technical Badges & Mono:** `JetBrains Mono` / monospace (Index counters, uppercase tags, metadata).

---

## 3. Section Engineering Registry

### `aylesva-home-hero-v3.liquid`
- **Purpose:** Interactive cinematic showcase with real-time service synchronization.
- **Key Features:**
  - Dynamic 4x Grand Spotlight Stage with continuous Ken Burns subtle zoom.
  - Interactive 6-service dock with animated SVG icons and live progress bars.
  - Mobile-first responsive hierarchy: The visual stage is loaded in the upper fold on mobile viewports.

### `aylesva-corp-cards.liquid`
- **Purpose:** High-end service and project showcases (*Global Estates, Direct, Lanza tu Marca*).
- **Key Features:**
  - Multi-image gallery support with modal window for architectural blueprints and project photography.
  - Conditional call-to-action routing: Seamlessly switches between gallery modals and direct landing page links.

### `aylesva-home-split.liquid`
- **Purpose:** Split 2-column commercial showcase for Marketplace and B2B/B2C dropshipping.
- **Key Features:**
  - Interactive 4-quadrant editorial photography gallery with hover lift and catalog badges.
  - Category chip filter pills with gold diamond bullet points.
  - Dual action buttons (Direct catalog exploration & E-commerce brand creation).

---

## 4. Performance & Optimization

1. **GPU Acceleration:** Heavy visual animations use `transform` and `opacity` with `will-change` properties to avoid browser reflows and achieve smooth 60 FPS.
2. **Native Lazy Loading:** All below-the-fold media tags use `loading="lazy"` and Shopify's `image_url` CDN filter with responsive width parameters (`320px`, `900px`, `1600px`).
3. **Zero Heavy JS Frameworks:** Built entirely in lightweight vanilla JavaScript (ES6+) with zero dependencies on jQuery or bloated animation libraries.
