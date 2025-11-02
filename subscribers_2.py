

import streamlit as st
import json

st.set_page_config(layout="wide", page_title="FluXTape Contributor Studio", page_icon="🎚️")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
  background: linear-gradient(160deg, #0f1115 0%, #1a1d25 100%) fixed !important;
}
[data-testid="stHeader"] {
  background: rgba(0,0,0,0) !important;
}
[data-testid="stSidebar"] {
  background: rgba(0,0,0,0.15) !important;
}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'my_uploads' not in st.session_state:
    st.session_state.my_uploads = {}
if 'muted_stems' not in st.session_state:
    st.session_state.muted_stems = set()
if 'submission_count' not in st.session_state:
    st.session_state.submission_count = 0
if 'my_ranking' not in st.session_state:
    st.session_state.my_ranking = None

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

html = f"""
<div style="text-align:center; margin-bottom:20px;">
  <h1 style="font-family:'Inter', sans-serif; font-weight:800; color:#ffffff; font-size:42px; margin-bottom:8px; letter-spacing:-0.5px;">
    FluXTape / Contributor Studio
  </h1>
  <h3 style="font-family:'Inter', sans-serif; font-weight:400; color:#8b92a8; font-size:14px; margin-top:0; letter-spacing:0.5px;">
    Mid-nite Free-Quensee by Zlisterr
  </h3>
  <div id="loadingStatus" style="color:#8b92a8; margin:10px 0; font-size:14px;">Loading audio files...</div>
  <div style="margin-top:15px;">
    <button id="playBtn" class="play-btn" title="Play/Pause (Space)" disabled style="opacity:0.5;">▶</button>
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
  <div class="vis-bar" style="animation-delay: 0.18s;"></div>
  <div class="vis-bar" style="animation-delay: 0.08s;"></div>
  <div class="vis-bar" style="animation-delay: 0.22s;"></div>
  <div class="vis-bar" style="animation-delay: 0.28s;"></div>
</div>

<div style="display:flex; justify-content:center; align-items:center; margin-top:20px; gap:20px;">
  <div id="time-display" style="color:#ffffff; font-family:'JetBrains Mono', 'Courier New', monospace; font-size:24px; font-weight:600; letter-spacing:2px;">
    0:00 / 0:00
  </div>
  <div style="display:flex; gap:10px;">
    <button id="loopBtn" class="control-btn" title="Toggle Loop">🔁</button>
    <button id="exportBtn" class="control-btn" title="Export Current Mix">💾</button>
  </div>
</div>

<div style="text-align:center; margin:25px 0;">
  <div style="color:#8b92a8; font-size:22px; margin-bottom:8px;">🔊</div>
  <input id="volumeSlider" type="range" min="0" max="1" step="0.01" value="1" class="slider" title="Master Volume">
</div>

<div class="controls-grid">
  <div class="control-section">
    <div class="control-header">
      LYRICS
      <button class="mute-btn" data-stem="lyrics" title="Mute to replace with your own">🔇</button>
    </div>
    <div class="knob-wrap-small">
      <div id="lyricsKnob" class="knob-small" title="Click to cycle lyrics">
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
    <div class="control-header">
      GROOVE
      <button class="mute-btn" data-stem="groove" title="Mute to replace with your own">🔇</button>
    </div>
    <div class="knob-wrap-small">
      <div id="grooveKnob" class="knob-small" title="Click to cycle groove">
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
    <div class="control-header">
      SOLO <span style="font-size:10px; font-weight:400; opacity:0.7;">(from 1:03)</span>
      <button class="mute-btn" data-stem="solo" title="Mute to replace with your own">🔇</button>
    </div>
    <div class="knob-wrap-small">
      <div id="soloKnob" class="knob-small" title="Click to cycle solo">
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
    <div class="control-header">
      SPATIALIZE
      <button class="mute-btn" data-stem="spatialize" title="Mute to replace with your own">🔇</button>
    </div>
    <div class="knob-wrap-small">
      <div id="spatializeKnob" class="knob-small" title="Click to toggle spatialize">
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
    <div class="control-header">
      BACK VOCALS
      <button class="mute-btn" data-stem="backvocals" title="Mute to replace with your own">🔇</button>
    </div>
    <div class="knob-wrap-small">
      <div id="backVocalsKnob" class="knob-small" title="Click to toggle back vocals">
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

<div style="text-align:center; margin-top:30px; padding:20px; background:rgba(255,255,255,0.03); border-radius:12px; max-width:600px; margin-left:auto; margin-right:auto;">
  <div style="color:#8b92a8; font-size:13px; font-family:'Inter', sans-serif; margin-bottom:10px; font-weight:600;">
    ⌨️ KEYBOARD SHORTCUTS
  </div>
  <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; color:#6b7280; font-size:12px; font-family:'Inter', sans-serif;">
    <div><kbd style="background:#2a2f3a; padding:2px 8px; border-radius:4px; color:#fff;">Space</kbd> Play/Pause</div>
    <div><kbd style="background:#2a2f3a; padding:2px 8px; border-radius:4px; color:#fff;">←→</kbd> Seek ±5s</div>
    <div><kbd style="background:#2a2f3a; padding:2px 8px; border-radius:4px; color:#fff;">1/2/3</kbd> Lyrics A/B/C</div>
    <div><kbd style="background:#2a2f3a; padding:2px 8px; border-radius:4px; color:#fff;">↑↓</kbd> Volume ±10%</div>
    <div><kbd style="background:#2a2f3a; padding:2px 8px; border-radius:4px; color:#fff;">L</kbd> Toggle Loop</div>
    <div><kbd style="background:#2a2f3a; padding:2px 8px; border-radius:4px; color:#fff;">E</kbd> Export Mix</div>
  </div>
</div>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap');
  
  :root {{
    --bg: #0f1115;
    --accent: #4CAF50;
    --accent-hover: #66BB6A;
    --text: #ffffff;
    --text-muted: #8b92a8;
  }}
  
  * {{ font-family: 'Inter', sans-serif; }}

  html, body, .stApp {{
    height: 100%;
    margin: 0;
    background: linear-gradient(160deg, #0f1115 0%, #1a1d25 100%);
  }}

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
    box-shadow: 0 12px 32px rgba(76,175,80,.6);
  }}
  .play-btn:active {{ transform: scale(0.98); }}
  .play-btn.pause {{
    background: #FBC02D;
    box-shadow: 0 8px 24px rgba(251,192,45,.5);
  }}
  .play-btn.pause:hover {{
    background: #FDD835;
    box-shadow: 0 12px 32px rgba(251,192,45,.6);
  }}
  .play-btn:disabled {{
    cursor: not-allowed;
    opacity: 0.5;
  }}

  .control-btn {{
    width: 40px;
    height: 40px;
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.1);
    background: rgba(255,255,255,0.05);
    color: #fff;
    font-size: 18px;
    cursor: pointer;
    transition: all 0.2s ease;
  }}
  .control-btn:hover {{
    background: rgba(255,255,255,0.1);
    border-color: rgba(255,255,255,0.2);
    transform: scale(1.05);
  }}
  .control-btn.active {{
    background: #4CAF50;
    border-color: #66BB6A;
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
    position: relative;
  }}

  .control-section.muted {{
    opacity: 0.4;
    border: 2px solid rgba(251,192,45,0.5);
  }}

  .control-header {{
    color: #8b92a8;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 8px;
  }}

  .mute-btn {{
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    color: #8b92a8;
    padding: 4px 8px;
    border-radius: 6px;
    font-size: 12px;
    cursor: pointer;
    transition: all 0.2s ease;
  }}
  .mute-btn:hover {{
    background: rgba(255,255,255,0.1);
    color: #fff;
  }}
  .mute-btn.active {{
    background: rgba(251,192,45,0.2);
    border-color: #FBC02D;
    color: #FDD835;
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
  .knob-small:active {{ transform: scale(0.98); }}

  .center-dot-small {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #cfd8dc;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%,-50%);
    box-shadow: 0 1px 4px rgba(0,0,0,0.4);
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
    color: var(--text);
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
    border-color: #4a5160;
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
    transition: all 0.2s ease;
  }}
  .slider:hover {{ height: 9px; }}
  .slider::-webkit-slider-thumb {{
    -webkit-appearance: none;
    appearance: none;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: #cfd8dc;
    box-shadow: 0 2px 8px rgba(200,200,200,.7);
    transition: transform 0.2s ease;
    cursor: grab;
  }}
  .slider::-webkit-slider-thumb:hover {{ transform: scale(1.3); }}
  .slider::-webkit-slider-thumb:active {{ cursor: grabbing; }}
  .slider::-moz-range-thumb {{
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: #cfd8dc;
    box-shadow: 0 2px 8px rgba(200,200,200,.7);
    cursor: pointer;
    border: none;
  }}

  .visualizer-container {{
    display: flex;
    justify-content: center;
    align-items: flex-end;
    gap: 6px;
    height: 100px;
    margin: 25px auto;
    max-width: 400px;
    padding: 0 20px;
  }}
  
  .vis-bar {{
    width: 14px;
    background: linear-gradient(to top, #5f6bff, #8b9dff);
    border-radius: 8px 8px 0 0;
    height: 20%;
    box-shadow: 0 0 15px rgba(95, 107, 255, 0.5);
    animation: pulse 0.8s ease-in-out infinite alternate;
    transition: opacity 0.3s ease;
  }}
  
  @keyframes pulse {{
    0% {{ height: 15%; opacity: 0.6; }}
    50% {{ height: 75%; opacity: 1; }}
    100% {{ height: 30%; opacity: 0.7; }}
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
    transition: all 0.2s ease;
  }}
  .volume-knob:hover {{ height: 8px; }}
  .volume-knob::-webkit-slider-thumb {{
    -webkit-appearance: none;
    appearance: none;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: #cfd8dc;
    box-shadow: 0 2px 6px rgba(200,200,200,.7);
    transition: transform 0.2s ease;
    cursor: grab;
  }}
  .volume-knob::-webkit-slider-thumb:hover {{ transform: scale(1.2); }}
  .volume-knob::-webkit-slider-thumb:active {{ cursor: grabbing; }}
  .volume-knob::-moz-range-thumb {{
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: #cfd8dc;
    box-shadow: 0 2px 6px rgba(200,200,200,.7);
    cursor: pointer;
    border: none;
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

  const AudioContext = window.AudioContext || window.webkitAudioContext;
  const audioContext = new AudioContext();
  
  const masterGain = audioContext.createGain();
  masterGain.gain.value = 1.0;
  masterGain.connect(audioContext.destination);
  
  const masterAnalyser = audioContext.createAnalyser();
  masterAnalyser.fftSize = 2048;
  masterGain.connect(masterAnalyser);

  const grooveAWS = WaveSurfer.create({{
    container: '#waveform',
    waveColor: '#4a5568',
    progressColor: '#5f6bff',
    height: 140,
    backend: 'WebAudio',
    audioContext: audioContext,
    cursorWidth: 2,
    cursorColor: '#fff',
    barWidth: 3,
    barGap: 2,
    barRadius: 3,
    responsive: true,
    normalize: true
  }});

  function createHiddenWS() {{
    const div = document.createElement('div');
    div.style.display = 'none';
    document.body.appendChild(div);
    return WaveSurfer.create({{
      container: div,
      backend: 'WebAudio',
      audioContext: audioContext
    }});
  }}

  const stems = {{
    grooveB: createHiddenWS(),
    grooveC: createHiddenWS(),
    lyricsA: createHiddenWS(),
    lyricsB: createHiddenWS(),
    lyricsC: createHiddenWS(),
    soloA: createHiddenWS(),
    soloB: createHiddenWS(),
    soloC: createHiddenWS(),
    harmony_narrow: createHiddenWS(),
    harmony_wide: createHiddenWS(),
    adlibA: createHiddenWS(),
    adlibB: createHiddenWS(),
    adlibC: createHiddenWS()
  }};

  let currentLyrics = 'A';
  let currentGroove = 'A';
  let currentSolo = 'A';
  let spatializeOn = false;
  let backVocalsOn = false;
  let isPlaying = false;
  let allReady = false;
  let readyCount = 0;
  let isLooping = false;
  
  let lyricsVolume = 1.0;
  let grooveVolume = 1.0;
  let soloVolume = 1.0;
  let spatializeVolume = 1.0;
  let backVocalsVolume = 1.0;

  const mutedStems = new Set();

  const playBtn = document.getElementById('playBtn');
  const loopBtn = document.getElementById('loopBtn');
  const exportBtn = document.getElementById('exportBtn');
  const loadingStatus = document.getElementById('loadingStatus');
  const lyricsPointer = document.getElementById('lyricsPointer');
  const lyricsLabels = Array.from(document.querySelectorAll('[data-lyrics]'));
  const groovePointer = document.getElementById('groovePointer');
  const grooveLabels = Array.from(document.querySelectorAll('[data-groove]'));
  const soloPointer = document.getElementById('soloPointer');
  const soloLabels = Array.from(document.querySelectorAll('[data-solo]'));
  const spatializePointer = document.getElementById('spatializePointer');
  const spatializeLabels = Array.from(document.querySelectorAll('[data-spatialize]'));
  const backVocalsPointer = document.getElementById('backVocalsPointer');
  const backVocalsLabels = Array.from(document.querySelectorAll('[data-backvocals]'));
  const timeDisplay = document.getElementById('time-display');
  const volSlider = document.getElementById('volumeSlider');
  const visualizer = document.querySelector('.visualizer-container');
  const lyricsDisplay = document.getElementById('lyricsDisplay');
  const grooveDisplay = document.getElementById('grooveDisplay');
  const soloDisplay = document.getElementById('soloDisplay');
  const spatializeDisplay = document.getElementById('spatializeDisplay');
  const backVocalsDisplay = document.getElementById('backVocalsDisplay');

  // Mute button handling
  const muteButtons = document.querySelectorAll('.mute-btn');
  muteButtons.forEach(btn => {{
    btn.addEventListener('click', (e) => {{
      e.stopPropagation();
      const stem = btn.getAttribute('data-stem');
      if (mutedStems.has(stem)) {{
        mutedStems.delete(stem);
        btn.classList.remove('active');
        btn.closest('.control-section').classList.remove('muted');
      }} else {{
        mutedStems.add(stem);
        btn.classList.add('active');
        btn.closest('.control-section').classList.add('muted');
      }}
      updateVolumes();
    }});
  }});

  // Loop button
  loopBtn.addEventListener('click', () => {{
    isLooping = !isLooping;
    grooveAWS.setOptions({{ 
      interact: true,
      hideScrollbar: false
    }});
    if (isLooping) {{
      loopBtn.classList.add('active');
    }} else {{
      loopBtn.classList.remove('active');
    }}
  }});

  // Export button
  exportBtn.addEventListener('click', () => {{
    const settings = {{
      lyrics: currentLyrics,
      groove: currentGroove,
      solo: currentSolo,
      spatialize: spatializeOn ? 'wide' : 'narrow',
      backVocals: backVocalsOn ? 'on' : 'off',
      volumes: {{
        master: parseFloat(volSlider.value),
        lyrics: lyricsVolume,
        groove: grooveVolume,
        solo: soloVolume,
        spatialize: spatializeVolume,
        backVocals: backVocalsVolume
      }},
      mutedStems: Array.from(mutedStems)
    }};
    console.log('Export settings:', settings);
    alert('Mix settings saved! Ready for submission.\\n\\n' + JSON.stringify(settings, null, 2));
  }});

  function formatTime(sec) {{
    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60).toString().padStart(2, '0');
    return m + ':' + s;
  }}

  function updateTime() {{
    const cur = grooveAWS.getCurrentTime();
    const total = grooveAWS.getDuration();
    timeDisplay.textContent = formatTime(cur) + ' / ' + formatTime(total);
  }}

  function checkReady() {{
    readyCount++;
    console.log('Ready:', readyCount + '/14');
    loadingStatus.textContent = 'Loading... (' + readyCount + '/14)';
    
    if (readyCount === 14) {{
      allReady = true;
      console.log('✅ All stems ready!');
      loadingStatus.textContent = '✅ Ready to mix!';
      loadingStatus.style.color = '#4CAF50';
      
      playBtn.disabled = false;
      playBtn.style.opacity = '1';
      
      updateVolumes();
      
      console.log('✅ Ready to create your version!');
    }}
  }}

  function updateVolumes() {{
    const masterVol = parseFloat(volSlider.value);
    
    const grooveMuted = mutedStems.has('groove');
    const grooveVol = grooveMuted ? 0 : masterVol * grooveVolume;
    grooveAWS.setVolume(currentGroove === 'A' ? grooveVol : 0);
    stems.grooveB.setVolume(currentGroove === 'B' ? grooveVol : 0);
    stems.grooveC.setVolume(currentGroove === 'C' ? grooveVol : 0);
    
    const lyricsMuted = mutedStems.has('lyrics');
    const lyricsVol = lyricsMuted ? 0 : masterVol * lyricsVolume;
    stems.lyricsA.setVolume(currentLyrics === 'A' ? lyricsVol : 0);
    stems.lyricsB.setVolume(currentLyrics === 'B' ? lyricsVol : 0);
    stems.lyricsC.setVolume(currentLyrics === 'C' ? lyricsVol : 0);
    
    const soloMuted = mutedStems.has('solo');
    const soloVol = soloMuted ? 0 : masterVol * soloVolume;
    stems.soloA.setVolume(currentSolo === 'A' ? soloVol : 0);
    stems.soloB.setVolume(currentSolo === 'B' ? soloVol : 0);
    stems.soloC.setVolume(currentSolo === 'C' ? soloVol : 0);
    
    const spatMuted = mutedStems.has('spatialize');
    const spatVol = spatMuted ? 0 : masterVol * spatializeVolume;
    stems.harmony_narrow.setVolume(!spatializeOn ? spatVol : 0);
    stems.harmony_wide.setVolume(spatializeOn ? spatVol : 0);
    
    const backMuted = mutedStems.has('backvocals');
    const backVol = backMuted ? 0 : masterVol * backVocalsVolume;
    stems.adlibA.setVolume(backVocalsOn && currentLyrics === 'A' ? backVol : 0);
    stems.adlibB.setVolume(backVocalsOn && currentLyrics === 'B' ? backVol : 0);
    stems.adlibC.setVolume(backVocalsOn && currentLyrics === 'C' ? backVol : 0);
  }}

  function playAll() {{
    if (!allReady) return;
    
    if (audioContext.state === 'suspended') {{
      audioContext.resume();
    }}
    
    isPlaying = true;
    const currentTime = grooveAWS.getCurrentTime();
    grooveAWS.play(currentTime);
    Object.values(stems).forEach(ws => ws.play(currentTime));
  }}

  function pauseAll() {{
    isPlaying = false;
    grooveAWS.pause();
    Object.values(stems).forEach(ws => ws.pause());
  }}

  grooveAWS.load(audioMap.grooveA);
  
  grooveAWS.on('error', (err) => {{
    console.error('Groove A load error:', err);
    loadingStatus.textContent = '❌ Error loading audio. Check console.';
    loadingStatus.style.color = '#f44336';
  }});
  
  grooveAWS.on('ready', () => {{
    console.log('✓ Groove A');
    updateTime();
    const grooveBackend = grooveAWS.backend;
    if (grooveBackend && grooveBackend.gainNode) {{
      grooveBackend.gainNode.disconnect();
      grooveBackend.gainNode.connect(masterGain);
    }}
    checkReady();
  }});

  Object.keys(stems).forEach(key => {{
    stems[key].load(audioMap[key]);
    
    stems[key].on('error', (err) => {{
      console.error(key + ' load error:', err);
      loadingStatus.textContent = '❌ Error loading ' + key;
      loadingStatus.style.color = '#f44336';
    }});
    
    stems[key].on('ready', () => {{
      console.log('✓', key);
      const backend = stems[key].backend;
      if (backend && backend.gainNode) {{
        backend.gainNode.disconnect();
        backend.gainNode.connect(masterGain);
      }}
      checkReady();
    }});
  }});

  grooveAWS.on('audioprocess', updateTime);
  grooveAWS.on('finish', () => {{
    if (isLooping) {{
      grooveAWS.seekTo(0);
      Object.values(stems).forEach(ws => ws.seekTo(0));
      playAll();
    }} else {{
      pauseAll();
      playBtn.textContent = '▶';
      playBtn.classList.remove('pause');
      visualizer.classList.add('paused');
    }}
  }});

  playBtn.addEventListener('click', () => {{
    if (isPlaying) {{
      pauseAll();
      playBtn.textContent = '▶';
      playBtn.classList.remove('pause');
      visualizer.classList.add('paused');
    }} else {{
      playAll();
      playBtn.textContent = '⏸';
      playBtn.classList.add('pause');
      visualizer.classList.remove('paused');
    }}
  }});

  function setLyricsActive(version) {{
    lyricsLabels.forEach(el => {{
      el.classList.toggle('active', el.getAttribute('data-lyrics') === version);
    }});
    lyricsPointer.style.transform = 'translate(-50%, 0) rotate(' + lyricsAngles[version] + 'deg)';
    lyricsDisplay.textContent = 'Lyrics ' + version;
  }}

  function switchLyrics(version) {{
    if (version === currentLyrics) return;
    currentLyrics = version;
    updateVolumes();
    setLyricsActive(version);
  }}

  document.getElementById('lyricsKnob').addEventListener('click', () => {{
    const next = {{"A": "B", "B": "C", "C": "A"}}[currentLyrics];
    switchLyrics(next);
  }});

  lyricsLabels.forEach(el => {{
    el.addEventListener('click', (e) => {{
      e.stopPropagation();
      switchLyrics(el.getAttribute('data-lyrics'));
    }});
  }});

  function setGrooveActive(version) {{
    grooveLabels.forEach(el => {{
      el.classList.toggle('active', el.getAttribute('data-groove') === version);
    }});
    groovePointer.style.transform = 'translate(-50%, 0) rotate(' + grooveAngles[version] + 'deg)';
    grooveDisplay.textContent = 'Groove ' + version;
  }}

  function switchGroove(version) {{
    if (version === currentGroove) return;
    currentGroove = version;
    updateVolumes();
    setGrooveActive(version);
  }}

  document.getElementById('grooveKnob').addEventListener('click', () => {{
    const next = {{"A": "B", "B": "C", "C": "A"}}[currentGroove];
    switchGroove(next);
  }});

  grooveLabels.forEach(el => {{
    el.addEventListener('click', (e) => {{
      e.stopPropagation();
      switchGroove(el.getAttribute('data-groove'));
    }});
  }});

  function setSoloActive(version) {{
    soloLabels.forEach(el => {{
      el.classList.toggle('active', el.getAttribute('data-solo') === version);
    }});
    soloPointer.style.transform = 'translate(-50%, 0) rotate(' + soloAngles[version] + 'deg)';
    soloDisplay.textContent = 'Take ' + version;
  }}

  function switchSolo(version) {{
    if (version === currentSolo) return;
    currentSolo = version;
    updateVolumes();
    setSoloActive(version);
  }}

  document.getElementById('soloKnob').addEventListener('click', () => {{
    const next = {{"A": "B", "B": "C", "C": "A"}}[currentSolo];
    switchSolo(next);
  }});

  soloLabels.forEach(el => {{
    el.addEventListener('click', (e) => {{
      e.stopPropagation();
      switchSolo(el.getAttribute('data-solo'));
    }});
  }});

  document.getElementById('spatializeKnob').addEventListener('click', () => {{
    toggleSpatialize();
  }});

  spatializeLabels.forEach(el => {{
    el.addEventListener('click', (e) => {{
      e.stopPropagation();
      const isWide = el.getAttribute('data-spatialize') === 'wide';
      if (isWide !== spatializeOn) {{
        toggleSpatialize();
      }}
    }});
  }});

  function toggleSpatialize() {{
    spatializeOn = !spatializeOn;
    updateVolumes();
    spatializeLabels.forEach(el => {{
      const isWide = el.getAttribute('data-spatialize') === 'wide';
      el.classList.toggle('active', isWide === spatializeOn);
    }});
    const angle = spatializeOn ? 90 : 270;
    spatializePointer.style.transform = 'translate(-50%, 0) rotate(' + angle + 'deg)';
    spatializeDisplay.textContent = spatializeOn ? 'Wide' : 'Narrow';
  }}

  document.getElementById('backVocalsKnob').addEventListener('click', () => {{
    toggleBackVocals();
  }});

  backVocalsLabels.forEach(el => {{
    el.addEventListener('click', (e) => {{
      e.stopPropagation();
      const isOn = el.getAttribute('data-backvocals') === 'on';
      if (isOn !== backVocalsOn) {{
        toggleBackVocals();
      }}
    }});
  }});

  function toggleBackVocals() {{
    backVocalsOn = !backVocalsOn;
    updateVolumes();
    backVocalsLabels.forEach(el => {{
      const isOn = el.getAttribute('data-backvocals') === 'on';
      el.classList.toggle('active', isOn === backVocalsOn);
    }});
    const angle = backVocalsOn ? 90 : 270;
    backVocalsPointer.style.transform = 'translate(-50%, 0) rotate(' + angle + 'deg)';
    backVocalsDisplay.textContent = backVocalsOn ? 'On' : 'Off';
  }}

  function updateSliderGradient(value) {{
    const percent = value * 100;
    volSlider.style.background = 'linear-gradient(to right, #5f6bff ' + percent + '%, #3a4150 ' + percent + '%)';
  }}

  volSlider.addEventListener('input', e => {{
    updateSliderGradient(e.target.value);
    updateVolumes();
  }});

  let isSeeking = false;
  let wasPlayingBeforeSeek = false;

  grooveAWS.on('interaction', () => {{
    if (isPlaying && !isSeeking) {{
      console.log('Seeking started - pausing playback');
      isSeeking = true;
      wasPlayingBeforeSeek = true;
      grooveAWS.pause();
      Object.values(stems).forEach(ws => ws.pause());
      isPlaying = false;
    }}
  }});

  grooveAWS.on('seek', (progress) => {{
    const targetTime = progress * grooveAWS.getDuration();
    console.log('Seek to:', targetTime);
    Object.values(stems).forEach(ws => {{
      ws.setTime(Math.min(targetTime, ws.getDuration() - 0.01));
    }});
    if (wasPlayingBeforeSeek) {{
      setTimeout(() => {{
        if (isSeeking) {{
          console.log('Seek ended - restarting playback');
          isSeeking = false;
          wasPlayingBeforeSeek = false;
          const exactTime = grooveAWS.getCurrentTime();
          console.log('Restarting all at exact time:', exactTime);
          isPlaying = true;
          grooveAWS.play(exactTime);
          Object.values(stems).forEach(ws => ws.play(exactTime));
        }}
      }}, 100);
    }}
  }});

  document.addEventListener('keydown', (e) => {{
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.tagName === 'SELECT') return;
    switch(e.key) {{
      case ' ':
        e.preventDefault();
        playBtn.click();
        break;
      case '1':
        e.preventDefault();
        switchLyrics('A');
        break;
      case '2':
        e.preventDefault();
        switchLyrics('B');
        break;
      case '3':
        e.preventDefault();
        switchLyrics('C');
        break;
      case 'ArrowLeft':
        e.preventDefault();
        grooveAWS.skip(-5);
        Object.values(stems).forEach(ws => ws.skip(-5));
        break;
      case 'ArrowRight':
        e.preventDefault();
        grooveAWS.skip(5);
        Object.values(stems).forEach(ws => ws.skip(5));
        break;
      case 'ArrowUp':
        e.preventDefault();
        const newVolUp = Math.min(1, parseFloat(volSlider.value) + 0.1);
        volSlider.value = newVolUp;
        updateSliderGradient(newVolUp);
        updateVolumes();
        break;
      case 'ArrowDown':
        e.preventDefault();
        const newVolDown = Math.max(0, parseFloat(volSlider.value) - 0.1);
        volSlider.value = newVolDown;
        updateSliderGradient(newVolDown);
        updateVolumes();
        break;
      case 'l':
      case 'L':
        e.preventDefault();
        loopBtn.click();
        break;
      case 'e':
      case 'E':
        e.preventDefault();
        exportBtn.click();
        break;
    }}
  }});

  document.getElementById('waveform').style.cursor = 'pointer';
  updateSliderGradient(1);

  // Individual volume knobs
  const lyricsVolumeSlider = document.getElementById('lyricsVolume');
  const lyricsVolumeDisplay = document.getElementById('lyricsVolumeDisplay');
  const grooveVolumeSlider = document.getElementById('grooveVolume');
  const grooveVolumeDisplay = document.getElementById('grooveVolumeDisplay');
  const soloVolumeSlider = document.getElementById('soloVolume');
  const soloVolumeDisplay = document.getElementById('soloVolumeDisplay');
  const spatializeVolumeSlider = document.getElementById('spatializeVolume');
  const spatializeVolumeDisplay = document.getElementById('spatializeVolumeDisplay');
  const backVocalsVolumeSlider = document.getElementById('backVocalsVolume');
  const backVocalsVolumeDisplay = document.getElementById('backVocalsVolumeDisplay');

  function updateVolumeKnobGradient(slider, value) {{
    const percent = value;
    slider.style.background = 'linear-gradient(to right, #5f6bff ' + percent + '%, #3a4150 ' + percent + '%)';
  }}

  lyricsVolumeSlider.addEventListener('input', e => {{
    const val = parseInt(e.target.value);
    lyricsVolume = val / 100;
    lyricsVolumeDisplay.textContent = val + '%';
    updateVolumeKnobGradient(lyricsVolumeSlider, val);
    updateVolumes();
  }});

  grooveVolumeSlider.addEventListener('input', e => {{
    const val = parseInt(e.target.value);
    grooveVolume = val / 100;
    grooveVolumeDisplay.textContent = val + '%';
    updateVolumeKnobGradient(grooveVolumeSlider, val);
    updateVolumes();
  }});

  soloVolumeSlider.addEventListener('input', e => {{
    const val = parseInt(e.target.value);
    soloVolume = val / 100;
    soloVolumeDisplay.textContent = val + '%';
    updateVolumeKnobGradient(soloVolumeSlider, val);
    updateVolumes();
  }});

  spatializeVolumeSlider.addEventListener('input', e => {{
    const val = parseInt(e.target.value);
    spatializeVolume = val / 100;
    spatializeVolumeDisplay.textContent = val + '%';
    updateVolumeKnobGradient(spatializeVolumeSlider, val);
    updateVolumes();
  }});

  backVocalsVolumeSlider.addEventListener('input', e => {{
    const val = parseInt(e.target.value);
    backVocalsVolume = val / 100;
    backVocalsVolumeDisplay.textContent = val + '%';
    updateVolumeKnobGradient(backVocalsVolumeSlider, val);
    updateVolumes();
  }});

  // Initialize volume knob gradients
  updateVolumeKnobGradient(lyricsVolumeSlider, 100);
  updateVolumeKnobGradient(grooveVolumeSlider, 100);
  updateVolumeKnobGradient(soloVolumeSlider, 100);
  updateVolumeKnobGradient(spatializeVolumeSlider, 100);
  updateVolumeKnobGradient(backVocalsVolumeSlider, 100);
</script>
"""

