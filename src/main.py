import sys
from statics import copy_static_to_dir
from page_generation import generate_page, generate_pages_recursive

def main() -> None:
    print(sys.argv)
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    if not basepath.startswith("/"): 
        basepath = "/" + basepath
    if not basepath.endswith("/"): 
        basepath += "/"

    target_path = "docs"

    copy_static_to_dir(target_path)
    generate_pages_recursive("content", "template.html", target_path, basepath)
    
main()
