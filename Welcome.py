import streamlit as st

from utils.utils import footer, get_text, page_setup, screenshot

page_setup("Welcome", "assets/logo.png")

col1, col2 = st.columns([1, 14])
with col1:
    st.image("assets/logo.png", width=72)
with col2:
    st.markdown("## TraceME Manual")
    st.caption("Annotate video frames with SAM2 and track objects through whole videos.")

st.markdown(get_text("intro"))
st.page_link("pages/1_Install_and_Setup.py", label="Download TraceME", icon="⬇️")

st.divider()
st.markdown("### How it works")
cols = st.columns(4)
for i, (col, step) in enumerate(zip(cols, get_text("workflow", []))):
    with col:
        with st.container(border=True):
            st.markdown(f"#### {step['icon']}")
            st.caption(f"STEP {i + 1}")
            st.markdown(f"**{step['title']}**")
            st.markdown(step["text"])

st.markdown("### Jump straight in")
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.page_link("pages/1_Install_and_Setup.py", label="Install & Setup", icon="⚙️")
with c2:
    st.page_link("pages/2_Interface_Tour.py", label="Interface Tour", icon="🧭")
with c3:
    st.page_link("pages/3_Projects_and_Videos.py", label="Annotating & Tracking", icon="📈")
with c4:
    st.page_link("pages/6_Keyboard_Shortcuts.py", label="Keyboard Shortcuts", icon="⌨️")

st.divider()
screenshot("main_window", "Annotating two objects in the main window")

footer()
st.caption("This manual is a work in progress. Feedback and suggestions are welcome!")
