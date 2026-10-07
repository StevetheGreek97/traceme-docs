import streamlit as st

from utils.utils import footer, page_setup, screenshot

page_setup("Projects and Videos", "📁")
st.header("📁 Projects and Videos")
st.markdown(
    "The whole workflow in one place: set up a project and import your videos, annotate the objects on "
    "a few frames, then track them through the video and export the results."
)

tab_projects, tab_annotating, tab_tracking = st.tabs(
    ["📁 Projects and videos", "✨ Annotating", "📈 Tracking"]
)

with tab_projects:
    st.markdown("### Projects")
    st.markdown(
        "A project is a folder holding your videos' frames, the objects you track, all annotations and the "
        "tracking results. Everything is **saved automatically** as you work, and the project reopens "
        "where you left off.\n\n"
        "- **File → New Project** (Ctrl+N): choose a folder and a name.\n"
        "- **File → Open Project** (Ctrl+O): pick the project's `.tme` file (or its folder).\n"
        "- **File → Open Recent**: your last projects.\n"
        "- Double-click a `.tme` file in your file manager."
    )

    st.markdown("### Importing videos")
    st.markdown(
        "**File → Import Videos** (Ctrl+I) accepts MP4, MOV, AVI, MKV, M4V, MPEG, WMV and WebM, several at "
        "once. TraceME extracts each video's frames as images. Long or high-resolution videos produce a lot "
        "of frames, so before extracting you can choose what to keep:"
    )
    c1, c2 = st.columns([3, 2])
    with c1:
        screenshot("import_options", "The import options window")
    with c2:
        st.markdown(
            "**Keep every N frames** — e.g. every 3rd frame of a 30 fps video gives 10 fps. Tracking and "
            "exported videos still play at real speed.\n\n"
            "**Only part of the video** — a start and end time in seconds. The preview jumps to the start.\n\n"
            "**Crop to an area** — drag a rectangle on the preview. Everything outside it is dropped, which "
            "also makes tracking faster. *Whole frame* removes the crop.\n\n"
            "The bottom line estimates how many frames you'll get and their size. The options apply to every "
            "video you selected; a crop larger than a video is cut to fit it. Leave everything unchanged to "
            "extract every frame at full size."
        )
    st.info(
        "TraceME remembers how each video was imported, so frame numbers can always be mapped back to the "
        "original video: frame *i* is about `start × fps + i × step` of the source."
    )

    st.markdown("### Importing a folder of frames")
    st.markdown(
        "Already have frames (e.g. extracted with ffmpeg on a cluster)? **File → Import Frames Folder** adds "
        "a folder of images (`00000.jpg`, `00001.jpg`, …) as a video, in place, without copying it."
    )

    st.markdown("### What's in a project folder")
    st.code(
        """my_project/
  my_project.tme        project file: videos, objects, where you left off
  annotations.db        all annotations (and tracking results), in one database
  frames/
    my_video/
      00000.jpg
      00001.jpg
      ...
  results/
    my_video/           tracking results and exports (see the Tracking tab)""",
        language="text",
    )
    st.markdown(
        "**File → Export YAMLs** writes each video's annotations as a YAML file of prompts (frame, object, "
        "points, labels, box or outline), e.g. for running the pipeline yourself."
    )

with tab_annotating:
    st.markdown(
        "Annotations tell SAM2 what each object looks like. You don't need to annotate every frame: a few "
        "good frames per object (typically where it first appears, and where it's hard to see) are enough "
        "for tracking."
    )

    st.markdown("### 1. Add your objects")
    st.markdown(
        "In the **Objects** panel click **+** (or right-click → *Add object*) and give it a name, e.g. "
        "*Mouse A*. Each object gets its own colour. Objects are shared by every video in the project.\n\n"
        "- **Double-click** an object to rename it; **right-click** for Rename / Recolor / Delete.\n"
        "- The **selected** object is the one your clicks belong to."
    )
    st.warning(
        "Deleting an object removes it and **all its annotations in every video**, and can't be undone."
    )

    st.markdown("### 2. Mark the object on a frame")
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.markdown("**Points**")
            st.markdown(
                "- **Left-click**: positive point — *this is the object*.\n"
                "- **Right-click**: negative point — *this is not part of it*.\n"
                "- **Ctrl+click** a point to remove it."
            )
    with c2:
        with st.container(border=True):
            st.markdown("**Box**")
            st.markdown(
                "- Hold **Shift** and drag with the left mouse button around the object.\n"
                "- Combine it with points for more control."
            )

    st.markdown("### 3. Let SAM2 outline it")
    st.markdown(
        "Press **E** to run SAM2 on the selected object: its outline appears on the canvas. If it's not "
        "right, add a positive point where it's missing or a negative point where it spills over, then "
        "press **E** again. Changing an object's points or box clears its outline, since it no longer "
        "matches. **D** clears the outline by hand."
    )
    st.markdown(
        "The model used is chosen in **Settings → Models**; the status bar shows "
        "whether it runs on the GPU or the CPU."
    )

    st.markdown("### Tips")
    st.markdown(
        "- Annotate **every object on the same frames** where possible: tracking starts from annotated "
        "frames and runs forward.\n"
        "- Add an annotation where an object **reappears**, changes shape a lot, or touches another object.\n"
        "- Use **Show → Annotated** in the frames list to review your annotated frames quickly.\n"
        "- Zoom in (mouse wheel) for small objects; **F** fits the frame again."
    )

