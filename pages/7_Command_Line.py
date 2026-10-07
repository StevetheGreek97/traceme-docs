import streamlit as st

from utils.utils import PIPELINE_REPO, PYPI_URL, footer, page_setup

page_setup("Command Line", "🖥️")
st.header("🖥️ Tracking from the Command Line")

st.markdown(
    f"The tracking in TraceME is done by **[traceme-pipeline]({PIPELINE_REPO})**, which you can also "
    "run on its own, without the app. You annotate in the app, export the annotations, and run the "
    "tracking from a terminal."
)

c1, c2 = st.columns(2)
with c1:
    with st.container(border=True):
        st.markdown("**1 · Annotate in the app**")
        st.markdown("Mark your objects on a few frames, then **File → Export YAMLs**: one prompt file per video.")
with c2:
    with st.container(border=True):
        st.markdown("**2 · Run `traceme`**")
        st.markdown("One command per video gives a CSV, an annotated video and, if you ask, masks.")

tab_install, tab_input, tab_run, tab_output, tab_batch, tab_help = st.tabs(
    ["📦 Install", "📥 Input", "▶️ Run", "📤 Output", "🗂️ Many videos", "🛠️ Resume and problems"]
)

# ───────────────────────── Install ─────────────────────────
with tab_install:
    st.markdown(f"The pipeline is on [PyPI]({PYPI_URL}) and needs **Python 3.12 or newer**:")
    st.code("pip install traceme-pipeline", language="bash")
    st.markdown(
        "This installs three commands: `traceme` (the tracking), `traceme-gen-tasks` (task lists for many "
        "videos) and `traceme-download-checkpoints` (the models). A CUDA GPU is recommended; the CPU "
        "works but is slow."
    )

    st.markdown("### Models")
    st.markdown(
        "The SAM2 model a run needs is **downloaded automatically** the first time, into "
        "`~/.cache/traceme/sam2/checkpoints`. On a machine without internet access, "
        "download them beforehand:"
    )
    st.code(
        """traceme-download-checkpoints                       # all four SAM2 models
traceme-download-checkpoints --model small         # just one: tiny, small, base_plus or large
traceme-download-checkpoints --dir /data/models    # somewhere else than the cache folder""",
        language="bash",
    )
    st.markdown(
        "If you download to another folder, point the pipeline at it with `SAM2_CHECKPOINT_DIR` (see "
        "*Environment variables* in the **Run** tab)."
    )

    st.markdown("### SAM3 (optional)")
    st.code(
        """pip install 'traceme-pipeline[sam3]'
traceme -i frames/ -o out/ -p prompts.yaml --model sam3""",
        language="bash",
    )
    st.markdown(
        "The SAM3 model is **not** downloaded automatically, because it's gated on Hugging Face: log in "
        "with `hf auth login`, download it from the `facebook/sam3` repository, and put it in your "
        "checkpoint folder as `sam3.pt`."
    )

# ───────────────────────── Input ─────────────────────────
with tab_input:
    st.markdown("A run needs two things: a folder of frames and a YAML file of prompts.")

    st.markdown("### Frames folder")
    st.markdown(
        "One folder per video, holding its frames as images (`00000.jpg`, `00001.jpg`, …). Frames are "
        "used in sorted order, and **frame numbers are 0-based positions in that order**. In a TraceME "
        "project these are the folders under `frames/`. The folder's name becomes the name of the "
        "output files."
    )

    st.markdown("### Prompt file")
    st.markdown(
        "**File → Export YAMLs** in TraceME writes one per video from your annotations, so you normally "
        "don't write it by hand. It holds a top-level `prompts` list with one entry per object per "
        "annotated frame:"
    )
    st.code(
        """prompts:
  - frame_idx: 0            # the frame this annotation is on (0-based)
    obj_id: 1               # the object; the same id on every frame it is annotated
    points: [[486, 1094], [512, 1111]]   # [x, y] in pixels
    labels: [1, 0]          # one per point: 1 = positive (the object), 0 = negative (not part of it)
    box: [672, 914, 74, 110]             # optional: [x, y, width, height]
  - frame_idx: 0
    obj_id: 2
    points: [[1320, 640]]
    labels: [1]""",
        language="yaml",
    )
    st.markdown(
        "| Key | Required | Meaning |\n"
        "|---|---|---|\n"
        "| `frame_idx` | yes | Frame number, 0-based. |\n"
        "| `obj_id` | yes | A whole number identifying the object. It's the `obj_id` in the results. |\n"
        "| `points` | yes | List of `[x, y]` pixel positions. |\n"
        "| `labels` | yes | One per point: `1` positive, `0` negative. |\n"
        "| `box` | no | `[x, y, width, height]` in pixels. A box of zero width or height is ignored. |\n"
        "| `polygon` | no | The object's outline as a list of `[x, y]` points. |"
    )
    st.info(
        "Tracking runs **forward** from an annotated frame, exactly as in the app: frames before an "
        "object's first annotation aren't tracked for it."
    )

