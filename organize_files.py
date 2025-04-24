import os
import shutil

def organize_files():
    # Create directories if they don't exist
    os.makedirs('analysis_results/elasonggur', exist_ok=True)
    os.makedirs('analysis_results/nasa', exist_ok=True)
    os.makedirs('analysis_results/comparison', exist_ok=True)
    
    # Move files for elasonggur
    for file in os.listdir('.'):
        if file.endswith('_elasonggur.png'):
            shutil.move(file, f'analysis_results/elasonggur/{file.replace("_elasonggur", "")}')
        elif file.endswith('_nasa.png'):
            shutil.move(file, f'analysis_results/nasa/{file.replace("_nasa", "")}')
    
    # Move comparison files
    comparison_files = ['account_comparison.png']
    for file in comparison_files:
        if os.path.exists(file):
            shutil.move(file, f'analysis_results/comparison/{file}')
    
    # Move any remaining analysis files to appropriate folders
    for file in os.listdir('.'):
        if file.endswith('.png') and not any(x in file for x in ['_elasonggur', '_nasa']):
            if 'comparison' in file:
                shutil.move(file, f'analysis_results/comparison/{file}')
            else:
                # These are general analysis files, we'll keep them in both folders
                shutil.copy(file, f'analysis_results/elasonggur/{file}')
                shutil.copy(file, f'analysis_results/nasa/{file}')
                os.remove(file)

if __name__ == "__main__":
    organize_files()
    print("Files have been organized into the analysis_results directory.") 