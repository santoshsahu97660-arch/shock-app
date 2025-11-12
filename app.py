# streamlit_shock_app.py
# A visually striking "shock" Streamlit app with animated particle background,
# neon glass cards, interactive controls and a surprise "shock" (confetti + sound).
# Requirements:
#   pip install streamlit
# To run:
#   streamlit run streamlit_shock_app.py

import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(page_title="ShockWave — Neon Showcase", layout="wide")

# --------------------------- APP STYLE / THEME ---------------------------
GLOBAL_HTML = r"""
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <style>
      /* Full page neon gradient and glass effect */
      :root{
        --bg1: #0f172a; /* deep navy */
        --accent1: #7c3aed; /* purple */
        --accent2: #06b6d4; /* teal */
        --glass: rgba(255,255,255,0.04);
      }
      html,body,#root{height:100%;margin:0;padding:0;font-family:Inter,ui-sans-serif,system-ui,-apple-system,'Segoe UI',Roboto,'Helvetica Neue',Arial}
      body{background: radial-gradient(circle at 10% 20%, rgba(124,58,237,0.12), transparent 8%),
            radial-gradient(circle at 90% 80%, rgba(6,182,212,0.08), transparent 12%),
            linear-gradient(180deg,var(--bg1),#020617 120%); color:#e6eef8}
      .container{padding:28px;}

      /* neon title */
      .neon{
        font-size:48px; font-weight:800; letter-spacing:1px;
        text-transform:uppercase; display:inline-block;
        text-shadow: 0 0 8px rgba(124,58,237,0.6), 0 0 24px rgba(6,182,212,0.08);
        background: linear-gradient(90deg,#7c3aed,#06b6d4);
        -webkit-background-clip:text; background-clip:text; color:transparent;
      }

      .glass-card{
        background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.02));
        border-radius:18px; padding:20px; border:1px solid rgba(255,255,255,0.06);
        backdrop-filter: blur(6px) saturate(120%);
        box-shadow: 0 10px 30px rgba(2,6,23,0.6);
      }

      .big-hero{display:flex; gap:18px; align-items:center}

      .card-visual{
        width:460px; height:300px; border-radius:12px; overflow:hidden; position:relative;
      }

      .controls{display:flex;gap:8px;flex-wrap:wrap}
      .pill{padding:8px 12px;border-radius:999px;border:1px solid rgba(255,255,255,0.06);font-weight:600}

      /* floating element */
      .floating{position:relative; transform-origin:center; animation:float 6s ease-in-out infinite}
      @keyframes float{ 0%{ transform:translateY(0) } 50% { transform:translateY(-10px) } 100%{ transform:translateY(0)} }

      /* small footer */
      .muted{opacity:0.7;font-size:13px}

      /* button style for html area */
      .shock-btn{background:linear-gradient(90deg,#7c3aed,#06b6d4);border:none;padding:14px 22px;border-radius:12px;color:white;font-weight:700;font-size:15px;cursor:pointer}

      /* responsive */
      @media (max-width:900px){ .big-hero{flex-direction:column} .card-visual{width:100%} }
    </style>
  </head>
  <body>
    <div id="root"></div>
    <script src="https://cdn.jsdelivr.net/npm/tsparticles@2.11.1/tsparticles.bundle.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <script>
      // Attach a particle background to a given container element
      function mountParticles(container) {
        tsParticles.load(container, {
          fullScreen: { enable: false },
          detectRetina: true,
          fpsLimit: 60,
          particles: {
            number: { value: 60 },
            color: { value: ["#7c3aed", "#06b6d4", "#22c55e"] },
            shape: { type: "circle" },
            opacity: { value: 0.7 },
            size: { value: { min: 1, max: 4 } },
            move: { speed: 0.9, outModes: { default: "out" } },
            links: { enable: true, distance: 140, color: "#ffffff22", opacity: 0.06 }
          },
          interactivity: { events: { onHover: { enable: true, mode: "grab" }, onClick: { enable: true, mode: "push" } }, modes: { push: { quantity: 4 } } }
        });
      }

      // create an SVG-ish visual inside the card
      function createVisual(cardId) {
        const card = document.getElementById(cardId);
        card.innerHTML = `
          <svg viewBox="0 0 460 300" preserveAspectRatio="xMidYMid meet" style="width:100%;height:100%">
            <defs>
              <linearGradient id="g1" x1="0" x2="1"><stop offset="0" stop-color="#7c3aed" stop-opacity="0.9"/><stop offset="1" stop-color="#06b6d4" stop-opacity="0.9"/></linearGradient>
            </defs>
            <rect x="10" y="40" rx="12" ry="12" width="440" height="220" fill="url(#g1)" opacity="0.06"/>
            <g transform="translate(40,60)">
              <circle cx="80" cy="60" r="36" fill="#ffffff10" stroke="#ffffff20"/>
              <rect x="150" y="18" rx="8" ry="8" width="200" height="32" fill="#ffffff10" stroke="#ffffff12"/>
              <g id="moving" transform="translate(0,0)">
                <rect x="12" y="120" rx="6" ry="6" width="120" height="14" fill="#ffffff14"/>
                <rect x="140" y="120" rx="6" ry="6" width="180" height="14" fill="#ffffff14"/>
              </g>
            </g>
          </svg>
        `;

        // make the small group oscillate
        let t = 0;
        function tick(){
          const el = document.getElementById('moving');
          if(!el) return;
          el.setAttribute('transform', `translate(${Math.sin(t/20)*8},${Math.cos(t/30)*6})`);
          t++;
          requestAnimationFrame(tick);
        }
        tick();
      }

      // expose a function to trigger the "shock" from Python side via re-render
      window.triggerShock = function(){
        // confetti burst
        confetti({ particleCount: 180, spread: 80, origin: { y: 0.4 } });
        confetti({ particleCount: 60, scalar: 0.9, origin: { x: 0.1, y: 0.2 } });
        confetti({ particleCount: 60, scalar: 0.9, origin: { x: 0.9, y: 0.2 } });
        // small page flash
        const flash = document.createElement('div');
        flash.style.position='fixed'; flash.style.left=0; flash.style.top=0; flash.style.width='100%'; flash.style.height='100%';
        flash.style.background='#fff'; flash.style.opacity=0; flash.style.pointerEvents='none'; flash.style.zIndex=9999;
        document.body.appendChild(flash);
        let op=0.0; const step=0.06;
        const int=setInterval(()=>{ op+=step; flash.style.opacity=op; if(op>=0.7){ clearInterval(int); setTimeout(()=>{ flash.style.transition='opacity 700ms'; flash.style.opacity=0; setTimeout(()=>flash.remove(),800); },120); } },20);
        // play a short 'whoosh' audio using WebAudio API (generated tone) for surprise
        try{
          const ctx = new (window.AudioContext || window.webkitAudioContext)();
          const o = ctx.createOscillator(); const g = ctx.createGain();
          o.type='sawtooth'; o.frequency.value=520; g.gain.value=0.0015;
          o.connect(g); g.connect(ctx.destination);
          o.start(); g.gain.exponentialRampToValueAtTime(0.6, ctx.currentTime + 0.03);
          g.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 0.25);
          o.stop(ctx.currentTime + 0.28);
        }catch(e){ /* ignore audio permission issues */ }
      }

      // when DOM loaded
      document.addEventListener('DOMContentLoaded',()=>{
        // create holders
        const root = document.getElementById('root');
        root.innerHTML = `
          <div class="container">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:18px">
              <div>
                <div class="neon">ShockWave</div>
                <div class="muted">A neon-glass Streamlit showcase — press the "Shock" button.</div>
              </div>
              <div style="display:flex;gap:10px;align-items:center">
                <div class="pill">Interactive • Animated • Surprise</div>
              </div>
            </div>

            <div class="big-hero">
              <div class="glass-card floating" style="flex:1;min-width:380px">
                <div id="visual" class="card-visual"></div>
              </div>

              <div style="flex:1.1">
                <div class="glass-card">
                  <h3 style="margin:0 0 12px 0">Controls</h3>
                  <div class="controls">
                    <div class="pill">Particles: <select id="density"><option value="30">Low</option><option value="60" selected>Medium</option><option value="160">High</option></select></div>
                    <div class="pill">Motion: <select id="speed"><option value="0.5">Slow</option><option value="0.9" selected>Normal</option><option value="2">Fast</option></select></div>
                    <div class="pill">Theme: <select id="theme"><option value="neon">Neon</option><option value="sunset">Sunset</option></select></div>
                  </div>

                  <div style="height:18px"></div>
                  <div style="display:flex;gap:10px;align-items:center">
                    <button class="shock-btn" id="shockBtn">Shock the Viewer</button>
                    <button class="pill" id="previewBtn">Preview small burst</button>
                  </div>

                  <div style="height:12px"></div>
                  <div class="muted">Tip: Click/hover the background. The animation and surprise are pure web-canvas — works in Streamlit's HTML component.</div>
                </div>

                <div style="height:14px"></div>
                <div class="glass-card muted">Made with HTML5 canvas, tsParticles and canvas-confetti — creative demo for Streamlit embedding.</div>
              </div>
            </div>

            <div style="height:22px"></div>
            <div class="muted">Footer: Press the big Shock button for a full-screen celebratory rupture (confetti + flash + sound).</div>
          </div>
        `;

        // mount particles in the visual card
        const card = document.getElementById('visual');
        card.style.position='relative';
        // create a full-size particles canvas holder
        const holder = document.createElement('div'); holder.id='particles-holder'; holder.style.width='100%'; holder.style.height='100%'; holder.style.position='absolute'; holder.style.left=0; holder.style.top=0; holder.style.zIndex=0;
        card.appendChild(holder);
        // create overlay for svg visuals
        const overlay = document.createElement('div'); overlay.id='svg-overlay'; overlay.style.position='absolute'; overlay.style.left=0; overlay.style.top=0; overlay.style.width='100%'; overlay.style.height='100%'; overlay.style.zIndex=1; overlay.style.pointerEvents='none';
        card.appendChild(overlay);

        mountParticles('particles-holder');
        createVisual('svg-overlay');

        // wire up controls
        const density = document.getElementById('density');
        const speed = document.getElementById('speed');
        const theme = document.getElementById('theme');

        density.addEventListener('change', () => { tsParticles.domItem(0).options.particles.number.value = parseInt(density.value); tsParticles.domItem(0).refresh(); });
        speed.addEventListener('change', () => { tsParticles.domItem(0).options.particles.move.speed = parseFloat(speed.value); tsParticles.domItem(0).refresh(); });
        theme.addEventListener('change', ()=>{ /* could swap colors */ });

        document.getElementById('shockBtn').addEventListener('click', ()=>{ window.triggerShock(); });
        document.getElementById('previewBtn').addEventListener('click', ()=>{ confetti({ particleCount: 40, spread: 60, origin: { y: 0.5 }}); });
      });
    </script>
  </body>
</html>
"""

