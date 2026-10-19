[app]
title = MC清理器Pro
package.name = mccleaner
package.domain = org.mccleaner

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0
requirements = python3, kivy
p4a.branch = master

# 安卓
android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a

# 不使用全屏
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1
