"""Shared helpers for the TraceME manual pages."""
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import streamlit as st
import yaml

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

APP_REPO = "https://github.com/StevetheGreek97/traceme-app"
PIPELINE_REPO = "https://github.com/StevetheGreek97/traceme-pipeline"
# "latest", not a version: each release's file names carry the version, CPU/CUDA
# flavor and architecture, so linking the release page never goes stale.
RELEASES_URL = f"{APP_REPO}/releases/latest"
ISSUES_URL = f"{APP_REPO}/issues"
PYPI_URL = "https://pypi.org/project/traceme-pipeline/"
LAB_URL = "https://www.biologie.uni-hamburg.de/forschung/populationsgenomik.html"


def page_setup(title: str, icon: str, layout: str = "wide"):
    st.set_page_config(page_title=f"{title} · TraceME Manual", page_icon=icon, layout=layout)


@st.cache_data
def _texts() -> dict:
    with open(ASSETS / "text.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def get_text(section: str, default=""):
    """A section of assets/text.yaml."""
    return _texts().get(section, default)


def screenshot(name: str, caption: str = ""):
    """An app screenshot from assets/screens/, or a note if it's missing."""
    path = ASSETS / "screens" / f"{name}.png"
    if path.is_file():
        st.image(str(path), caption=caption or None, width="stretch")
    else:
        st.caption(f"(Screenshot '{name}' not available yet.)")


def footer():
    st.divider()
    st.caption(
        f"Made by Stylianos (Steve) Mavrianos – [Lab website]({LAB_URL}) · "
        f"[TraceME on GitHub]({APP_REPO}) · [Report a problem]({ISSUES_URL})"
    )


# ── Installer requests (pages/1_Install_and_Setup.py) ───────────────────────

_PLATFORM_NAMES = {"windows": "Windows", "macos": "macOS", "linux": "Linux"}

_BUILD_LABELS = {"cpu": "CPU", "cuda": "CUDA"}

_INSTALL_STEPS = {
    ("windows", "cpu"): """Download TraceME-<version>-windows-cpu-x64-setup.exe from the release page and run it.
It installs for your user account and needs no administrator rights. This build works on any
computer, with or without an NVIDIA GPU.

The installer isn't code-signed yet. If Windows SmartScreen warns you, click More info -> Run anyway.""",
    ("windows", "cuda"): """This build needs an NVIDIA GPU. Download TraceME-<version>-windows-cuda-x64-setup.exe and every
TraceME-<version>-windows-cuda-x64-setup-N.bin file from the release page, keep them all in the
same folder, and run the .exe. It installs for your user account and needs no administrator rights.

The installer isn't code-signed yet. If Windows SmartScreen warns you, click More info -> Run anyway.""",
    ("macos", "cpu"): """Download TraceME-<version>-macos-arm64.dmg from the release page and open it.
Drag TraceME onto the Applications shortcut inside the window. This build is for Apple Silicon Macs
only, and uses the Apple GPU automatically.

The first time, right-click TraceME in Applications and choose Open (the app isn't signed yet, so a
normal double-click is blocked once).""",
    ("linux", "cpu"): """Debian, Ubuntu, or Mint -- download traceme_<version>_amd64.deb (_arm64.deb on an ARM machine)
and install it:

    sudo apt install ./traceme_<version>_amd64.deb

TraceME then appears in the applications menu (or run: traceme), and .tme project files open with
it on double-click. Needs Ubuntu 22.04 or newer (24.04 or newer on ARM). Remove it later with:
sudo apt remove traceme

Other distributions -- download TraceME-<version>-linux-cpu-x64.tar.gz (or -arm64 on an ARM machine),
then unpack it and run the app:

    tar xzf TraceME-<version>-linux-cpu-x64.tar.gz
    ./TraceME/traceme

From source -- needs Python 3.12 or newer and Git. Clone the repository, then install and run:

    git clone https://github.com/StevetheGreek97/traceme-app.git
    cd traceme-app
    ./install.sh
    ./run.sh""",
    ("linux", "cuda"): """This build needs an NVIDIA GPU. It comes in parts, so download every
traceme-cuda_<version>_amd64.deb.part-NN file and SHA256SUMS from the release page, then join, verify,
and install them:

    cat traceme-cuda_<version>_amd64.deb.part-* > traceme-cuda_<version>_amd64.deb
    sha256sum --ignore-missing -c SHA256SUMS
    sudo apt install ./traceme-cuda_<version>_amd64.deb""",
}


def is_valid_email(email):
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))


def _send_mail(subject, body, recipient_email, smtp_user, smtp_pass):
    msg = MIMEMultipart()
    msg["From"] = smtp_user
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)


def send_auto_reply(platform, name, last_name, recipient_email, smtp_user, smtp_pass, build="cpu"):
    """Email the requester the release link and the install steps for their platform and build."""
    platform = platform.lower()
    platform_name = _PLATFORM_NAMES[platform]
    build_label = _BUILD_LABELS[build]

    body = f"""
Hi {name} {last_name},

Thanks for your interest in TraceME! Your {platform_name} {build_label} download is ready on the latest release page:
🔗 {RELEASES_URL}

Each release lists several files -- pick the one for {platform_name} {build_label}.

How to install TraceME on {platform_name} ({build_label} build):

{_INSTALL_STEPS[(platform, build)]}

The first project you open offers to download a SAM model; you can also do it at any time under
Settings -> Models.

If you have any questions or feedback, feel free to reply to this email.

Best regards,
PopGen Team
"""
    _send_mail("🎉 Your TraceME Installer is Ready", body, recipient_email, smtp_user, smtp_pass)


def notify_admin(name, last_name, user_email, comments, smtp_user, smtp_pass, recipient_email, build="cpu"):
    """Tell the admin about a new installer request."""
    body = f"""
You received a new request for the TraceME installer.

👤 Name: {name} {last_name}
📧 Email: {user_email}
📦 Build: {_BUILD_LABELS[build]}
📝 Comments: {comments or 'None provided'}

Please follow up manually with the download link.
"""
    _send_mail("📥 New TraceME Installer Request", body, recipient_email, smtp_user, smtp_pass)
