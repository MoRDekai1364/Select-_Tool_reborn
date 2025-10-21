#!/usr/bin/env python3
"""
Precompile Python modules for faster startup.
Run this script after making changes to the main SelectPlus script.
"""

import py_compile
import os
import sys

def precompile_modules():
    """Precompile Python modules to bytecode for faster loading."""
    
    src_dir = os.path.join(os.path.dirname(__file__), '..', 'src')
    main_script = os.path.join(src_dir, 'SelectPlus_V3.3.py')
    
    if not os.path.exists(main_script):
        print(f"Error: Main script not found at {main_script}")
        return False
    
    try:
        print("Precompiling SelectPlus modules...")
        
        # Compile main script
        py_compile.compile(main_script, doraise=True, optimize=2)
        print(f"✅ Compiled: {main_script}")
        
        # Compile any other Python files in src directory
        for filename in os.listdir(src_dir):
            if filename.endswith('.py') and filename != 'SelectPlus_V3.3.py':
                filepath = os.path.join(src_dir, filename)
                try:
                    py_compile.compile(filepath, doraise=True, optimize=2) 
                    print(f"✅ Compiled: {filepath}")
                except Exception as e:
                    print(f"⚠️ Could not compile {filepath}: {e}")
        
        print("\n✅ Precompilation completed successfully!")
        print("The optimized startup should now be faster.")
        return True
        
    except Exception as e:
        print(f"❌ Error during precompilation: {e}")
        return False

if __name__ == "__main__":
    success = precompile_modules()
    if not success:
        sys.exit(1)
    
    input("\nPress Enter to continue...")
