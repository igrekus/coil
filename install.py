import subprocess

subprocess.run(['pyinstaller', '--onedir', 'coil.py', '--clean'])
