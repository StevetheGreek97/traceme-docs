import streamlit as st

from utils.utils import footer, page_setup, screenshot

page_setup("Interface Tour", "🧭")

st.markdown("""
<style>
    .hero {
        padding: 1.8rem 2rem;
        border-radius: 18px;
        border: 1px solid rgba(128, 128, 128, 0.2);
        background: linear-gradient(135deg,
            rgba(59, 130, 246, 0.16) 0%,
            rgba(16, 185, 129, 0.12) 55%,
            rgba(245, 158, 11, 0.10) 100%);
        margin-bottom: 1.4rem;
    }
    .hero h1 { margin: 0 0 0.4rem 0; font-size: 2.2rem; }
    .hero p { margin: 0; font-size: 1.05rem; opacity: 0.9; max-width: 54rem; }

    .area-card {
        height: 100%;
        padding: 1.2rem 1.3rem;
        border-radius: 16px;
        border: 1px solid rgba(128, 128, 128, 0.22);
        border-left: 5px solid var(--accent);
        background-color: rgba(255, 255, 255, 0.03);
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.12);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .area-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 26px rgba(0, 0, 0, 0.22);
    }
    .area-head { display: flex; align-items: center; gap: 0.7rem; margin-bottom: 0.5rem; }
    .area-badge {
        width: 2.1rem; height: 2.1rem; border-radius: 50%;
        background: var(--accent); color: #fff;
        display: inline-flex; align-items: center; justify-content: center;
        font-weight: 700; font-size: 0.95rem; flex-shrink: 0;
    }
    .area-head h4 { margin: 0; font-size: 1.15rem; }
    .area-card p { margin: 0; font-size: 0.95rem; opacity: 0.9; }

    .st-key-shot img {
        border-radius: 16px;
        box-shadow: 0 12px 34px rgba(0, 0, 0, 0.25);
        border: 1px solid rgba(128, 128, 128, 0.2);
    }

    .key-card {
        display: flex; align-items: center; gap: 0.9rem;
        padding: 0.8rem 1rem;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.2);
        background-color: rgba(255, 255, 255, 0.03);
        margin-bottom: 0.6rem;
    }
    .key-chip {
        min-width: 6.2rem; text-align: center;
        padding: 0.3rem 0.6rem;
        border-radius: 7px;
        border: 1px solid rgba(128, 128, 128, 0.5);
        border-bottom-width: 3px;
        background-color: rgba(128, 128, 128, 0.12);
        font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        font-size: 0.92rem;
        white-space: nowrap;
    }
    .key-desc { font-size: 0.95rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🧭 Interface</h1>
    <p>The TraceME window has four areas. The canvas on the right is where most of the work happens, and the
    other three support it.</p>
</div>
""", unsafe_allow_html=True)

