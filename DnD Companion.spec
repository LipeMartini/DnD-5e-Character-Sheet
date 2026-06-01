# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('data', 'data')],
    hiddenimports=['h11', 'h11._readers', 'h11._writers', 'h11._connection', 'h11._events', 'httpx', 'httpx._transports.default', 'httpx._transports.asgi', 'httpcore', 'httpcore._async.http11', 'httpcore._sync.http11', 'certifi', 'anyio', 'anyio._backends._asyncio', 'sniffio', 'supabase', 'supabase_auth', 'supabase_auth._async.client', 'supabase_auth._sync.client', 'postgrest', 'realtime', 'storage3', 'websockets', 'websockets.legacy.client', 'pydantic', 'pyjwt', 'strenum', 'yarl'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='DnD Companion',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
