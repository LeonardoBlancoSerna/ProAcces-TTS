[app]
title = ProAcces TTS
package.name = proacces
package.domain = org.proacces
source.dir = ProAcces-TTS
source.include_exts = py,png,jpg,syn,dic,txt
version = 2.1
requirements = python3,numpy,scipy,pyaudio

# (Específico para Android)
android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 23b
android.arch = armeabi-v7a, arm64-v8a

# Permisos
android.permissions = RECORD_AUDIO, MODIFY_AUDIO_SETTINGS

# Aquí es donde vinculamos el servicio de TTS nativo
android.services = tts:tts_service.py

# Icono
#icon.filename = %(source.dir)s/icon.png

[buildozer]
log_level = 2
warn_on_root = 1
