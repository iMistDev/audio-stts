# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

# --- RECOLECCIÓN AUTOMÁTICA DE DEPENDENCIAS ---
# Esto busca todos los binarios, datos (onnx) y dependencias ocultas
datas, binaries, hiddenimports = collect_all('faster_whisper')

# A veces ctranslate2 también da guerra, mejor prevenir:
tmp_ret = collect_all('ctranslate2')
datas += tmp_ret[0]
binaries += tmp_ret[1]
hiddenimports += tmp_ret[2]

# --- TU ANÁLISIS ---
block_cipher = None

a = Analysis(
    ['main_eel.py'],
    pathex=[],
    binaries=binaries,  # <--- AGREGAMOS LOS BINARIOS RECOLECTADOS
    datas=datas + [('web', 'web')], # <--- AGREGAMOS LOS DATOS RECOLECTADOS + TU CARPETA WEB
    hiddenimports=hiddenimports + ['bottle_websocket', 'engineio', 'socketio', 'pyaudio'], # <--- SUMAMOS LOS HIDDEN IMPORTS
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ShhStreamer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False, # Mantenlo en False si quieres ocultar la consola, o True para seguir depurando
    disable_windowed_traceback=True,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app.ico',
)