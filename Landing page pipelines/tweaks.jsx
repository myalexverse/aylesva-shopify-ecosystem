// tweaks.jsx — Tweaks for the Aylesva landing page.
const { useEffect } = React;

const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
  "primary": "orange",
  "heroHeadline": "negocio",
  "blobs": true
}/*EDITMODE-END*/;

const PRIMARIES = {
  orange: { color: "#F4691F", deep: "#D9530E", shadow: "rgba(244,105,31,.34)" },
  pink:   { color: "#EC1E79", deep: "#C9156A", shadow: "rgba(236,30,121,.34)" },
  blue:   { color: "#1F74EB", deep: "#155FC9", shadow: "rgba(31,116,235,.34)" },
  green:  { color: "#29B24A", deep: "#1E9A3C", shadow: "rgba(41,178,74,.34)" },
};

const HEADLINES = {
  negocio:      'Haz que más personas conozcan <span class="grad-text">tu negocio.</span>',
  ecosistema:   'Un ecosistema. <span class="grad-text">Infinitas</span> formas de crecer.',
  clientes:     'Convierte tu visibilidad en <span class="grad-text">más clientes.</span>',
};

function App() {
  const [t, setTweak] = useTweaks(TWEAK_DEFAULTS);

  useEffect(() => {
    const p = PRIMARIES[t.primary] || PRIMARIES.orange;
    const r = document.documentElement.style;
    r.setProperty("--orange", p.color);
    r.setProperty("--orange-d", p.deep);
    r.setProperty("--shadow-orange", "0 10px 26px " + p.shadow);
  }, [t.primary]);

  useEffect(() => {
    const h1 = document.querySelector(".hero h1");
    if (h1) h1.innerHTML = HEADLINES[t.heroHeadline] || HEADLINES.negocio;
  }, [t.heroHeadline]);

  useEffect(() => {
    document.querySelectorAll(".blob, .dots").forEach((el) => {
      el.style.display = t.blobs ? "" : "none";
    });
  }, [t.blobs]);

  return (
    <TweaksPanel>
      <TweakSection label="Color principal (botones)" />
      <TweakColor
        label="Color del CTA"
        value={PRIMARIES[t.primary].color}
        options={Object.values(PRIMARIES).map((p) => p.color)}
        onChange={(hex) => {
          const key = Object.keys(PRIMARIES).find((k) => PRIMARIES[k].color === hex) || "orange";
          setTweak("primary", key);
        }}
      />
      <TweakSection label="Titular principal" />
      <TweakSelect
        label="Variante"
        value={t.heroHeadline}
        options={[
          { value: "negocio", label: "Conozcan tu negocio" },
          { value: "ecosistema", label: "Infinitas formas de crecer" },
          { value: "clientes", label: "Visibilidad en más clientes" },
        ]}
        onChange={(v) => setTweak("heroHeadline", v)}
      />
      <TweakSection label="Decoración" />
      <TweakToggle
        label="Formas de color (blobs)"
        value={t.blobs}
        onChange={(v) => setTweak("blobs", v)}
      />
    </TweaksPanel>
  );
}

ReactDOM.createRoot(document.getElementById("tweaks-root")).render(<App />);
