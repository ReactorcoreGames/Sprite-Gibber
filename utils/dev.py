import sys

# True when running from source; False in a PyInstaller-frozen exe.
# Used to gate developer-only features (e.g. "Save to Source" preset button).
DEV_MODE = not getattr(sys, "frozen", False)
