import streamlit as st
import json
from datetime import datetime
import hashlib
import os
st.set_page_config(layout="wide", page_title="FluXTape Study", page_icon="🎵")

# Get participant and song info from URL
query_params = st.query_params
participant_id = query_params.get("pid", ["test_user"])[0]
song_id = query_params.get("song", ["song1"])[0]

# Initialize session state
if 'participant_id' not in st.session_state:
    st.session_state.participant_id = participant_id
if 'song_id' not in st.session_state:
    st.session_state.song_id = song_id
if 'interaction_log' not in st.session_state:
    st.session_state.interaction_log = []
if 'session_start' not in st.session_state:
    st.session_state.session_start = datetime.now().isoformat()

# Logging function
def log_interaction(control_type, from_value, to_value):
    st.session_state.interaction_log.append({
        'timestamp': datetime.now().isoformat(),
        'participant_id': st.session_state.participant_id,
        'song_id': st.session_state.song_id,
        'control': control_type,
        'from': from_value,
        'to': to_value
    })

# Configuration ID generator
def get_config_id(lyrics, groove, solo, spatialize, backing):
    config_string = f"{lyrics}_{groove}_{solo}_{spatialize}_{backing}"
    return hashlib.md5(config_string.encode()).hexdigest()[:8]

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
  background: linear-gradient(160deg, #0f1115 0%, #1a1d25 100%) fixed !important;
}
[data-testid="stHeader"] {
  background: rgba(0,0,0,0) !important;
}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Audio map - UPDATE THIS WITH YOUR ACTUAL SONG URLS
audio_map = {
    "grooveA": "https://raw.githubusercontent.com/theallophones/audio/main/grooveA.mp3",
    "grooveB": "https://raw.githubusercontent.com/theallophones/audio/main/grooveB.mp3",
    "grooveC": "https://raw.githubusercontent.com/theallophones/audio/main/grooveC.mp3",
    "lyricsA": "https://raw.githubusercontent.com/theallophones/audio/main/lyricsA.mp3",
    "lyricsB": "https://raw.githubusercontent.com/theallophones/audio/main/lyricsB.mp3",
    "lyricsC": "https://raw.githubusercontent.com/theallophones/audio/main/lyricsC.mp3",
    "soloA": "https://raw.githubusercontent.com/theallophones/audio/main/soloA.mp3",
    "soloB": "https://raw.githubusercontent.com/theallophones/audio/main/soloB.mp3",
    "soloC": "https://raw.githubusercontent.com/theallophones/audio/main/soloC.mp3",
    "harmony_narrow": "https://raw.githubusercontent.com/theallophones/audio/main/harmony_narrow.mp3",
    "harmony_wide": "https://raw.githubusercontent.com/theallophones/audio/main/harmony_wide.mp3",
    "adlibA": "https://raw.githubusercontent.com/theallophones/audio/main/adlibA.mp3",
    "adlibB": "https://raw.githubusercontent.com/theallophones/audio/main/adlibB.mp3",
    "adlibC": "https://raw.githubusercontent.com/theallophones/audio/main/adlibC.mp3",
}

audio_map_json = json.dumps(audio_map)

# JavaScript for logging interactions
logging_js = f"""
<script>
window.logInteraction = function(control, fromValue, toValue) {{
    // Send to Streamlit
    const data = {{
        control: control,
        from: fromValue,
        to: toValue,
        timestamp: new Date().toISOString()
    }};
    
    // Store in sessionStorage as backup
    const log = JSON.parse(sessionStorage.getItem('interaction_log') || '[]');
    log.push(data);
    sessionStorage.setItem('interaction_log', JSON.stringify(log));
    
    console.log('Logged:', data);
}};
</script>
"""

