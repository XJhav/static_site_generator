import shutil
import os

def copy_static_to_dir(target_dir: str):
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    _ = shutil.copytree("static", target_dir)
