"""
═══════════════════════════════════════════════════════════════
  Herramienta visual para mover pines del mapa — Global States
  
  Ejecuta: python3 pin_editor.py
  Abre:    http://localhost:8500
  
  → Haz clic en el mapa para mover un pin
  → Presiona "Guardar cambios" y se actualiza en aylesva.mx
═══════════════════════════════════════════════════════════════
"""
import os, json, http.server, urllib.parse, threading, webbrowser, time
import requests as req
import urllib3
urllib3.disable_warnings()
from dotenv import load_dotenv
load_dotenv()

SHOP   = os.getenv("SHOP_NAME")
TOKEN  = os.getenv("ACCESS_TOKEN")
API    = os.getenv("API_VERSION", "2025-01")
THEME  = os.getenv("THEME_ID")
HEADERS = {"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"}
PORT   = 8500

# ─── Leer template actual de Shopify ─────────────────────
def get_template():
    url = f"https://{SHOP}/admin/api/{API}/themes/{THEME}/assets.json?asset[key]=templates/page.globalstates.json"
    r = req.get(url, headers=HEADERS, verify=False, timeout=30)
    return json.loads(r.json()["asset"]["value"])

def save_template(template):
    url = f"https://{SHOP}/admin/api/{API}/themes/{THEME}/assets.json"
    payload = {"asset": {"key": "templates/page.globalstates.json", "value": json.dumps(template, indent=2, ensure_ascii=False)}}
    r = req.put(url, json=payload, headers=HEADERS, verify=False, timeout=30)
    return r.status_code in [200, 201]

