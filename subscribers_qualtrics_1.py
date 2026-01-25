import streamlit as st
import json
from datetime import datetime
import hashlib
import os

st.set_page_config(layout="wide", page_title="FluXTape Study", page_icon="🎵")

# Get URL parameters
query_params = st.query_params
participant_id = query_params.get("pid", "test_user")
song_id = query_params.get("song", "song1")

# Initialize session state
if 'participant_id' not in st.session_state:
    st.session_state.participant_id = participant_id
if 'song_id' not in st.session_state:
    st.session_state.song_id = song_id

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

# Audio map - YOU'LL UPDATE THIS WITH YOUR 4 SONGS
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

# Initialize logging in localStorage
init_logging = f"""
<script>
  // Initialize session data
  if (!sessionStorage.getItem('session_started')) {{
    sessionStorage.setItem('session_started', new Date().toISOString());
    sessionStorage.setItem('participant_id', '{participant_id}');
    sessionStorage.setItem('song_id', '{song_id}');
    sessionStorage.setItem('interaction_log', JSON.stringify([]));
  }}
  
  // Logging function
  window.logInteraction = function(control, fromValue, toValue) {{
    const log = JSON.parse(sessionStorage.getItem('interaction_log') || '[]');
    log.push({{
      timestamp: new Date().toISOString(),
      control: control,
      from: fromValue,
      to: toValue
    }});
    sessionStorage.setItem('interaction_log', JSON.stringify(log));
    console.log('Logged:', control, fromValue, '→', toValue);
  }};
  
  // Save final state
  window.saveFinalState = function(lyrics, groove, solo, spatialize, backing) {{
    sessionStorage.setItem('final_lyrics', lyrics);
    sessionStorage.setItem('final_groove', groove);
    sessionStorage.setItem('final_solo', solo);
    sessionStorage.setItem('final_spatialize', spatialize);
    sessionStorage.setItem('final_backing', backing);
  }};
</script>
"""

