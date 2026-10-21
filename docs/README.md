# Project Documentation (`docs/`)

This directory contains technical monographs, operational manuals, hardware guides, and command cheat sheets for the Delto-3F in-hand dexterous manipulation system.

---

## Documentation Index

| Document | Format | Description |
| :--- | :---: | :--- |
| [**`IN_HAND_MANIPULATION_DOCUMENTATION.pdf`**](IN_HAND_MANIPULATION_DOCUMENTATION.pdf) | PDF (55 pages) | Publication-grade comprehensive technical monograph covering all 57 reward iterations, biomechanical safety proofs, Sim-to-Real domain randomization physics, and benchmark graphs. |
| [**`learning.md`**](learning.md) | Markdown | Complete technical engineering notes and mathematical derivations (57 exhaustive sections). |
| [**`teleop_pipeline_guide.md`**](teleop_pipeline_guide.md) | Markdown | Hardware setup manual, webcam ArUco tracking guide, calibration instructions, and data collection pipeline. |
| [**`commands.txt`**](commands.txt) | Plain Text | Fast command cheat sheet for evaluation, training, teleoperation, and benchmarking. |

---

## Re-compiling the Technical PDF

The 55-page publication monograph `IN_HAND_MANIPULATION_DOCUMENTATION.pdf` can be automatically regenerated from `learning.md` using the Chrome Headless KaTeX compiler:

```bash
python3 scripts/generate_documentation_pdf.py
```

Prerequisites:
- Google Chrome or Chromium installed (`google-chrome` or `chromium-browser` on PATH).
- Python dependencies: `markdown`, `pygments`.
