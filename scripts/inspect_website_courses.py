import glob, os

files = glob.glob('apps/website/src/**/courses/**/*', recursive=True)
for f in files:
    if os.path.isfile(f) and f.endswith(('.tsx', '.ts')):
        print(f)