# ─── HTML de la herramienta ──────────────────────────────
def build_html(template):
    blocks = template["sections"]["main"]["blocks"]
    settings = template["sections"]["main"]["settings"]
    
    # Obtener pines y su data
    pins_data = []
    for key, block in blocks.items():
        if block.get("type") == "map_pin":
            s = block["settings"]
            pins_data.append({
                "id": key,
                "name": s.get("name", key),
                "status": s.get("status", ""),
                "x": s.get("pos_x", 50),
                "y": s.get("pos_y", 50),
            })
    
    map_image_ref = settings.get("map_image", "")
    # Obtener la URL real del CDN de la imagen del mapa
    map_url = "https://www.aylesva.com/cdn/shop/files/mapofmexico.jpg"
    
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Editor de Pines — Global States</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: 'Inter', sans-serif; background: #0F1B21; color: #fff; min-height: 100vh; display: flex; flex-direction: column; }}
  
  .header {{
    background: linear-gradient(135deg, #14262E 0%, #1a3340 100%);
    padding: 16px 24px;
    display: flex; align-items: center; justify-content: space-between;
    border-bottom: 1px solid rgba(192,138,62,.3);
  }}
  .header h1 {{ font-size: 18px; font-weight: 600; }}
  .header h1 span {{ color: #C08A3E; }}
  .header .status {{ font-size: 13px; color: rgba(255,255,255,.5); }}
  
  .toolbar {{
    background: #14262E;
    padding: 12px 24px;
    display: flex; align-items: center; gap: 16px;
    border-bottom: 1px solid rgba(255,255,255,.1);
  }}
  .toolbar .instructions {{
    flex: 1; font-size: 13px; color: rgba(255,255,255,.6);
  }}
  .toolbar .instructions b {{ color: #C08A3E; }}
  
  .btn-save {{
    background: linear-gradient(135deg, #C08A3E, #A0722E);
    color: #fff; border: none; padding: 10px 28px;
    border-radius: 6px; font-size: 14px; font-weight: 600;
    cursor: pointer; transition: all .2s;
    box-shadow: 0 4px 12px rgba(192,138,62,.3);
  }}
  .btn-save:hover {{ transform: translateY(-1px); box-shadow: 0 6px 20px rgba(192,138,62,.4); }}
  .btn-save:disabled {{ opacity: .5; cursor: default; transform: none; }}
  .btn-save.saved {{ background: linear-gradient(135deg, #2E7D32, #1B5E20); }}
  
  .editor {{
    flex: 1; display: flex; padding: 24px; gap: 24px;
    background: #0F1B21;
  }}
  
  .map-container {{
    flex: 1; position: relative; border-radius: 12px; overflow: hidden;
    background: #E5DCCB;
    box-shadow: 0 8px 32px rgba(0,0,0,.4);
    cursor: crosshair;
  }}
  .map-container img {{
    width: 100%; height: 100%; object-fit: contain; display: block;
  }}
  .map-overlay {{
    position: absolute; inset: 0; z-index: 2;
  }}
  
  .pin {{
    position: absolute; transform: translate(-50%, -50%);
    cursor: pointer; z-index: 5; transition: left .3s ease, top .3s ease;
  }}
  .pin.moving {{ transition: none; }}
  .pin .dot {{
    width: 20px; height: 20px; border-radius: 50%;
    background: #C08A3E; border: 3px solid #fff;
    box-shadow: 0 2px 8px rgba(0,0,0,.4);
    transition: transform .2s;
  }}
  .pin:hover .dot {{ transform: scale(1.3); }}
  .pin.selected .dot {{
    background: #fff; border-color: #C08A3E;
    box-shadow: 0 0 0 4px rgba(192,138,62,.4), 0 2px 8px rgba(0,0,0,.4);
    transform: scale(1.3);
  }}
  .pin .label {{
    position: absolute; left: 50%; transform: translateX(-50%);
    top: -32px; background: #14262E; color: #fff;
    font-size: 11px; font-weight: 600; padding: 4px 10px;
    border-radius: 4px; white-space: nowrap;
    box-shadow: 0 2px 8px rgba(0,0,0,.3);
    pointer-events: none;
  }}
  .pin .label::after {{
    content: ''; position: absolute; left: 50%; bottom: -4px;
    transform: translateX(-50%); border-left: 5px solid transparent;
    border-right: 5px solid transparent; border-top: 5px solid #14262E;
  }}
  
  .sidebar {{
    width: 280px; background: #14262E; border-radius: 12px;
    padding: 20px; overflow-y: auto;
    box-shadow: 0 8px 32px rgba(0,0,0,.3);
  }}
  .sidebar h2 {{
    font-size: 12px; letter-spacing: .2em; text-transform: uppercase;
    color: rgba(255,255,255,.4); margin-bottom: 16px;
  }}
  
  .pin-card {{
    background: rgba(255,255,255,.05);
    border: 1px solid rgba(255,255,255,.1);
    border-radius: 8px; padding: 14px; margin-bottom: 12px;
    cursor: pointer; transition: all .2s;
  }}
  .pin-card:hover {{ background: rgba(255,255,255,.08); }}
  .pin-card.selected {{
    border-color: #C08A3E;
    background: rgba(192,138,62,.1);
  }}
  .pin-card .name {{ font-weight: 600; font-size: 14px; margin-bottom: 2px; }}
  .pin-card .pin-status {{ font-size: 11px; color: rgba(255,255,255,.4); }}
  .pin-card .coords {{
    margin-top: 8px; font-size: 12px; color: #C08A3E;
    font-family: 'SF Mono', monospace;
  }}
  .pin-card .coords.changed {{ color: #4CAF50; font-weight: 600; }}
  
  .toast {{
    position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%);
    background: #14262E; border: 1px solid rgba(192,138,62,.5);
    color: #fff; padding: 12px 24px; border-radius: 8px;
    font-size: 14px; font-weight: 500;
    box-shadow: 0 8px 32px rgba(0,0,0,.4);
    opacity: 0; transition: opacity .3s; pointer-events: none; z-index: 100;
  }}
  .toast.show {{ opacity: 1; }}
</style>
</head>
<body>

<div class="header">
  <h1>📍 Editor de Pines — <span>Global States</span></h1>
  <div class="status">aylesva.mx</div>
</div>

<div class="toolbar">
  <div class="instructions">
    <b>1.</b> Selecciona un pin en el panel derecho &nbsp;→&nbsp;
    <b>2.</b> Haz clic en el mapa donde quieras moverlo &nbsp;→&nbsp;
    <b>3.</b> Presiona <b>Guardar</b>
  </div>
  <button class="btn-save" id="btnSave" disabled onclick="saveChanges()">Guardar cambios</button>
</div>

<div class="editor">
  <div class="map-container" id="mapContainer">
    <img src="{map_url}" alt="Mapa" id="mapImg" crossorigin="anonymous">
    <div class="map-overlay" id="mapOverlay">
      {"".join(f'''
      <div class="pin" id="pin-{p['id']}" data-id="{p['id']}" style="left:{p['x']}%;top:{p['y']}%">
        <div class="label">{p['name']}</div>
        <div class="dot"></div>
      </div>
      ''' for p in pins_data)}
    </div>
  </div>
  
  <div class="sidebar">
    <h2>Pines del mapa</h2>
    {"".join(f'''
    <div class="pin-card" data-id="{p['id']}" onclick="selectPin('{p['id']}')">
      <div class="name">📌 {p['name']}</div>
      <div class="pin-status">{p['status']}</div>
      <div class="coords" id="coords-{p['id']}">X: {p['x']}  ·  Y: {p['y']}</div>
    </div>
    ''' for p in pins_data)}
    
    <div style="margin-top:20px;padding:12px;background:rgba(255,255,255,.03);border-radius:6px;font-size:11px;color:rgba(255,255,255,.35);line-height:1.6">
      💡 Los valores X/Y son porcentajes de la imagen del mapa (0-100).
      Los cambios se guardan directamente en aylesva.mx.
    </div>
  </div>
</div>

<div class="toast" id="toast"></div>

<script>
var pinsData = {json.dumps({p['id']: {'x': p['x'], 'y': p['y'], 'name': p['name']} for p in pins_data})};
var originalData = JSON.parse(JSON.stringify(pinsData));
var selectedPinId = null;
var hasChanges = false;
var mapImg = document.getElementById('mapImg');
var overlay = document.getElementById('mapOverlay');

function selectPin(id) {{
  selectedPinId = id;
  document.querySelectorAll('.pin-card').forEach(function(c) {{
    c.classList.toggle('selected', c.dataset.id === id);
  }});
  document.querySelectorAll('.pin').forEach(function(p) {{
    p.classList.toggle('selected', p.dataset.id === id);
  }});
}}

/* Calcular coordenadas relativas a la imagen (object-fit:contain) */
function getImageCoords(e) {{
  var container = document.getElementById('mapContainer');
  var rect = container.getBoundingClientRect();
  var img = mapImg;
  
  var cw = rect.width, ch = rect.height;
  var iw = img.naturalWidth, ih = img.naturalHeight;
  var scale = Math.min(cw / iw, ch / ih);
  var rw = iw * scale, rh = ih * scale;
  var rx = (cw - rw) / 2, ry = (ch - rh) / 2;
  
  var mx = e.clientX - rect.left;
  var my = e.clientY - rect.top;
  
  var px = Math.round((mx - rx) / rw * 100);
  var py = Math.round((my - ry) / rh * 100);
  
  px = Math.max(0, Math.min(100, px));
  py = Math.max(0, Math.min(100, py));
  
  return {{ x: px, y: py }};
}}

/* Posicionar pines según object-fit:contain */
function layoutPins() {{
  var container = document.getElementById('mapContainer');
  var rect = container.getBoundingClientRect();
  var img = mapImg;
  if (!img.naturalWidth) return;
  
  var cw = rect.width, ch = rect.height;
  var iw = img.naturalWidth, ih = img.naturalHeight;
  var scale = Math.min(cw / iw, ch / ih);
  var rw = iw * scale, rh = ih * scale;
  var rx = (cw - rw) / 2, ry = (ch - rh) / 2;
  
  Object.keys(pinsData).forEach(function(id) {{
    var pin = document.getElementById('pin-' + id);
    if (!pin) return;
    var d = pinsData[id];
    pin.style.left = (rx + (d.x / 100) * rw) + 'px';
    pin.style.top = (ry + (d.y / 100) * rh) + 'px';
  }});
}}

overlay.addEventListener('click', function(e) {{
  if (!selectedPinId) {{
    showToast('⚠️ Primero selecciona un pin en el panel derecho');
    return;
  }}
  
  var coords = getImageCoords(e);
  pinsData[selectedPinId].x = coords.x;
  pinsData[selectedPinId].y = coords.y;
  
  layoutPins();
  
  var coordEl = document.getElementById('coords-' + selectedPinId);
  if (coordEl) {{
    coordEl.textContent = 'X: ' + coords.x + '  ·  Y: ' + coords.y;
    coordEl.className = 'coords changed';
  }}
  
  hasChanges = true;
  document.getElementById('btnSave').disabled = false;
  document.getElementById('btnSave').className = 'btn-save';
  
  showToast('✅ ' + pinsData[selectedPinId].name + ' → X: ' + coords.x + ' · Y: ' + coords.y);
}});

function saveChanges() {{
  var btn = document.getElementById('btnSave');
  btn.textContent = 'Guardando...';
  btn.disabled = true;
  
  fetch('/save', {{
    method: 'POST',
    headers: {{ 'Content-Type': 'application/json' }},
    body: JSON.stringify(pinsData)
  }})
  .then(function(r) {{ return r.json(); }})
  .then(function(data) {{
    if (data.success) {{
      btn.textContent = '✅ ¡Guardado!';
      btn.className = 'btn-save saved';
      showToast('🎉 Cambios guardados en aylesva.mx');
      originalData = JSON.parse(JSON.stringify(pinsData));
      hasChanges = false;
      setTimeout(function() {{
        btn.textContent = 'Guardar cambios';
        btn.disabled = true;
      }}, 3000);
    }} else {{
      btn.textContent = 'Error — Reintentar';
      btn.disabled = false;
      showToast('❌ Error al guardar: ' + (data.error || 'desconocido'));
    }}
  }})
  .catch(function(err) {{
    btn.textContent = 'Error — Reintentar';
    btn.disabled = false;
    showToast('❌ Error de conexión');
  }});
}}

function showToast(msg) {{
  var t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(function() {{ t.classList.remove('show'); }}, 3000);
}}

/* Init */
if (mapImg.complete) layoutPins();
mapImg.addEventListener('load', layoutPins);
window.addEventListener('resize', layoutPins);

/* Seleccionar primer pin por defecto */
var firstId = Object.keys(pinsData)[0];
if (firstId) selectPin(firstId);
</script>
</body>
</html>"""

# ─── Servidor HTTP ───────────────────────────────────────
class PinEditorHandler(http.server.BaseHTTPRequestHandler):
    template = None
    
    def log_message(self, format, *args):
        pass  # Silenciar logs
    
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            if not PinEditorHandler.template:
                PinEditorHandler.template = get_template()
            html = build_html(PinEditorHandler.template)
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
        else:
            self.send_error(404)
    
    def do_POST(self):
        if self.path == "/save":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length))
            
            # Actualizar posiciones en el template
            template = get_template()  # Re-leer para no perder cambios del usuario
            blocks = template["sections"]["main"]["blocks"]
            
            for pin_id, coords in body.items():
                if pin_id in blocks and blocks[pin_id].get("type") == "map_pin":
                    blocks[pin_id]["settings"]["pos_x"] = coords["x"]
                    blocks[pin_id]["settings"]["pos_y"] = coords["y"]
            
            success = save_template(template)
            PinEditorHandler.template = template if success else PinEditorHandler.template
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            result = {"success": success}
            if not success:
                result["error"] = "Error al subir al tema"
            self.wfile.write(json.dumps(result).encode("utf-8"))
        else:
            self.send_error(404)

def main():
    print("═" * 50)
    print("  📍 Editor de Pines — Global States")
    print("═" * 50)
    print(f"  Tienda: {SHOP}")
    print(f"  Tema:   {THEME}")
    print()
    print(f"  🌐 Abre en tu navegador:")
    print(f"     http://localhost:{PORT}")
    print()
    print("  Presiona Ctrl+C para cerrar")
    print("═" * 50)
    
    server = http.server.HTTPServer(("", PORT), PinEditorHandler)
    
    # Abrir navegador automáticamente
    threading.Timer(1.0, lambda: webbrowser.open(f"http://localhost:{PORT}")).start()
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Editor cerrado")
        server.server_close()

if __name__ == "__main__":
    main()
