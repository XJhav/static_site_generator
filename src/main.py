from statics import copy_static_to_public
from page_generation import generate_page, generate_pages_recursive

def main() -> None:
    copy_static_to_public()
    generate_pages_recursive("content", "template.html", "public")
    
main()
