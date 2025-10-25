# -*- mode: python ; coding: utf-8 -*-
# Full standalone build with all dependencies

import sys
from PyInstaller.utils.hooks import collect_all, collect_submodules

# Collect all submodules for packages
selenium_imports = collect_submodules('selenium')
urllib3_imports = collect_submodules('urllib3')
certifi_imports = collect_submodules('certifi')
charset_normalizer_imports = collect_submodules('charset_normalizer')
idna_imports = collect_submodules('idna')
cryptography_imports = collect_submodules('cryptography')

# Collect all data files
selenium_datas, selenium_binaries, selenium_hiddenimports = collect_all('selenium')
urllib3_datas, urllib3_binaries, urllib3_hiddenimports = collect_all('urllib3')
certifi_datas, certifi_binaries, certifi_hiddenimports = collect_all('certifi')

# All hidden imports
hiddenimports = [
    # Selenium
    'selenium',
    'selenium.webdriver',
    'selenium.webdriver.chrome',
    'selenium.webdriver.chrome.service',
    'selenium.webdriver.chrome.options',
    'selenium.webdriver.common',
    'selenium.webdriver.common.by',
    'selenium.webdriver.common.keys',
    'selenium.webdriver.support',
    'selenium.webdriver.support.ui',
    'selenium.webdriver.support.expected_conditions',
    'selenium.webdriver.remote',
    'selenium.webdriver.remote.webdriver',
    'selenium.common',
    'selenium.common.exceptions',

    # Requests and HTTP
    'requests',
    'requests.adapters',
    'requests.auth',
    'requests.cookies',
    'requests.exceptions',
    'requests.models',
    'requests.sessions',
    'requests.structures',
    'requests.utils',
    'urllib3',
    'urllib3.util',
    'urllib3.util.ssl_',
    'urllib3.util.retry',
    'urllib3.connection',
    'urllib3.connectionpool',
    'urllib3.poolmanager',
    'urllib3.response',
    'urllib3.exceptions',
    'urllib3.contrib',
    'urllib3.contrib.pyopenssl',

    # SSL/TLS
    'ssl',
    'certifi',
    'certifi.core',

    # Encoding
    'charset_normalizer',
    'idna',
    'idna.core',
    'idna.idnadata',

    # Cryptography
    'cryptography',
    'cryptography.fernet',
    'cryptography.hazmat',
    'cryptography.hazmat.primitives',
    'cryptography.hazmat.backends',
    'cryptography.hazmat.backends.openssl',

    # Tkinter
    'tkinter',
    'tkinter.ttk',
    'tkinter.font',
    'tkinter.messagebox',
    'tkinter.filedialog',
    '_tkinter',

    # Standard library
    'subprocess',
    'threading',
    'json',
    're',
    'os',
    'sys',
    'time',
    'datetime',
    'hashlib',
    'base64',
    'uuid',
    'pathlib',
    'shutil',
    'glob',
    'tempfile',

    # Windows specific
    'winreg',
    'ctypes',
    'ctypes.wintypes',

    # XML (for Selenium)
    'xml',
    'xml.etree',
    'xml.etree.ElementTree',

    # HTTP parsing
    'http',
    'http.client',
    'http.cookies',

    # URL parsing
    'urllib',
    'urllib.parse',
    'urllib.request',
    'urllib.error',

    # Sockets
    'socket',
    'socketserver',

    # Collections
    'collections',
    'collections.abc',

    # IO
    'io',
    'io.BytesIO',

    # Logging
    'logging',
    'logging.handlers',

    # Platform
    'platform',

    # Queue
    'queue',

    # Warnings
    'warnings',

    # Weakref
    'weakref',

    # Copy
    'copy',

    # Functools
    'functools',

    # Itertools
    'itertools',

    # Typing
    'typing',
    'typing_extensions',
]

# Add collected imports
hiddenimports.extend(selenium_imports)
hiddenimports.extend(urllib3_imports)
hiddenimports.extend(certifi_imports)
hiddenimports.extend(charset_normalizer_imports)
hiddenimports.extend(idna_imports)
hiddenimports.extend(cryptography_imports)
hiddenimports.extend(selenium_hiddenimports)
hiddenimports.extend(urllib3_hiddenimports)
hiddenimports.extend(certifi_hiddenimports)

# Remove duplicates
hiddenimports = list(set(hiddenimports))

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=selenium_binaries + urllib3_binaries + certifi_binaries,
    datas=[
        ('controller', 'controller'),
        ('common', 'common')
    ] + selenium_datas + urllib3_datas + certifi_datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'PIL',
        'PyQt5',
        'PyQt6',
        'PySide2',
        'PySide6',
        'wx',
        'setuptools',
        'pkg_resources',
    ],
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
    name='VideoDownloader',
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
    icon='icon.ico',
)
