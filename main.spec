# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

file_list = [
    'src/main.py',
    'src/common.py',
    'src/config.py',
    'src/gacha_export.py',
    'src/utils.py',
    'src/update.py',
]

resource_path = 'resource'

exe_name = 'Genshin_Impact_Tools'

icon_path = 'resource/ys.ico'

data_list = [
    (resource_path, resource_path)
]

a = Analysis(
    file_list,
    pathex=[],
    binaries=[],
    datas=data_list,
    hiddenimports=[],
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
    name=exe_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path,
)