# ───────────────────────── Run ─────────────────────────
with tab_run:
    st.code("traceme -i /path/to/frames -o /path/to/output -p /path/to/prompts.yaml", language="bash")

    st.markdown("### Common recipes")
    st.code(
        """# Only part of the video (frame numbers, both ends included; either can be left out)
traceme -i frames/clipA -o out -p clipA.yaml --start-frame 1200 --end-frame 2400

# A smaller, faster model
traceme -i frames/clipA -o out -p clipA.yaml --model small

# Also keep full masks and outlines, for shape analysis and review
traceme -i frames/clipA -o out -p clipA.yaml --save-masks --save-contours

# Numbers only: skip rendering the annotated video
traceme -i frames/clipA -o out -p clipA.yaml --no-video

# Less memory: smaller chunks
traceme -i frames/clipA -o out -p clipA.yaml -c 300

# Force the CPU, and clean up the temporary files afterwards
traceme -i frames/clipA -o out -p clipA.yaml --device cpu --del_tmp""",
        language="bash",
    )
    st.markdown(
        "With a frame range, prompts outside the range are ignored and the results keep the video's own "
        "frame numbers: frame 1200 in the CSV is frame 1200 of the video, not of the range."
    )

    st.markdown("### All options")
    st.markdown(
        "| Option | Default | What it does |\n"
        "|---|---|---|\n"
        "| `-i`, `--frame_dir` | required | The folder of frames. |\n"
        "| `-o`, `--output_folder` | required | Where the results go. |\n"
        "| `-p`, `--prompt_file` | required | The prompt YAML. |\n"
        "| `--model` | `large` | `tiny`, `small`, `base_plus`, `large` (SAM2) or `sam3`. |\n"
        "| `--device` | `auto` | `auto`, `cuda`, `mps` or `cpu`. *Auto* tries CUDA, then Apple MPS, then the CPU. A device that isn't available falls back to the CPU. |\n"
        "| `--start-frame` | first frame | First frame to track. |\n"
        "| `--end-frame` | last frame | Last frame to track, included. |\n"
        "| `-c`, `--chunk_size` | `500` | Frames per chunk. The video is tracked in chunks to limit memory use. |\n"
        "| `--overlap` | `1` | Frames shared by neighbouring chunks, which carry each object across the seam. |\n"
        "| `--fps` | `60` | Frame rate of the annotated video. |\n"
        "| `--save-masks` | off | Keep every object's full mask in `<video>_masks.npz`. |\n"
        "| `--save-contours` | off | Write each object's outline per frame to `<video>_contours.jsonl`. |\n"
        "| `--no-video` | off | Don't render the annotated `.mp4`. |\n"
        "| `-d`, `--del_tmp` | off | Delete the temporary chunk folders when the run has finished. |\n"
        "| `--no-resume` | off | Track everything again, even chunks an earlier run completed. |\n"
        "| `--chunk-mode` | `auto` | `auto` reuses the chunk folders of an earlier run when they still fit; `force` rebuilds them. |"
    )
    st.caption("`traceme --help` prints the same list for the version you have installed.")
    st.warning(
        "`--fps` defaults to **60**, not to your video's frame rate. Set it to the video's own rate (or "
        "that rate divided by N, if you kept every Nth frame on import) so the annotated video plays at "
        "real speed."
    )

    st.markdown("### Environment variables")
    st.markdown(
        "An option on the command line wins over the matching variable.\n\n"
        "| Variable | What it does |\n"
        "|---|---|\n"
        "| `SAM2_MODEL` | The model, like `--model`. |\n"
        "| `TRACEME_DEVICE` | The device, like `--device`. |\n"
        "| `SAM2_CHECKPOINT_DIR` | The folder holding the models, instead of `~/.cache/traceme/sam2/checkpoints`. |\n"
        "| `SAM2_CHECKPOINT` | The path of one specific model file. |\n"
        "| `TRACEME_AUTO_DOWNLOAD=0` | Never download a missing model; stop with an error instead. |\n"
        "| `HYDRA_FULL_ERROR=1` | Show SAM2's full error messages. |"
    )

    st.markdown("### Chunk size and memory")
    st.markdown(
        "Tracking time depends on the number of frames, but every chunk costs some extra start-up time, "
        "so **use the largest chunks your memory allows** and keep the overlap small (the default of 1 "
        "is usually enough). Memory grows with the chunk size:\n\n"
        "- Without `--save-masks`: about **12.6 MB per frame** of a chunk, so roughly 6 GB for the "
        "default 500 frames.\n"
        "- With `--save-masks`: add `objects × height × width ÷ 8` bytes per frame. This is the expensive "
        "part on large frames with many objects."
    )
    st.markdown(
        "For example, 12 objects on 5312 × 2988 frames:\n\n"
        "| `-c` | Tracking | `--save-masks` | Total |\n"
        "|---|---|---|---|\n"
        "| 300 | 3.8 GB | 7.1 GB | ~11 GB |\n"
        "| 1000 | 12.6 GB | 23.8 GB | ~36 GB |\n"
        "| 2000 | 25.2 GB | 47.6 GB | ~73 GB |"
    )

