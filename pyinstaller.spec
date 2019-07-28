
# -*- mode: python ; coding: utf-8 -*-

# arrangeit - cross-platform desktop utility for easy windows management
# Copyright (C) 1999-2019 Ivica Paleka

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>

block_cipher = None

datas = [
    ('./arrangeit/resources', './arrangeit/resources'),
    ('./arrangeit/locale', './arrangeit/locale')
]

hiddenimports = [
    'arrangeit.windows',
    'arrangeit.windows.api',
    'arrangeit.windows.app',
    'arrangeit.windows.collector',
    'arrangeit.windows.controller',
    'arrangeit.windows.utils',
    'arrangeit.windows.vdi',
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
