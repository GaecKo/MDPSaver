import os
import shutil
import pathlib

# get repository path
repo_path = pathlib.Path(__file__).parent.absolute()

# PPG archive path
ppg_archive_path = repo_path / "requirements" / "PPG-main.zip"

# get virtual environment folder name
venv_folder_name = os.environ.get("VIRTUAL_ENV").split(os.sep)[-1]

# PPG extract path
ppg_extract_path = repo_path / "requirements" / "PPG"

# extract PPG
shutil.unpack_archive(str(ppg_archive_path), str(ppg_extract_path))

# copy PPG to site-packages directory
shutil.copytree(ppg_extract_path / "PPG-main" / "ppg" , repo_path / venv_folder_name / "lib" / "site-packages" / "ppg", dirs_exist_ok=True)
shutil.copytree(ppg_extract_path / "PPG-main" / "ppg_runtime" , repo_path / venv_folder_name / "lib" / "site-packages" / "ppg_runtime", dirs_exist_ok=True)
shutil.copytree(ppg_extract_path / "PPG-main", repo_path / venv_folder_name / "lib" / "site-packages" / "PPG", dirs_exist_ok=True)

# run setup.py
os.system(f"python {repo_path / venv_folder_name / 'lib' / 'site-packages' / 'PPG' / 'setup.py'} install")

# remove PPG extract
shutil.rmtree(ppg_extract_path)

# install other dependencies
os.system(f"python -m pip install -r {repo_path / 'requirements' / 'requirements.txt'}")


