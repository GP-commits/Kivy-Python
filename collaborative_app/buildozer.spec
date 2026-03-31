[app]

# (str) Title of your application
title = Collaborative Sandbox

# (str) Package name
package.name = collab_sandbox

# (str) Package domain (needed for android/ios packaging)
package.domain = org.test

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let leave it empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 0.1

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
# We need websockets for the network, and kivy
requirements = python3,kivy,websockets

# (str) Custom source folders for requirements
# This is how we include your local libraries into the mobile app!
# It tells buildozer to package these directories directly into the APK.
source.include_dirs = ../kivy-dragdrop, ../kivy-network-project

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