html = logging_js + f"""
<div style="text-align:center; margin-bottom:20px;">
  <h1 style="font-family:'Inter', sans-serif; font-weight:800; color:#ffffff; font-size:42px; margin-bottom:8px;">
    FluXTape
  </h1>
  <h3 style="font-family:'Inter', sans-serif; font-weight:400; color:#8b92a8; font-size:14px; margin-top:0;">
    Listen and create your preferred version
  </h3>
  <div id="loadingStatus" style="color:#8b92a8; margin:10px 0; font-size:14px;">Loading audio...</div>
  <div style="margin-top:15px;">
    <button id="playBtn" class="play-btn" disabled style="opacity:0.5;">▶</button>
  </div>
</div>

<div id="waveform" style="margin:30px auto; width:90%; max-width:1200px;"></div>

<div class="visualizer-container paused">
  <div class="vis-bar" style="animation-delay: 0s;"></div>
  <div class="vis-bar" style="animation-delay: 0.1s;"></div>
  <div class="vis-bar" style="animation-delay: 0.2s;"></div>
  <div class="vis-bar" style="animation-delay: 0.15s;"></div>
  <div class="vis-bar" style="animation-delay: 0.05s;"></div>
  <div class="vis-bar" style="animation-delay: 0.25s;"></div>
  <div class="vis-bar" style="animation-delay: 0.3s;"></div>
  <div class="vis-bar" style="animation-delay: 0.12s;"></div>
</div>

<div style="display:flex; justify-content:center; margin-top:20px;">
  <div id="time-display" style="color:#ffffff; font-family:'JetBrains Mono', monospace; font-size:24px; font-weight:600; letter-spacing:2px;">
    0:00 / 0:00
  </div>
</div>

<div style="text-align:center; margin:25px 0;">
  <div style="color:#8b92a8; font-size:22px; margin-bottom:8px;">🔊</div>
  <input id="volumeSlider" type="range" min="0" max="1" step="0.01" value="1" class="slider">
</div>

<div class="controls-grid">
  <div class="control-section">
    <div class="control-header">LYRICS</div>
    <div class="knob-wrap-small">
      <div id="lyricsKnob" class="knob-small">
        <div id="lyricsPointer" class="pointer-small"></div>
        <div class="center-dot-small"></div>
      </div>
      <div class="label-small labelA-small active" data-lyrics="A">A</div>
      <div class="label-small labelB-small" data-lyrics="B">B</div>
      <div class="label-small labelC-small" data-lyrics="C">C</div>
    </div>
    <div id="lyricsDisplay" class="version-badge">Lyrics A</div>
    <div class="volume-knob-container">
      <input type="range" id="lyricsVolume" class="volume-knob" min="0" max="100" value="100">
      <div class="volume-label">Volume: <span id="lyricsVolumeDisplay">100%</span></div>
    </div>
  </div>

  <div class="control-section">
    <div class="control-header">GROOVE</div>
    <div class="knob-wrap-small">
      <div id="grooveKnob" class="knob-small">
        <div id="groovePointer" class="pointer-small"></div>
        <div class="center-dot-small"></div>
      </div>
      <div class="label-small labelA-small active" data-groove="A">A</div>
      <div class="label-small labelB-small" data-groove="B">B</div>
      <div class="label-small labelC-small" data-groove="C">C</div>
    </div>
    <div id="grooveDisplay" class="version-badge">Groove A</div>
    <div class="volume-knob-container">
      <input type="range" id="grooveVolume" class="volume-knob" min="0" max="100" value="100">
      <div class="volume-label">Volume: <span id="grooveVolumeDisplay">100%</span></div>
    </div>
  </div>

  <div class="control-section">
    <div class="control-header">SOLO</div>
    <div class="knob-wrap-small">
      <div id="soloKnob" class="knob-small">
        <div id="soloPointer" class="pointer-small"></div>
        <div class="center-dot-small"></div>
      </div>
      <div class="label-small labelA-small active" data-solo="A">A</div>
      <div class="label-small labelB-small" data-solo="B">B</div>
      <div class="label-small labelC-small" data-solo="C">C</div>
    </div>
    <div id="soloDisplay" class="version-badge">Take A</div>
    <div class="volume-knob-container">
      <input type="range" id="soloVolume" class="volume-knob" min="0" max="100" value="100">
      <div class="volume-label">Volume: <span id="soloVolumeDisplay">100%</span></div>
    </div>
  </div>

  <div class="control-section">
    <div class="control-header">SPATIALIZE</div>
    <div class="knob-wrap-small">
      <div id="spatializeKnob" class="knob-small">
        <div id="spatializePointer" class="pointer-small"></div>
        <div class="center-dot-small"></div>
      </div>
      <div class="label-small labelLeft-small active" data-spatialize="narrow">N</div>
      <div class="label-small labelRight-small" data-spatialize="wide">W</div>
    </div>
    <div id="spatializeDisplay" class="version-badge">Narrow</div>
    <div class="volume-knob-container">
      <input type="range" id="spatializeVolume" class="volume-knob" min="0" max="100" value="100">
      <div class="volume-label">Volume: <span id="spatializeVolumeDisplay">100%</span></div>
    </div>
  </div>

  <div class="control-section">
    <div class="control-header">BACK VOCALS</div>
    <div class="knob-wrap-small">
      <div id="backVocalsKnob" class="knob-small">
        <div id="backVocalsPointer" class="pointer-small"></div>
        <div class="center-dot-small"></div>
      </div>
      <div class="label-small labelLeft-small active" data-backvocals="off">OFF</div>
      <div class="label-small labelRight-small" data-backvocals="on">ON</div>
    </div>
    <div id="backVocalsDisplay" class="version-badge">Off</div>
    <div class="volume-knob-container">
      <input type="range" id="backVocalsVolume" class="volume-knob" min="0" max="100" value="100">
      <div class="volume-label">Volume: <span id="backVocalsVolumeDisplay">100%</span></div>
    </div>
  </div>
</div>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap');
  
  :root {{
    --bg: #0f1115;
    --accent: #4CAF50;
    --accent-hover: #66BB6A;
  }}
  
  * {{ font-family: 'Inter', sans-serif; }}

  .play-btn {{
    width: 90px;
    height: 90px;
    border-radius: 50%;
    border: none;
    font-size: 36px;
    cursor: pointer;
    color: #fff;
    background: var(--accent);
    transition: all 0.3s ease;
    box-shadow: 0 8px 24px rgba(76,175,80,.5);
  }}
  .play-btn:hover {{ 
    transform: scale(1.08); 
    background: var(--accent-hover);
  }}
  .play-btn.pause {{
    background: #FBC02D;
  }}
  .play-btn:disabled {{
    opacity: 0.5;
    cursor: not-allowed;
  }}

  .controls-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 30px;
    max-width: 1100px;
    margin: 40px auto 60px auto;
    padding: 0 20px;
  }}

  .control-section {{
    background: rgba(255,255,255,0.03);
    border-radius: 16px;
    padding: 25px 20px 30px 20px;
    text-align: center;
  }}

  .control-header {{
    color: #8b92a8;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 20px;
  }}

  .version-badge {{
    margin-top: 15px;
    display: inline-block;
    background: rgba(95,107,255,0.2);
    border: 1px solid #5f6bff;
    border-radius: 12px;
    padding: 6px 14px;
    color: #8b9dff;
    font-size: 13px;
    font-weight: 600;
  }}

  .knob-wrap-small {{
    position: relative;
    width: 140px;
    height: 140px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: center;
  }}

  .knob-small {{
    width: 90px;
    height: 90px;
    border-radius: 50%;
    background: radial-gradient(circle at 30% 30%, #2b313c, #1b1f27 70%);
    position: relative;
    box-shadow: inset 0 4px 10px rgba(0,0,0,.6), 0 6px 18px rgba(0,0,0,.4);
    border: 2px solid #2e3440;
    cursor: pointer;
    transition: transform 0.2s ease;
  }}
  .knob-small:hover {{ transform: scale(1.05); }}

  .center-dot-small {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #cfd8dc;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%,-50%);
  }}

  .pointer-small {{
    position: absolute;
    width: 3px;
    height: 30px;
    background: linear-gradient(to top, #ffffff, #e0e0e0);
    border-radius: 2px;
    transform-origin: bottom center;
    bottom: 50%;
    left: 50%;
    translate: -50% 0;
    box-shadow: 0 0 8px rgba(255,255,255,.5);
    transition: transform 0.5s cubic-bezier(0.4, 0.0, 0.2, 1);
  }}

  .label-small {{
    position: absolute;
    background: #2a2f3a;
    color: #fff;
    padding: 6px 12px;
    border-radius: 10px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    border: 1px solid transparent;
    user-select: none;
  }}
  .label-small:hover {{
    background: #3a4150;
  }}
  .label-small.active {{
    background: #b71c1c;
    box-shadow: 0 0 12px rgba(183,28,28,0.9);
    border-color: #d32f2f;
  }}

  .labelA-small {{ top: 50%; left: -20px; transform: translateY(-50%); }}
  .labelB-small {{ top: -15px; left: 50%; transform: translateX(-50%); }}
  .labelC-small {{ top: 50%; right: -20px; transform: translateY(-50%); }}
  .labelLeft-small {{ top: 50%; left: -25px; transform: translateY(-50%); }}
  .labelRight-small {{ top: 50%; right: -25px; transform: translateY(-50%); }}

  .slider {{
    -webkit-appearance: none;
    width: 300px;
    height: 7px;
    border-radius: 4px;
    background: linear-gradient(to right, #5f6bff 100%, #3a4150 0%);
    outline: none;
    cursor: pointer;
  }}
  .slider::-webkit-slider-thumb {{
    -webkit-appearance: none;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: #cfd8dc;
    box-shadow: 0 2px 8px rgba(200,200,200,.7);
    cursor: grab;
  }}

  .visualizer-container {{
    display: flex;
    justify-content: center;
    align-items: flex-end;
    gap: 6px;
    height: 100px;
    margin: 25px auto;
    max-width: 400px;
  }}
  
  .vis-bar {{
    width: 14px;
    background: linear-gradient(to top, #5f6bff, #8b9dff);
    border-radius: 8px 8px 0 0;
    height: 20%;
    animation: pulse 0.8s ease-in-out infinite alternate;
  }}
  
  @keyframes pulse {{
    0% {{ height: 15%; }}
    50% {{ height: 75%; }}
    100% {{ height: 30%; }}
  }}
  
  .visualizer-container.paused .vis-bar {{
    animation: none;
    height: 20%;
    opacity: 0.3;
  }}

  .volume-knob-container {{
    margin-top: 20px;
    padding-top: 15px;
    border-top: 1px solid rgba(255,255,255,0.1);
  }}

  .volume-knob {{
    -webkit-appearance: none;
    width: 100%;
    height: 6px;
    border-radius: 3px;
    background: linear-gradient(to right, #5f6bff 100%, #3a4150 0%);
    outline: none;
    cursor: pointer;
  }}
  .volume-knob::-webkit-slider-thumb {{
    -webkit-appearance: none;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: #cfd8dc;
    cursor: grab;
  }}

  .volume-label {{
    margin-top: 8px;
    color: #8b92a8;
    font-size: 11px;
    font-weight: 600;
    text-align: center;
  }}
</style>

<script src="https://unpkg.com/wavesurfer.js@7/dist/wavesurfer.min.js"></script>

<script>
  const audioMap = {audio_map_json};
  const lyricsAngles = {{"A": 270, "B": 0, "C": 90}};
  const grooveAngles = {{"A": 270, "B": 0, "C": 90}};
  const soloAngles = {{"A": 270, "B": 0, "C": 90}};

  // Current state
  let currentLyrics = 'A';
  let currentGroove = 'A';
  let currentSolo = 'A';
  let spatializeOn = false;
  let backVocalsOn = false;
  let isPlaying = false;

  // [REST OF THE JAVASCRIPT - WaveSurfer setup, playback controls, etc.]
  // I'll continue if you want the full JS, but this is getting long
  
  function switchLyrics(version) {{
    if (version === currentLyrics) return;
    window.logInteraction('lyrics', currentLyrics, version);
    currentLyrics = version;
    // ... rest of switch logic
  }}

  function switchGroove(version) {{
    if (version === currentGroove) return;
    window.logInteraction('groove', currentGroove, version);
    currentGroove = version;
    // ... rest of switch logic
  }}

  // Similar for other controls...
</script>
"""

st.components.v1.html(html, height=1600)

# Submit section (below the player)
st.markdown("<h2 style='margin-top:40px; text-align:center;'>Submit Your Preferred Version</h2>", unsafe_allow_html=True)

if st.button("✓ Submit and Continue", use_container_width=True, type="primary"):
    # Get final configuration from JavaScript (you'll need to implement this)
    final_config = {
        'participant_id': st.session_state.participant_id,
        'song_id': st.session_state.song_id,
        'session_start': st.session_state.session_start,
        'session_end': datetime.now().isoformat(),
        'interaction_log': st.session_state.interaction_log,
        # You'll need to capture final state from JS
    }
    
    # Save to file
    import os
    os.makedirs('data', exist_ok=True)
    with open(f'data/{participant_id}_{song_id}.json', 'w') as f:
        json.dump(final_config, f, indent=2)
    
    st.success("Submitted! Redirecting back to survey...")
    
    # Redirect back to Qualtrics
    st.markdown(f"""
    <script>
    window.parent.location.href = "YOUR_QUALTRICS_URL?pid={participant_id}&completed={song_id}";
    </script>
    """, unsafe_allow_html=True)