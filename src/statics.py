import shutil
import os

def copy_static_to_public():
    if os.path.exists("public/"):
        shutil.rmtree("public/")
    _ = shutil.copytree("static/", "public/")
