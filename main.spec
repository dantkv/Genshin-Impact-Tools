# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

SRC_ROOT_DIR = "genshin/"

file_list = [
    SRC_ROOT_DIR + "main.py",
    SRC_ROOT_DIR + "config.py",
    SRC_ROOT_DIR + "__init__.py",

    SRC_ROOT_DIR + "common/__init__.py",
    SRC_ROOT_DIR + "common/const.py",
    SRC_ROOT_DIR + "common/user.py",
    
    SRC_ROOT_DIR + "module/__init__.py",
    SRC_ROOT_DIR + "module/gacha_export.py",
    SRC_ROOT_DIR + "module/update.py",
    
    SRC_ROOT_DIR + "utils/__init__.py",
    SRC_ROOT_DIR + "utils/functional.py",
    SRC_ROOT_DIR + "utils/logger.py",
    SRC_ROOT_DIR + "utils/version.py",
]

resource_path = "resource"

exe_name = "Genshin_Impact_Tools"

icon_path = "resource/ys.ico"

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
