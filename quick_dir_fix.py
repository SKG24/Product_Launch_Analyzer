import os

# Create all necessary directories
dirs = ['data', 'logs', 'src', 'tests', 'scripts', 'utility_scripts']
for d in dirs:
    os.makedirs(d, exist_ok=True)
    print(f" {d}/")

# Create __init__.py files
init_files = ['src/__init__.py', 'tests/__init__.py']
for f in init_files:
    if not os.path.exists(f):
        open(f, 'w').write("# Package file\n")
        print(f" {f}")

print(" All directories ready! Now you can run any script.")