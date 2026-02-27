"""
System Check Script - Verify all requirements before running analysis
"""

import sys

def check_python_version():
    """Check if Python version is 3.7 or higher"""
    print("Checking Python version...")
    version = sys.version_info
    print(f"  Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 7:
        print("  ✓ Python version is compatible")
        return True
    else:
        print("  ✗ Python 3.7 or higher is required")
        return False

def check_packages():
    """Check if all required packages are installed"""
    print("\nChecking required packages...")
    
    required_packages = {
        'pandas': 'pandas',
        'numpy': 'numpy',
        'matplotlib': 'matplotlib',
        'seaborn': 'seaborn',
        'sklearn': 'scikit-learn',
        'xgboost': 'xgboost',
        'PyPDF2': 'PyPDF2'
    }
    
    missing = []
    
    for import_name, package_name in required_packages.items():
        try:
            __import__(import_name)
            print(f"  ✓ {package_name}")
        except ImportError:
            print(f"  ✗ {package_name} - NOT INSTALLED")
            missing.append(package_name)
    
    return len(missing) == 0, missing

def check_dataset():
    """Check if dataset file exists"""
    print("\nChecking dataset file...")
    import os
    
    if os.path.exists('Student_Depression_Dataset.csv'):
        print("  ✓ Student_Depression_Dataset.csv found")
        
        # Check file size
        size = os.path.getsize('Student_Depression_Dataset.csv')
        print(f"  ✓ File size: {size:,} bytes")
        return True
    else:
        print("  ✗ Student_Depression_Dataset.csv NOT FOUND")
        print("    Please ensure the dataset file is in the same directory")
        return False

def main():
    print("=" * 80)
    print("STUDENT DEPRESSION ANALYSIS SYSTEM - REQUIREMENTS CHECK")
    print("=" * 80)
    
    all_good = True
    
    # Check Python version
    if not check_python_version():
        all_good = False
    
    # Check packages
    packages_ok, missing = check_packages()
    if not packages_ok:
        all_good = False
        print("\n" + "!" * 80)
        print("MISSING PACKAGES DETECTED")
        print("!" * 80)
        print("\nTo install missing packages, run:")
        print("  pip install -r requirements.txt")
        print("\nOr install individually:")
        for pkg in missing:
            print(f"  pip install {pkg}")
    
    # Check dataset
    if not check_dataset():
        all_good = False
    
    # Final verdict
    print("\n" + "=" * 80)
    if all_good:
        print("✅ ALL REQUIREMENTS MET - READY TO RUN!")
        print("=" * 80)
        print("\nYou can now run the analysis:")
        print("  python depression_analysis.py")
        print("\nOr use the automated script:")
        print("  Double-click run_analysis.bat")
    else:
        print("❌ SOME REQUIREMENTS NOT MET")
        print("=" * 80)
        print("\nPlease fix the issues above before running the analysis.")
    
    print("=" * 80)
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
