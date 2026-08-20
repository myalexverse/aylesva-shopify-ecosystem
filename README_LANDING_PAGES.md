# Shopify Landing Pages: Fink, Care, and All Cities Global

This document contains the complete code and deployment instructions for the **Préstamos Fink**, **Aylesva Care**, and **All Cities Global** landing pages, developed as custom reusable Shopify sections. Share this guide with your USA team so they can easily recreate these pages on their own Shopify store.

---

## Table of Contents
1. [General Deployment Instructions](#general-deployment-instructions)
2. [Préstamos Fink Landing Page](#1-préstamos-fink-landing-page)
   - [Section Code: `prestamos-fink.liquid`](#section-code-prestamos-finkliquid)
   - [Page Template Code: `page.prestamos-fink.json`](#page-template-code-pageprestamos-finkjson)
3. [Aylesva Care Landing Page](#2-aylesva-care-landing-page)
   - [Section Code: `aylesva-care.liquid`](#section-code-aylesva-careliquid)
   - [Page Template Code: `page.aylesva-care.json`](#page-template-code-pageaylesva-carejson)
4. [All Cities Global Landing Page](#3-all-cities-global-landing-page)
   - [Section Code: `allcities-global.liquid`](#section-code-allcities-globalliquid)
   - [Page Template Code: `page.allcities-global.json`](#page-template-code-pageallcities-globaljson)

---

## General Deployment Instructions

To deploy any of the landing pages on a Shopify store, follow these 3 simple steps:

### Step 1: Create the Liquid Section
1. From your Shopify Admin, go to **Online Store** > **Themes**.
2. Click the three dots next to your theme and select **Edit Code**.
3. Under the **Sections** folder, click **Add a new section**.
4. Name the section exactly as specified (e.g., `prestamos-fink`, `aylesva-care`, or `allcities-global`).
5. Copy the corresponding liquid section code below, paste it into the file, and click **Save**.

### Step 2: Create the JSON Page Template
1. Under the **Templates** folder in the theme editor, click **Add a new template**.
2. Select **Page** as the template type.
3. Select **JSON** as the template format.
4. Name the template exactly as specified (e.g., `prestamos-fink`, `aylesva-care`, or `allcities-global`).
5. Replace the default JSON contents with the template code block provided below, and click **Save**.
   *Note: This JSON file automatically pre-configures all block contents, text copies, and default layouts so that you don't have to input them manually in the Shopify Theme Editor.*

### Step 3: Create the Page in Shopify Admin
1. Go to **Online Store** > **Pages** and click **Add Page**.
2. Enter the title of your page (e.g., `Servicios Financieros Fink`, `Aylesva Care`, or `All Cities Global`).
3. In the right-hand panel, under **Theme template**, select the newly created template suffix:
   - Select `prestamos-fink` for the Fink page.
   - Select `aylesva-care` for the Aylesva Care page.
   - Select `allcities-global` for the All Cities Global page.
4. Click **Save**.
5. Customize colors, texts, and replace placeholder image links via the **Shopify Customizer** under the Page template view.

---

## 1. Préstamos Fink Landing Page

### Section Code: `prestamos-fink.liquid`
Create a new file in your theme under `Sections/prestamos-fink.liquid`:

```liquid
{% comment %}
  ============================================================
  Servicios Financieros Fink — Premium landing section
  Single reusable Shopify section. Almost everything is editable
  via the Theme Editor and compatible with Translate & Adapt.
  Repeatable content uses blocks (trust, solution card,
  timeline step).
  ============================================================
{% endcomment %}

{%- liquid
  assign brand_blue = section.settings.color_brand
  assign navy = section.settings.color_navy
  assign light = section.settings.color_light
  assign white = section.settings.color_white
  assign accent = section.settings.color_accent
  assign logo_align = section.settings.logo_align
  assign contact_anchor = '#fink-contact-' | append: section.id
-%}

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">

<style>
  #fink-{{ section.id }} {
    --fk-brand: {{ brand_blue }};
    --fk-navy: {{ navy }};
    --fk-light: {{ light }};
    --fk-white: {{ white }};
    --fk-accent: {{ accent }};
    --fk-ink: #0F172A;
    --fk-muted: #64748B;
    --fk-line: rgba(15,23,42,.08);
    --fk-radius: 20px;
    --fk-radius-sm: 14px;
    --fk-shadow: 0 1px 2px rgba(15,23,42,.04), 0 12px 32px rgba(15,23,42,.06);
    --fk-shadow-lg: 0 30px 60px -20px rgba(15,23,42,.2);
    --fk-maxw: 1240px;
    font-family: 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    color: var(--fk-ink);
    background: var(--fk-white);
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
  }
  #fink-{{ section.id }} * { box-sizing: border-box; }
  #fink-{{ section.id }} .fk-wrap { max-width: var(--fk-maxw); margin: 0 auto; padding: 0 24px; }

  /* ---------- TYPOGRAPHY & BUTTONS ---------- */
  #fink-{{ section.id }} h1, #fink-{{ section.id }} h2, #fink-{{ section.id }} h3, #fink-{{ section.id }} h4 { margin: 0; line-height: 1.2; font-weight: 800; color: var(--fk-navy); }
  #fink-{{ section.id }} p { margin: 0; line-height: 1.6; }
  #fink-{{ section.id }} .fk-eyebrow { display: inline-block; font-size: 13px; font-weight: 800; letter-spacing: 2px; text-transform: uppercase; color: var(--fk-brand); margin-bottom: 12px; }
  
  #fink-{{ section.id }} .fk-btn { display: inline-flex; align-items: center; justify-content: center; font-size: 15px; font-weight: 700; padding: 14px 28px; border-radius: 30px; text-decoration: none; transition: all .25s ease; cursor: pointer; border: none; font-family: inherit; }
  #fink-{{ section.id }} .fk-btn--primary { background: var(--fk-brand); color: #fff; box-shadow: 0 4px 14px rgba(30,58,138,.3); }
  #fink-{{ section.id }} .fk-btn--primary:hover { background: var(--fk-navy); transform: translateY(-2px); box-shadow: 0 6px 20px rgba(30,58,138,.4); }
  #fink-{{ section.id }} .fk-btn--ghost { background: transparent; color: var(--fk-navy); border: 2px solid var(--fk-navy); }
  #fink-{{ section.id }} .fk-btn--ghost:hover { background: var(--fk-navy); color: #fff; transform: translateY(-2px); }
  #fink-{{ section.id }} .fk-btn--light { background: var(--fk-white); color: var(--fk-navy); box-shadow: 0 4px 12px rgba(0,0,0,.08); }
  #fink-{{ section.id }} .fk-btn--light:hover { background: var(--fk-brand); color: #fff; transform: translateY(-2px); box-shadow: 0 6px 16px rgba(30,58,138,.25); }

  /* ---------- LAYOUT SECTIONS ---------- */
  #fink-{{ section.id }} .fk-band { padding: clamp(50px,7vw,92px) 0; }
  #fink-{{ section.id }} .fk-band--gray { background: var(--fk-light); }
  #fink-{{ section.id }} .fk-section-head { text-align: center; max-width: 680px; margin: 0 auto clamp(36px,5vw,60px); }
  #fink-{{ section.id }} .fk-section-head h2 { font-size: clamp(26px,3.2vw,38px); }
  #fink-{{ section.id }} .fk-section-head p { font-size: 16px; color: var(--fk-muted); margin-top: 14px; }

  /* ---------- ANIMATION EFFECTS ---------- */
  #fink-{{ section.id }} .fk-reveal { opacity: 0; transform: translateY(24px); transition: opacity .65s ease, transform .65s ease; }
  #fink-{{ section.id }} .fk-reveal.fk-in { opacity: 1; transform: translateY(0); }

  /* ---------- LOGO HEADER ---------- */
  #fink-{{ section.id }} .fk-logo-wrap { padding: 24px 0 12px; }
  #fink-{{ section.id }} .fk-logo { display: flex; }
  #fink-{{ section.id }} .fk-logo--left { justify-content: flex-start; }
  #fink-{{ section.id }} .fk-logo--center { justify-content: center; }
  #fink-{{ section.id }} .fk-logo--right { justify-content: flex-end; }
  #fink-{{ section.id }} .fk-logo img { height: clamp(48px,6vw,72px); width: auto; object-fit: contain; }
  #fink-{{ section.id }} .fk-logo-text { font-size: 26px; font-weight: 800; color: var(--fk-brand); letter-spacing: -0.5px; }
  #fink-{{ section.id }} .fk-logo-text b { color: var(--fk-navy); }

  /* ---------- 1. HERO SECTION ---------- */
  #fink-{{ section.id }} .fk-hero { padding: clamp(40px,5vw,70px) 0; overflow: hidden; }
  #fink-{{ section.id }} .fk-hero-grid { display: grid; grid-template-columns: 1fr 1fr; gap: clamp(32px,5vw,64px); align-items: center; }
  #fink-{{ section.id }} .fk-hero-copy h1 { font-size: clamp(34px,4.5vw,56px); font-weight: 800; letter-spacing: -1.5px; color: var(--fk-navy); }
  #fink-{{ section.id }} .fk-lede { font-size: clamp(16px,2vw,19px); line-height: 1.65; color: var(--fk-muted); margin-top: 24px; }
  #fink-{{ section.id }} .fk-hero-cta { display: flex; flex-wrap: wrap; gap: 14px; margin-top: 32px; }
  #fink-{{ section.id }} .fk-trust { display: flex; flex-wrap: wrap; gap: 16px 28px; margin-top: 40px; padding-top: 28px; border-top: 1px solid var(--fk-line); }
  #fink-{{ section.id }} .fk-trust-item { display: flex; align-items: center; gap: 9px; font-size: 14px; font-weight: 700; color: var(--fk-navy); }
  #fink-{{ section.id }} .fk-check { width: 22px; height: 22px; border-radius: 50%; background: rgba(16,185,129,.1); color: #10B981; display: grid; place-items: center; flex: none; }
  #fink-{{ section.id }} .fk-check svg { width: 14px; height: 14px; }
  
  /* Image collage style for Hero */
  #fink-{{ section.id }} .fk-collage { display: grid; grid-template-columns: repeat(12, 1fr); gap: 16px; position: relative; }
  #fink-{{ section.id }} .fk-tile { border-radius: var(--fk-radius); overflow: hidden; box-shadow: var(--fk-shadow); position: relative; aspect-ratio: 4/3; background: var(--fk-light); }
  #fink-{{ section.id }} .fk-tile img { width: 100%; height: 100%; object-fit: cover; transition: transform .6s ease; }
  #fink-{{ section.id }} .fk-tile:hover img { transform: scale(1.06); }
  #fink-{{ section.id }} .fk-tile--1 { grid-column: 1 / 8; grid-row: 1 / 4; aspect-ratio: 16/10; }
  #fink-{{ section.id }} .fk-tile--2 { grid-column: 8 / 13; grid-row: 1 / 3; aspect-ratio: 1; }
  #fink-{{ section.id }} .fk-tile--3 { grid-column: 1 / 6; grid-row: 4 / 6; aspect-ratio: 1; margin-top: -16px; }
  #fink-{{ section.id }} .fk-tile--4 { grid-column: 6 / 13; grid-row: 3 / 6; aspect-ratio: 16/10; }

  /* ---------- 2. SOLUTIONS (SOURCE CARDS) ---------- */
  #fink-{{ section.id }} .fk-cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 28px; }
  #fink-{{ section.id }} .fk-card { background: var(--fk-white); border-radius: var(--fk-radius); overflow: hidden; box-shadow: var(--fk-shadow); transition: transform .4s ease, box-shadow .4s ease; display: flex; flex-direction: column; height: 100%; border: 1px solid var(--fk-line); }
  #fink-{{ section.id }} .fk-card:hover { transform: translateY(-8px); box-shadow: var(--fk-shadow-lg); }
  #fink-{{ section.id }} .fk-card-media { height: 180px; position: relative; background: var(--fk-light); overflow: hidden; }
  #fink-{{ section.id }} .fk-card-media img { width: 100%; height: 100%; object-fit: cover; }
  #fink-{{ section.id }} .fk-card-ic { position: absolute; bottom: 16px; left: 16px; width: 44px; height: 44px; border-radius: 12px; background: var(--fk-brand); color: #fff; display: grid; place-items: center; box-shadow: 0 4px 10px rgba(30,58,138,.3); z-index: 2; }
  #fink-{{ section.id }} .fk-card-ic svg { width: 22px; height: 22px; }
  #fink-{{ section.id }} .fk-card-body { padding: 24px; display: flex; flex-direction: column; flex-grow: 1; }
  #fink-{{ section.id }} .fk-card-body h3 { font-size: 20px; font-weight: 700; margin-bottom: 12px; }
  #fink-{{ section.id }} .fk-card-body p { font-size: 14.5px; color: var(--fk-muted); flex-grow: 1; }
  #fink-{{ section.id }} .fk-card-link { display: inline-flex; align-items: center; gap: 6px; font-size: 14.5px; font-weight: 700; color: var(--fk-brand); text-decoration: none; margin-top: 20px; }
  #fink-{{ section.id }} .fk-card-link svg { width: 16px; height: 16px; transition: transform .2s ease; }
  #fink-{{ section.id }} .fk-card-link:hover svg { transform: translateX(3px); }

  /* ---------- 3. MISSION, VISION, VALUES ---------- */
  #fink-{{ section.id }} .fk-mv-grid { display: grid; grid-template-columns: 1fr 1fr; gap: clamp(32px,5vw,64px); align-items: center; }
  #fink-{{ section.id }} .fk-mv-copy h2 { font-size: clamp(26px,3vw,38px); }
  #fink-{{ section.id }} .fk-mv-tabs { display: flex; flex-direction: column; gap: 16px; margin-top: 32px; }
  #fink-{{ section.id }} .fk-mv-tab { border-left: 3px solid var(--fk-line); padding-left: 20px; transition: border-color .3s ease; }
  #fink-{{ section.id }} .fk-mv-tab.fk-active { border-color: var(--fk-brand); }
  #fink-{{ section.id }} .fk-mv-tab h3 { font-size: 18px; font-weight: 700; cursor: pointer; transition: color .2s; }
  #fink-{{ section.id }} .fk-mv-tab h3:hover { color: var(--fk-brand); }
  #fink-{{ section.id }} .fk-mv-tab p { margin-top: 8px; font-size: 14.5px; color: var(--fk-muted); display: none; }
  #fink-{{ section.id }} .fk-mv-tab.fk-active p { display: block; }
  
  #fink-{{ section.id }} .fk-values-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 40px; border-top: 1px solid var(--fk-line); padding-top: 40px; }
  #fink-{{ section.id }} .fk-value-card { background: var(--fk-light); padding: 20px; border-radius: var(--fk-radius-sm); border: 1px solid var(--fk-line); }
  #fink-{{ section.id }} .fk-value-card h4 { font-size: 16px; font-weight: 700; color: var(--fk-brand); margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px; }
  #fink-{{ section.id }} .fk-value-card p { font-size: 13.5px; color: var(--fk-muted); }

  /* ---------- 4. HOW IT WORKS (TIMELINE) ---------- */
  #fink-{{ section.id }} .fk-timeline { display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; position: relative; }
  #fink-{{ section.id }} .fk-timeline::before { content: ""; position: absolute; top: 22px; left: 0; right: 0; height: 2px; background: repeating-linear-gradient(90deg, var(--fk-line) 0 8px, transparent 8px 16px); z-index: 0; }
  #fink-{{ section.id }} .fk-step { position: relative; z-index: 1; text-align: center; }
  #fink-{{ section.id }} .fk-step-dot { width: 44px; height: 44px; border-radius: 50%; background: var(--fk-white); border: 2px dashed var(--fk-brand); display: grid; place-items: center; margin: 0 auto 16px; box-shadow: var(--fk-shadow); position: relative; z-index: 2; transition: all .3s; }
  #fink-{{ section.id }} .fk-step:hover .fk-step-dot { background: var(--fk-brand); color: #fff; transform: scale(1.08); }
  #fink-{{ section.id }} .fk-step-num { font-size: 15px; font-weight: 800; color: var(--fk-brand); transition: color .3s; }
  #fink-{{ section.id }} .fk-step:hover .fk-step-num { color: #fff; }
  #fink-{{ section.id }} .fk-step-text h3 { font-size: 17px; font-weight: 700; margin-bottom: 8px; }
  #fink-{{ section.id }} .fk-step-text p { font-size: 13.5px; color: var(--fk-muted); }

  /* ---------- 5. FORM SECTION ---------- */
  #fink-{{ section.id }} .fk-form-wrap { max-width: 820px; margin: 0 auto; background: var(--fk-white); border: 1px solid var(--fk-line); border-radius: 26px; box-shadow: var(--fk-shadow); padding: clamp(28px,4vw,52px); }
  #fink-{{ section.id }} .fk-form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }
  #fink-{{ section.id }} .fk-field { display: flex; flex-direction: column; gap: 6px; }
  #fink-{{ section.id }} .fk-field.fk-span2 { grid-column: 1 / -1; }
  #fink-{{ section.id }} .fk-field label { font-size: 13.5px; font-weight: 700; color: var(--fk-navy); }
  #fink-{{ section.id }} .fk-field input, #fink-{{ section.id }} .fk-field select, #fink-{{ section.id }} .fk-field textarea { font-family: inherit; font-size: 15px; color: var(--fk-ink); background: var(--fk-light); border: 1px solid var(--fk-line); border-radius: 12px; padding: 13px 15px; transition: border-color .2s, box-shadow .2s, background .2s; width: 100%; }
  #fink-{{ section.id }} .fk-field input:focus, #fink-{{ section.id }} .fk-field select:focus, #fink-{{ section.id }} .fk-field textarea:focus { outline: none; border-color: var(--fk-brand); background: #fff; box-shadow: 0 0 0 4px rgba(30,58,138,.10); }
  #fink-{{ section.id }} .fk-field textarea { resize: vertical; min-height: 110px; }
  #fink-{{ section.id }} .fk-form-note { font-size: 13px; color: var(--fk-muted); margin-top: 16px; display: inline-flex; align-items: center; gap: 6px; }
  #fink-{{ section.id }} .fk-form-note svg { flex: none; width: 18px; height: 18px; color: var(--fk-brand); }
  #fink-{{ section.id }} .fk-form-actions { margin-top: 24px; text-align: center; }
  #fink-{{ section.id }} .fk-form-success { background: rgba(16,185,129,.10); border: 1px solid rgba(16,185,129,.2); color: #059669; border-radius: 12px; padding: 16px 18px; font-weight: 600; margin-bottom: 22px; text-align: center; }

  /* ---------- RESPONSIVE LAYOUTS ---------- */
  @media (max-width: 900px) {
    #fink-{{ section.id }} .fk-hero-grid { grid-template-columns: 1fr; }
    #fink-{{ section.id }} .fk-cards { grid-template-columns: 1fr; gap: 20px; }
    #fink-{{ section.id }} .fk-mv-grid { grid-template-columns: 1fr; }
    #fink-{{ section.id }} .fk-values-grid { grid-template-columns: 1fr; gap: 12px; }
    
    /* timeline responsive */
    #fink-{{ section.id }} .fk-timeline { grid-template-columns: 1fr; gap: 0; }
    #fink-{{ section.id }} .fk-timeline::before { top: 0; bottom: 0; left: 21px; right: auto; width: 2px; height: auto; }
    #fink-{{ section.id }} .fk-step { text-align: left; display: grid; grid-template-columns: 44px 1fr; gap: 16px; padding-bottom: 24px; }
    #fink-{{ section.id }} .fk-step-dot { margin: 0; }
    #fink-{{ section.id }} .fk-step-text { padding-top: 8px; }
  }
  @media (max-width: 560px) {
    #fink-{{ section.id }} .fk-form-grid { grid-template-columns: 1fr; }
    #fink-{{ section.id }} .fk-form-grid .fk-field { grid-column: auto !important; }
    #fink-{{ section.id }} .fk-hero-cta { flex-direction: column; }
    #fink-{{ section.id }} .fk-hero-cta .fk-btn { width: 100%; text-align: center; }
  }
</style>

<div id="fink-{{ section.id }}">
  
  {%- comment -%} ============ LOGO HEADER ============ {%- endcomment -%}
  {%- if section.settings.show_logo_header -%}
    <div class="fk-logo-wrap">
      <div class="fk-wrap">
        <div class="fk-logo fk-logo--{{ logo_align }}">
          {%- if section.settings.logo != blank -%}
            <img src="{{ section.settings.logo | image_url: width: 600 }}" alt="{{ section.settings.logo.alt | default: shop.name | escape }}" loading="eager">
          {%- else -%}
            <span class="fk-logo-text">Servicios Financieros <b>Fink</b></span>
          {%- endif -%}
        </div>
      </div>
    </div>
  {%- endif -%}

  {%- comment -%} ============ HERO SECTION ============ {%- endcomment -%}
  <section class="fk-hero">
    <div class="fk-wrap">
      <div class="fk-hero-grid">
        <div class="fk-hero-copy fk-reveal">
          {%- if section.settings.hero_eyebrow != blank -%}<span class="fk-eyebrow">{{ section.settings.hero_eyebrow }}</span>{%- endif -%}
          <h1>{{ section.settings.hero_headline }}</h1>
          <div class="fk-lede">{{ section.settings.hero_description }}</div>
          
          <div class="fk-hero-cta">
            {%- if section.settings.hero_btn1_text != blank -%}
              <a href="{{ section.settings.hero_btn1_link | default: contact_anchor }}" class="fk-btn fk-btn--primary">{{ section.settings.hero_btn1_text }}</a>
            {%- endif -%}
            {%- if section.settings.hero_btn2_text != blank -%}
              <a href="{{ section.settings.hero_btn2_link | default: contact_anchor }}" class="fk-btn fk-btn--ghost">{{ section.settings.hero_btn2_text }}</a>
            {%- endif -%}
          </div>

          {%- assign trust_blocks = section.blocks | where: 'type', 'trust' -%}
          {%- if trust_blocks.size > 0 -%}
            <div class="fk-trust">
              {%- for block in trust_blocks -%}
                <div class="fk-trust-item" {{ block.shopify_attributes }}>
                  <span class="fk-check">
                    <svg viewBox="0 0 24 24" fill="none"><path d="M5 13l4 4L19 7" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>
                  </span>
                  <span>{{ block.settings.text }}</span>
                </div>
              {%- endfor -%}
            </div>
          {%- endif -%}
        </div>

        {%- assign hero_imgs = section.blocks | where: 'type', 'hero_image' -%}
        {%- if hero_imgs.size > 0 -%}
          <div class="fk-collage fk-reveal">
            {%- for block in hero_imgs limit: 4 -%}
              {%- liquid
                assign src = ''
                if block.settings.image != blank
                  assign src = block.settings.image | image_url: width: 800
                elsif block.settings.image_url != blank
                  assign src = block.settings.image_url
                elsif forloop.first
                  assign src = 'family-business-soul.jpg' | asset_url
                endif
              -%}
              {%- if src != blank -%}
                <div class="fk-tile fk-tile--{{ forloop.index }}" {{ block.shopify_attributes }}>
                  <img src="{{ src }}" alt="{{ block.settings.alt | escape }}" loading="lazy">
                </div>
              {%- endif -%}
            {%- endfor -%}
          </div>
        {%- endif -%}
      </div>
    </div>
  </section>

  {%- comment -%} ============ SOLUTIONS SECTION ============ {%- endcomment -%}
  {%- assign solution_cards = section.blocks | where: 'type', 'solution_card' -%}
  {%- if solution_cards.size > 0 -%}
    <section class="fk-band fk-band--gray">
      <div class="fk-wrap">
        <div class="fk-section-head fk-reveal">
          <h2>{{ section.settings.solutions_title }}</h2>
          {%- if section.settings.solutions_subtitle != blank -%}<p>{{ section.settings.solutions_subtitle }}</p>{%- endif -%}
        </div>
        <div class="fk-cards">
          {%- for block in solution_cards -%}
            {%- liquid
              assign src = ''
              if block.settings.image != blank
                assign src = block.settings.image | image_url: width: 800
              elsif block.settings.image_url != blank
                assign src = block.settings.image_url
              endif
            -%}
            <div class="fk-card fk-reveal" {{ block.shopify_attributes }}>
              <div class="fk-card-media">
                {%- if src != blank -%}<img src="{{ src }}" alt="{{ block.settings.title | escape }}" loading="lazy">{%- endif -%}
                <span class="fk-card-ic">
                  {%- case block.settings.icon -%}
                    {%- when 'credit' -%}<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="4" width="22" height="16" rx="2" ry="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>
                    {%- when 'company' -%}<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 21H2V3h20v18z"/><path d="M9 21V9h6v12"/></svg>
                    {%- when 'home' -%}<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
                    {%- else -%}<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>
                  {%- endcase -%}
                </span>
              </div>
              <div class="fk-card-body">
                <h3>{{ block.settings.title }}</h3>
                <p>{{ block.settings.description }}</p>
                <a href="{{ contact_anchor }}" class="fk-card-link" data-fk-scroll>
                  <span>{{ block.settings.btn_text | default: 'Solicitar Información' }}</span>
                  <svg viewBox="0 0 24 24" fill="none"><path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                </a>
              </div>
            </div>
          {%- endfor -%}
        </div>
      </div>
    </section>
  {%- endif -%}

  {%- comment -%} ============ IDENTITY (MISSION, VISION, VALUES) ============ {%- endcomment -%}
  <section class="fk-band">
    <div class="fk-wrap">
      <div class="fk-mv-grid">
        <div class="fk-mv-copy fk-reveal">
          <span class="fk-eyebrow">{{ section.settings.identity_eyebrow | default: 'Quiénes Somos' }}</span>
          <h2>{{ section.settings.identity_title | default: 'Existimos para trabajar contigo' }}</h2>
          
          <div class="fk-mv-tabs">
            <div class="fk-mv-tab fk-active" onclick="FinkTab(this)">
              <h3>Misión</h3>
              <p>{{ section.settings.mission_text }}</p>
            </div>
            <div class="fk-mv-tab" onclick="FinkTab(this)">
              <h3>Visión</h3>
              <p>{{ section.settings.vision_text }}</p>
            </div>
          </div>
        </div>
        
        <div class="fk-mv-val-wrap fk-reveal">
          <h3 style="font-size: 22px; font-weight:800; color:var(--fk-navy);">Nuestros Valores</h3>
          <div class="fk-values-grid">
            <div class="fk-value-card">
              <h4>Confianza</h4>
              <p>Construimos relaciones transparentes y de largo plazo con cada cliente.</p>
            </div>
            <div class="fk-value-card">
              <h4>Compromiso</h4>
              <p>Buscamos activamente obtener las mejores tasas y plazos posibles.</p>
            </div>
            <div class="fk-value-card">
              <h4>Agilidad</h4>
              <p>Simplificamos trámites burocráticos para ofrecer respuestas rápidas.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  {%- comment -%} ============ TIMELINE SECTION ============ {%- endcomment -%}
  {%- assign timeline_steps = section.blocks | where: 'type', 'timeline_step' -%}
  {%- if timeline_steps.size > 0 -%}
    <section class="fk-band fk-band--gray">
      <div class="fk-wrap">
        <div class="fk-section-head fk-reveal">
          <h2>{{ section.settings.timeline_title }}</h2>
          {%- if section.settings.timeline_subtitle != blank -%}<p>{{ section.settings.timeline_subtitle }}</p>{%- endif -%}
        </div>
        <div class="fk-timeline">
          {%- for block in timeline_steps -%}
            <div class="fk-step fk-reveal" {{ block.shopify_attributes }}>
              <div class="fk-step-dot">
                <span class="fk-step-num">{{ forloop.index }}</span>
              </div>
              <div class="fk-step-text">
                <h3>{{ block.settings.title }}</h3>
                <p>{{ block.settings.description }}</p>
              </div>
            </div>
          {%- endfor -%}
        </div>
      </div>
    </section>
  {%- endif -%}

  {%- comment -%} ============ CONTACT FORM ============ {%- endcomment -%}
  <section class="fk-band" id="{{ contact_anchor | remove: '#' }}">
    <div class="fk-wrap">
      <div class="fk-section-head fk-reveal">
        <h2>{{ section.settings.form_title }}</h2>
        {%- if section.settings.form_subtitle != blank -%}<p>{{ section.settings.form_subtitle }}</p>{%- endif -%}
      </div>
      
      <div class="fk-form-wrap fk-reveal">
        {%- form 'contact', id: 'fink-contact-form' -%}
          {%- if form.posted_successfully? -%}
            <div class="fk-form-success">{{ section.settings.form_success }}</div>
          {%- endif -%}
          
          <div class="fk-form-grid">
            <div class="fk-field">
              <label>Nombre Completo</label>
              <input type="text" name="contact[name]" required placeholder="Ej. Juan Pérez">
            </div>
            <div class="fk-field">
              <label>Nombre de la Empresa</label>
              <input type="text" name="contact[company]" placeholder="Ej. Mi PyME S.A.">
            </div>
            <div class="fk-field">
              <label>Teléfono / WhatsApp</label>
              <input type="tel" name="contact[phone]" placeholder="Ej. 55 1234 5678">
            </div>
            <div class="fk-field">
              <label>Correo Electrónico</label>
              <input type="email" name="contact[email]" required placeholder="Ej. juan@empresa.com">
            </div>
            <div class="fk-field">
              <label>Tipo de Crédito</label>
              <select name="contact[credit_type]">
                <option value="Credito PyME Inmediato">Crédito PyME Inmediato</option>
                <option value="Financiamiento Empresarial">Financiamiento Empresarial</option>
                <option value="Credito Hipotecario">Crédito Hipotecario</option>
                <option value="Credito Personal">Crédito Personal</option>
              </select>
            </div>
            <div class="fk-field">
              <label>Monto Solicitado (Aprox.)</label>
              <input type="text" name="contact[amount]" placeholder="Ej. $250,000 MXN">
            </div>
            <div class="fk-field fk-span2">
              <label>Detalles de tu solicitud</label>
              <textarea name="contact[body]" placeholder="Cuéntanos un poco sobre tu negocio y para qué necesitas el financiamiento..."></textarea>
            </div>
          </div>
          
          {%- if section.settings.form_note != blank -%}
            <p class="fk-form-note">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
              {{ section.settings.form_note }}
            </p>
          {%- endif -%}
          
          <div class="fk-form-actions">
            <button type="submit" class="fk-btn fk-btn--primary">{{ section.settings.form_btn_text }}</button>
          </div>
        {%- endform -%}
      </div>
    </div>
  </section>

</div>

<script>
  function FinkTab(el) {
    var tabs = el.parentElement.querySelectorAll('.fk-mv-tab');
    tabs.forEach(function(tab) {
      tab.classList.remove('fk-active');
    });
    el.classList.add('fk-active');
  }

  (function(){
    var root = document.getElementById('fink-{{ section.id }}');
    if(!root) return;
    
    // Reveal animations
    var els = root.querySelectorAll('.fk-reveal');
    if(!('IntersectionObserver' in window)){ 
      els.forEach(function(e){ e.classList.add('fk-in'); }); 
      return; 
    }
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(en){
        if(en.isIntersecting){ 
          en.target.classList.add('fk-in'); 
          io.unobserve(en.target); 
        }
      });
    }, { threshold: 0.1 });
    els.forEach(function(e){ io.observe(e); });

    // Smooth scroll for anchors
    root.querySelectorAll('a[data-fk-scroll]').forEach(function(a){
      a.addEventListener('click', function(ev){
        var href = a.getAttribute('href') || '';
        if(href.charAt(0) !== '#') return;
        var target = document.getElementById(href.slice(1));
        if(!target) return;
        ev.preventDefault();
        var y = target.getBoundingClientRect().top + window.pageYOffset - 24;
        window.scrollTo({ top: y, behavior: 'smooth' });
      });
    });
  })();
</script>

{% schema %}
{
  "name": "Préstamos Fink",
  "tag": "section",
  "class": "fink-loans-section",
  "settings": [
    { "type": "header", "content": "Header Logo" },
    { "type": "checkbox", "id": "show_logo_header", "label": "Mostrar logotipo", "default": true },
    { "type": "image_picker", "id": "logo", "label": "Logotipo de Fink" },
    { "type": "select", "id": "logo_align", "label": "Alineación del logotipo", "options": [ {"value":"left","label":"Izquierda"}, {"value":"center","label":"Centro"}, {"value":"right","label":"Derecha"} ], "default": "center" },

    { "type": "header", "content": "Diseño y Colores" },
    { "type": "color", "id": "color_brand", "label": "Azul de Marca", "default": "#1E3A8A" },
    { "type": "color", "id": "color_navy", "label": "Azul Obscuro / Texto", "default": "#0F172A" },
    { "type": "color", "id": "color_light", "label": "Gris Claro", "default": "#F8FAFC" },
    { "type": "color", "id": "color_white", "label": "Blanco / Fondo", "default": "#FFFFFF" },
    { "type": "color", "id": "color_accent", "label": "Acento de Marca", "default": "#D97706" },

    { "type": "header", "content": "1 · Hero" },
    { "type": "text", "id": "hero_eyebrow", "label": "Subtítulo Hero", "default": "ALIANZA FINANCIERA" },
    { "type": "text", "id": "hero_headline", "label": "Título Principal", "default": "Intermediación Financiera Ágil para PyMEs" },
    { "type": "richtext", "id": "hero_description", "label": "Descripción Hero", "default": "<p>En Servicios Financieros Fink nos especializamos en facilitar el acceso a soluciones de crédito personal, hipotecario y empresarial para PyMEs mexicanas. Analizamos tu perfil para conectarte con las mejores opciones y tasas del mercado.<\/p>" },
    { "type": "text", "id": "hero_btn1_text", "label": "Botón Principal", "default": "Solicitar Información" },
    { "type": "url", "id": "hero_btn1_link", "label": "Enlace del Botón Principal" },
    { "type": "text", "id": "hero_btn2_text", "label": "Botón Secundario", "default": "Conocer Soluciones" },
    { "type": "url", "id": "hero_btn2_link", "label": "Enlace del Botón Secundario" },

    { "type": "header", "content": "2 · Soluciones Financieras" },
    { "type": "text", "id": "solutions_title", "label": "Título Sección", "default": "¿Buscas servicios financieros?" },
    { "type": "text", "id": "solutions_subtitle", "label": "Subtítulo Sección", "default": "Conectamos tu negocio con las soluciones de financiamiento que necesitas." },

    { "type": "header", "content": "3 · Misión y Visión" },
    { "type": "text", "id": "identity_eyebrow", "label": "Subtítulo Identidad", "default": "QUIÉNES SOMOS" },
    { "type": "text", "id": "identity_title", "label": "Título Identidad", "default": "Existimos para trabajar contigo" },
    { "type": "textarea", "id": "mission_text", "label": "Misión", "default": "Brindar servicios de intermediación financiera eficientes y confiables, facilitando a las PyMEs mexicanas el acceso a créditos adecuados mediante soluciones personalizadas, ágiles y competitivas." },
    { "type": "textarea", "id": "vision_text", "label": "Visión", "default": "Ser un referente en intermediación financiera en México, reconocidos por nuestra capacidad de conectar a nuestros clientes con las mejores opciones del mercado, impulsando su crecimiento y estabilidad." },

    { "type": "header", "content": "4 · Proceso de Solicitud" },
    { "type": "text", "id": "timeline_title", "label": "Título Proceso", "default": "Un proceso simple y ágil" },
    { "type": "text", "id": "timeline_subtitle", "label": "Subtítulo Proceso", "default": "Obtén respuesta en sencillos pasos." },

    { "type": "header", "content": "5 · Formulario de Contacto" },
    { "type": "text", "id": "form_title", "label": "Título Formulario", "default": "Solicita tu Asesoría Financiera" },
    { "type": "text", "id": "form_subtitle", "label": "Subtítulo Formulario", "default": "Compártenos tus datos de contacto y necesidades para que un asesor te contacte a la brevedad." },
    { "type": "text", "id": "form_note", "label": "Nota aclaratoria", "default": "Tus datos están protegidos por nuestro Aviso de Privacidad." },
    { "type": "text", "id": "form_btn_text", "label": "Texto del Botón Enviar", "default": "Enviar Solicitud" },
    { "type": "text", "id": "form_success", "label": "Mensaje de Éxito", "default": "¡Gracias! Tu solicitud ha sido recibida con éxito. Un asesor de Fink se comunicará contigo muy pronto." }
  ],
  "blocks": [
    {
      "type": "trust",
      "name": "Insignia de Confianza",
      "settings": [
        { "type": "text", "id": "text", "label": "Texto de la insignia", "default": "Proceso ágil" }
      ]
    },
    {
      "type": "hero_image",
      "name": "Imagen de Collage (Hero)",
      "settings": [
        { "type": "image_picker", "id": "image", "label": "Imagen" },
        { "type": "text", "id": "image_url", "label": "URL de la imagen (alternativa)" },
        { "type": "text", "id": "alt", "label": "Texto descriptivo (alt)", "default": "Logística y finanzas Fink" }
      ]
    },
    {
      "type": "solution_card",
      "name": "Tarjeta de Solución",
      "settings": [
        { "type": "text", "id": "title", "label": "Título de la solución", "default": "Crédito PyME" },
        { "type": "textarea", "id": "description", "label": "Descripción", "default": "Solución de crédito rápido para capital de trabajo, inventario y liquidez inmediata." },
        { "type": "select", "id": "icon", "label": "Icono", "options": [ {"value":"credit","label":"Tarjeta de Crédito"}, {"value":"company","label":"Empresas / PyMEs"}, {"value":"home","label":"Hipotecario / Casa"} ], "default": "credit" },
        { "type": "text", "id": "btn_text", "label": "Texto del botón", "default": "Solicitar Información" },
        { "type": "image_picker", "id": "image", "label": "Imagen de fondo" },
        { "type": "text", "id": "image_url", "label": "URL de la imagen de fondo" }
      ]
    },
    {
      "type": "timeline_step",
      "name": "Paso del Proceso",
      "settings": [
        { "type": "text", "id": "title", "label": "Título", "default": "1. Cuéntanos lo que necesitas" },
        { "type": "textarea", "id": "description", "label": "Descripción", "default": "Completa el formulario describiendo el tipo de crédito de tu interés." }
      ]
    }
  ]
}
{% endschema %}
```

### Page Template Code: `page.prestamos-fink.json`
Create a new template file in your theme under `Templates/page.prestamos-fink.json`:

```json
{
  "sections": {
    "main": {
      "type": "prestamos-fink",
      "settings": {
        "show_logo_header": true,
        "color_brand": "#1E3A8A",
        "color_navy": "#0F172A",
        "color_light": "#F8FAFC",
        "color_white": "#FFFFFF",
        "color_accent": "#D97706",
        "hero_eyebrow": "INTERMEDIACIÓN FINANCIERA",
        "hero_headline": "Créditos PyME y Financiamiento Empresarial Ágil",
        "hero_description": "<p>En Servicios Financieros Fink somos tus aliados estratégicos. Facilitamos el acceso a créditos empresariales, personales e hipotecarios con las mejores tasas y plazos del mercado, optimizando tus tiempos de respuesta.<\/p>",
        "hero_btn1_text": "Solicitar Crédito",
        "hero_btn2_text": "Nuestras Soluciones",
        "solutions_title": "¿Buscas servicios financieros?",
        "solutions_subtitle": "Conectamos tu negocio con las soluciones de financiamiento adecuadas para su crecimiento y liquidez.",
        "identity_eyebrow": "QUIÉNES SOMOS",
        "identity_title": "Existimos para trabajar contigo",
        "mission_text": "Brindar servicios de intermediación financiera eficientes y confiables, facilitando a las PyMEs mexicanas el acceso a créditos adecuados mediante soluciones personalizadas, ágiles y competitivas.",
        "vision_text": "Ser un referente en intermediación financiera en México, reconocidos por nuestra capacidad de conectar a nuestros clientes con las mejores opciones del mercado, impulsando su crecimiento y estabilidad.",
        "timeline_title": "Un proceso simple y ágil",
        "timeline_subtitle": "Obtén el financiamiento que necesitas en 4 sencillos pasos.",
        "form_title": "Solicita tu Asesoría Financiera",
        "form_subtitle": "Compártenos tus datos de contacto y necesidades para que un asesor te contacte a la brevedad.",
        "form_note": "Tus datos están protegidos por nuestro Aviso de Privacidad.",
        "form_btn_text": "Enviar Solicitud",
        "form_success": "¡Gracias! Tu solicitud ha sido recibida con éxito. Un asesor de Fink se comunicará contigo muy pronto."
      },
      "blocks": {
        "trust_1": {
          "type": "trust",
          "settings": {
            "text": "Alianzas Estratégicas"
          }
        },
        "trust_2": {
          "type": "trust",
          "settings": {
            "text": "Tiempos de Respuesta Ágiles"
          }
        },
        "trust_3": {
          "type": "trust",
          "settings": {
            "text": "Asesoría de Expertos"
          }
        },
        "hero_img_1": {
          "type": "hero_image",
          "settings": {
            "image_url": "https://images.unsplash.com/photo-1556742044-3c52d6e88c62?auto=format&fit=crop&w=800&q=80",
            "alt": "Negocio family business"
          }
        },
        "hero_img_2": {
          "type": "hero_image",
          "settings": {
            "image_url": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=800&q=80",
            "alt": "Firma de contrato financiero"
          }
        },
        "hero_img_3": {
          "type": "hero_image",
          "settings": {
            "image_url": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=800&q=80",
            "alt": "Asesora financiera trabajando"
          }
        },
        "hero_img_4": {
          "type": "hero_image",
          "settings": {
            "image_url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=800&q=80",
            "alt": "Edificio corporativo moderno"
          }
        },
        "sol_1": {
          "type": "solution_card",
          "settings": {
            "title": "Crédito PyME / Inmediatos",
            "description": "Liquidez inmediata y capital de trabajo para cubrir necesidades operativas del día a día, adquisición de mercancía o pago a proveedores.",
            "icon": "credit",
            "btn_text": "Solicitar Información",
            "image_url": "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?auto=format&fit=crop&w=800&q=80"
          }
        },
        "sol_2": {
          "type": "solution_card",
          "settings": {
            "title": "Financiamiento Empresarial",
            "description": "Créditos estructurados a mediano y largo plazo orientados a la expansión de tu negocio, compra de maquinaria y adquisición de activos.",
            "icon": "company",
            "btn_text": "Solicitar Información",
            "image_url": "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&w=800&q=80"
          }
        },
        "sol_3": {
          "type": "solution_card",
          "settings": {
            "title": "Créditos Personales e Hipotecarios",
            "description": "Asesoría y acceso a las mejores ofertas hipotecarias y de crédito personal del mercado mexicano con condiciones a tu medida.",
            "icon": "home",
            "btn_text": "Solicitar Información",
            "image_url": "https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=800&q=80"
          }
        },
        "step_1": {
          "type": "timeline_step",
          "settings": {
            "title": "1. Cuéntanos tu necesidad",
            "description": "Completa el formulario de contacto contándonos sobre tu empresa o proyecto."
          }
        },
        "step_2": {
          "type": "timeline_step",
          "settings": {
            "title": "2. Análisis y Diagnóstico",
            "description": "Un asesor experto de Fink evalúa tu perfil para identificar la mejor opción."
          }
        },
        "step_3": {
          "type": "timeline_step",
          "settings": {
            "title": "3. Conexión de Opciones",
            "description": "Te presentamos las ofertas más competitivas de nuestras instituciones aliadas."
          }
        },
        "step_4": {
          "type": "timeline_step",
          "settings": {
            "title": "4. Formalización y Entrega",
            "description": "Te acompañamos en todo el trámite hasta el desembolso y activación de tu crédito."
          }
        }
      },
      "block_order": [
        "trust_1",
        "trust_2",
        "trust_3",
        "hero_img_1",
        "hero_img_2",
        "hero_img_3",
        "hero_img_4",
        "sol_1",
        "sol_2",
        "sol_3",
        "step_1",
        "step_2",
        "step_3",
        "step_4"
      ]
    }
  },
  "order": [
    "main"
  ]
}
```

---

## 2. Aylesva Care Landing Page

### Section Code: `aylesva-care.liquid`
Create a new file in your theme under `Sections/aylesva-care.liquid`:

```liquid
{% comment %}
  ============================================================
  Aylesva Care — Premium Health & Benefits Landing Section
  Fully custom, responsive, beautiful CSS & hover animations.
  Translate & Adapt compatible, editable via Shopify Customizer.
  Repeatable content uses blocks (trust badge, package, process step).
  ============================================================
{% endcomment %}

{%- liquid
  assign brand_red = section.settings.color_red
  assign brand_blue = section.settings.color_blue
  assign light_bg = section.settings.color_light
  assign white_bg = section.settings.color_white
  assign accent_green = section.settings.color_accent
  assign contact_anchor = '#care-contact-' | append: section.id
-%}

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

<style>
  #care-{{ section.id }} {
    --ac-red: {{ brand_red }};
    --ac-blue: {{ brand_blue }};
    --ac-light: {{ light_bg }};
    --ac-white: {{ white_bg }};
    --ac-green: {{ accent_green }};
    --ac-ink: #1E293B;
    --ac-muted: #64748B;
    --ac-line: rgba(124,25,34,.08);
    --ac-radius: 24px;
    --ac-radius-sm: 16px;
    --ac-shadow: 0 4px 20px rgba(124,25,34,.04), 0 10px 30px rgba(124,25,34,.05);
    --ac-shadow-hover: 0 24px 50px -12px rgba(124,25,34,.16);
    --ac-maxw: 1240px;
    font-family: 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    color: var(--ac-ink);
    background: var(--ac-white);
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
  }
  #care-{{ section.id }} * { box-sizing: border-box; }
  #care-{{ section.id }} .ac-wrap { max-width: var(--ac-maxw); margin: 0 auto; padding: 0 24px; }

  /* ---------- TYPOGRAPHY & BUTTONS ---------- */
  #care-{{ section.id }} h1, 
  #care-{{ section.id }} h2, 
  #care-{{ section.id }} h3, 
  #care-{{ section.id }} h4 { margin: 0; line-height: 1.25; font-weight: 800; color: var(--ac-blue); letter-spacing: -0.5px; }
  #care-{{ section.id }} p { margin: 0; line-height: 1.65; }
  #care-{{ section.id }} .ac-eyebrow { display: inline-block; font-size: 13px; font-weight: 800; letter-spacing: 2.5px; text-transform: uppercase; color: var(--ac-red); margin-bottom: 12px; }
  
  #care-{{ section.id }} .ac-btn { display: inline-flex; align-items: center; justify-content: center; font-size: 15px; font-weight: 700; padding: 14px 30px; border-radius: 30px; text-decoration: none; transition: all .3s cubic-bezier(0.16, 1, 0.3, 1); cursor: pointer; border: none; font-family: inherit; }
  #care-{{ section.id }} .ac-btn--primary { background: var(--ac-red); color: #fff; box-shadow: 0 4px 14px rgba(124,25,34,.25); }
  #care-{{ section.id }} .ac-btn--primary:hover { background: var(--ac-blue); transform: translateY(-2px); box-shadow: 0 6px 20px rgba(28,65,112,.35); }
  #care-{{ section.id }} .ac-btn--outline { background: transparent; color: var(--ac-blue); border: 2px solid var(--ac-blue); }
  #care-{{ section.id }} .ac-btn--outline:hover { background: var(--ac-blue); color: #fff; transform: translateY(-2px); }

  /* ---------- LAYOUT BANDS ---------- */
  #care-{{ section.id }} .ac-band { padding: clamp(60px,8vw,100px) 0; }
  #care-{{ section.id }} .ac-band--gray { background: var(--ac-light); }
  #care-{{ section.id }} .ac-section-head { text-align: center; max-width: 720px; margin: 0 auto clamp(40px,6vw,68px); }
  #care-{{ section.id }} .ac-section-head h2 { font-size: clamp(28px,3.5vw,40px); }
  #care-{{ section.id }} .ac-section-head p { font-size: 16px; color: var(--ac-muted); margin-top: 14px; }

  /* ---------- REVEAL ANIMATIONS ---------- */
  #care-{{ section.id }} .ac-reveal { opacity: 0; transform: translateY(28px); transition: opacity .75s cubic-bezier(0.16, 1, 0.3, 1), transform .75s cubic-bezier(0.16, 1, 0.3, 1); }
  #care-{{ section.id }} .ac-reveal.ac-in { opacity: 1; transform: translateY(0); }

  /* ---------- HERO SECTION ---------- */
  #care-{{ section.id }} .ac-hero { position: relative; padding: clamp(70px,10vw,140px) 0; overflow: hidden; background-size: cover; background-position: center; display: flex; align-items: center; min-height: clamp(500px, 75vh, 780px); }
  #care-{{ section.id }} .ac-hero::before { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(28,65,112,0.85) 0%, rgba(28,65,112,0.55) 50%, rgba(28,65,112,0.9) 100%); z-index: 1; }
  #care-{{ section.id }} .ac-hero-content { position: relative; z-index: 2; max-width: 760px; color: #fff; }
  #care-{{ section.id }} .ac-hero-content h1 { font-size: clamp(36px,5vw,60px); color: #fff; font-weight: 800; letter-spacing: -1.5px; }
  #care-{{ section.id }} .ac-hero-content p { font-size: clamp(16px,2.2vw,20px); line-height: 1.6; color: rgba(255,255,255,0.9); margin: 24px 0 36px; font-weight: 400; }
  #care-{{ section.id }} .ac-hero-cta { display: flex; flex-wrap: wrap; gap: 16px; }
  #care-{{ section.id }} .ac-hero-cta .ac-btn--outline { border-color: #fff; color: #fff; }
  #care-{{ section.id }} .ac-hero-cta .ac-btn--outline:hover { background: #fff; color: var(--ac-blue); }

  /* ---------- BENEFITS / PACKAGES GRID ---------- */
  #care-{{ section.id }} .ac-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 32px; }
  #care-{{ section.id }} .ac-card { background: var(--ac-white); border-radius: var(--ac-radius); overflow: hidden; box-shadow: var(--ac-shadow); border: 1px solid var(--ac-line); display: flex; flex-direction: column; height: 100%; transition: all .4s cubic-bezier(0.16, 1, 0.3, 1); position: relative; }
  
  /* HOVER ANIMATION FOR CARDS */
  #care-{{ section.id }} .ac-card:hover { transform: translateY(-10px); box-shadow: var(--ac-shadow-hover); border-color: var(--ac-red); }
  
  #care-{{ section.id }} .ac-card-media { height: clamp(200px, 15vw, 240px); overflow: hidden; position: relative; background: var(--ac-light); }
  #care-{{ section.id }} .ac-card-media img { width: 100%; height: 100%; object-fit: cover; transition: transform .6s cubic-bezier(0.16, 1, 0.3, 1); }
  
  /* Zoom image on hover */
  #care-{{ section.id }} .ac-card:hover .ac-card-media img { transform: scale(1.08); }
  
  #care-{{ section.id }} .ac-badge { position: absolute; top: 16px; left: 16px; padding: 6px 12px; border-radius: 30px; font-size: 11px; font-weight: 800; text-transform: uppercase; background: var(--ac-green); color: #fff; z-index: 2; box-shadow: 0 4px 8px rgba(0,0,0,0.1); letter-spacing: 0.5px; }
  #care-{{ section.id }} .ac-card-body { padding: 28px; display: flex; flex-direction: column; flex-grow: 1; }
  #care-{{ section.id }} .ac-card-body h3 { font-size: 22px; margin-bottom: 12px; font-weight: 700; transition: color .3s; }
  
  #care-{{ section.id }} .ac-card:hover .ac-card-body h3 { color: var(--ac-red); }
  #care-{{ section.id }} .ac-card-body p { font-size: 15px; color: var(--ac-muted); line-height: 1.6; flex-grow: 1; }
  
  #care-{{ section.id }} .ac-card-footer { display: flex; align-items: center; justify-content: space-between; margin-top: 24px; padding-top: 20px; border-top: 1px solid var(--ac-line); }
  #care-{{ section.id }} .ac-price-label { font-size: 11px; text-transform: uppercase; color: var(--ac-muted); font-weight: 700; letter-spacing: 0.5px; }
  #care-{{ section.id }} .ac-price { font-size: 22px; font-weight: 800; color: var(--ac-blue); margin-top: 2px; }
  #care-{{ section.id }} .ac-price span { font-size: 13px; font-weight: 600; color: var(--ac-muted); }
  
  #care-{{ section.id }} .ac-card-link { font-size: 14.5px; font-weight: 800; color: var(--ac-blue); text-decoration: none; display: inline-flex; align-items: center; gap: 6px; transition: color .2s; }
  #care-{{ section.id }} .ac-card-link svg { width: 16px; height: 16px; transition: transform .3s cubic-bezier(0.16, 1, 0.3, 1); }
  
  #care-{{ section.id }} .ac-card:hover .ac-card-link { color: var(--ac-red); }
  #care-{{ section.id }} .ac-card:hover .ac-card-link svg { transform: translateX(5px); color: var(--ac-red); }

  /* ---------- COMPLIANCE DISCLOSURE SECTION ---------- */
  #care-{{ section.id }} .ac-disclosure-band { background: #F1F5F9; border-top: 1px solid #E2E8F0; border-bottom: 1px solid #E2E8F0; padding: 24px 0; }
  #care-{{ section.id }} .ac-disclosure-box { display: flex; gap: 20px; align-items: flex-start; max-width: 960px; margin: 0 auto; }
  #care-{{ section.id }} .ac-disc-icon { width: 44px; height: 44px; border-radius: 50%; background: #E2E8F0; color: var(--ac-red); display: grid; place-items: center; flex-shrink: 0; }
  #care-{{ section.id }} .ac-disc-icon svg { width: 22px; height: 22px; }
  #care-{{ section.id }} .ac-disclosure-box p { font-size: 12.5px; line-height: 1.6; color: #475569; }
  #care-{{ section.id }} .ac-disclosure-box p strong { color: var(--ac-blue); font-weight: 700; }
  #care-{{ section.id }} .ac-disclosure-box p a { color: var(--ac-red); font-weight: 700; text-decoration: underline; }

  /* ---------- INFO / BENEFITS OVERVIEW ---------- */
  #care-{{ section.id }} .ac-info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: clamp(32px,6vw,80px); align-items: center; }
  #care-{{ section.id }} .ac-info-media { position: relative; border-radius: var(--ac-radius); overflow: hidden; box-shadow: var(--ac-shadow-hover); aspect-ratio: 4/3; }
  #care-{{ section.id }} .ac-info-media img { width: 100%; height: 100%; object-fit: cover; }
  #care-{{ section.id }} .ac-info-body h2 { font-size: clamp(26px,3vw,38px); margin-bottom: 24px; }
  #care-{{ section.id }} .ac-info-body p { color: var(--ac-muted); margin-bottom: 20px; }
  
  #care-{{ section.id }} .ac-features { display: flex; flex-direction: column; gap: 16px; margin-top: 28px; }
  #care-{{ section.id }} .ac-feature { display: flex; gap: 14px; }
  #care-{{ section.id }} .ac-feat-icon { width: 38px; height: 38px; border-radius: 10px; background: rgba(124,25,34,0.06); color: var(--ac-red); display: grid; place-items: center; flex-shrink: 0; }
  #care-{{ section.id }} .ac-feat-icon svg { width: 20px; height: 20px; }
  #care-{{ section.id }} .ac-feat-text h4 { font-size: 16px; font-weight: 700; margin-bottom: 4px; color: var(--ac-blue); }
  #care-{{ section.id }} .ac-feat-text p { font-size: 14px; color: var(--ac-muted); margin: 0; }

  /* ---------- TIMELINE PROCESS ---------- */
  #care-{{ section.id }} .ac-process { display: grid; grid-template-columns: repeat(3, 1fr); gap: 32px; position: relative; }
  #care-{{ section.id }} .ac-process-card { background: var(--ac-white); padding: 32px; border-radius: var(--ac-radius); border: 1px solid var(--ac-line); box-shadow: var(--ac-shadow); transition: all .3s; }
  #care-{{ section.id }} .ac-process-card:hover { transform: translateY(-4px); border-color: var(--ac-red); }
  #care-{{ section.id }} .ac-proc-num { font-size: 38px; font-weight: 800; color: rgba(124,25,34,0.15); margin-bottom: 16px; line-height: 1; }
  #care-{{ section.id }} .ac-process-card h3 { font-size: 18px; font-weight: 700; margin-bottom: 10px; }
  #care-{{ section.id }} .ac-process-card p { font-size: 14px; color: var(--ac-muted); }

  /* ---------- REGISTRATION FORM ---------- */
  #care-{{ section.id }} .ac-form-box { max-width: 820px; margin: 0 auto; background: var(--ac-white); border: 1px solid var(--ac-line); border-radius: 26px; box-shadow: var(--ac-shadow-hover); padding: clamp(28px,4vw,56px); }
  #care-{{ section.id }} .ac-form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
  #care-{{ section.id }} .ac-field { display: flex; flex-direction: column; gap: 6px; }
  #care-{{ section.id }} .ac-field.ac-span2 { grid-column: 1 / -1; }
  #care-{{ section.id }} .ac-field label { font-size: 13.5px; font-weight: 700; color: var(--ac-blue); }
  #care-{{ section.id }} .ac-field input, 
  #care-{{ section.id }} .ac-field select, 
  #care-{{ section.id }} .ac-field textarea { font-family: inherit; font-size: 15px; color: var(--ac-ink); background: var(--ac-light); border: 1px solid var(--ac-line); border-radius: 12px; padding: 13px 15px; transition: all .25s ease; width: 100%; }
  #care-{{ section.id }} .ac-field input:focus, 
  #care-{{ section.id }} .ac-field select:focus, 
  #care-{{ section.id }} .ac-field textarea:focus { outline: none; border-color: var(--ac-red); background: #fff; box-shadow: 0 0 0 4px rgba(124,25,34,.15); }
  #care-{{ section.id }} .ac-field textarea { resize: vertical; min-height: 120px; }
  #care-{{ section.id }} .ac-form-actions { margin-top: 32px; text-align: center; }
  #care-{{ section.id }} .ac-form-success { background: rgba(16,185,129,.10); border: 1px solid rgba(16,185,129,.2); color: #059669; border-radius: 12px; padding: 16px 18px; font-weight: 600; margin-bottom: 24px; text-align: center; }

  /* ---------- RESPONSIVE DESIGN ---------- */
  @media (max-width: 990px) {
    #care-{{ section.id }} .ac-grid { grid-template-columns: 1fr; gap: 24px; max-width: 420px; margin: 0 auto; }
    #care-{{ section.id }} .ac-info-grid { grid-template-columns: 1fr; }
    #care-{{ section.id }} .ac-process { grid-template-columns: 1fr; gap: 20px; }
  }
  @media (max-width: 580px) {
    #care-{{ section.id }} .ac-form-grid { grid-template-columns: 1fr; }
    #care-{{ section.id }} .ac-form-grid .ac-field { grid-column: auto !important; }
    #care-{{ section.id }} .ac-hero-cta { flex-direction: column; }
    #care-{{ section.id }} .ac-hero-cta .ac-btn { width: 100%; }
  }
</style>

<div id="care-{{ section.id }}">

  {%- comment -%}============ HERO SECTION ============{%- endcomment -%}
  {%- liquid
    assign hero_bg = ''
    if section.settings.hero_image != blank
      assign hero_bg = section.settings.hero_image | image_url: width: 1800
    else
      assign hero_bg = section.settings.hero_image_url
    endif
  -%}
  <section class="ac-hero" style="background-image: url('{{ hero_bg }}');">
    <div class="ac-wrap">
      <div class="ac-hero-content ac-reveal">
        {%- if section.settings.hero_eyebrow != blank -%}<span class="ac-eyebrow">{{ section.settings.hero_eyebrow }}</span>{%- endif -%}
        <h1>{{ section.settings.hero_title }}</h1>
        <p>{{ section.settings.hero_subtitle }}</p>
        <div class="ac-hero-cta">
          {%- if section.settings.hero_btn1_text != blank -%}
            <a href="{{ section.settings.hero_btn1_link | default: contact_anchor }}" class="ac-btn ac-btn--primary">{{ section.settings.hero_btn1_text }}</a>
          {%- endif -%}
          {%- if section.settings.hero_btn2_text != blank -%}
            <a href="{{ section.settings.hero_btn2_link | default: '#packages-featured' }}" class="ac-btn ac-btn--outline" data-ac-scroll>{{ section.settings.hero_btn2_text }}</a>
          {%- endif -%}
        </div>
      </div>
    </div>
  </section>

  {%- comment -%}============ BENEFITS PACKAGES ============ {%- endcomment -%}
  {%- assign package_blocks = section.blocks | where: 'type', 'package_card' -%}
  {%- if package_blocks.size > 0 -%}
    <section class="ac-band ac-band--gray" id="packages-featured">
      <div class="ac-wrap">
        <div class="ac-section-head ac-reveal">
          <h2>{{ section.settings.props_title }}</h2>
          {%- if section.settings.props_subtitle != blank -%}<p>{{ section.settings.props_subtitle }}</p>{%- endif -%}
        </div>
        
        <div class="ac-grid">
          {%- for block in package_blocks -%}
            {%- liquid
              assign card_img = ''
              if block.settings.image != blank
                assign card_img = block.settings.image | image_url: width: 600
              else
                assign card_img = block.settings.image_url
              endif
            -%}
            <div class="ac-card ac-reveal" {{ block.shopify_attributes }}>
              <div class="ac-card-media">
                {%- if card_img != blank -%}<img src="{{ card_img }}" alt="{{ block.settings.title | escape }}" loading="lazy">{%- endif -%}
                {%- if block.settings.featured_badge -%}<span class="ac-badge">Popular</span>{%- endif -%}
              </div>
              <div class="ac-card-body">
                <h3>{{ block.settings.title }}</h3>
                <p>{{ block.settings.description }}</p>
                
                <div class="ac-card-footer">
                  <div>
                    <span class="ac-price-label">Desde solo</span>
                    <div class="ac-price">{{ block.settings.price }} <span>USD/mes</span></div>
                  </div>
                  <a href="{{ contact_anchor }}" class="ac-card-link" data-ac-scroll>
                    <span>Saber más</span>
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                  </a>
                </div>
              </div>
            </div>
          {%- endfor -%}
        </div>
      </div>
    </section>
  {%- endif -%}

  {%- comment -%}============ COMPLIANCE DISCLOSURE ============{%- endcomment -%}
  <section class="ac-disclosure-band">
    <div class="ac-wrap">
      <div class="ac-disclosure-box">
        <div class="ac-disc-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
        </div>
        <div>
          <p>
            <strong>Este programa NO es un seguro de gastos médicos.</strong> No está diseñado para reemplazar seguros ni cumple con los requisitos de cobertura mínima obligatoria de la Ley de Cuidado de Salud Asequible. Proporciona descuentos y tarifas preferenciales exclusivamente en la red de proveedores de salud contratados por <strong>New Benefits, Ltd.</strong> Cada miembro es responsable de pagar el costo total de los servicios médicos con descuento en el momento de recibirlos. Para conocer el listado completo de revelaciones legales, <a href="http://content.newbenefits.com/feed.aspx?hash=1nCjynVyHgD3qMTJC7SQg" target="_blank" rel="noopener">haga clic aquí</a>. Organización del Plan de Descuento: New Benefits, Ltd., Attn: Compliance Department, PO Box 803475, Dallas, TX 75380-3475.
          </p>
        </div>
      </div>
    </div>
  </section>

  {%- comment -%}============ INFO & BENEFITS ============{%- endcomment -%}
  <section class="ac-band">
    <div class="ac-wrap">
      <div class="ac-info-grid">
        {%- liquid
          assign info_img = ''
          if section.settings.info_image != blank
            assign info_img = section.settings.info_image | image_url: width: 1000
          else
            assign info_img = section.settings.info_image_url
          endif
        -%}
        <div class="ac-info-media acg-reveal">
          {%- if info_img != blank -%}<img src="{{ info_img }}" alt="Atención médica y bienestar familiar" loading="lazy">{%- endif -%}
        </div>
        <div class="ac-info-body ac-reveal">
          <span class="ac-eyebrow">{{ section.settings.info_eyebrow }}</span>
          <h2>{{ section.settings.info_title }}</h2>
          <p>{{ section.settings.info_description }}</p>
          
          <div class="ac-features">
            <div class="ac-feature">
              <div class="ac-feat-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
              </div>
              <div class="ac-feat-text">
                <h4>Beneficios Flexibles</h4>
                <p>Planes diseñados a la medida para cubrir desde necesidades médicas diarias hasta servicios complementarios para el hogar.</p>
              </div>
            </div>
            <div class="ac-feature">
              <div class="ac-feat-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
              </div>
              <div class="ac-feat-text">
                <h4>Cobertura de Dependientes</h4>
                <p>Agrega fácilmente a miembros de tu familia para extender los descuentos de salud y el bienestar a todos tus seres queridos.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  {%- comment -%}============ PROCESO DE COMPRA ============{%- endcomment -%}
  {%- assign timeline_blocks = section.blocks | where: 'type', 'timeline_step' -%}
  {%- if timeline_blocks.size > 0 -%}
    <section class="ac-band ac-band--gray">
      <div class="ac-wrap">
        <div class="ac-section-head ac-reveal">
          <h2>{{ section.settings.timeline_title }}</h2>
          {%- if section.settings.timeline_subtitle != blank -%}<p>{{ section.settings.timeline_subtitle }}</p>{%- endif -%}
        </div>
        
        <div class="ac-process">
          {%- for block in timeline_blocks -%}
            <div class="ac-process-card ac-reveal" {{ block.shopify_attributes }}>
              <div class="ac-proc-num">0{{ forloop.index }}</div>
              <h3>{{ block.settings.title }}</h3>
              <p>{{ block.settings.description }}</p>
            </div>
          {%- endfor -%}
        </div>
      </div>
    </section>
  {%- endif -%}

  {%- comment -%}============ CONTACT / REGISTRATION FORM ============{%- endcomment -%}
  <section class="ac-band" id="{{ contact_anchor | remove: '#' }}">
    <div class="ac-wrap">
      <div class="ac-section-head ac-reveal">
        <h2>{{ section.settings.form_title }}</h2>
        {%- if section.settings.form_subtitle != blank -%}<p>{{ section.settings.form_subtitle }}</p>{%- endif -%}
      </div>
      
      <div class="ac-form-box ac-reveal">
        {%- form 'contact', id: 'care-contact-form' -%}
          {%- if form.posted_successfully? -%}
            <div class="ac-form-success">{{ section.settings.form_success }}</div>
          {%- endif -%}
          
          <div class="ac-form-grid">
            <div class="ac-field">
              <label>Nombre Completo</label>
              <input type="text" name="contact[name]" required placeholder="Ej. Ana Beltrán">
            </div>
            <div class="ac-field">
              <label>Correo Electrónico</label>
              <input type="email" name="contact[email]" required placeholder="Ej. ana@dominio.com">
            </div>
            <div class="ac-field">
              <label>Teléfono / WhatsApp</label>
              <input type="tel" name="contact[phone]" placeholder="Ej. 55 9876 5432">
            </div>
            <div class="ac-field">
              <label>Plan de Interés</label>
              <select name="contact[plan_type]">
                <option value="Paquete Salud Briotech">Paquete Salud Briotech</option>
                <option value="Seguros Complementarios Aflac/UHOne">Seguros Complementarios Aflac/UHOne</option>
                <option value="Homezie - Cuidados del Hogar">Homezie - Cuidados del Hogar</option>
                <option value="Todo Incluido">Todo Incluido</option>
              </select>
            </div>
            <div class="ac-field">
              <label>Número de Dependientes</label>
              <select name="contact[dependents]">
                <option value="Solo Yo">Solo Yo</option>
                <option value="Yo + 1 Dependiente">Yo + 1 Dependiente</option>
                <option value="Yo + 2 Dependientes">Yo + 2 Dependientes</option>
                <option value="Familia Completa (Más de 3)">Familia Completa (Más de 3)</option>
              </select>
            </div>
            <div class="ac-field ac-span2">
              <label>Preguntas / Mensaje adicional</label>
              <textarea name="contact[body]" placeholder="Escribe aquí tus dudas o el tipo de beneficio médico que estás buscando..."></textarea>
            </div>
          </div>
          
          <div class="ac-form-actions">
            <button type="submit" class="ac-btn ac-btn--primary">{{ section.settings.form_btn_text }}</button>
          </div>
        {%- endform -%}
      </div>
    </div>
  </section>

</div>

<script>
  (function(){
    var root = document.getElementById('care-{{ section.id }}');
    if(!root) return;
    
    // Reveal animations
    var els = root.querySelectorAll('.ac-reveal');
    if(!('IntersectionObserver' in window)){ 
      els.forEach(function(e){ e.classList.add('ac-in'); }); 
      return; 
    }
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(en){
        if(en.isIntersecting){ 
          en.target.classList.add('ac-in'); 
          io.unobserve(en.target); 
        }
      });
    }, { threshold: 0.08 });
    els.forEach(function(e){ io.observe(e); });

    // Smooth scroll for anchors
    root.querySelectorAll('a[data-ac-scroll]').forEach(function(a){
      a.addEventListener('click', function(ev){
        var href = a.getAttribute('href') || '';
        if(href.charAt(0) !== '#') return;
        var target = document.getElementById(href.slice(1));
        if(!target) return;
        ev.preventDefault();
        var y = target.getBoundingClientRect().top + window.pageYOffset - 24;
        window.scrollTo({ top: y, behavior: 'smooth' });
      });
    });
  })();
</script>

{% schema %}
{
  "name": "Aylesva Care",
  "tag": "section",
  "class": "aylesva-care-section",
  "settings": [
    { "type": "header", "content": "Diseño y Colores" },
    { "type": "color", "id": "color_red", "label": "Rojo Vino (Principal)", "default": "#7C1922" },
    { "type": "color", "id": "color_blue", "label": "Azul Acero (Texto)", "default": "#1C4170" },
    { "type": "color", "id": "color_light", "label": "Gris Claro", "default": "#F8FAFC" },
    { "type": "color", "id": "color_white", "label": "Blanco / Fondo", "default": "#FFFFFF" },
    { "type": "color", "id": "color_accent", "label": "Verde (Acento)", "default": "#4E8424" },

    { "type": "header", "content": "1 · Hero" },
    { "type": "text", "id": "hero_eyebrow", "label": "Subtítulo Hero", "default": "AYLESVA CARE" },
    { "type": "text", "id": "hero_title", "label": "Título Principal", "default": "Protección y Bienestar Integral para ti y tu Familia" },
    { "type": "textarea", "id": "hero_subtitle", "label": "Descripción Hero", "default": "Accede a los mejores paquetes de beneficios de salud, hogar y seguros complementarios de la mano de New Benefits desde solo $20 USD." },
    { "type": "text", "id": "hero_btn1_text", "label": "Botón Principal", "default": "Solicitar Información" },
    { "type": "url", "id": "hero_btn1_link", "label": "Enlace Botón Principal" },
    { "type": "text", "id": "hero_btn2_text", "label": "Botón Secundario", "default": "Conocer Beneficios" },
    { "type": "url", "id": "hero_btn2_link", "label": "Enlace Botón Secundario" },
    { "type": "image_picker", "id": "hero_image", "label": "Imagen de Fondo Hero" },
    { "type": "text", "id": "hero_image_url", "label": "URL Alternativa Fondo Hero" },

    { "type": "header", "content": "2 · Paquetes y Planes" },
    { "type": "text", "id": "props_title", "label": "Título Sección", "default": "Planes de Beneficios de Salud y Hogar" },
    { "type": "text", "id": "props_subtitle", "label": "Subtítulo Sección", "default": "Encuentra opciones diseñadas para cuidar tu salud diaria, protegerte ante accidentes y dar soporte a tu hogar." },

    { "type": "header", "content": "3 · Información General" },
    { "type": "text", "id": "info_eyebrow", "label": "Subtítulo Sección Info", "default": "RESPALDO INTEGRAL" },
    { "type": "text", "id": "info_title", "label": "Título Sección Info", "default": "Un Ecosistema de Salud y Descuentos" },
    { "type": "textarea", "id": "info_description", "label": "Descripción Info", "default": "New Benefits es el principal proveedor de planes de descuento en salud en los Estados Unidos. A través de Aylesva Care, te conectamos directamente con servicios de consultas y telemedicina, descuentos farmacéuticos y seguros suplementarios de líderes de la industria." },
    { "type": "image_picker", "id": "info_image", "label": "Imagen de Sección Info" },
    { "type": "text", "id": "info_image_url", "label": "URL Alternativa Imagen Info" },

    { "type": "header", "content": "4 · Proceso de Registro" },
    { "type": "text", "id": "timeline_title", "label": "Pasos para Registrarte" },
    { "type": "text", "id": "timeline_subtitle", "label": "Subtítulo del Proceso" },

    { "type": "header", "content": "5 · Formulario de Contacto" },
    { "type": "text", "id": "form_title", "label": "Solicita tu Asesoría Personalizada" },
    { "type": "text", "id": "form_subtitle", "label": "Subtítulo del Formulario" },
    { "type": "text", "id": "form_btn_text", "label": "Texto del Botón Enviar", "default": "Solicitar Información" },
    { "type": "text", "id": "form_success", "label": "Mensaje de Éxito", "default": "¡Gracias! Tu solicitud ha sido recibida con éxito. Un agente especializado de Aylesva Care se pondrá en contacto contigo muy pronto." }
  ],
  "blocks": [
    {
      "type": "package_card",
      "name": "Paquete de Beneficios",
      "settings": [
        { "type": "text", "id": "title", "label": "Nombre del Paquete", "default": "Health & Household" },
        { "type": "textarea", "id": "description", "label": "Descripción", "default": "Beneficios de salud diaria, telemedicina 24/7, consultas médicas preferenciales y productos Briotech de grado médico." },
        { "type": "text", "id": "price", "label": "Precio Inicial", "default": "$20" },
        { "type": "checkbox", "id": "featured_badge", "label": "Marcar como Popular", "default": true },
        { "type": "image_picker", "id": "image", "label": "Imagen del Paquete" },
        { "type": "text", "id": "image_url", "label": "URL Alternativa de Imagen" }
      ]
    },
    {
      "type": "timeline_step",
      "name": "Paso de Registro",
      "settings": [
        { "type": "text", "id": "title", "label": "Título", "default": "1. Selección de Plan" },
        { "type": "textarea", "id": "description", "label": "Descripción", "default": "Elige el plan de beneficios que mejor se adapte a ti y tus dependientes." }
      ]
    }
  ]
}
{% endschema %}
```

### Page Template Code: `page.aylesva-care.json`
Create a new template file in your theme under `Templates/page.aylesva-care.json`:

```json
{
  "sections": {
    "main": {
      "type": "aylesva-care",
      "settings": {
        "color_red": "#7C1922",
        "color_blue": "#1C4170",
        "color_light": "#F8FAFC",
        "color_white": "#FFFFFF",
        "color_accent": "#4E8424",
        "hero_eyebrow": "AYLESVA CARE",
        "hero_title": "Protección y Bienestar Integral para ti y tu Familia",
        "hero_subtitle": "Accede a los mejores paquetes de beneficios de salud, hogar y seguros complementarios de la mano de New Benefits desde solo $20 USD.",
        "hero_btn1_text": "Solicitar Información",
        "hero_btn2_text": "Conocer Beneficios",
        "hero_image_url": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?auto=format&fit=crop&w=1800&q=80",
        "props_title": "Planes de Beneficios de Salud y Hogar",
        "props_subtitle": "Encuentra opciones diseñadas para cuidar tu salud diaria, protegerte ante accidentes y dar soporte a tu hogar.",
        "info_eyebrow": "RESPALDO INTEGRAL",
        "info_title": "Un Ecosistema de Salud y Descuentos",
        "info_description": "New Benefits es el principal proveedor de planes de descuento en salud en los Estados Unidos. A través de Aylesva Care, te conectamos directamente con servicios de consultas y telemedicina, descuentos farmacéuticos y seguros suplementarios de líderes de la industria.",
        "info_image_url": "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=1000&q=80",
        "timeline_title": "Pasos para Registrarte",
        "timeline_subtitle": "Un proceso de activación simple para comenzar a disfrutar de tus beneficios.",
        "form_title": "Solicita tu Asesoría Personalizada",
        "form_subtitle": "Compártenos tus datos para presentarte los planes de descuentos médicos y seguros suplementarios.",
        "form_btn_text": "Solicitar Información",
        "form_success": "¡Gracias! Tu solicitud ha sido recibida con éxito. Un agente especializado de Aylesva Care se pondrá en contacto contigo muy pronto."
      },
      "blocks": {
        "pack_1": {
          "type": "package_card",
          "settings": {
            "title": "Health & Household",
            "description": "Beneficios de salud diaria, telemedicina 24/7, consultas médicas preferenciales y productos Briotech de grado médico para el cuidado diario.",
            "price": "$20",
            "featured_badge": true,
            "image_url": "https://images.unsplash.com/photo-1471864190281-a93a3070b6de?auto=format&fit=crop&w=800&q=80"
          }
        },
        "pack_2": {
          "type": "package_card",
          "settings": {
            "title": "Supplemental Insurance",
            "description": "Planes complementarios con el respaldo de Aflac y UHOne diseñados para cubrir accidentes, hospitalización y gastos de visión/dentales.",
            "price": "$35",
            "featured_badge": true,
            "image_url": "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?auto=format&fit=crop&w=800&q=80"
          }
        },
        "pack_3": {
          "type": "package_card",
          "settings": {
            "title": "Homezie",
            "description": "Descuentos y beneficios integrales para el cuidado, soporte y economía de tu hogar, facilitando el acceso a técnicos y reparaciones.",
            "price": "$15",
            "featured_badge": false,
            "image_url": "https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=800&q=80"
          }
        },
        "step_1": {
          "type": "timeline_step",
          "settings": {
            "title": "1. Elección de Plan",
            "description": "Selecciona entre nuestros paquetes de beneficios médicos y de protección complementaria."
          }
        },
        "step_2": {
          "type": "timeline_step",
          "settings": {
            "title": "2. Formulario de Inscripción",
            "description": "Proporciona tus datos básicos y los de tus dependientes familiares para abrir tu perfil."
          }
        },
        "step_3": {
          "type": "timeline_step",
          "settings": {
            "title": "3. Activación de Beneficios",
            "description": "Recibe tu tarjeta digital de Aylesva Care y empieza a ahorrar en consultas y medicamentos."
          }
        }
      },
      "block_order": [
        "pack_1",
        "pack_2",
        "pack_3",
        "step_1",
        "step_2",
        "step_3"
      ]
    }
  },
  "order": [
    "main"
  ]
}
```

---

## 3. All Cities Global Landing Page

### Section Code: `allcities-global.liquid`
Create a new file in your theme under `Sections/allcities-global.liquid`:

```liquid
{% comment %}
  ============================================================
  All Cities Global — Premium Real Estate Landing Section
  Fully custom, responsive, beautiful CSS & hover animations.
  Translate & Adapt compatible, editable via Shopify Customizer.
  Repeatable content uses blocks (trust badge, property, timeline).
  ============================================================
{% endcomment %}

{%- liquid
  assign brand_navy = section.settings.color_navy
  assign accent_gold = section.settings.color_gold
  assign light_bg = section.settings.color_light
  assign white_bg = section.settings.color_white
  assign contact_anchor = '#allcities-contact-' | append: section.id
-%}

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

<style>
  #allcities-{{ section.id }} {
    --acg-navy: {{ brand_navy }};
    --acg-gold: {{ accent_gold }};
    --acg-light: {{ light_bg }};
    --acg-white: {{ white_bg }};
    --acg-ink: #1E293B;
    --acg-muted: #64748B;
    --acg-line: rgba(14,49,83,.08);
    --acg-radius: 24px;
    --acg-radius-sm: 16px;
    --acg-shadow: 0 4px 20px rgba(14,49,83,.04), 0 10px 30px rgba(14,49,83,.05);
    --acg-shadow-hover: 0 24px 50px -12px rgba(14,49,83,.18);
    --acg-maxw: 1240px;
    font-family: 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    color: var(--acg-ink);
    background: var(--acg-white);
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
  }
  #allcities-{{ section.id }} * { box-sizing: border-box; }
  #allcities-{{ section.id }} .acg-wrap { max-width: var(--acg-maxw); margin: 0 auto; padding: 0 24px; }

  /* ---------- TYPOGRAPHY & BUTTONS ---------- */
  #allcities-{{ section.id }} h1, 
  #allcities-{{ section.id }} h2, 
  #allcities-{{ section.id }} h3, 
  #allcities-{{ section.id }} h4 { margin: 0; line-height: 1.25; font-weight: 800; color: var(--acg-navy); letter-spacing: -0.5px; }
  #allcities-{{ section.id }} p { margin: 0; line-height: 1.65; }
  #allcities-{{ section.id }} .acg-eyebrow { display: inline-block; font-size: 13px; font-weight: 800; letter-spacing: 2.5px; text-transform: uppercase; color: var(--acg-gold); margin-bottom: 12px; }
  
  #allcities-{{ section.id }} .acg-btn { display: inline-flex; align-items: center; justify-content: center; font-size: 15px; font-weight: 700; padding: 14px 30px; border-radius: 30px; text-decoration: none; transition: all .3s cubic-bezier(0.16, 1, 0.3, 1); cursor: pointer; border: none; font-family: inherit; }
  #allcities-{{ section.id }} .acg-btn--primary { background: var(--acg-navy); color: #fff; box-shadow: 0 4px 14px rgba(14,49,83,.25); }
  #allcities-{{ section.id }} .acg-btn--primary:hover { background: var(--acg-gold); transform: translateY(-2px); box-shadow: 0 6px 20px rgba(197,164,126,.4); }
  #allcities-{{ section.id }} .acg-btn--outline { background: transparent; color: var(--acg-navy); border: 2px solid var(--acg-navy); }
  #allcities-{{ section.id }} .acg-btn--outline:hover { background: var(--acg-navy); color: #fff; transform: translateY(-2px); }

  /* ---------- LAYOUT BANDS ---------- */
  #allcities-{{ section.id }} .acg-band { padding: clamp(60px,8vw,100px) 0; }
  #allcities-{{ section.id }} .acg-band--gray { background: var(--acg-light); }
  #allcities-{{ section.id }} .acg-section-head { text-align: center; max-width: 720px; margin: 0 auto clamp(40px,6vw,68px); }
  #allcities-{{ section.id }} .acg-section-head h2 { font-size: clamp(28px,3.5vw,40px); }
  #allcities-{{ section.id }} .acg-section-head p { font-size: 16px; color: var(--acg-muted); margin-top: 14px; }

  /* ---------- REVEAL ANIMATIONS ---------- */
  #allcities-{{ section.id }} .acg-reveal { opacity: 0; transform: translateY(28px); transition: opacity .75s cubic-bezier(0.16, 1, 0.3, 1), transform .75s cubic-bezier(0.16, 1, 0.3, 1); }
  #allcities-{{ section.id }} .acg-reveal.acg-in { opacity: 1; transform: translateY(0); }

  /* ---------- HERO SECTION ---------- */
  #allcities-{{ section.id }} .acg-hero { position: relative; padding: clamp(70px,10vw,140px) 0; overflow: hidden; background-size: cover; background-position: center; display: flex; align-items: center; min-height: clamp(500px, 75vh, 780px); }
  #allcities-{{ section.id }} .acg-hero::before { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(14,49,83,0.78) 0%, rgba(14,49,83,0.45) 50%, rgba(14,49,83,0.85) 100%); z-index: 1; }
  #allcities-{{ section.id }} .acg-hero-content { position: relative; z-index: 2; max-width: 760px; color: #fff; }
  #allcities-{{ section.id }} .acg-hero-content h1 { font-size: clamp(36px,5vw,60px); color: #fff; font-weight: 800; letter-spacing: -1.5px; }
  #allcities-{{ section.id }} .acg-hero-content p { font-size: clamp(16px,2.2vw,20px); line-height: 1.6; color: rgba(255,255,255,0.9); margin: 24px 0 36px; font-weight: 400; }
  #allcities-{{ section.id }} .acg-hero-cta { display: flex; flex-wrap: wrap; gap: 16px; }
  #allcities-{{ section.id }} .acg-hero-cta .acg-btn--outline { border-color: #fff; color: #fff; }
  #allcities-{{ section.id }} .acg-hero-cta .acg-btn--outline:hover { background: #fff; color: var(--acg-navy); }

  /* ---------- PROPERTIES GRID (VILLAS) ---------- */
  #allcities-{{ section.id }} .acg-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 32px; }
  #allcities-{{ section.id }} .acg-card { background: var(--acg-white); border-radius: var(--acg-radius); overflow: hidden; box-shadow: var(--acg-shadow); border: 1px solid var(--acg-line); display: flex; flex-direction: column; height: 100%; transition: all .4s cubic-bezier(0.16, 1, 0.3, 1); position: relative; }
  
  /* HOVER ANIMATION FOR CARDS */
  #allcities-{{ section.id }} .acg-card:hover { transform: translateY(-10px); box-shadow: var(--acg-shadow-hover); border-color: var(--acg-gold); }
  
  #allcities-{{ section.id }} .acg-card-media { height: clamp(200px, 15vw, 240px); overflow: hidden; position: relative; background: var(--acg-light); }
  #allcities-{{ section.id }} .acg-card-media img { width: 100%; height: 100%; object-fit: cover; transition: transform .6s cubic-bezier(0.16, 1, 0.3, 1); }
  
  /* Zoom image on hover */
  #allcities-{{ section.id }} .acg-card:hover .acg-card-media img { transform: scale(1.08); }
  
  #allcities-{{ section.id }} .acg-badge { position: absolute; top: 16px; left: 16px; padding: 6px 12px; border-radius: 30px; font-size: 11px; font-weight: 800; text-transform: uppercase; background: var(--acg-gold); color: #fff; z-index: 2; box-shadow: 0 4px 8px rgba(0,0,0,0.1); letter-spacing: 0.5px; }
  #allcities-{{ section.id }} .acg-card-body { padding: 28px; display: flex; flex-direction: column; flex-grow: 1; }
  #allcities-{{ section.id }} .acg-card-body h3 { font-size: 22px; margin-bottom: 8px; font-weight: 700; transition: color .3s; }
  
  #allcities-{{ section.id }} .acg-card:hover .acg-card-body h3 { color: var(--acg-gold); }
  
  #allcities-{{ section.id }} .acg-loc { font-size: 14px; color: var(--acg-muted); margin-bottom: 20px; display: flex; align-items: center; gap: 6px; }
  #allcities-{{ section.id }} .acg-loc svg { width: 15px; height: 15px; color: var(--acg-gold); flex-shrink: 0; }
  
  /* Specs block */
  #allcities-{{ section.id }} .acg-specs { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; padding: 16px 0; border-top: 1px solid var(--acg-line); border-bottom: 1px solid var(--acg-line); margin-bottom: 20px; background: var(--acg-light); border-radius: var(--acg-radius-sm); padding-left: 12px; padding-right: 12px; transition: background .3s; }
  #allcities-{{ section.id }} .acg-card:hover .acg-specs { background: rgba(14,49,83,0.03); }
  
  #allcities-{{ section.id }} .acg-spec { display: flex; flex-direction: column; align-items: center; gap: 4px; font-size: 13px; font-weight: 700; text-align: center; }
  #allcities-{{ section.id }} .acg-spec-label { font-size: 10px; text-transform: uppercase; color: var(--acg-muted); font-weight: 600; letter-spacing: 0.5px; }
  #allcities-{{ section.id }} .acg-spec svg { width: 18px; height: 18px; color: var(--acg-navy); transition: transform .3s; }
  
  /* Bounce icons on hover */
  #allcities-{{ section.id }} .acg-card:hover .acg-spec svg { transform: translateY(-2px); }

  #allcities-{{ section.id }} .acg-price-label { font-size: 12px; text-transform: uppercase; color: var(--acg-muted); font-weight: 700; letter-spacing: 0.5px; }
  #allcities-{{ section.id }} .acg-price { font-size: clamp(20px, 2.5vw, 24px); font-weight: 800; color: var(--acg-navy); margin-top: 4px; display: flex; align-items: baseline; gap: 4px; }
  #allcities-{{ section.id }} .acg-price span { font-size: 14px; font-weight: 600; color: var(--acg-gold); }
  
  #allcities-{{ section.id }} .acg-card-footer { display: flex; align-items: center; justify-content: space-between; margin-top: auto; padding-top: 20px; }
  #allcities-{{ section.id }} .acg-card-link { font-size: 14.5px; font-weight: 800; color: var(--acg-navy); text-decoration: none; display: inline-flex; align-items: center; gap: 6px; transition: color .2s; }
  #allcities-{{ section.id }} .acg-card-link svg { width: 16px; height: 16px; transition: transform .3s cubic-bezier(0.16, 1, 0.3, 1); }
  
  #allcities-{{ section.id }} .acg-card:hover .acg-card-link { color: var(--acg-gold); }
  #allcities-{{ section.id }} .acg-card:hover .acg-card-link svg { transform: translateX(5px); color: var(--acg-gold); }

  /* ---------- INFO / EXPERIENCE SECTION ---------- */
  #allcities-{{ section.id }} .acg-info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: clamp(32px,6vw,80px); align-items: center; }
  #allcities-{{ section.id }} .acg-info-media { position: relative; border-radius: var(--acg-radius); overflow: hidden; box-shadow: var(--acg-shadow-hover); aspect-ratio: 4/3; }
  #allcities-{{ section.id }} .acg-info-media img { width: 100%; height: 100%; object-fit: cover; }
  #allcities-{{ section.id }} .acg-info-body h2 { font-size: clamp(26px,3vw,38px); margin-bottom: 24px; }
  #allcities-{{ section.id }} .acg-info-body p { color: var(--acg-muted); margin-bottom: 20px; }
  
  /* Expat features list */
  #allcities-{{ section.id }} .acg-features { display: flex; flex-direction: column; gap: 16px; margin-top: 28px; }
  #allcities-{{ section.id }} .acg-feature { display: flex; gap: 14px; }
  #allcities-{{ section.id }} .acg-feat-icon { width: 38px; height: 38px; border-radius: 10px; background: rgba(14,49,83,0.06); color: var(--acg-navy); display: grid; place-items: center; flex-shrink: 0; }
  #allcities-{{ section.id }} .acg-feat-icon svg { width: 20px; height: 20px; }
  #allcities-{{ section.id }} .acg-feat-text h4 { font-size: 16px; font-weight: 700; margin-bottom: 4px; }
  #allcities-{{ section.id }} .acg-feat-text p { font-size: 14px; color: var(--acg-muted); margin: 0; }

  /* ---------- TIMELINE PROCESS ---------- */
  #allcities-{{ section.id }} .acg-process { display: grid; grid-template-columns: repeat(3, 1fr); gap: 32px; position: relative; }
  #allcities-{{ section.id }} .acg-process-card { background: var(--acg-white); padding: 32px; border-radius: var(--acg-radius); border: 1px solid var(--acg-line); box-shadow: var(--acg-shadow); transition: all .3s; }
  #allcities-{{ section.id }} .acg-process-card:hover { transform: translateY(-4px); border-color: var(--acg-gold); }
  #allcities-{{ section.id }} .acg-proc-num { font-size: 38px; font-weight: 800; color: rgba(197,164,126,0.35); margin-bottom: 16px; line-height: 1; }
  #allcities-{{ section.id }} .acg-process-card h3 { font-size: 18px; font-weight: 700; margin-bottom: 10px; }
  #allcities-{{ section.id }} .acg-process-card p { font-size: 14px; color: var(--acg-muted); }

  /* ---------- REGISTRATION FORM ---------- */
  #allcities-{{ section.id }} .acg-form-box { max-width: 820px; margin: 0 auto; background: var(--acg-white); border: 1px solid var(--acg-line); border-radius: 26px; box-shadow: var(--acg-shadow-hover); padding: clamp(28px,4vw,56px); }
  #allcities-{{ section.id }} .acg-form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
  #allcities-{{ section.id }} .acg-field { display: flex; flex-direction: column; gap: 6px; }
  #allcities-{{ section.id }} .acg-field.acg-span2 { grid-column: 1 / -1; }
  #allcities-{{ section.id }} .acg-field label { font-size: 13.5px; font-weight: 700; color: var(--acg-navy); }
  #allcities-{{ section.id }} .acg-field input, 
  #allcities-{{ section.id }} .acg-field select, 
  #allcities-{{ section.id }} .acg-field textarea { font-family: inherit; font-size: 15px; color: var(--acg-ink); background: var(--acg-light); border: 1px solid var(--acg-line); border-radius: 12px; padding: 13px 15px; transition: all .25s ease; width: 100%; }
  #allcities-{{ section.id }} .acg-field input:focus, 
  #allcities-{{ section.id }} .acg-field select:focus, 
  #allcities-{{ section.id }} .acg-field textarea:focus { outline: none; border-color: var(--acg-gold); background: #fff; box-shadow: 0 0 0 4px rgba(197,164,126,.15); }
  #allcities-{{ section.id }} .acg-field textarea { resize: vertical; min-height: 120px; }
  #allcities-{{ section.id }} .acg-form-actions { margin-top: 32px; text-align: center; }
  #allcities-{{ section.id }} .acg-form-success { background: rgba(16,185,129,.10); border: 1px solid rgba(16,185,129,.2); color: #059669; border-radius: 12px; padding: 16px 18px; font-weight: 600; margin-bottom: 24px; text-align: center; }

  /* ---------- RESPONSIVE DESIGN ---------- */
  @media (max-width: 990px) {
    #allcities-{{ section.id }} .acg-grid { grid-template-columns: 1fr; gap: 24px; max-width: 420px; margin: 0 auto; }
    #allcities-{{ section.id }} .acg-info-grid { grid-template-columns: 1fr; }
    #allcities-{{ section.id }} .acg-process { grid-template-columns: 1fr; gap: 20px; }
  }
  @media (max-width: 580px) {
    #allcities-{{ section.id }} .acg-form-grid { grid-template-columns: 1fr; }
    #allcities-{{ section.id }} .acg-form-grid .acg-field { grid-column: auto !important; }
    #allcities-{{ section.id }} .acg-hero-cta { flex-direction: column; }
    #allcities-{{ section.id }} .acg-hero-cta .acg-btn { width: 100%; }
  }
</style>

<div id="allcities-{{ section.id }}">

  {%- comment -%}============ HERO SECTION ============{%- endcomment -%}
  {%- liquid
    assign hero_bg = ''
    if section.settings.hero_image != blank
      assign hero_bg = section.settings.hero_image | image_url: width: 1800
    else
      assign hero_bg = section.settings.hero_image_url
    endif
  -%}
  <section class="acg-hero" style="background-image: url('{{ hero_bg }}');">
    <div class="acg-wrap">
      <div class="acg-hero-content acg-reveal">
        {%- if section.settings.hero_eyebrow != blank -%}<span class="acg-eyebrow">{{ section.settings.hero_eyebrow }}</span>{%- endif -%}
        <h1>{{ section.settings.hero_title }}</h1>
        <p>{{ section.settings.hero_subtitle }}</p>
        <div class="acg-hero-cta">
          {%- if section.settings.hero_btn1_text != blank -%}
            <a href="{{ section.settings.hero_btn1_link | default: contact_anchor }}" class="acg-btn acg-btn--primary">{{ section.settings.hero_btn1_text }}</a>
          {%- endif -%}
          {%- if section.settings.hero_btn2_text != blank -%}
            <a href="{{ section.settings.hero_btn2_link | default: '#villas-featured' }}" class="acg-btn acg-btn--outline" data-acg-scroll>{{ section.settings.hero_btn2_text }}</a>
          {%- endif -%}
        </div>
      </div>
    </div>
  </section>

  {%- comment -%}============ PROPERTIES (VILLAS) ============{%- endcomment -%}
  {%- assign property_blocks = section.blocks | where: 'type', 'property_card' -%}
  {%- if property_blocks.size > 0 -%}
    <section class="acg-band acg-band--gray" id="villas-featured">
      <div class="acg-wrap">
        <div class="acg-section-head acg-reveal">
          <h2>{{ section.settings.props_title }}</h2>
          {%- if section.settings.props_subtitle != blank -%}<p>{{ section.settings.props_subtitle }}</p>{%- endif -%}
        </div>
        
        <div class="acg-grid">
          {%- for block in property_blocks -%}
            {%- liquid
              assign card_img = ''
              if block.settings.image != blank
                assign card_img = block.settings.image | image_url: width: 600
              else
                assign card_img = block.settings.image_url
              endif
            -%}
            <div class="acg-card acg-reveal" {{ block.shopify_attributes }}>
              <div class="acg-card-media">
                {%- if card_img != blank -%}<img src="{{ card_img }}" alt="{{ block.settings.title | escape }}" loading="lazy">{%- endif -%}
                {%- if block.settings.featured_badge -%}<span class="acg-badge">Destacada</span>{%- endif -%}
              </div>
              <div class="acg-card-body">
                <h3>{{ block.settings.title }}</h3>
                <div class="acg-loc">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
                  <span>{{ block.settings.location }}</span>
                </div>
                
                <div class="acg-specs">
                  <div class="acg-spec">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 4v16M22 4v16M2 8h20M2 14h20M6 8v6M18 8v6"/></svg>
                    <span>{{ block.settings.beds }}</span>
                    <span class="acg-spec-label">Hab</span>
                  </div>
                  <div class="acg-spec">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16v16H4zM4 10h16M10 4v16"/></svg>
                    <span>{{ block.settings.baths }}</span>
                    <span class="acg-spec-label">Baños</span>
                  </div>
                  <div class="acg-spec">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 3H3v18h18V3zM9 3v18M3 9h18"/></svg>
                    <span>{{ block.settings.area }}</span>
                    <span class="acg-spec-label">Sq Ft</span>
                  </div>
                </div>
                
                <div class="acg-card-footer">
                  <div>
                    <span class="acg-price-label">Precio Inicial</span>
                    <div class="acg-price">{{ block.settings.price }} <span>USD</span></div>
                  </div>
                  <a href="{{ contact_anchor }}" class="acg-card-link" data-acg-scroll>
                    <span>Saber más</span>
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                  </a>
                </div>
              </div>
            </div>
          {%- endfor -%}
        </div>
      </div>
    </section>
  {%- endif -%}

  {%- comment -%}============ INFO & BENEFITS ============{%- endcomment -%}
  <section class="acg-band">
    <div class="acg-wrap">
      <div class="acg-info-grid">
        {%- liquid
          assign info_img = ''
          if section.settings.info_image != blank
            assign info_img = section.settings.info_image | image_url: width: 1000
          else
            assign info_img = section.settings.info_image_url
          endif
        -%}
        <div class="acg-info-media acg-reveal">
          {%- if info_img != blank -%}<img src="{{ info_img }}" alt="Inversión inmobiliaria segura" loading="lazy">{%- endif -%}
        </div>
        <div class="acg-info-body acg-reveal">
          <span class="acg-eyebrow">{{ section.settings.info_eyebrow }}</span>
          <h2>{{ section.settings.info_title }}</h2>
          <p>{{ section.settings.info_description }}</p>
          
          <div class="acg-features">
            <div class="acg-feature">
              <div class="acg-feat-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
              </div>
              <div class="acg-feat-text">
                <h4>Fideicomiso & Estructura Legal</h4>
                <p>Te guiamos de forma segura en la adquisición de inmuebles bajo Fideicomiso o Corporación Mexicana.</p>
              </div>
            </div>
            <div class="acg-feature">
              <div class="acg-feat-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 8v4l3 3"/></svg>
              </div>
              <div class="acg-feat-text">
                <h4>Altos Niveles de Plusvalía</h4>
                <p>Inversiones estratégicas en ubicaciones de gran potencial e infraestructura de crecimiento para 2026 en adelante.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  {%- comment -%}============ PROCESO DE COMPRA ============{%- endcomment -%}
  {%- assign timeline_blocks = section.blocks | where: 'type', 'timeline_step' -%}
  {%- if timeline_blocks.size > 0 -%}
    <section class="acg-band acg-band--gray">
      <div class="acg-wrap">
        <div class="acg-section-head acg-reveal">
          <h2>{{ section.settings.timeline_title }}</h2>
          {%- if section.settings.timeline_subtitle != blank -%}<p>{{ section.settings.timeline_subtitle }}</p>{%- endif -%}
        </div>
        
        <div class="acg-process">
          {%- for block in timeline_blocks -%}
            <div class="acg-process-card acg-reveal" {{ block.shopify_attributes }}>
              <div class="acg-proc-num">0{{ forloop.index }}</div>
              <h3>{{ block.settings.title }}</h3>
              <p>{{ block.settings.description }}</p>
            </div>
          {%- endfor -%}
        </div>
      </div>
    </section>
  {%- endif -%}

  {%- comment -%}============ CONTACT / REGISTRATION FORM ============{%- endcomment -%}
  <section class="acg-band" id="{{ contact_anchor | remove: '#' }}">
    <div class="acg-wrap">
      <div class="acg-section-head acg-reveal">
        <h2>{{ section.settings.form_title }}</h2>
        {%- if section.settings.form_subtitle != blank -%}<p>{{ section.settings.form_subtitle }}</p>{%- endif -%}
      </div>
      
      <div class="acg-form-box acg-reveal">
        {%- form 'contact', id: 'allcities-contact-form' -%}
          {%- if form.posted_successfully? -%}
            <div class="acg-form-success">{{ section.settings.form_success }}</div>
          {%- endif -%}
          
          <div class="acg-form-grid">
            <div class="acg-field">
              <label>Nombre Completo</label>
              <input type="text" name="contact[name]" required placeholder="Ej. Carlos Mendoza">
            </div>
            <div class="acg-field">
              <label>Correo Electrónico</label>
              <input type="email" name="contact[email]" required placeholder="Ej. carlos@dominio.com">
            </div>
            <div class="acg-field">
              <label>Teléfono / WhatsApp</label>
              <input type="tel" name="contact[phone]" placeholder="Ej. 998 123 4567">
            </div>
            <div class="acg-field">
              <label>Ubicación de Interés</label>
              <select name="contact[destination]">
                <option value="Altarena - Sea of Cortez">Altarena - Sea of Cortez (Villas)</option>
                <option value="Riviera Maya">Riviera Maya / Cancún</option>
                <option value="Puerto Vallarta">Puerto Vallarta</option>
                <option value="Los Cabos">Los Cabos</option>
                <option value="Otro">Otro Destino</option>
              </select>
            </div>
            <div class="acg-field">
              <label>Presupuesto Estimado</label>
              <select name="contact[budget]">
                <option value="Under $300k">Menos de $300,000 USD</option>
                <option value="$300k - $500k">$300,000 - $500,000 USD</option>
                <option value="$500k - $800k">$500,000 - $800,000 USD</option>
                <option value="Over $800k">Más de $800,000 USD</option>
              </select>
            </div>
            <div class="acg-field">
              <label>Plazo de Inversión</label>
              <select name="contact[timeline]">
                <option value="Inmediato">Inmediato (menos de 3 meses)</option>
                <option value="3 a 6 meses">De 3 a 6 meses</option>
                <option value="6 a 12 meses">De 6 a 12 meses</option>
                <option value="Explorando">Solo explorando opciones</option>
              </select>
            </div>
            <div class="acg-field acg-span2">
              <label>Detalles / Comentarios adicionales</label>
              <textarea name="contact[body]" placeholder="Escribe tus preguntas o las características específicas que buscas en tu propiedad..."></textarea>
            </div>
          </div>
          
          <div class="acg-form-actions">
            <button type="submit" class="acg-btn acg-btn--primary">{{ section.settings.form_btn_text }}</button>
          </div>
        {%- endform -%}
      </div>
    </div>
  </section>

</div>

<script>
  (function(){
    var root = document.getElementById('allcities-{{ section.id }}');
    if(!root) return;
    
    // Reveal animations
    var els = root.querySelectorAll('.acg-reveal');
    if(!('IntersectionObserver' in window)){ 
      els.forEach(function(e){ e.classList.add('acg-in'); }); 
      return; 
    }
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(en){
        if(en.isIntersecting){ 
          en.target.classList.add('acg-in'); 
          io.unobserve(en.target); 
        }
      });
    }, { threshold: 0.08 });
    els.forEach(function(e){ io.observe(e); });

    // Smooth scroll for anchors
    root.querySelectorAll('a[data-acg-scroll]').forEach(function(a){
      a.addEventListener('click', function(ev){
        var href = a.getAttribute('href') || '';
        if(href.charAt(0) !== '#') return;
        var target = document.getElementById(href.slice(1));
        if(!target) return;
        ev.preventDefault();
        var y = target.getBoundingClientRect().top + window.pageYOffset - 24;
        window.scrollTo({ top: y, behavior: 'smooth' });
      });
    });
  })();
</script>

{% schema %}
{
  "name": "All Cities Global",
  "tag": "section",
  "class": "allcities-global-section",
  "settings": [
    { "type": "header", "content": "Diseño y Colores" },
    { "type": "color", "id": "color_navy", "label": "Azul Marino (Principal)", "default": "#0E3153" },
    { "type": "color", "id": "color_gold", "label": "Dorado (Acento)", "default": "#C5A47E" },
    { "type": "color", "id": "color_light", "label": "Gris Claro", "default": "#F8FAFC" },
    { "type": "color", "id": "color_white", "label": "Blanco / Fondo", "default": "#FFFFFF" },

    { "type": "header", "content": "1 · Hero" },
    { "type": "text", "id": "hero_eyebrow", "label": "Subtítulo Hero", "default": "BIENES RAÍCES EXCLUSIVOS" },
    { "type": "text", "id": "hero_title", "label": "Título Principal", "default": "Tu Santuario de Estilo de Vida en México y el Caribe" },
    { "type": "textarea", "id": "hero_subtitle", "label": "Descripción Hero", "default": "Encuentra la casa de tus sueños o tu próxima gran oportunidad de inversión. Te guiamos de forma segura en todo el proceso legal de compra." },
    { "type": "text", "id": "hero_btn1_text", "label": "Botón Principal", "default": "Iniciar Inversión" },
    { "type": "url", "id": "hero_btn1_link", "label": "Enlace Botón Principal" },
    { "type": "text", "id": "hero_btn2_text", "label": "Botón Secundario", "default": "Ver Propiedades" },
    { "type": "url", "id": "hero_btn2_link", "label": "Enlace Botón Secundario" },
    { "type": "image_picker", "id": "hero_image", "label": "Imagen de Fondo Hero" },
    { "type": "text", "id": "hero_image_url", "label": "URL Alternativa Fondo Hero" },

    { "type": "header", "content": "2 · Propiedades Destacadas" },
    { "type": "text", "id": "props_title", "label": "Título Sección", "default": "Propiedades para Cada Estilo de Vida" },
    { "type": "text", "id": "props_subtitle", "label": "Subtítulo Sección", "default": "Conoce los desarrollos residenciales más exclusivos y con mejor plusvalía del Mar de Cortés y el Caribe." },

    { "type": "header", "content": "3 · Información de Inversión y Fideicomiso" },
    { "type": "text", "id": "info_eyebrow", "label": "Subtítulo Sección Info", "default": "GUÍA Y SEGURIDAD" },
    { "type": "text", "id": "info_title", "label": "Título Sección Info", "default": "Inversión Inmobiliaria Transparente y Simplificada" },
    { "type": "textarea", "id": "info_description", "label": "Descripción Info", "default": "Adquirir una propiedad en el extranjero no tiene por qué ser complicado. En All Cities Global te brindamos el acompañamiento legal necesario para realizar adquisiciones transparentes mediante fideicomisos bancarios o estructuración corporativa, garantizando la seguridad de tu patrimonio." },
    { "type": "image_picker", "id": "info_image", "label": "Imagen de Sección Info" },
    { "type": "text", "id": "info_image_url", "label": "URL Alternativa Imagen Info" },

    { "type": "header", "content": "4 · Proceso de Compra" },
    { "type": "text", "id": "timeline_title", "label": "Título Proceso", "default": "Adquisición Segura en 3 Pasos" },
    { "type": "text", "id": "timeline_subtitle", "label": "Subtítulo Proceso", "default": "Un acompañamiento integral de principio a fin." },

    { "type": "header", "content": "5 · Formulario de Registro" },
    { "type": "text", "id": "form_title", "label": "Encuentra tu Propiedad Ideal" },
    { "type": "text", "id": "form_subtitle", "label": "Subtítulo del Formulario" },
    { "type": "text", "id": "form_btn_text", "label": "Texto del Botón Enviar", "default": "Solicitar Asesoría" },
    { "type": "text", "id": "form_success", "label": "Mensaje de Éxito", "default": "¡Gracias! Tu solicitud ha sido recibida con éxito. Un agente especializado de All Cities Global se pondrá en contacto contigo muy pronto." }
  ],
  "blocks": [
    {
      "type": "property_card",
      "name": "Propiedad",
      "settings": [
        { "type": "text", "id": "title", "label": "Nombre de la Propiedad", "default": "Villa Hai" },
        { "type": "text", "id": "location", "label": "Ubicación", "default": "Altarena, Sea of Cortez" },
        { "type": "text", "id": "beds", "label": "Recámaras (Hab)", "default": "3" },
        { "type": "text", "id": "baths", "label": "Baños", "default": "3.5" },
        { "type": "text", "id": "area", "label": "Área (Sq Ft)", "default": "2,615.43" },
        { "type": "text", "id": "price", "label": "Precio Inicial (USD)", "default": "$465,512" },
        { "type": "checkbox", "id": "featured_badge", "label": "Marcar como Destacada", "default": true },
        { "type": "image_picker", "id": "image", "label": "Imagen de la Propiedad" },
        { "type": "text", "id": "image_url", "label": "URL Alternativa de Imagen" }
      ]
    },
    {
      "type": "timeline_step",
      "name": "Paso de Proceso",
      "settings": [
        { "type": "text", "id": "title", "label": "Título", "default": "1. Selección y Perfil" },
        { "type": "textarea", "id": "description", "label": "Descripción", "default": "Definimos tus preferencias de estilo de vida, ubicación y presupuesto para filtrar las opciones ideales." }
      ]
    }
  ]
}
{% endschema %}
```
