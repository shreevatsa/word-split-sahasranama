Serving at [vishnu-sahasranama.shreevatsa.net](https://vishnu-sahasranama.shreevatsa.net/)

This is basically just the data from https://www.swami-krishnananda.org/vishnu/vishnu_1.html etc (just a page I found online), coloured such that consecutive names are in different colours.

---

How this was generated:

- Opened Emacs and ran the elisp in `manual-process/emacs-setup.el`
- Manually copied the data from https://www.swami-krishnananda.org/vishnu/vishnu_1.html (etc) into `slokas.txt` via a Markdown editor (Obsidian).
- Manually went over the file `slokas.txt` using the `=` character set up in Emacs above. See video file `editing-sample.mov` for a video recording.
- Now `data.js` is generated from this file (see `Makefile`) using the Python script.
- The file `template.html` incorporates `data.js`.


---

AI usage statement: The Python script (`sloka_parser_flexible_format.py`), the HTML template (`template.html`) and even the supporting Elisp (`emacs-setup.el`) were AI generated. All the data is manually copied from Swami Krishnananda's website and edited as above, with no AI involvement.
