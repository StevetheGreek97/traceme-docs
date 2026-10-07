# TraceME-docs

The Streamlit user manual for [TraceME](https://github.com/StevetheGreek97/traceme-app): installing it,
the interface, projects and video import, annotating, tracking, keyboard shortcuts, the command-line
pipeline, and help.

## Run locally

```bash
pip install -r requirements.txt
streamlit run Welcome.py
```

## Layout

- `Welcome.py` – start page; `pages/` – one file per page, numbered in sidebar order.
- `assets/text.yaml` – longer texts (intro, workflow steps, FAQ).
- `assets/screens/` – app screenshots; `assets/logo.png` – the app icon.
- `utils/utils.py` – shared links (releases, issues, PyPI) and helpers.

## Deploy

On [Streamlit Community Cloud](https://share.streamlit.io): *New app* → this repository, branch `main`,
main file `Welcome.py`.

The Install and Setup page logs installer requests to a Google Sheet and emails the download link, so
it needs these secrets (`.streamlit/secrets.toml` locally, *Settings → Secrets* on Community Cloud):

- `[google]` – a Google service-account key; the same one SegmentME-docs uses. Requests go to the shared
  `SegmentME Downloads` sheet, with `TraceME` in its App column.
- `[email]` – `user` and `password` (an app password) of the Gmail account that sends the emails.