areas = [
    ("1", "📋", "Menu bar", "#ef4444", "Projects, video import, model settings, and tracking."),
    ("2", "🧰", "Sidebar", "#ef4444", "The project's videos and the objects you track."),
    ("3", "🎞️", "Frames list", "#ef4444", "Every frame of the open video. A tick marks the annotated ones."),
    ("4", "🖼️", "Canvas", "#ef4444", "The current frame and its annotations. Annotating happens here."),
]
cols = st.columns(4)
for col, (num, icon, title, accent, summary) in zip(cols, areas):
    with col:
        st.markdown(
            f"""
            <div class="area-card" style="--accent: {accent};">
                <div class="area-head">
                    <span class="area-badge">{num}</span>
                    <h4>{icon} {title}</h4>
                </div>
                <p>{summary}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.write("")
with st.container(key="shot"):
    st.image("assets/screens/interface.png", caption="The TraceME window", width="stretch")

st.subheader("Keys and mouse on the canvas")
keys = [
    ("← / →", "Previous and next frame"),
    ("Home / End", "First and last frame"),
    ("Scroll", "Zoom in and out"),
    ("Middle-drag", "Pan a zoomed frame"),
    ("F", "Fit the frame to the window"),
    ("Left-click", "Positive point: this is the object"),
    ("Right-click", "Negative point: this is not part of it"),
    ("Shift-drag", "Draw a box around the object"),
    ("E", "Run SAM2 on the selected object"),
    ("D", "Clear the selected object's outline"),
]
left, right = st.columns(2)
for i, (chord, desc) in enumerate(keys):
    chips = "".join(f'<span class="key-chip">{part.strip()}</span>' for part in chord.split("/"))
    target = left if i % 2 == 0 else right
    with target:
        st.markdown(
            f'<div class="key-card">{chips}<span class="key-desc">{desc}</span></div>',
            unsafe_allow_html=True,
        )

st.page_link("pages/6_Keyboard_Shortcuts.py", label="All keyboard shortcuts", icon="⌨️")

st.subheader("Each area in detail")
tab_menu, tab_sidebar, tab_frames, tab_canvas = st.tabs(
    ["📋 1 · Menu bar", "🧰 2 · Sidebar", "🎞️ 3 · Frames list", "🖼️ 4 · Canvas"]
)

with tab_menu:
    st.markdown("""
- **File** — **New Project** (Ctrl+N), **Open Project** (Ctrl+O), **Open Recent**, and **Save Project**;
  **Import Videos** and **Import Frames Folder**; **Export YAMLs**; **Quit**.
- **Settings** — **Models…**: download SAM models, and choose the one in use and the device it runs on.
- **Tracking** — **Run Tracking…** (Ctrl+R), **Tracking Results…** (Ctrl+T), and **Open Results Folder**.
- **Help** — **How to Use TraceME**, **Show Log Folder**, and **About**.
""")
    st.page_link("pages/3_Projects_and_Videos.py", label="Projects and Videos", icon="📁")

with tab_sidebar:
    st.markdown("""
- **Project** — the project's name, and the **Videos** in it. Click a video to open it.
- **Objects** — the things you track (an animal, a cell, a body part), each with its own name and colour, shared by
  every video in the project. **+** adds one. **Double-click** an object to rename it; **right-click** for Rename,
  Recolor, and Delete.
- The **selected** object is the one you're annotating.
""")
    st.page_link("pages/3_Projects_and_Videos.py", label="Annotating (in Projects and Videos)", icon="✨")

with tab_frames:
    st.markdown("""
Every frame of the open video, in order.

- **Click** a frame to jump to it.
- A **tick** marks the frames you've annotated.
- **Show** filters the list to *All frames* or *Annotated* only, which is a quick way to review your annotations.
""")

with tab_canvas:
    st.markdown("""
The canvas shows the current frame with your annotations: positive points (green), negative points (red), boxes, and
the SAM2 outlines, each in its object's colour and labelled with its name.

- **Scroll** to zoom. **Middle-drag** to pan. **F** fits the frame to the window. Your zoom is kept while you step
  through frames.
- **Left-click** adds a positive point and **right-click** a negative one, for the selected object. **Ctrl+click** a
  point to remove it.
- Hold **Shift** and drag to draw a box.
- **Press `E`** to run SAM2 on the selected object. **Press `D`** to clear its outline.

Below the canvas, drag the **frame slider** (or use ← →, Home, End) to move through the video. The **status bar** at
the bottom of the window shows what TraceME is doing: video import progress, which device a model runs on, and
messages after each action.
""")
    st.page_link("pages/3_Projects_and_Videos.py", label="Annotating (in Projects and Videos)", icon="✨")

st.subheader("Welcome screen")
st.markdown(
    "With no project open, TraceME shows how it works in four steps. Projects are created and opened "
    "from the **File** menu; double-clicking a `.tme` project file also opens it."
)
screenshot("welcome")
st.caption(
    "TraceME follows your system's light or dark setting, and switches along when you change it, on "
    "Windows, macOS and Linux alike."
)

footer()
