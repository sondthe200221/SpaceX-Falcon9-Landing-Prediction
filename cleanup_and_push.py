import os
import shutil
import subprocess

base = r'C:\Users\Do Truong Son\Desktop\IBM_SpaceX_Capstone'
nested = os.path.join(base, 'IBM_SpaceX_Capstone')

if os.path.exists(nested):
    for item in os.listdir(nested):
        s = os.path.join(nested, item)
        d = os.path.join(base, item)
        if os.path.isdir(s):
            if os.path.exists(d):
                shutil.rmtree(d)
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)
    shutil.rmtree(nested)
    print("Nested folder cleaned up.")

# Git add, commit, push
subprocess.run(['git', 'add', '.'], cwd=base, check=True)
res = subprocess.run(['git', 'status', '--porcelain'], cwd=base, capture_output=True, text=True)
if res.stdout.strip():
    subprocess.run(['git', 'commit', '-m', 'Clean up directory structure and finalize deliverables'], cwd=base, check=True)
    subprocess.run(['git', 'push', 'origin', 'main'], cwd=base, check=True)
    print("Changes committed and pushed.")
else:
    print("Working tree clean, everything up to date.")