# ───────────────────────── Output ─────────────────────────
with tab_output:
    st.markdown("For a frames folder named `clipA`, the output folder gets:")
    st.markdown(
        "| File | Contents |\n"
        "|---|---|\n"
        "| `clipA.csv` | Per-frame, per-object statistics. |\n"
        "| `clipA.mp4` | The annotated video: one colour and `id:` label per object, and exactly one video frame per input frame. Not written with `--no-video`. |\n"
        "| `clipA_run_summary.json` | Whether the run is `complete` or `partial`, which chunks were tracked, resumed or failed, and the settings used. |\n"
        "| `clipA_masks.npz` | Every object's full mask. Only with `--save-masks`. |\n"
        "| `clipA_contours.jsonl` | Every object's outline. Only with `--save-contours`. |\n"
        "| `clipA_tmp/` | Temporary chunk files, kept so a run can resume. Removed by `--del_tmp`. They link to your frames rather than copying them, so they take almost no space. |"
    )

    st.markdown("### The CSV")
    st.markdown(
        "One row per object per frame:\n\n"
        "| Column | Meaning |\n"
        "|---|---|\n"
        "| `global_frame_idx` | Frame number in the video (0-based). |\n"
        "| `obj_id` | The object, as in the prompt file. |\n"
        "| `area_px` | Mask area in pixels. |\n"
        "| `centroid_x`, `centroid_y` | Centre of the mask, in pixels. |\n"
        "| `bbox_x`, `bbox_y`, `bbox_w`, `bbox_h` | Bounding box: top-left corner, width and height. |\n"
        "| `chunk_id`, `in_chunk_idx` | Which chunk the row came from, and the frame's position in it. |"
    )
    st.markdown(
        "- A row with **every statistic `-1`** means the object was lost on that frame.\n"
        "- A frame with no tracked objects at all has a single row with an empty `obj_id` and `area_px` 0."
    )
    st.code(
        """import pandas as pd

df = pd.read_csv("out/clipA.csv")
df = df[df["obj_id"].notna()]                # drop frames without any object
lost = df["area_px"] == -1                   # frames where an object was lost

track = df[~lost & (df["obj_id"] == 1)]      # object 1's trajectory
print(track[["global_frame_idx", "centroid_x", "centroid_y", "area_px"]])""",
        language="python",
    )

    st.markdown("### Masks")
    st.markdown(
        "`--save-masks` stores one mask per object per frame, tightly packed, and only where the object "
        "was found. Unpack them with the pipeline's own helper:"
    )
    st.code(
        """import numpy as np
from traceme.sam2.io import _unpack_mask

data = np.load("out/clipA_masks.npz", allow_pickle=True)
for frame, obj, packed, shape in zip(
    data["global_frame_idx"], data["obj_id"], data["packed"], data["shape"]
):
    mask = _unpack_mask(packed, tuple(shape))    # True/False image, (height, width)""",
        language="python",
    )

    st.markdown("### Contours")
    st.markdown(
        "`--save-contours` writes one line per frame, with each object's outline as polygons. An empty "
        "list means the object was lost on that frame. It's much smaller than the masks, and it's the "
        "file the TraceME app uses to show tracking results."
    )
    st.code('{"frame": 12, "objects": {"1": [[[x, y], ...]], "2": []}}', language="json")

