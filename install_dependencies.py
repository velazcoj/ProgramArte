import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

packages = ["Pillow", "fireworks-python-client", "matplotlib", "requests"]

for package in packages:
    install(package)

print("Instalación completa.")