st.components.v1.html(html, height=1900)

# Below the player: Contributor features
st.markdown("<h2 style='margin-top:40px; text-align:center;'>🎚️ Your Contributor Tools</h2>", unsafe_allow_html=True)

# Upload section
with st.expander("**📤 UPLOAD YOUR OWN STEMS**", expanded=False):
    st.markdown("""
    <div style="background:rgba(76,175,80,0.05); border-left:4px solid #4CAF50; padding:15px; border-radius:8px; margin-bottom:20px;">
        <div style="color:#4CAF50; font-weight:600; margin-bottom:8px;">💡 Contributor Guidelines</div>
        <ul style="color:#8b92a8; font-size:13px; line-height:1.8;">
            <li><strong>Mute First:</strong> Click the 🔇 button on any stem to mute the original</li>
            <li><strong>Upload Your Version:</strong> Add your own recording below</li>
            <li><strong>Same Length Required:</strong> Your stem must match the song duration</li>
            <li><strong>Quality Standards:</strong> WAV/AIFF preferred, 24-bit, 48kHz minimum</li>
            <li><strong>Be Creative:</strong> Reinterpret, don't just copy!</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🎤 Replace Vocals/Lyrics**")
        uploaded_vocals = st.file_uploader(
            "Upload your vocal track",
            type=["wav", "aiff", "mp3"],
            key="contributor_vocals"
        )
        if uploaded_vocals:
            st.session_state.my_uploads['vocals'] = uploaded_vocals
            st.success(f"✓ {uploaded_vocals.name} uploaded")
        
        st.markdown("**🎸 Replace Solo**")
        uploaded_solo = st.file_uploader(
            "Upload your solo",
            type=["wav", "aiff", "mp3"],
            key="contributor_solo"
        )
        if uploaded_solo:
            st.session_state.my_uploads['solo'] = uploaded_solo
            st.success(f"✓ {uploaded_solo.name} uploaded")
    
    with col2:
        st.markdown("**🥁 Replace Groove**")
        uploaded_groove = st.file_uploader(
            "Upload your groove/drums",
            type=["wav", "aiff", "mp3"],
            key="contributor_groove"
        )
        if uploaded_groove:
            st.session_state.my_uploads['groove'] = uploaded_groove
            st.success(f"✓ {uploaded_groove.name} uploaded")
        
        st.markdown("**🎹 Add Instrumental Layer**")
        uploaded_instrument = st.file_uploader(
            "Upload additional instrument",
            type=["wav", "aiff", "mp3"],
            key="contributor_instrument"
        )
        if uploaded_instrument:
            st.session_state.my_uploads['instrument'] = uploaded_instrument
            st.success(f"✓ {uploaded_instrument.name} uploaded")

# Submission section
st.markdown("<h3 style='margin-top:40px;'>📝 Submit Your Version</h3>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    version_name = st.text_input(
        "Version Name",
        placeholder="e.g., 'Dark Atmospheric Take' or 'Upbeat Remix'",
        key="version_name"
    )
    
    version_description = st.text_area(
        "Description (Optional)",
        placeholder="Describe what makes your version unique...",
        height=100,
        key="version_description"
    )

with col2:
    st.markdown("""
    <div style="background:rgba(255,255,255,0.03); padding:20px; border-radius:12px; height:100%;">
        <div style="color:#8b92a8; font-size:13px; margin-bottom:15px; font-weight:600;">📊 YOUR STATS</div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:15px;">
            <div style="text-align:center;">
                <div style="font-size:28px; color:#4CAF50; font-weight:700;">{}</div>
                <div style="font-size:11px; color:#8b92a8; margin-top:5px;">SUBMISSIONS</div>
            </div>
            <div style="text-align:center;">
                <div style="font-size:28px; color:#5f6bff; font-weight:700;">{}</div>
                <div style="font-size:11px; color:#8b92a8; margin-top:5px;">AVG RANKING</div>
            </div>
        </div>
    </div>
    """.format(
        st.session_state.submission_count,
        st.session_state.my_ranking if st.session_state.my_ranking else "—"
    ), unsafe_allow_html=True)

# Action buttons
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("💾 Save Draft", use_container_width=True):
        st.success("Draft saved! You can continue working on it later.")

with col2:
    if st.button("👁️ Preview Mix", use_container_width=True):
        st.info("Preview your mix before submitting (plays current settings)")

with col3:
    if st.button("🔄 Reset All", use_container_width=True):
        st.session_state.my_uploads = {}
        st.session_state.muted_stems = set()
        st.rerun()

with col4:
    if st.button("🚀 Submit Version", use_container_width=True, type="primary"):
        if version_name and version_name.strip():
            st.session_state.submission_count += 1
            st.success(f"🎉 Version '{version_name}' submitted! It will enter peer review.")
            st.balloons()
        else:
            st.error("Please provide a version name before submitting.")

# Peer review section
st.markdown("<h3 style='margin-top:50px;'>🗳️ Peer Review - Vote on Other Versions</h3>", unsafe_allow_html=True)

st.markdown("""
<div style="background:rgba(95,107,255,0.05); border-left:4px solid #5f6bff; padding:15px; border-radius:8px; margin-bottom:20px;">
    <div style="color:#5f6bff; font-weight:600; margin-bottom:8px;">ℹ️ How Peer Review Works</div>
    <p style="color:#8b92a8; font-size:13px; line-height:1.6; margin:0;">
        Listen to other contributors' versions and vote for the ones you think are best. Higher-ranked versions 
        have a better chance of being heard by listeners and the artist. Vote honestly and constructively!
    </p>
</div>
""", unsafe_allow_html=True)

# Mock peer review items
peer_versions = [
    {"name": "Ethereal Dream Mix", "contributor": "@soundwaver_42", "votes": 23},
    {"name": "Aggressive Rock Take", "contributor": "@guitarslinger", "votes": 18},
    {"name": "Lo-fi Bedroom Version", "contributor": "@bedroomproducer", "votes": 15},
]

for i, version in enumerate(peer_versions):
    col1, col2, col3 = st.columns([3, 2, 1])
    
    with col1:
        st.markdown(f"""
        <div style="color:#ffffff; font-weight:600; font-size:15px;">{version['name']}</div>
        <div style="color:#8b92a8; font-size:12px; margin-top:3px;">by {version['contributor']}</div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="text-align:center; padding:10px; background:rgba(255,255,255,0.03); border-radius:8px;">
            <div style="color:#FDD835; font-weight:600;">{version['votes']} votes</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.button("👍 Vote", key=f"vote_{i}", use_container_width=True):
            st.success(f"Voted for {version['name']}!")
    
    st.markdown("<hr style='border:0; border-top:1px solid rgba(255,255,255,0.05); margin:15px 0;'>", unsafe_allow_html=True)

# Leaderboard preview
st.markdown("<h3 style='margin-top:40px;'>🏆 Current Leaderboard (Top 5)</h3>", unsafe_allow_html=True)

leaderboard = [
    {"rank": 1, "name": "Neo-Soul Reimagining", "contributor": "@groovycat", "votes": 89},
    {"rank": 2, "name": "Stripped Down Acoustic", "contributor": "@folkstar", "votes": 76},
    {"rank": 3, "name": "Electronic Fusion", "contributor": "@synthwave_ninja", "votes": 64},
    {"rank": 4, "name": "Jazz-Hop Blend", "contributor": "@jazzhands", "votes": 52},
    {"rank": 5, "name": "Punk Energy Version", "contributor": "@punknotdead", "votes": 48},
]

for entry in leaderboard:
    st.markdown(f"""
    <div style="display:flex; align-items:center; justify-content:space-between; padding:15px; background:rgba(255,255,255,0.03); border-radius:10px; margin:10px 0;">
        <div style="display:flex; align-items:center; gap:15px;">
            <div style="font-size:22px; color:#4CAF50; font-weight:700; min-width:35px;">#{entry['rank']}</div>
            <div>
                <div style="color:#ffffff; font-weight:600; font-size:15px;">{entry['name']}</div>
                <div style="color:#8b92a8; font-size:12px; margin-top:3px;">by {entry['contributor']}</div>
            </div>
        </div>
        <div style="color:#FDD835; font-weight:600; font-size:16px;">{entry['votes']} votes</div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align:center; margin-top:60px; padding:30px; background:rgba(255,255,255,0.02); border-radius:12px;">
  <div style="color:#8b92a8; font-size:13px; font-family:'Inter', sans-serif; margin-bottom:15px; font-weight:600;">
    🎚️ CONTRIBUTOR BENEFITS
  </div>
  <p style="color:#6b7280; font-size:12px; font-family:'Inter', sans-serif; line-height:1.8; margin-bottom:15px;">
    • Full creative control over stems and mixing<br>
    • Upload your own recordings to replace any stem<br>
    • Vote on other contributors' versions<br>
    • Compete for top rankings
  </p>
  
  <p style="color:#8b92a8; font-size:12px; line-height:1.7; margin-top:20px;">
    If the artist selects your mix for official release, you'll earn a percentage of 
    performance royalties as recognition for your contribution.
  </p>
  
  <p style="font-size:10px; color:#6b7280; margin-top:15px;">
    Platform designed by Peyman Salimi • CCML Lab • Georgia Institute of Technology
  </p>
</div>
""", unsafe_allow_html=True)


#version2 before addtional stems
'''
import streamlit as st
import json

st.set_page_config(layout="wide", page_title="FluXTape Contributor", page_icon="🎚️")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
  background: linear-gradient(160deg, #0f1115 0%, #1a1d25 100%) fixed !important;
}
[data-testid="stHeader"] {
  background: rgba(0,0,0,0) !important;
}
[data-testid="stSidebar"] {
  background: rgba(0,0,0,0.15) !important;
}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'my_uploads' not in st.session_state:
    st.session_state.my_uploads = {}
if 'muted_stems' not in st.session_state:
    st.session_state.muted_stems = set()
if 'submission_count' not in st.session_state:
    st.session_state.submission_count = 0
if 'my_ranking' not in st.session_state:
    st.session_state.my_ranking = None

audio_map = {
    "groove": "https://raw.githubusercontent.com/theallophones/audio/main/groove.mp3",
    "lyricsA": "https://raw.githubusercontent.com/theallophones/audio/main/lyricsA.mp3",
    "lyricsB": "https://raw.githubusercontent.com/theallophones/audio/main/lyricsB.mp3",
    "lyricsC": "https://raw.githubusercontent.com/theallophones/audio/main/lyricsC.mp3",
    "soloA": "https://raw.githubusercontent.com/theallophones/audio/main/soloA.mp3",
    "soloB": "https://raw.githubusercontent.com/theallophones/audio/main/soloB.mp3",
    "harmony_narrow": "https://raw.githubusercontent.com/theallophones/audio/main/harmony_narrow.mp3",
    "harmony_wide": "https://raw.githubusercontent.com/theallophones/audio/main/harmony_wide.mp3",
    "adlibA": "https://raw.githubusercontent.com/theallophones/audio/main/adlibA.mp3",
    "adlibB": "https://raw.githubusercontent.com/theallophones/audio/main/adlibB.mp3",
    "adlibC": "https://raw.githubusercontent.com/theallophones/audio/main/adlibC.mp3",
}

audio_map_json = json.dumps(audio_map)

html = f"""
<div style="text-align:center; margin-bottom:20px;">
  <h1 style="font-family:'Inter', sans-serif; font-weight:700; color:#ffffff; font-size:36px; margin-bottom:8px; letter-spacing:-0.5px;">
    FluXTape / Contributor Interface
  </h1>
  <h3 style="font-family:'Inter', sans-serif; font-weight:400; color:#8b92a8; font-size:14px; margin-top:0; letter-spacing:0.5px;">
    Mid-nite Free-Quensee by Zlisterr
  </h3>
  <div id="loadingStatus" style="color:#8b92a8; margin:10px 0; font-size:14px;">Loading audio files...</div>
  <div style="margin-top:15px;">
    <button id="playBtn" class="play-btn" title="Play/Pause (Space)" disabled style="opacity:0.5;">▶</button>
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
  <div class="vis-bar" style="animation-delay: 0.18s;"></div>
  <div class="vis-bar" style="animation-delay: 0.08s;"></div>
  <div class="vis-bar" style="animation-delay: 0.22s;"></div>
  <div class="vis-bar" style="animation-delay: 0.28s;"></div>
</div> 

<div style="display:flex; justify-content:center; align-items:center; margin-top:20px; gap:20px;">
  <div id="time-display" style="color:#ffffff; font-family:'JetBrains Mono', 'Courier New', monospace; font-size:24px; font-weight:600; letter-spacing:2px;">
    0:00 / 0:00
  </div>
  <div style="display:flex; gap:10px;">
    <button id="loopBtn" class="control-btn" title="Toggle Loop">🔁</button>
    <button id="exportBtn" class="control-btn" title="Export Current Mix">💾</button>
  </div>
</div>

<div style="text-align:center; margin:25px 0;">
  <div style="color:#8b92a8; font-size:22px; margin-bottom:8px;">🔊</div>
  <input id="volumeSlider" type="range" min="0" max="1" step="0.01" value="1" class="slider" title="Master Volume">
</div>

<div class="controls-grid">
  <div class="control-section">
    <div class="control-header">
      LYRICS
      <button class="mute-btn" data-stem="lyrics" title="Mute to replace with your own">🔇</button>
    </div>
    <div class="knob-wrap-small">
      <div id="lyricsKnob" class="knob-small" title="Click to cycle lyrics">
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
    <div class="control-header">
      SOLO <span style="font-size:10px; font-weight:400; opacity:0.7;">(from 1:03)</span>
      <button class="mute-btn" data-stem="solo" title="Mute to replace with your own">🔇</button>
    </div>
    <div class="knob-wrap-small">
      <div id="soloKnob" class="knob-small" title="Click to switch solo">
        <div id="soloPointer" class="pointer-small"></div>
        <div class="center-dot-small"></div>
      </div>
      <div class="label-small labelLeft-small active" data-solo="A">A</div>
      <div class="label-small labelRight-small" data-solo="B">B</div>
    </div>
    <div id="soloDisplay" class="version-badge">Take A</div>
    <div class="volume-knob-container">
      <input type="range" id="soloVolume" class="volume-knob" min="0" max="100" value="100">
      <div class="volume-label">Volume: <span id="soloVolumeDisplay">100%</span></div>
    </div>
  </div>

  <div class="control-section">
    <div class="control-header">
      SPATIALIZE
      <button class="mute-btn" data-stem="spatialize" title="Mute to replace with your own">🔇</button>
    </div>
    <div class="knob-wrap-small">
      <div id="spatializeKnob" class="knob-small" title="Click to toggle spatialize">
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
    <div class="control-header">
      BACK VOCALS
      <button class="mute-btn" data-stem="backvocals" title="Mute to replace with your own">🔇</button>
    </div>
    <div class="knob-wrap-small">
      <div id="backVocalsKnob" class="knob-small" title="Click to toggle back vocals">
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

  <div class="control-section">
    <div class="control-header">
      GROOVE
      <button class="mute-btn" data-stem="groove" title="Mute to replace with your own">🔇</button>
    </div>
    <div style="text-align:center; margin:20px 0;">
      <div style="font-size:32px; color:#4CAF50;">🥁</div>
      <div style="color:#8b92a8; font-size:13px; margin-top:10px;">Rhythm Section</div>
    </div>
    <div class="volume-knob-container">
      <input type="range" id="grooveVolume" class="volume-knob" min="0" max="100" value="100">
      <div class="volume-label">Volume: <span id="grooveVolumeDisplay">100%</span></div>
    </div>
  </div>
</div>

<div style="text-align:center; margin-top:30px; padding:20px; background:rgba(255,255,255,0.03); border-radius:12px; max-width:600px; margin-left:auto; margin-right:auto;">
  <div style="color:#8b92a8; font-size:13px; font-family:'Inter', sans-serif; margin-bottom:10px; font-weight:600;">
    ⌨️ KEYBOARD SHORTCUTS
  </div>
  <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; color:#6b7280; font-size:12px; font-family:'Inter', sans-serif;">
    <div><kbd style="background:#2a2f3a; padding:2px 8px; border-radius:4px; color:#fff;">Space</kbd> Play/Pause</div>
    <div><kbd style="background:#2a2f3a; padding:2px 8px; border-radius:4px; color:#fff;">←→</kbd> Seek ±5s</div>
    <div><kbd style="background:#2a2f3a; padding:2px 8px; border-radius:4px; color:#fff;">1/2/3</kbd> Lyrics A/B/C</div>
    <div><kbd style="background:#2a2f3a; padding:2px 8px; border-radius:4px; color:#fff;">↑↓</kbd> Volume ±10%</div>
    <div><kbd style="background:#2a2f3a; padding:2px 8px; border-radius:4px; color:#fff;">L</kbd> Toggle Loop</div>
    <div><kbd style="background:#2a2f3a; padding:2px 8px; border-radius:4px; color:#fff;">E</kbd> Export Mix</div>
  </div>
</div>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap');
  
  :root {{
    --bg: #0f1115;
    --accent: #4CAF50;
    --accent-hover: #66BB6A;
    --text: #ffffff;
    --text-muted: #8b92a8;
  }}
  
  * {{ font-family: 'Inter', sans-serif; }}

  html, body, .stApp {{
    height: 100%;
    margin: 0;
    background: linear-gradient(160deg, #0f1115 0%, #1a1d25 100%);
  }}

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
    box-shadow: 0 12px 32px rgba(76,175,80,.6);
  }}
  .play-btn:active {{ transform: scale(0.98); }}
  .play-btn.pause {{
    background: #FBC02D;
    box-shadow: 0 8px 24px rgba(251,192,45,.5);
  }}
  .play-btn.pause:hover {{
    background: #FDD835;
    box-shadow: 0 12px 32px rgba(251,192,45,.6);
  }}
  .play-btn:disabled {{
    cursor: not-allowed;
    opacity: 0.5;
  }}

  .control-btn {{
    width: 40px;
    height: 40px;
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.1);
    background: rgba(255,255,255,0.05);
    color: #fff;
    font-size: 18px;
    cursor: pointer;
    transition: all 0.2s ease;
  }}
  .control-btn:hover {{
    background: rgba(255,255,255,0.1);
    border-color: rgba(255,255,255,0.2);
    transform: scale(1.05);
  }}
  .control-btn.active {{
    background: #4CAF50;
    border-color: #66BB6A;
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
    position: relative;
  }}

  .control-section.muted {{
    opacity: 0.4;
    border: 2px solid rgba(251,192,45,0.5);
  }}

  .control-header {{
    color: #8b92a8;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 8px;
  }}

  .mute-btn {{
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    color: #8b92a8;
    padding: 4px 8px;
    border-radius: 6px;
    font-size: 12px;
    cursor: pointer;
    transition: all 0.2s ease;
  }}
  .mute-btn:hover {{
    background: rgba(255,255,255,0.1);
    color: #fff;
  }}
  .mute-btn.active {{
    background: rgba(251,192,45,0.2);
    border-color: #FBC02D;
    color: #FDD835;
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
  .knob-small:active {{ transform: scale(0.98); }}

  .center-dot-small {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #cfd8dc;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%,-50%);
    box-shadow: 0 1px 4px rgba(0,0,0,0.4);
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
    color: var(--text);
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
    border-color: #4a5160;
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
    transition: all 0.2s ease;
  }}
  .slider:hover {{ height: 9px; }}
  .slider::-webkit-slider-thumb {{
    -webkit-appearance: none;
    appearance: none;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: #cfd8dc;
    box-shadow: 0 2px 8px rgba(200,200,200,.7);
    transition: transform 0.2s ease;
    cursor: grab;
  }}
  .slider::-webkit-slider-thumb:hover {{ transform: scale(1.3); }}
  .slider::-webkit-slider-thumb:active {{ cursor: grabbing; }}
  .slider::-moz-range-thumb {{
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: #cfd8dc;
    box-shadow: 0 2px 8px rgba(200,200,200,.7);
    cursor: pointer;
    border: none;
  }}

  .visualizer-container {{
    display: flex;
    justify-content: center;
    align-items: flex-end;
    gap: 6px;
    height: 100px;
    margin: 25px auto;
    max-width: 400px;
    padding: 0 20px;
  }}
  
  .vis-bar {{
    width: 14px;
    background: linear-gradient(to top, #5f6bff, #8b9dff);
    border-radius: 8px 8px 0 0;
    height: 20%;
    box-shadow: 0 0 15px rgba(95, 107, 255, 0.5);
    animation: pulse 0.8s ease-in-out infinite alternate;
    transition: opacity 0.3s ease;
  }}
  
  @keyframes pulse {{
    0% {{ height: 15%; opacity: 0.6; }}
    50% {{ height: 75%; opacity: 1; }}
    100% {{ height: 30%; opacity: 0.7; }}
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
    transition: all 0.2s ease;
  }}
  .volume-knob:hover {{ height: 8px; }}
  .volume-knob::-webkit-slider-thumb {{
    -webkit-appearance: none;
    appearance: none;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: #cfd8dc;
    box-shadow: 0 2px 6px rgba(200,200,200,.7);
    transition: transform 0.2s ease;
    cursor: grab;
  }}
  .volume-knob::-webkit-slider-thumb:hover {{ transform: scale(1.2); }}
  .volume-knob::-webkit-slider-thumb:active {{ cursor: grabbing; }}
  .volume-knob::-moz-range-thumb {{
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: #cfd8dc;
    box-shadow: 0 2px 6px rgba(200,200,200,.7);
    cursor: pointer;
    border: none;
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

  const AudioContext = window.AudioContext || window.webkitAudioContext;
  const audioContext = new AudioContext();
  
  const masterGain = audioContext.createGain();
  masterGain.gain.value = 1.0;
  masterGain.connect(audioContext.destination);
  
  const masterAnalyser = audioContext.createAnalyser();
  masterAnalyser.fftSize = 2048;
  masterGain.connect(masterAnalyser);

  const grooveWS = WaveSurfer.create({{
    container: '#waveform',
    waveColor: '#4a5568',
    progressColor: '#5f6bff',
    height: 140,
    backend: 'WebAudio',
    audioContext: audioContext,
    cursorWidth: 2,
    cursorColor: '#fff',
    barWidth: 3,
    barGap: 2,
    barRadius: 3,
    responsive: true,
    normalize: true
  }});

  function createHiddenWS() {{
    const div = document.createElement('div');
    div.style.display = 'none';
    document.body.appendChild(div);
    return WaveSurfer.create({{
      container: div,
      backend: 'WebAudio',
      audioContext: audioContext
    }});
  }}

  const stems = {{
    lyricsA: createHiddenWS(),
    lyricsB: createHiddenWS(),
    lyricsC: createHiddenWS(),
    soloA: createHiddenWS(),
    soloB: createHiddenWS(),
    harmony_narrow: createHiddenWS(),
    harmony_wide: createHiddenWS(),
    adlibA: createHiddenWS(),
    adlibB: createHiddenWS(),
    adlibC: createHiddenWS()
  }};

  let currentLyrics = 'A';
  let currentSolo = 'A';
  let spatializeOn = false;
  let backVocalsOn = false;
  let isPlaying = false;
  let allReady = false;
  let readyCount = 0;
  let isLooping = false;
  
  let lyricsVolume = 1.0;
  let soloVolume = 1.0;
  let spatializeVolume = 1.0;
  let backVocalsVolume = 1.0;
  let grooveVolume = 1.0;

  const mutedStems = new Set();

  const playBtn = document.getElementById('playBtn');
  const loopBtn = document.getElementById('loopBtn');
  const exportBtn = document.getElementById('exportBtn');
  const loadingStatus = document.getElementById('loadingStatus');
  const lyricsPointer = document.getElementById('lyricsPointer');
  const lyricsLabels = Array.from(document.querySelectorAll('[data-lyrics]'));
  const soloPointer = document.getElementById('soloPointer');
  const soloLabels = Array.from(document.querySelectorAll('[data-solo]'));
  const spatializePointer = document.getElementById('spatializePointer');
  const spatializeLabels = Array.from(document.querySelectorAll('[data-spatialize]'));
  const backVocalsPointer = document.getElementById('backVocalsPointer');
  const backVocalsLabels = Array.from(document.querySelectorAll('[data-backvocals]'));
  const timeDisplay = document.getElementById('time-display');
  const volSlider = document.getElementById('volumeSlider');
  const visualizer = document.querySelector('.visualizer-container');
  const lyricsDisplay = document.getElementById('lyricsDisplay');
  const soloDisplay = document.getElementById('soloDisplay');
  const spatializeDisplay = document.getElementById('spatializeDisplay');
  const backVocalsDisplay = document.getElementById('backVocalsDisplay');

  // Mute button handling
  const muteButtons = document.querySelectorAll('.mute-btn');
  muteButtons.forEach(btn => {{
    btn.addEventListener('click', (e) => {{
      e.stopPropagation();
      const stem = btn.getAttribute('data-stem');
      if (mutedStems.has(stem)) {{
        mutedStems.delete(stem);
        btn.classList.remove('active');
        btn.closest('.control-section').classList.remove('muted');
      }} else {{
        mutedStems.add(stem);
        btn.classList.add('active');
        btn.closest('.control-section').classList.add('muted');
      }}
      updateVolumes();
    }});
  }});

  // Loop button
  loopBtn.addEventListener('click', () => {{
    isLooping = !isLooping;
    grooveWS.setOptions({{ 
      interact: true,
      hideScrollbar: false
    }});
    if (isLooping) {{
      loopBtn.classList.add('active');
    }} else {{
      loopBtn.classList.remove('active');
    }}
  }});

  // Export button
  exportBtn.addEventListener('click', () => {{
    const settings = {{
      lyrics: currentLyrics,
      solo: currentSolo,
      spatialize: spatializeOn ? 'wide' : 'narrow',
      backVocals: backVocalsOn ? 'on' : 'off',
      volumes: {{
        master: parseFloat(volSlider.value),
        lyrics: lyricsVolume,
        solo: soloVolume,
        spatialize: spatializeVolume,
        backVocals: backVocalsVolume,
        groove: grooveVolume
      }},
      mutedStems: Array.from(mutedStems)
    }};
    console.log('Export settings:', settings);
    alert('Mix settings saved! Ready for submission.\\n\\n' + JSON.stringify(settings, null, 2));
  }});

  function formatTime(sec) {{
    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60).toString().padStart(2, '0');
    return m + ':' + s;
  }}

  function updateTime() {{
    const cur = grooveWS.getCurrentTime();
    const total = grooveWS.getDuration();
    timeDisplay.textContent = formatTime(cur) + ' / ' + formatTime(total);
  }}

  function checkReady() {{
    readyCount++;
    console.log('Ready:', readyCount + '/11');
    loadingStatus.textContent = 'Loading... (' + readyCount + '/11)';
    
    if (readyCount === 11) {{
      allReady = true;
      console.log('✅ All stems ready!');
      loadingStatus.textContent = '✅ Ready to mix!';
      loadingStatus.style.color = '#4CAF50';
      
      playBtn.disabled = false;
      playBtn.style.opacity = '1';
      
      updateVolumes();
      
      console.log('✅ Ready to create your version!');
    }}
  }}

  function updateVolumes() {{
    const masterVol = parseFloat(volSlider.value);
    
    const grooveMuted = mutedStems.has('groove');
    grooveWS.setVolume(grooveMuted ? 0 : masterVol * grooveVolume);
    
    const lyricsMuted = mutedStems.has('lyrics');
    const lyricsVol = lyricsMuted ? 0 : masterVol * lyricsVolume;
    stems.lyricsA.setVolume(currentLyrics === 'A' ? lyricsVol : 0);
    stems.lyricsB.setVolume(currentLyrics === 'B' ? lyricsVol : 0);
    stems.lyricsC.setVolume(currentLyrics === 'C' ? lyricsVol : 0);
    
    const soloMuted = mutedStems.has('solo');
    const soloVol = soloMuted ? 0 : masterVol * soloVolume;
    stems.soloA.setVolume(currentSolo === 'A' ? soloVol : 0);
    stems.soloB.setVolume(currentSolo === 'B' ? soloVol : 0);
    
    const spatMuted = mutedStems.has('spatialize');
    const spatVol = spatMuted ? 0 : masterVol * spatializeVolume;
    stems.harmony_narrow.setVolume(!spatializeOn ? spatVol : 0);
    stems.harmony_wide.setVolume(spatializeOn ? spatVol : 0);
    
    const backMuted = mutedStems.has('backvocals');
    const backVol = backMuted ? 0 : masterVol * backVocalsVolume;
    stems.adlibA.setVolume(backVocalsOn && currentLyrics === 'A' ? backVol : 0);
    stems.adlibB.setVolume(backVocalsOn && currentLyrics === 'B' ? backVol : 0);
    stems.adlibC.setVolume(backVocalsOn && currentLyrics === 'C' ? backVol : 0);
  }}

  function playAll() {{
    if (!allReady) return;
    
    if (audioContext.state === 'suspended') {{
      audioContext.resume();
    }}
    
    isPlaying = true;
    const currentTime = grooveWS.getCurrentTime();
    grooveWS.play(currentTime);
    Object.values(stems).forEach(ws => ws.play(currentTime));
  }}

  function pauseAll() {{
    isPlaying = false;
    grooveWS.pause();
    Object.values(stems).forEach(ws => ws.pause());
  }}

  grooveWS.load(audioMap.groove);
  
  grooveWS.on('error', (err) => {{
    console.error('Groove load error:', err);
    loadingStatus.textContent = '❌ Error loading audio. Check console.';
    loadingStatus.style.color = '#f44336';
  }});
  
  grooveWS.on('ready', () => {{
    console.log('✓ Groove');
    updateTime();
    const grooveBackend = grooveWS.backend;
    if (grooveBackend && grooveBackend.gainNode) {{
      grooveBackend.gainNode.disconnect();
      grooveBackend.gainNode.connect(masterGain);
    }}
    checkReady();
  }});

  Object.keys(stems).forEach(key => {{
    stems[key].load(audioMap[key]);
    
    stems[key].on('error', (err) => {{
      console.error(key + ' load error:', err);
      loadingStatus.textContent = '❌ Error loading ' + key;
      loadingStatus.style.color = '#f44336';
    }});
    
    stems[key].on('ready', () => {{
      console.log('✓', key);
      const backend = stems[key].backend;
      if (backend && backend.gainNode) {{
        backend.gainNode.disconnect();
        backend.gainNode.connect(masterGain);
      }}
      checkReady();
    }});
  }});

  grooveWS.on('audioprocess', updateTime);
  grooveWS.on('finish', () => {{
    if (isLooping) {{
      grooveWS.seekTo(0);
      Object.values(stems).forEach(ws => ws.seekTo(0));
      playAll();
    }} else {{
      pauseAll();
      playBtn.textContent = '▶';
      playBtn.classList.remove('pause');
      visualizer.classList.add('paused');
    }}
  }});

  playBtn.addEventListener('click', () => {{
    if (isPlaying) {{
      pauseAll();
      playBtn.textContent = '▶';
      playBtn.classList.remove('pause');
      visualizer.classList.add('paused');
    }} else {{
      playAll();
      playBtn.textContent = '⏸';
      playBtn.classList.add('pause');
      visualizer.classList.remove('paused');
    }}
  }});

  function setLyricsActive(version) {{
    lyricsLabels.forEach(el => {{
      el.classList.toggle('active', el.getAttribute('data-lyrics') === version);
    }});
    lyricsPointer.style.transform = 'translate(-50%, 0) rotate(' + lyricsAngles[version] + 'deg)';
    lyricsDisplay.textContent = 'Lyrics ' + version;
  }}

  function switchLyrics(version) {{
    if (version === currentLyrics) return;
    currentLyrics = version;
    updateVolumes();
    setLyricsActive(version);
  }}

  document.getElementById('lyricsKnob').addEventListener('click', () => {{
    const next = {{"A": "B", "B": "C", "C": "A"}}[currentLyrics];
    switchLyrics(next);
  }});

  lyricsLabels.forEach(el => {{
    el.addEventListener('click', (e) => {{
      e.stopPropagation();
      switchLyrics(el.getAttribute('data-lyrics'));
    }});
  }});

  document.getElementById('soloKnob').addEventListener('click', () => {{
    const next = currentSolo === 'A' ? 'B' : 'A';
    switchSolo(next);
  }});

  soloLabels.forEach(el => {{
    el.addEventListener('click', (e) => {{
      e.stopPropagation();
      switchSolo(el.getAttribute('data-solo'));
    }});
  }});

  function switchSolo(version) {{
    if (version === currentSolo) return;
    currentSolo = version;
    updateVolumes();
    soloLabels.forEach(el => {{
      el.classList.toggle('active', el.getAttribute('data-solo') === version);
    }});
    const angle = version === 'A' ? 270 : 90;
    soloPointer.style.transform = 'translate(-50%, 0) rotate(' + angle + 'deg)';
    soloDisplay.textContent = 'Take ' + version;
  }}

  document.getElementById('spatializeKnob').addEventListener('click', () => {{
    toggleSpatialize();
  }});

  spatializeLabels.forEach(el => {{
    el.addEventListener('click', (e) => {{
      e.stopPropagation();
      const isWide = el.getAttribute('data-spatialize') === 'wide';
      if (isWide !== spatializeOn) {{
        toggleSpatialize();
      }}
    }});
  }});

  function toggleSpatialize() {{
    spatializeOn = !spatializeOn;
    updateVolumes();
    spatializeLabels.forEach(el => {{
      const isWide = el.getAttribute('data-spatialize') === 'wide';
      el.classList.toggle('active', isWide === spatializeOn);
    }});
    const angle = spatializeOn ? 90 : 270;
    spatializePointer.style.transform = 'translate(-50%, 0) rotate(' + angle + 'deg)';
    spatializeDisplay.textContent = spatializeOn ? 'Wide' : 'Narrow';
  }}

  document.getElementById('backVocalsKnob').addEventListener('click', () => {{
    toggleBackVocals();
  }});

  backVocalsLabels.forEach(el => {{
    el.addEventListener('click', (e) => {{
      e.stopPropagation();
      const isOn = el.getAttribute('data-backvocals') === 'on';
      if (isOn !== backVocalsOn) {{
        toggleBackVocals();
      }}
    }});
  }});

  function toggleBackVocals() {{
    backVocalsOn = !backVocalsOn;
    updateVolumes();
    backVocalsLabels.forEach(el => {{
      const isOn = el.getAttribute('data-backvocals') === 'on';
      el.classList.toggle('active', isOn === backVocalsOn);
    }});
    const angle = backVocalsOn ? 90 : 270;
    backVocalsPointer.style.transform = 'translate(-50%, 0) rotate(' + angle + 'deg)';
    backVocalsDisplay.textContent = backVocalsOn ? 'On' : 'Off';
  }}

  function updateSliderGradient(value) {{
    const percent = value * 100;
    volSlider.style.background = 'linear-gradient(to right, #5f6bff ' + percent + '%, #3a4150 ' + percent + '%)';
  }}

  volSlider.addEventListener('input', e => {{
    updateSliderGradient(e.target.value);
    updateVolumes();
  }});

  let isSeeking = false;
  let wasPlayingBeforeSeek = false;

  grooveWS.on('interaction', () => {{
    if (isPlaying && !isSeeking) {{
      console.log('Seeking started - pausing playback');
      isSeeking = true;
      wasPlayingBeforeSeek = true;
      grooveWS.pause();
      Object.values(stems).forEach(ws => ws.pause());
      isPlaying = false;
    }}
  }});

  grooveWS.on('seek', (progress) => {{
    const targetTime = progress * grooveWS.getDuration();
    console.log('Seek to:', targetTime);
    Object.values(stems).forEach(ws => {{
      ws.setTime(Math.min(targetTime, ws.getDuration() - 0.01));
    }});
    if (wasPlayingBeforeSeek) {{
      setTimeout(() => {{
        if (isSeeking) {{
          console.log('Seek ended - restarting playback');
          isSeeking = false;
          wasPlayingBeforeSeek = false;
          const exactTime = grooveWS.getCurrentTime();
          console.log('Restarting all at exact time:', exactTime);
          isPlaying = true;
          grooveWS.play(exactTime);
          Object.values(stems).forEach(ws => ws.play(exactTime));
        }}
      }}, 100);
    }}
  }});

  document.addEventListener('keydown', (e) => {{
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.tagName === 'SELECT') return;
    switch(e.key) {{
      case ' ':
        e.preventDefault();
        playBtn.click();
        break;
      case '1':
        e.preventDefault();
        switchLyrics('A');
        break;
      case '2':
        e.preventDefault();
        switchLyrics('B');
        break;
      case '3':
        e.preventDefault();
        switchLyrics('C');
        break;
      case 'ArrowLeft':
        e.preventDefault();
        grooveWS.skip(-5);
        Object.values(stems).forEach(ws => ws.skip(-5));
        break;
      case 'ArrowRight':
        e.preventDefault();
        grooveWS.skip(5);
        Object.values(stems).forEach(ws => ws.skip(5));
        break;
      case 'ArrowUp':
        e.preventDefault();
        const newVolUp = Math.min(1, parseFloat(volSlider.value) + 0.1);
        volSlider.value = newVolUp;
        updateSliderGradient(newVolUp);
        updateVolumes();
        break;
      case 'ArrowDown':
        e.preventDefault();
        const newVolDown = Math.max(0, parseFloat(volSlider.value) - 0.1);
        volSlider.value = newVolDown;
        updateSliderGradient(newVolDown);
        updateVolumes();
        break;
      case 'l':
      case 'L':
        e.preventDefault();
        loopBtn.click();
        break;
      case 'e':
      case 'E':
        e.preventDefault();
        exportBtn.click();
        break;
    }}
  }});

  document.getElementById('waveform').style.cursor = 'pointer';
  updateSliderGradient(1);

  // Individual volume knobs
  const lyricsVolumeSlider = document.getElementById('lyricsVolume');
  const lyricsVolumeDisplay = document.getElementById('lyricsVolumeDisplay');
  const soloVolumeSlider = document.getElementById('soloVolume');
  const soloVolumeDisplay = document.getElementById('soloVolumeDisplay');
  const spatializeVolumeSlider = document.getElementById('spatializeVolume');
  const spatializeVolumeDisplay = document.getElementById('spatializeVolumeDisplay');
  const backVocalsVolumeSlider = document.getElementById('backVocalsVolume');
  const backVocalsVolumeDisplay = document.getElementById('backVocalsVolumeDisplay');
  const grooveVolumeSlider = document.getElementById('grooveVolume');
  const grooveVolumeDisplay = document.getElementById('grooveVolumeDisplay');

  function updateVolumeKnobGradient(slider, value) {{
    const percent = value;
    slider.style.background = 'linear-gradient(to right, #5f6bff ' + percent + '%, #3a4150 ' + percent + '%)';
  }}

  lyricsVolumeSlider.addEventListener('input', e => {{
    const val = parseInt(e.target.value);
    lyricsVolume = val / 100;
    lyricsVolumeDisplay.textContent = val + '%';
    updateVolumeKnobGradient(lyricsVolumeSlider, val);
    updateVolumes();
  }});

  soloVolumeSlider.addEventListener('input', e => {{
    const val = parseInt(e.target.value);
    soloVolume = val / 100;
    soloVolumeDisplay.textContent = val + '%';
    updateVolumeKnobGradient(soloVolumeSlider, val);
    updateVolumes();
  }});

  spatializeVolumeSlider.addEventListener('input', e => {{
    const val = parseInt(e.target.value);
    spatializeVolume = val / 100;
    spatializeVolumeDisplay.textContent = val + '%';
    updateVolumeKnobGradient(spatializeVolumeSlider, val);
    updateVolumes();
  }});

  backVocalsVolumeSlider.addEventListener('input', e => {{
    const val = parseInt(e.target.value);
    backVocalsVolume = val / 100;
    backVocalsVolumeDisplay.textContent = val + '%';
    updateVolumeKnobGradient(backVocalsVolumeSlider, val);
    updateVolumes();
  }});

  grooveVolumeSlider.addEventListener('input', e => {{
    const val = parseInt(e.target.value);
    grooveVolume = val / 100;
    grooveVolumeDisplay.textContent = val + '%';
    updateVolumeKnobGradient(grooveVolumeSlider, val);
    updateVolumes();
  }});

  // Initialize volume knob gradients
  updateVolumeKnobGradient(lyricsVolumeSlider, 100);
  updateVolumeKnobGradient(soloVolumeSlider, 100);
  updateVolumeKnobGradient(spatializeVolumeSlider, 100);
  updateVolumeKnobGradient(backVocalsVolumeSlider, 100);
  updateVolumeKnobGradient(grooveVolumeSlider, 100);
</script>
"""

st.components.v1.html(html, height=1900)

# Below the player: Contributor features
st.markdown("<h2 style='margin-top:40px; text-align:center;'>Create Your Version</h2>", unsafe_allow_html=True)

# Upload section
with st.expander("**📤 UPLOAD YOUR OWN STEMS**", expanded=False):
    st.markdown("""
    <div style="background:rgba(95,107,255,0.05); border-left:4px solid #5f6bff; padding:15px; border-radius:8px; margin-bottom:20px;">
        <div style="color:#5f6bff; font-weight:600; margin-bottom:8px;">Guidelines for Contributors</div>
        <ul style="color:#8b92a8; font-size:13px; line-height:1.8;">
            <li><strong>Mute First:</strong> Click the 🔇 button on any stem to mute the original</li>
            <li><strong>Upload Your Version:</strong> Add your own recording below</li>
            <li><strong>Same Length Required:</strong> Your stem must match the song duration</li>
            <li><strong>Quality Standards:</strong> WAV/AIFF preferred, 24-bit, 48kHz minimum</li>
            <li><strong>Be Creative:</strong> Explore different interpretations</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🎤 Replace Vocals/Lyrics**")
        uploaded_vocals = st.file_uploader(
            "Upload your vocal track",
            type=["wav", "aiff", "mp3"],
            key="contributor_vocals"
        )
        if uploaded_vocals:
            st.session_state.my_uploads['vocals'] = uploaded_vocals
            st.success(f"✓ {uploaded_vocals.name} uploaded")
        
        st.markdown("**🎸 Replace Solo**")
        uploaded_solo = st.file_uploader(
            "Upload your solo",
            type=["wav", "aiff", "mp3"],
            key="contributor_solo"
        )
        if uploaded_solo:
            st.session_state.my_uploads['solo'] = uploaded_solo
            st.success(f"✓ {uploaded_solo.name} uploaded")
    
    with col2:
        st.markdown("**🥁 Replace Groove**")
        uploaded_groove = st.file_uploader(
            "Upload your groove/drums",
            type=["wav", "aiff", "mp3"],
            key="contributor_groove"
        )
        if uploaded_groove:
            st.session_state.my_uploads['groove'] = uploaded_groove
            st.success(f"✓ {uploaded_groove.name} uploaded")
        
        st.markdown("**🎹 Add Instrumental Layer**")
        uploaded_instrument = st.file_uploader(
            "Upload additional instrument",
            type=["wav", "aiff", "mp3"],
            key="contributor_instrument"
        )
        if uploaded_instrument:
            st.session_state.my_uploads['instrument'] = uploaded_instrument
            st.success(f"✓ {uploaded_instrument.name} uploaded")

# Submission section
st.markdown("<h3 style='margin-top:40px;'>📝 Submit Your Version</h3>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    version_name = st.text_input(
        "Version Name",
        placeholder="e.g., 'Dark Atmospheric Take' or 'Upbeat Remix'",
        key="version_name"
    )
    
    version_description = st.text_area(
        "Description (Optional)",
        placeholder="Describe what makes your version unique...",
        height=100,
        key="version_description"
    )

with col2:
    st.markdown("""
    <div style="background:rgba(255,255,255,0.03); padding:20px; border-radius:12px; height:100%;">
        <div style="color:#8b92a8; font-size:13px; margin-bottom:15px; font-weight:600;">YOUR ACTIVITY</div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:15px;">
            <div style="text-align:center;">
                <div style="font-size:28px; color:#8b92a8; font-weight:700;">{}</div>
                <div style="font-size:11px; color:#6b7280; margin-top:5px;">VERSIONS</div>
            </div>
            <div style="text-align:center;">
                <div style="font-size:28px; color:#8b92a8; font-weight:700;">{}</div>
                <div style="font-size:11px; color:#6b7280; margin-top:5px;">AVG RANK</div>
            </div>
        </div>
    </div>
    """.format(
        st.session_state.submission_count,
        st.session_state.my_ranking if st.session_state.my_ranking else "—"
    ), unsafe_allow_html=True)

# Action buttons
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("💾 Save Draft", use_container_width=True):
        st.success("Draft saved! You can continue working on it later.")

with col2:
    if st.button("👁️ Preview Mix", use_container_width=True):
        st.info("Preview your mix before submitting (plays current settings)")

with col3:
    if st.button("🔄 Reset All", use_container_width=True):
        st.session_state.my_uploads = {}
        st.session_state.muted_stems = set()
        st.rerun()

with col4:
    if st.button("🚀 Submit Version", use_container_width=True, type="primary"):
        if version_name and version_name.strip():
            st.session_state.submission_count += 1
            st.success(f"Version '{version_name}' submitted for peer review.")
        else:
            st.error("Please provide a version name before submitting.")

# Peer review section
st.markdown("<h3 style='margin-top:50px;'>Peer Review - Rate Other Versions</h3>", unsafe_allow_html=True)

st.markdown("""
<div style="background:rgba(95,107,255,0.05); border-left:4px solid #5f6bff; padding:15px; border-radius:8px; margin-bottom:20px;">
    <div style="color:#5f6bff; font-weight:600; margin-bottom:8px;">How Peer Review Works</div>
    <p style="color:#8b92a8; font-size:13px; line-height:1.6; margin:0;">
        Listen to other contributors' versions and provide ratings. This helps identify which combinations 
        of musical elements resonate most with listeners and contributes to the research data.
    </p>
</div>
""", unsafe_allow_html=True)

# Mock peer review items
peer_versions = [
    {"name": "Ethereal Dream Mix", "contributor": "@contributor_06", "ratings": 23},
    {"name": "Aggressive Rock Take", "contributor": "@contributor_07", "ratings": 18},
    {"name": "Lo-fi Bedroom Version", "contributor": "@contributor_08", "ratings": 15},
]

for i, version in enumerate(peer_versions):
    col1, col2, col3 = st.columns([3, 2, 1])
    
    with col1:
        st.markdown(f"""
        <div style="color:#ffffff; font-weight:600; font-size:15px;">{version['name']}</div>
        <div style="color:#8b92a8; font-size:12px; margin-top:3px;">by {version['contributor']}</div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="text-align:center; padding:10px; background:rgba(255,255,255,0.03); border-radius:8px;">
            <div style="color:#8b92a8; font-weight:500;">{version['ratings']} ratings</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.button("Rate", key=f"vote_{i}", use_container_width=True):
            st.success(f"Rating recorded for {version['name']}")
    
    st.markdown("<hr style='border:0; border-top:1px solid rgba(255,255,255,0.05); margin:15px 0;'>", unsafe_allow_html=True)

# Leaderboard preview
st.markdown("<h3 style='margin-top:40px;'>Current Rankings (Top 5)</h3>", unsafe_allow_html=True)

leaderboard = [
    {"rank": 1, "name": "Neo-Soul Reimagining", "contributor": "@contributor_09", "ratings": 89},
    {"rank": 2, "name": "Stripped Down Acoustic", "contributor": "@contributor_10", "ratings": 76},
    {"rank": 3, "name": "Electronic Fusion", "contributor": "@contributor_11", "ratings": 64},
    {"rank": 4, "name": "Jazz-Hop Blend", "contributor": "@contributor_12", "ratings": 52},
    {"rank": 5, "name": "Punk Energy Version", "contributor": "@contributor_13", "ratings": 48},
]

for entry in leaderboard:
    st.markdown(f"""
    <div style="display:flex; align-items:center; justify-content:space-between; padding:15px; background:rgba(255,255,255,0.03); border-radius:10px; margin:10px 0;">
        <div style="display:flex; align-items:center; gap:15px;">
            <div style="font-size:22px; color:#8b92a8; font-weight:700; min-width:35px;">#{entry['rank']}</div>
            <div>
                <div style="color:#ffffff; font-weight:600; font-size:15px;">{entry['name']}</div>
                <div style="color:#8b92a8; font-size:12px; margin-top:3px;">by {entry['contributor']}</div>
            </div>
        </div>
        <div style="color:#8b92a8; font-weight:500; font-size:16px;">{entry['ratings']} ratings</div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align:center; margin-top:60px; padding:30px; background:rgba(255,255,255,0.02); border-radius:12px;">
  <div style="color:#ffffff; font-weight:600; margin-bottom:15px; font-size:13px;">
    About This Interface
  </div>
  <p style="color:#8b92a8; font-size:12px; line-height:1.7; margin-bottom:12px;">
    This interface allows contributors to explore different combinations of musical elements 
    and create alternative versions of the song. Each submission contributes to research 
    investigating listener preferences across musical variations.
  </p>
  <p style="color:#8b92a8; font-size:12px; line-height:1.7;">
    Contributors have full creative control over stem selection, mixing, and can upload 
    their own recordings to replace any element. Peer ratings help identify which combinations 
    resonate most strongly with listeners.
  </p>
  <p style="font-size:10px; color:#6b7280; margin-top:15px;">
    Platform designed by Peyman Salimi • CCML Lab • Georgia Institute of Technology
  </p>
</div>
""", unsafe_allow_html=True)

'''