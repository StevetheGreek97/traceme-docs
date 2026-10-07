from datetime import datetime

import gspread
import streamlit as st
from google.oauth2.service_account import Credentials

from utils.utils import footer, is_valid_email, notify_admin, page_setup, send_auto_reply

page_setup("Install and Setup", "⚙️", layout="centered")
# Streamlit's centered column is a fixed 46rem, which looks tiny on a large
# screen: let it grow with the window instead.
st.markdown("<style>.stMainBlockContainer { max-width: max(46rem, 42vw); }</style>", unsafe_allow_html=True)

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
creds = Credentials.from_service_account_info(st.secrets["google"], scopes=scope)
client = gspread.authorize(creds)
# Shared with SegmentME-docs; the App column tells the two apart.
sheet = client.open("SegmentME Downloads").sheet1

BUILD_LABELS = {"cpu": "CPU (any computer)", "cuda": "CUDA (NVIDIA GPU only)"}


def log_download(name, email):
    timestamp = datetime.now().isoformat()
    sheet.append_row([timestamp, name, email, "TraceME"])


def request_form(platform, form_key, choose_build=False):
    with st.form(form_key, border=True):
        name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        email = st.text_input("📧 Email Address", placeholder="e.g. john@example.com")
        comments = st.text_area("💬 Comments (optional)", height=100)
        build = "cpu"
        if choose_build:
            build = st.radio("Build", list(BUILD_LABELS), horizontal=True, format_func=BUILD_LABELS.get)
        submitted = st.form_submit_button("📨 Submit Request")

        if not submitted:
            return
        if not name or not last_name or not email:
            st.error("❗ Please fill in your name, last name, and email.")
        elif not is_valid_email(email):
            st.error("❗ Please enter a valid email address.")
        else:
            log_download(name + " " + last_name, email)
            try:
                notify_admin(
                    name,
                    last_name,
                    email,
                    comments,
                    smtp_user=st.secrets["email"]["user"],
                    smtp_pass=st.secrets["email"]["password"],
                    recipient_email=st.secrets["email"]["user"],
                    build=build,
                )
                send_auto_reply(
                    platform=platform,
                    name=name,
                    last_name=last_name,
                    recipient_email=email,
                    smtp_user=st.secrets["email"]["user"],
                    smtp_pass=st.secrets["email"]["password"],
                    build=build,
                )
                st.success("✅ Your request has been submitted! The download link has been sent to your email.")
                st.balloons()
            except Exception as e:
                st.warning(f"Request was logged but email failed to send. Error: {e}")


st.header("⚙️ Install and Setup")

tabs = st.tabs(["Linux", "Windows", "MacOS"])

with tabs[0]:
    st.markdown("### Linux Installer Request")
    st.markdown("Please fill out the form below to request the Linux version of TraceME.")
    st.markdown("*You will receive the link by email after your request is approved.*")
    request_form("linux", "linux_download_form", choose_build=True)

with tabs[1]:
    st.image("assets/windows.png", width=50)
    st.markdown("### Windows Installer Request")
    st.markdown("Please fill out the form below to request the Windows version of TraceME.")
    st.markdown("*You will receive the link by email after your request is approved.*")
    request_form("windows", "windows_download_form", choose_build=True)

with tabs[2]:
    st.markdown("### macOS Installer Request")
    st.markdown("Please fill out the form below to request the macOS version of TraceME.")
    st.markdown("*You will receive the link by email after your request is approved — a `.dmg` "
                "disk image: open it and drag `TraceME.app` to the Applications shortcut inside, "
                "built for Apple Silicon Macs. There is no Intel build: GitHub retired hosted Intel "
                "macOS runners in December 2025, and Apple no longer sells Intel hardware.*")
    request_form("macos", "macos_download_form")

footer()
