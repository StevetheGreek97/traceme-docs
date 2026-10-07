import streamlit as st

from utils.utils import footer, page_setup

page_setup("Keyboard Shortcuts", "⌨️")
st.header("⌨️ Keyboard Shortcuts")
st.caption("On macOS, Ctrl is ⌘ (Cmd).")


def table(rows):
    st.markdown("| Key | Action |\n|---|---|\n" + "\n".join(f"| {k} | {a} |" for k, a in rows))


c1, c2 = st.columns(2)
with c1:
    st.markdown("### Navigation")
    table([
        ("→ / ←", "Next / previous frame"),
        ("Home / End", "First / last frame"),
        ("Mouse wheel", "Zoom in / out"),
        ("+ / −", "Zoom in / out"),
        ("Middle-mouse drag", "Pan a zoomed frame"),
        ("F", "Fit the frame to the window"),
    ])
    st.markdown("### Annotating (main window)")
    table([
        ("Left-click", "Positive point"),
        ("Right-click", "Negative point"),
        ("Ctrl + click a point", "Remove it"),
        ("Shift + drag", "Draw a box"),
        ("E", "Run SAM2 on the selected object"),
        ("D", "Clear the selected object's outline"),
        ("Del (in Objects)", "Delete the selected object"),
    ])
with c2:
    st.markdown("### Tracking window")
    table([
        ("→ / ← / Home / End / F", "Same as the main window"),
        ("M", "Show / hide tracked masks"),
        ("P", "Show / hide the annotations used"),
        ("E", "Apply SAM to fix the frame (Edit Masks on)"),
        ("Esc", "Clear the fix's clicks"),
    ])
    st.markdown("### Menus")
    table([
        ("Ctrl + N", "New project"),
        ("Ctrl + O", "Open project"),
        ("Ctrl + S", "Save project"),
        ("Ctrl + I", "Import videos"),
        ("Ctrl + R", "Run tracking"),
        ("Ctrl + T", "Tracking results"),
        ("F1", "Help"),
        ("Ctrl + Q", "Quit (Linux, macOS; Alt + F4 on Windows)"),
    ])

footer()
