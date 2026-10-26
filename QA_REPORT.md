# Build & quality check · 26 October 2026

- Built from uploaded `work-main.zip` using Python + Jinja2 + PyYAML + Pillow.
- Production target: `https://invernizziluca.github.io/work/` (the workflow assumes GitHub repository `work`).
- **20 generated HTML pages** across English, German and Italian.
- **875 local internal HTML links and asset references checked**, no missing targets in the generated site.
- Checked responsive layout in Chromium at **1440 × 900** and **390 × 844**, across EN, DE and IT: no horizontal overflow, body background `rgb(247, 249, 252)` with browser color scheme deliberately set to dark.
- Screenshots examined for the homepage, work experience and documentary evidence.
- Python build script compiled successfully; JavaScript passed syntax checking.
- No submission to Google and no publication to GitHub was performed.

**Check again after future edits:** run `python build.py --preview`, review the generated pages on desktop/mobile and inspect every modified source or metric.
