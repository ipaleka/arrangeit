
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

datas = [('./arrangeit/resources', './arrangeit/resources')]

hiddenimports = [
    'arrangeit.windows',
    'arrangeit.windows.apihelpers',
    'arrangeit.windows.app',
    'arrangeit.windows.collector',
    'arrangeit.windows.controller',
    'arrangeit.windows.utils',
    'tkinter',
]

excludes = [
    '_bz2',
    '_decimal',
    '_hashlib',
    '_lzma',
    '_socket',
    '_ssl',
    'java.lang',
    'PIL.ImageQt',
    'PIL._webp',
    'pyexpat',
    'pynput._util.darwin',
    'pynput._util.xorg',
    'pynput.keyboard._xorg',
    'pynput.mouse._darwin',
    'pynput.mouse._xorg',
    'select',
    'xml.sax',
]

a = Analysis(
    ['starter.py'],
    pathex=['C:\\dev\\arrangeit'],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='arrangeit',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon='arrangeit\\resources\\arrangeit.ico'
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='arrangeit',
)