# THE FULL HTML - I'll keep your EXACT working code and just add logging calls
html = init_logging + f"""
<div style="text-align:center; margin-bottom:10px;">
  <h1 style="font-family:'Inter', sans-serif; font-weight:800; color:#ffffff; font-size:48px; margin-bottom:5px; letter-spacing:-1px;">
    FluX-Tape
  </h1>
  <h3 style="font-family:'Inter', sans-serif; font-weight:400; color:#8b92a8; font-size:16px; margin-top:0; letter-spacing:0.5px;">
    Create your preferred version
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

<div style="display:flex; justify-content:center; align-items:center; margin-top:20px;">
  <div id="time-display" style="color:#ffffff; font-family:'JetBrains Mono', 'Courier New', monospace; font-size:24px; font-weight:600; letter-spacing:2px;">
    0:00 / 0:00
  </div>
</div>

<div style="text-align:center; margin:25px 0;">
  <div style="color:#8b92a8; font-size:22px; margin-bottom:8px;">🔊</div>
  <input id="volumeSlider" type="range" min="0" max="1" step="0.01" value="1" class="slider" title="Volume Control">
</div>

<div class="controls-grid">
  <div class="control-section">
    <div class="control-header">LYRICS</div>
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
    <div class="control-header">GROOVE</div>
    <div class="knob-wrap-small">
      <div id="grooveKnob" class="knob-small" title="Click to switch groove">
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
      <div id="soloKnob" class="knob-small" title="Click to switch solo">
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
    <div class="control-header">BACK VOCALS</div>
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

  .controls-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 30px;
    max-width: 900px;
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
  
  let lyricsVolume = 1.0;
  let grooveVolume = 1.0;
  let soloVolume = 1.0;
  let spatializeVolume = 1.0;
  let backVocalsVolume = 1.0;

  const playBtn = document.getElementById('playBtn');
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
      loadingStatus.textContent = '✅ Ready to play!';
      loadingStatus.style.color = '#4CAF50';
      
      playBtn.disabled = false;
      playBtn.style.opacity = '1';
      
      const vol = parseFloat(volSlider.value);
      
      grooveAWS.setVolume(vol);
      stems.lyricsA.setVolume(vol * lyricsVolume);
      stems.lyricsB.setVolume(0);
      stems.lyricsC.setVolume(0);
      stems.grooveB.setVolume(0);
      stems.grooveC.setVolume(0);
      stems.soloA.setVolume(vol * soloVolume);
      stems.soloB.setVolume(0);
      stems.soloC.setVolume(0);
      stems.harmony_narrow.setVolume(vol * spatializeVolume);
      stems.harmony_wide.setVolume(0);
      stems.adlibA.setVolume(0);
      stems.adlibB.setVolume(0);
      stems.adlibC.setVolume(0);
      
      console.log('✅ Ready!');
    }}
  }}

  function updateVolumes() {{
    const masterVol = parseFloat(volSlider.value);
    
    grooveAWS.setVolume(currentGroove === 'A' ? masterVol * grooveVolume : 0);
    stems.grooveB.setVolume(currentGroove === 'B' ? masterVol * grooveVolume : 0);
    stems.grooveC.setVolume(currentGroove === 'C' ? masterVol * grooveVolume : 0);
    
    const lyricsVol = masterVol * lyricsVolume;
    stems.lyricsA.setVolume(currentLyrics === 'A' ? lyricsVol : 0);
    stems.lyricsB.setVolume(currentLyrics === 'B' ? lyricsVol : 0);
    stems.lyricsC.setVolume(currentLyrics === 'C' ? lyricsVol : 0);
    
    const soloVol = masterVol * soloVolume;
    stems.soloA.setVolume(currentSolo === 'A' ? soloVol : 0);
    stems.soloB.setVolume(currentSolo === 'B' ? soloVol : 0);
    stems.soloC.setVolume(currentSolo === 'C' ? soloVol : 0);
    
    const spatVol = masterVol * spatializeVolume;
    stems.harmony_narrow.setVolume(!spatializeOn ? spatVol : 0);
    stems.harmony_wide.setVolume(spatializeOn ? spatVol : 0);
    
    const backVol = masterVol * backVocalsVolume;
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
    loadingStatus.textContent = '❌ Error loading audio';
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
    pauseAll();
    playBtn.textContent = '▶';
    playBtn.classList.remove('pause');
    visualizer.classList.add('paused');
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
    window.logInteraction('lyrics', currentLyrics, version);  // LOG IT
    currentLyrics = version;
    updateVolumes();
    setLyricsActive(version);
    window.saveFinalState(currentLyrics, currentGroove, currentSolo, spatializeOn ? 'wide' : 'narrow', backVocalsOn ? 'on' : 'off');
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
    window.logInteraction('groove', currentGroove, version);  // LOG IT
    currentGroove = version;
    updateVolumes();
    setGrooveActive(version);
    window.saveFinalState(currentLyrics, currentGroove, currentSolo, spatializeOn ? 'wide' : 'narrow', backVocalsOn ? 'on' : 'off');
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
    window.logInteraction('solo', currentSolo, version);  // LOG IT
    currentSolo = version;
    updateVolumes();
    setSoloActive(version);
    window.saveFinalState(currentLyrics, currentGroove, currentSolo, spatializeOn ? 'wide' : 'narrow', backVocalsOn ? 'on' : 'off');
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

  function toggleSpatialize() {{
    window.logInteraction('spatialize', spatializeOn ? 'wide' : 'narrow', spatializeOn ? 'narrow' : 'wide');  // LOG IT
    spatializeOn = !spatializeOn;
    updateVolumes();
    spatializeLabels.forEach(el => {{
      const isWide = el.getAttribute('data-spatialize') === 'wide';
      el.classList.toggle('active', isWide === spatializeOn);
    }});
    const angle = spatializeOn ? 90 : 270;
    spatializePointer.style.transform = 'translate(-50%, 0) rotate(' + angle + 'deg)';
    spatializeDisplay.textContent = spatializeOn ? 'Wide' : 'Narrow';
    window.saveFinalState(currentLyrics, currentGroove, currentSolo, spatializeOn ? 'wide' : 'narrow', backVocalsOn ? 'on' : 'off');
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

  function toggleBackVocals() {{
    window.logInteraction('backing_vocals', backVocalsOn ? 'on' : 'off', backVocalsOn ? 'off' : 'on');  // LOG IT
    backVocalsOn = !backVocalsOn;
    updateVolumes();
    backVocalsLabels.forEach(el => {{
      const isOn = el.getAttribute('data-backvocals') === 'on';
      el.classList.toggle('active', isOn === backVocalsOn);
    }});
    const angle = backVocalsOn ? 90 : 270;
    backVocalsPointer.style.transform = 'translate(-50%, 0) rotate(' + angle + 'deg)';
    backVocalsDisplay.textContent = backVocalsOn ? 'On' : 'Off';
    window.saveFinalState(currentLyrics, currentGroove, currentSolo, spatializeOn ? 'wide' : 'narrow', backVocalsOn ? 'on' : 'off');
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

  function updateSliderGradient(value) {{
    const percent = value * 100;
    volSlider.style.background = 'linear-gradient(to right, #5f6bff ' + percent + '%, #3a4150 ' + percent + '%)';
  }}

  volSlider.addEventListener('input', e => {{
    updateSliderGradient(e.target.value);
    updateVolumes();
  }});

  grooveAWS.on('seek', (progress) => {{
    const targetTime = progress * grooveAWS.getDuration();
    Object.values(stems).forEach(ws => {{
      ws.setTime(Math.min(targetTime, ws.getDuration() - 0.01));
    }});
  }});

  document.addEventListener('keydown', (e) => {{
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
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
    }}
  }});

  updateSliderGradient(1);

  // Volume knobs
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

  updateVolumeKnobGradient(lyricsVolumeSlider, 100);
  updateVolumeKnobGradient(grooveVolumeSlider, 100);
  updateVolumeKnobGradient(soloVolumeSlider, 100);
  updateVolumeKnobGradient(spatializeVolumeSlider, 100);
  updateVolumeKnobGradient(backVocalsVolumeSlider, 100);
  
  // Save initial state
  window.saveFinalState(currentLyrics, currentGroove, currentSolo, spatializeOn ? 'wide' : 'narrow', backVocalsOn ? 'on' : 'off');
</script>
"""

