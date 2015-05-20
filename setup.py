import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os"],
    "excludes": ["tkinter"],
    "include_msvcr": True,
    "include_files": [
        "copy_win/libEGL.dll",
        "copy_win/libGLESv2.dll",
        "controlers.db",
    ]
}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="IntielIPMultithermostat",
    version="1.0",
    description="Intiel IP Multithermostat Control Panel",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "main.py",
            base=base,
            targetName="IntielIPMTCP.exe"
        )
    ]
)
