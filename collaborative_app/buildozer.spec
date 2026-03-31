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
# We need websockets and kivy, as well as openssl for networking and hostpython3 for the build toolchain.
requirements = python3,kivy,websockets,openssl,hostpython3

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (int) Android API to use
android.api = 34

# (int) Minimum API your APK will support
android.minapi = 21

# (bool) Accept SDK license
android.accept_sdk_license = True

# (str) Android NDK version to use
# android.ndk = 25b

# (list) The Android architectures to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
