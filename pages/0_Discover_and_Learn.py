import streamlit as st

from utils.utils import footer, page_setup

page_setup("Discover and Learn", "🧠")
st.title("🧠 Discover and Learn")

# Fancy but theme-safe CSS
st.markdown("""
<style>
    /* Card Styling */
    .card {
        padding: 1.2rem 1.5rem;
        margin-bottom: 1.5rem;
        border-radius: 16px;
        background-color: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(10px);
        box-shadow:
            0 4px 10px rgba(0, 0, 0, 0.2),
            0 2px 4px rgba(0, 0, 0, 0.15);
        transition: all 0.2s ease;
    }

    /* Light theme override */
    body[data-theme="light"] .card {
        background-color: rgba(255, 255, 255, 0.8);
        border: 1px solid rgba(0, 0, 0, 0.05);
        box-shadow:
            0 6px 16px rgba(0, 0, 0, 0.15),
            0 3px 8px rgba(0, 0, 0, 0.1);
    }

    /* Hover effect for both themes */
    .card:hover {
        transform: scale(1.01);
        box-shadow:
            0 10px 30px rgba(0, 0, 0, 0.3),
            0 5px 15px rgba(0, 0, 0, 0.2);
    }

    .card h4 {
        margin-top: 0;
        margin-bottom: 0.75rem;
        font-size: 1.45rem;
        font-weight: 700;
        color: var(--primary-color);
    }

    .card ul {
        padding-left: 1.5rem;
        margin-bottom: 0;
    }

    .card p {
        color: var(--text-color);
        font-size: 0.96rem;
        margin: 0;
    }

</style>
""", unsafe_allow_html=True)

st.markdown("The terms used across TraceME and in video object tracking in general.")

# ─────────────────────────────
# TERMINOLOGY
# ─────────────────────────────
st.divider()
st.header("📘 Terminology")

groups = {
    "🧠 Vision Tasks": [
        ("Object Detection", "Detect and localize objects in a single image using bounding boxes."),
        ("Instance Segmentation", "Separate each object instance pixel-wise."),
        ("Promptable Segmentation", "Segment whatever a click or a box points at, as SAM does."),
        ("Video Object Segmentation", "Follow an object's mask through every frame of a video."),
        ("Multi-Object Tracking", "Follow several objects at once while keeping their identities apart."),
    ],
    "✍️ Annotation Concepts": [
        ("Object", "One thing you follow, e.g. Mouse A. It keeps its name and colour in every video."),
        ("Annotation", "An object marked on one frame; tracking starts from it."),
        ("Prompt", "The clicks or the box that tell SAM where the object is."),
        ("Foreground / Background Point", "A click on the object, or on something the mask should leave out."),
        ("Annotated Frame", "A frame holding at least one annotation. A few per object are enough."),
        ("Mask", "Region representing an object on one frame."),
    ],
    "🎞️ Video and Tracking": [
        ("Frame", "One image of a video. TraceME stores every imported frame as an image."),
        ("Frame Rate (FPS)", "Frames per second. Keeping every Nth frame lowers it."),
        ("Propagation", "Carrying a mask forward from an annotated frame to the frames after it."),
        ("Chunk / Overlap", "Long videos are tracked in pieces; overlap frames carry each object into the next piece."),
        ("Lost Object", "An object the model could not find on a frame, e.g. hidden or out of view."),
        ("Tracking Run", "One pass of the model over a frame range, giving masks, a video and metrics."),
    ],
    "📦 Geometric Structures": [
        ("Bounding Box", "A rectangle enclosing an object."),
        ("Centroid", "Center point of a mask; its path over time is the object's trajectory."),
        ("Mask Area", "Size of a mask in pixels."),
        ("Perimeter", "Length of a mask's outline."),
        ("Crop", "The part of the frame kept on import; everything outside is dropped."),
    ],
}

for section, terms in groups.items():
    st.subheader(section)
    cols = st.columns(3)
    for i, (term, desc) in enumerate(terms):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="card">
                <h4>{term}</h4>
                <p style="margin:0.2rem 0 0;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

footer()
