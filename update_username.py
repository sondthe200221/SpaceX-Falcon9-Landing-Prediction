import os
import subprocess

base = r'C:\Users\Do Truong Son\Desktop\IBM_SpaceX_Capstone'

gen_path = os.path.join(base, 'generate_capstone.py')
with open(gen_path, 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace('your-username', 'sondthe200221')

with open(gen_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("generate_capstone.py updated with sondthe200221")

# Regenerate PPTX
subprocess.run(['python', os.path.join(base, 'generate_capstone.py')], cwd=base, check=True)

# Regenerate PDF
subprocess.run(['python', os.path.join(base, 'convert_to_pdf.py')], cwd=base, check=True)

# Git commit and push
subprocess.run(['git', 'commit', '-am', 'Update links to https://github.com/sondthe200221/SpaceX-Falcon9-Landing-Prediction'], cwd=base, check=True)
subprocess.run(['git', 'push', 'origin', 'main'], cwd=base, check=True)

print("Successfully updated and pushed to GitHub!")
