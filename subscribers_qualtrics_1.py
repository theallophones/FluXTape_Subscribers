import streamlit as st
import json

st.set_page_config(layout="wide", page_title="FluXTape Study", page_icon="🎵")

# Google Sheets webhook URL
GOOGLE_SHEET_WEBHOOK = "https://script.google.com/macros/s/YOUR_WEBHOOK_HERE/exec"

# Qualtrics return URL (they'll add their survey ID)
QUALTRICS_SURVEY_URL = "https://gatech.co1.qualtrics.com/jfe/form/SV_XXXXX"

# Get URL parameters
pid = st.query_params.get("pid", "test_user")
participant_id = pid[0] if isinstance(pid, list) else pid
sid = st.query_params.get("song", "song1")
song_id = sid[0] if isinstance(sid, list) else sid

# Song metadata
song_info = {
    "song1": {"name": "Song Title 1", "number": 1, "emotion": "happy"},
    "song2": {"name": "Song Title 2", "number": 2, "emotion": "sad"},
    "song3": {"name": "Song Title 3", "number": 3, "emotion": "happy"},
    "song4": {"name": "Song Title 4", "number": 4, "emotion": "sad"}
}

current_song = song_info.get(song_id, {"name": "Unknown", "number": 0})

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

audio_map = {
    # ... your audio URLs ...
}

audio_map_json = json.dumps(audio_map)

html = f"""
<script>
  // Initialize session data using localStorage
  if (!localStorage.getItem('session_started')) {{
    localStorage.setItem('session_started', new Date().toISOString());
    localStorage.setItem('participant_id', '{participant_id}');
    localStorage.setItem('song_id', '{song_id}');
    localStorage.setItem('interaction_log', JSON.stringify([]));
  }}
  
  window.logInteraction = function(control, fromValue, toValue) {{
    const log = JSON.parse(localStorage.getItem('interaction_log') || '[]');
    log.push({{
      timestamp: new Date().toISOString(),
      control: control,
      from: fromValue,
      to: toValue
    }});
    localStorage.setItem('interaction_log', JSON.stringify(log));
  }};
  
  window.saveFinalState = function(lyrics, groove, solo, spatialize, backing) {{
    localStorage.setItem('final_lyrics', lyrics);
    localStorage.setItem('final_groove', groove);
    localStorage.setItem('final_solo', solo);
    localStorage.setItem('final_spatialize', spatialize);
    localStorage.setItem('final_backing', backing);
  }};
</script>

<!-- SONG NUMBER DISPLAY - PROMINENT -->
<div style="text-align:center; background:rgba(44,90,160,0.15); border:2px solid #2c5aa0; padding:20px; border-radius:12px; margin-bottom:30px;">
  <div style="color:#2c5aa0; font-size:16px; font-weight:700; letter-spacing:2px; margin-bottom:8px;">
    SONG {current_song['number']} OF 4
  </div>
  <div style="color:#8b92a8; font-size:20px; font-weight:600;">
    {current_song['name']}
  </div>
</div>

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

<!-- ... rest of your waveform, controls, etc ... -->

<!-- SUBMIT SECTION -->
<div style="text-align:center; margin:60px 0 40px 0;">
  <hr style="border:0; border-top:1px solid rgba(255,255,255,0.1); margin:40px auto; max-width:600px;">
  <h3 style="color:#ffffff; margin-bottom:10px;">Ready to submit?</h3>
  <p style="color:#8b92a8; margin-bottom:30px;">Your preferences will be saved and you'll return to the survey</p>
  <button id="submitBtn" style="
    background:#2c5aa0; 
    color:white; 
    border:none; 
    padding:16px 48px; 
    border-radius:12px; 
    font-size:18px; 
    font-weight:700; 
    cursor:pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(44,90,160,0.4);
  ">
    ✓ Submit My Version
  </button>
  <div id="submitStatus" style="margin-top:20px; color:#8b92a8; font-size:14px;"></div>
</div>

<style>
  /* ... all your existing styles ... */
</style>

<script src="https://unpkg.com/wavesurfer.js@7/dist/wavesurfer.min.js"></script>

<script>
  // ... all your existing audio code ...
  
  // SUBMIT BUTTON HANDLER
  document.getElementById('submitBtn').addEventListener('click', function() {{
    const btn = this;
    const status = document.getElementById('submitStatus');
    
    btn.disabled = true;
    btn.style.opacity = '0.5';
    btn.style.cursor = 'not-allowed';
    status.textContent = '💾 Saving your data...';
    status.style.color = '#8b92a8';
    
    const data = {{
      participant_id: localStorage.getItem('participant_id'),
      song_id: localStorage.getItem('song_id'),
      timestamp: new Date().toISOString(),
      interaction_log: localStorage.getItem('interaction_log'),
      final_lyrics: localStorage.getItem('final_lyrics'),
      final_groove: localStorage.getItem('final_groove'),
      final_solo: localStorage.getItem('final_solo'),
      final_spatialize: localStorage.getItem('final_spatialize'),
      final_backing: localStorage.getItem('final_backing')
    }};
    
    fetch('{GOOGLE_SHEET_WEBHOOK}', {{
      method: 'POST',
      headers: {{ 'Content-Type': 'text/plain;charset=utf-8' }},
      body: JSON.stringify(data)
    }})
    .then(response => {{
      status.innerHTML = '<div style="color:#4CAF50; font-weight:600; font-size:18px; margin-bottom:15px;">✓ Submission successful!</div>' +
                        '<div style="color:#ffffff; font-size:16px; margin-bottom:10px;">Returning to survey in 3 seconds...</div>' +
                        '<div style="color:#8b92a8; font-size:13px;">Please go back to your Qualtrics tab to continue</div>';
      
      // Auto-redirect after 3 seconds
      setTimeout(() => {{
        const returnUrl = '{QUALTRICS_SURVEY_URL}?pid=' + data.participant_id + '&completed=' + data.song_id;
        window.location.href = returnUrl;
      }}, 3000);
    }})
    .catch(err => {{
      console.error('Error:', err);
      status.innerHTML = '<span style="color:#f44336;">⚠ Error saving. Please try again.</span>';
      btn.disabled = false;
      btn.style.opacity = '1';
      btn.style.cursor = 'pointer';
    }});
  }});
</script>
"""

st.components.v1.html(html, height=2100, scrolling=True)