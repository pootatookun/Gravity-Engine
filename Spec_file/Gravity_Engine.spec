# -*- mode: python ; coding: utf-8 -*-

import os
from kivy.tools.packaging.pyinstaller_hooks import get_deps_minimal, get_deps_all, hookspath, runtime_hooks
from kivy_deps import sdl2, glew

spec_root = os.path.abspath(SPECPATH)
block_cipher = None

a = Analysis(['../Gravity_Engine.py'],
             pathex=['spec_root'],
             datas=[('../*.py', '.'),('../Gravity_Maths/*.py', './Gravity_Maths'),('../*.kv', '.')],
             hookspath=hookspath(),
             runtime_hooks=runtime_hooks(),
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False,
             **get_deps_minimal(video=None, audio=None))

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='gravity',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=True)
          
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=False,
               upx_exclude=[],
               name='gravity')