# ───────────────────────── Many videos ─────────────────────────
with tab_batch:
    st.markdown(
        "`traceme-gen-tasks` pairs every video folder with its prompt file and writes the list to a "
        "tab-separated file, one video per line. It expects one sub-folder per video, holding the frames "
        "and a prompt file named after the folder (or exactly one `.yaml`):"
    )
    st.code(
        """videos/
  clipA/
    00000.jpg ...
    clipA.yaml
  clipB/
    00000.jpg ...
    clipB.yaml""",
        language="text",
    )
    st.code(
        """traceme-gen-tasks videos -o tasks.tsv            # sub-folders of videos/
traceme-gen-tasks videos -o tasks.tsv --recursive    # folders at any depth""",
        language="bash",
    )
    st.markdown(
        "Folders without a prompt file (or with several that don't match the folder's name) are skipped, "
        "and the command says how many. Each line of `tasks.tsv` is `frames folder <TAB> prompt file`, "
        "so you can run them one after the other:"
    )
    st.code(
        """while IFS=$'\\t' read -r frames prompts; do
    traceme -i "$frames" -o results -p "$prompts" --no-video
done < tasks.tsv""",
        language="bash",
    )

# ───────────────────────── Resume and problems ─────────────────────────
with tab_help:
    st.markdown("### Interrupted runs")
    st.markdown(
        "- Run **the same command again**: chunks that already finished are skipped, and tracking "
        "continues from the first unfinished one. `--no-resume` tracks everything again.\n"
        "- If you changed the prompts, the model, the frame range or the chunk size since the earlier "
        "run into the same output folder, its chunks are thrown away rather than resumed, so results "
        "never mix two sets of inputs.\n"
        "- Resuming needs the `_tmp` folder, so don't delete it by hand between attempts."
    )

    st.markdown("### Failed chunks")
    st.markdown(
        "If a chunk fails (out of memory, for instance), the pipeline still merges the chunks it has, "
        "marks the run `partial` in `<video>_run_summary.json`, keeps the `_tmp` folder even with "
        "`--del_tmp`, and exits with code 1. Run the same command again to retry only the failed chunks; "
        "after an out-of-memory error, a smaller `-c` is the usual fix."
    )

    st.markdown("### Common problems")
    st.markdown(
        "| Problem | What to do |\n"
        "|---|---|\n"
        "| A model or its config can't be found | The error names the paths it looked in. Run `traceme-download-checkpoints`, or set `SAM2_CHECKPOINT_DIR` to where the models are. |\n"
        "| No internet on the machine | Download the models on one that has it and copy them over, then set `TRACEME_AUTO_DOWNLOAD=0` so a missing model is an error instead of a hanging download. |\n"
        "| It runs on the CPU although there's a GPU | Check that PyTorch sees it: `python -c \"import torch; print(torch.cuda.is_available())\"`. An unavailable `--device` silently falls back to the CPU. |\n"
        "| Out of memory | Use a smaller `-c`, or drop `--save-masks`. |\n"
        "| `YAML must contain a top-level 'prompts' list` | The prompt file isn't in the format shown in the **Input** tab. Export it again from the app. |\n"
        "| SAM2's error message is cut short | Set `HYDRA_FULL_ERROR=1` and run again. |\n"
        "| The annotated video plays too fast or too slow | Set `--fps` to the video's real frame rate. |"
    )

footer()