with tab_tracking:
    st.markdown(
        "Tracking follows every object from your annotated frames through the rest of the video. It runs in "
        "the background, as a separate process, so you can keep working, and a crash or out-of-memory error "
        "can't take the app down."
    )

    st.markdown("### Run tracking")
    st.markdown("**Tracking → Run Tracking…** (Ctrl+R) on the open video:")
    st.markdown(
        "| Option | What it does |\n"
        "|---|---|\n"
        "| **Model** | Any installed **SAM2.1** model, or SAM3 if available. |\n"
        "| **Frames from / to** | The range to track; the whole video by default. |\n"
        "| **Annotated frames** | Which of your annotated frames in the range are used as starting points. Tracking runs *forward* from an annotation, so frames before the first one aren't tracked. |\n"
        "| **Chunk size / Overlap** | The video is tracked in pieces (*chunks*) to limit memory use. Overlap frames carry each object into the next chunk. Smaller chunks need less memory. |\n"
        "| **Output FPS** | Frame rate of the annotated video; the video's own by default. |\n"
        "| **Device** | GPU or CPU; follows Settings → Models → Run on. The window warns you when a run would use the CPU (slow). |\n"
        "| **Save full masks** | Also keep every object's full mask, for shape analysis. |"
    )
    st.caption("Your choices are remembered for the next run.")

    st.markdown("### The Tracking window")
    st.markdown(
        "It opens when a run starts (and any time with **Tracking → Tracking Results…**, Ctrl+T). It's "
        "read-only: reviewing results never changes your annotations.\n\n"
        "- **While running:** progress, **Stop**, and a strip with one block per chunk — grey waiting, "
        "blue running, green done, red failed. Each chunk's results appear as soon as it's done; *Follow new "
        "batches* jumps to them.\n"
        "- **Viewer:** the tracked masks in object colours (**M** toggles them) and the annotations they came "
        "from (**P**). Frames where an object was **lost are red**; *Show* filters to tracked, lost or "
        "annotated frames.\n"
        "- Closing the window doesn't stop the run."
    )

    st.markdown("### Fixing mistakes")
    st.markdown(
        "- **Fix a single frame:** turn on **Edit → Edit Masks**, pick the object, click it on the frame "
        "(right-click to exclude, Shift+drag for a box) and press **E**. SAM replaces that frame's mask; "
        "**Esc** clears your clicks. Fixes are saved and included in the exports.\n"
        "- **Redo part of the video:** add or improve annotations in the main window, then run tracking "
        "again on just that range. The frames it tracks replace the old ones; everything else is kept. A "
        "cancelled or failed run changes nothing."
    )

    st.markdown("### Export")
    st.markdown("From the Tracking window's **Export** menu:")
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            st.markdown("**🎬 Video (.mp4)**")
            st.markdown(
                "The video with masks drawn on it. Choose the frame range, every Nth frame, speed, size, "
                "which objects, filled masks and/or outlines, names, and a frame number or time stamp."
            )
    with c2:
        with st.container(border=True):
            st.markdown("**🧩 Masks (.npz / .npy)**")
            st.markdown(
                "Label images: each pixel holds its object's id (0 = background). `.npz` has one array per "
                "frame; `.npy` is one array for the whole video."
            )
    with c3:
        with st.container(border=True):
            st.markdown("**📊 Metrics (.csv)**")
            st.markdown(
                "Per frame and object: area, centroid, bounding box and perimeter — ready for R, Python or "
                "a spreadsheet."
            )
    st.code(
        """import numpy as np
masks = np.load("my_video_masks.npz")
frame12 = masks["frame_000012"]        # (height, width), pixel value = object id
mouse_a = frame12 == 1                 # boolean mask of object 1""",
        language="python",
    )

    st.markdown("### Results folder")
    st.markdown(
        "Each video's results are also kept in `<project>/results/<video>/` (**Tracking → Open Results "
        "Folder**):\n\n"
        "| File | Contents |\n"
        "|---|---|\n"
        "| `<video>.csv` | Per-frame, per-object statistics |\n"
        "| `<video>_contours.jsonl` | Mask outlines (used by the Tracking window) |\n"
        "| `<video>_masks.npz` | Full masks, if *Save full masks* was on |\n"
        "| `<video>_prompts.json` | The annotations the tracking started from |\n"
        "| `tracking.json` | Which frames were tracked when, and with what |\n"
        "| `last_run.log` | The most recent run's log |"
    )

footer()
