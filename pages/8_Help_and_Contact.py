from datetime import datetime

import gspread
import streamlit as st
from google.oauth2.service_account import Credentials

from utils.utils import APP_REPO, ISSUES_URL, LAB_URL, get_text, is_valid_email, page_setup

# --- Auth with Google Sheets ---
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
creds = Credentials.from_service_account_info(st.secrets["google"], scopes=scope)
client = gspread.authorize(creds)
# Shared with SegmentME-docs; the last column tells the two apart.
sheet = client.open("SegmentME Downloads").worksheet("Contact")


def log_contact(name, email, message):
    timestamp = datetime.now().isoformat()
    sheet.append_row([timestamp, name, email, message, "TraceME"])


# --- Page Setup ---
page_setup("Contact", "📩")
st.title("📩 Contact Me")
st.caption("Having trouble with TraceME or just want to say hi? I'm happy to hear from you!")

st.markdown("### 📬 How can I help?")
st.markdown(
    """
    Fill in the form below to send me a message directly.
    I typically respond within 1–2 days.

    You can ask about:
    - ❓ Issues installing or using TraceME
    - 🐞 Reporting a bug
    - 💡 Feature requests
    - 🙋 General feedback or questions

    If something went wrong, attach the latest log file: **Help → Show Log Folder** in the app opens
    the folder. Please also say which TraceME version and system you use (**Help → About**).
    """
)

st.markdown("---")

# --- Contact Form ---
with st.form("contact_form", border=True):
    name = st.text_input("👤 Your Name", placeholder="e.g. John Doe")
    email = st.text_input("📧 Email Address", placeholder="e.g. john@example.com")
    message = st.text_area("💬 Your Message", placeholder="Describe the issue or your suggestion...")
    submitted = st.form_submit_button("📨 Send Message")

    if submitted:
        if not name or not email or not message:
            st.error("❗ Please fill in all fields.")
        elif not is_valid_email(email):
            st.error("❗ Please enter a valid email address.")
        else:
            log_contact(name, email, message)
            st.success("✅ Your message has been sent! I’ll get back to you as soon as possible.")
            st.balloons()

# --- Quick answers ---
st.markdown("---")
st.markdown("### Frequently asked questions")
for item in get_text("faq", []):
    with st.expander(item["q"]):
        st.markdown(item["a"])

st.markdown("### Error messages")
st.markdown(
    "| Message | What to do |\n"
    "|---|---|\n"
    "| *No SAM model installed* | Download one in **Settings → Models**. |\n"
    "| *FFmpeg not found* | Only when running from source: install FFmpeg, or `pip install imageio-ffmpeg`. The installed app includes it. |\n"
    "| *SAM2 dependencies are not available* | Only from source: install `torch` and `sam2`. |\n"
    "| A tracking run failed | Open the run's log: `last_run.log` in the video's results folder (**Tracking → Open Results Folder**). |"
)

# --- Footer: Links & Credits ---
st.markdown("---")
st.markdown(
    "🔗 Useful Links: "
    f"[GitHub]({APP_REPO}) • "
    f"[Report a problem]({ISSUES_URL}) • "
    f"[Research Group]({LAB_URL})"
)
