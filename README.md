# iTerm2 Auto Active/Inactive Window Transparency

A pair of scripts which automatically toggle the transparency of iTerm2 windows
based on active status:

- `transparency-toggle.py` for transparent active windows
- `transparency-toggle-opaque.py` for opaque active windows

Created as a solution to [this Stack Overflow question](https://stackoverflow.com/questions/48470804/iterm2-transparent-transparent-background-for-inactive-windows/69908530).

See the iTerm2 docs for details on [using Python scripts](https://iterm2.com/python-api/).

You want to set the desired transparency on your profile, and check the "Use
transparency" box for "Settings for New Windows" (Preferences -> Profiles ->
Window). This sounds counter-intuitive, but toggling that "Use transparency"
setting doesn't seem to be possible via the API, so the script instead relies on
"Use transparency" to always be set, and adjusts the transparency value on
active status changes.

---

macOS previously (macOS 11, Big Sur) treated windows the opposite of how people
usually approach transparent terminal windows—it maked active windows
transparent (at least, certain parts of them) and inactive ones opaque (and
faded). You could see this when opening new tabs in Safari (if you didn't have a
start page background image). It makes sense! The transparency creates a sense
of depth. Seeing that there are windows behind the active one emphasizes that
it's in front of them.

The variant which emulates this behavior is simpler than the opaque-on-active
version, and seems to run more smoothly. It works best if you have the blur
cranked to max, and transparency ~30.

With the opaque-on-active version, at least on my machine, the window flickers
briefly when first selected, but I'm not sure if there's anything I can do about
that.