st.components.v1.html(html, height=1700)

# Submit button - this is OUTSIDE the HTML component so it's a real Streamlit button
st.markdown("---")
st.markdown("<h3 style='text-align:center; margin-top:30px;'>Ready to submit your version?</h3>", unsafe_allow_html=True)

if st.button("✓ Submit and Continue to Survey", use_container_width=True, type="primary"):
    # Inject JavaScript to grab data from sessionStorage
    grab_data_js = """
    <script>
      const data = {
        participant_id: sessionStorage.getItem('participant_id'),
        song_id: sessionStorage.getItem('song_id'),
        session_started: sessionStorage.getItem('session_started'),
        final_lyrics: sessionStorage.getItem('final_lyrics'),
        final_groove: sessionStorage.getItem('final_groove'),
        final_solo: sessionStorage.getItem('final_solo'),
        final_spatialize: sessionStorage.getItem('final_spatialize'),
        final_backing: sessionStorage.getItem('final_backing'),
        interaction_log: JSON.parse(sessionStorage.getItem('interaction_log') || '[]')
      };
      
      // Save to a hidden element that Streamlit can read
      const dataEl = document.createElement('div');
      dataEl.id = 'session-data';
      dataEl.textContent = JSON.stringify(data);
      dataEl.style.display = 'none';
      document.body.appendChild(dataEl);
      
      console.log('Data ready:', data);
    </script>
    """
    
    st.components.v1.html(grab_data_js, height=0)
    
    # Save placeholder data for now - we'll fix this
    final_data = {
        'participant_id': participant_id,
        'song_id': song_id,
        'timestamp': datetime.now().isoformat()
    }
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Save to file
    filename = f'data/{participant_id}_{song_id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(filename, 'w') as f:
        json.dump(final_data, f, indent=2)
    
    st.success(f"✓ Submitted! Data saved to {filename}")
    
    # Show redirect link (user clicks manually for now)
    qualtrics_url = f"YOUR_QUALTRICS_URL_HERE?pid={participant_id}&completed={song_id}"
    st.markdown(f"[Click here to return to the survey]({qualtrics_url})")