import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Use "Win32GUI" para aplicativos GUI do Windows

executables = [Executable(
    "Cme.py",
    base=base,
    icon="C:/Users/carva/OneDrive/Docs/Day Trade/Sistema_Quant/Versões/Python/Cme.ico",
    
)]

options = {
    "build_exe": {
        # "packages": ["sua_biblioteca"],  # Adicione bibliotecas adicionais que seu script usa
    },
}

setup(
    name="Trava CMe",
    version="1.0",
    description="Trava CME by @Nztquant feat Daniel",
    executables=executables,
    options=options,
)