# --------------------------- STREAMLIT LAYOUT ---------------------------
st.markdown("""
# 
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("<div style='padding:12px 6px'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:26px;font-weight:800;color:transparent;background:linear-gradient(90deg,#7c3aed,#06b6d4);-webkit-background-clip:text;'>ShockWave — Neon Showcase</div>
    <div style='margin-top:6px;color:#cfe9ff;opacity:0.9'>Ek aisa app jo dekhne wale ko "kaise banaya?" kahega. Animation, particles, confetti aur ek surprise shock button.</div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.divider()
    st.subheader("Design Controls")
    particle_density = st.selectbox("Particle density", options=["Low","Medium","High"], index=1)
    motion = st.radio("Motion speed", options=["Slow","Normal","Fast"], index=1, horizontal=True)
    st.write("---")
    if 'shocked' not in st.session_state:
        st.session_state.shocked = False

    if st.button("Shock the Viewer 🔥", key='shock_main'):
        # Toggle session state to inform the HTML component to run shock via a small trick: re-render with JS call
        st.session_state.shocked = not st.session_state.shocked

with col2:
    st.markdown("""
    <div class='glass-card' style='padding:14px'>
      <div style='font-weight:700;font-size:16px;margin-bottom:6px'>Preview</div>
      <div style='font-size:13px;color:#cbdaf3;margin-bottom:8px'>Embedded interactive area — if your browser blocks scripts in Streamlit, open this file as a static HTML to preview the full experience.</div>
    </div>
    """, unsafe_allow_html=True)

    # Render the big HTML block. We will embed it and also, if the 'Shock the Viewer' button was pressed, call the JS function via small inline script.
    # Create a tiny binding script that, when re-rendered with a 'shock' param, calls the triggerShock function inside the embedded HTML's iframe context.

    # The html() component returns an iframe. We'll include a tiny hint in the HTML body to call triggerShock when parent passes `data-shock='1'` via postMessage

    # To keep things simple and robust across Streamlit versions, we just re-render the whole HTML. When the session state's 'shocked' toggles,
    # we'll append a short script inside the HTML that calls `triggerShock()` after load.

    html_to_mount = GLOBAL_HTML
    if st.session_state.shocked:
        # append a tiny auto-trigger script near the end before </body>
        html_to_mount = html_to_mount.replace('</body>', "<script>setTimeout(()=>{ if(window.triggerShock) window.triggerShock(); },420);</script></body>")

    # The height should be large enough for the interactive demo
    html(html_to_mount, height=720, scrolling=True)

st.write("\n")
st.markdown("---")
st.markdown("<div style='opacity:0.7;font-size:13px'>Tips: Use Chrome / Edge for best experience. If you want this exported as a single-page deployable app, I can provide a cleaned package (requirements.txt + static HTML fallback).</div>", unsafe_allow_html=True)

# End of file
