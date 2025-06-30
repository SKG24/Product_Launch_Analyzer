import os

def create_directories():
    """Create all necessary project directories"""
    print("  Creating Project Directories")
    print("=" * 30)
    
    directories = [
        'data',
        'logs', 
        'src',
        'tests',
        'scripts',
        'utility_scripts',
        'docs',
        'fallback_data'
    ]
    
    created = 0
    existed = 0
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"  Created: {directory}/")
            created += 1
        else:
            print(f"  Exists: {directory}/")
            existed += 1
    
    print(f"\n  Summary:")
    print(f"   Created: {created} directories")
    print(f"   Already existed: {existed} directories")
    print(f"   Total: {created + existed} directories")
    
    return True

def create_init_files():
    """Create __init__.py files for Python packages"""
    print(f"\n  Creating Package Files")
    print("=" * 30)
    
    init_files = [
        'src/__init__.py',
        'tests/__init__.py'
    ]
    
    for init_file in init_files:
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write("# This file makes the directory a Python package\n")
            print(f"  Created: {init_file}")
        else:
            print(f"  Exists: {init_file}")

def main():
    print("  Project Directory Setup")
    print("=" * 40)
    
    # Create directories
    create_directories()
    
    # Create __init__.py files
    create_init_files()
    
    print(f"\n  Setup Complete!")
    print("Now you can run any script without directory errors.")

if __name__ == "__main__":
    main()