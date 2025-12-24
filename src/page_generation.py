from pathlib import Path
from typing import final
from blocktext import markdown_to_html_node
import os

def extract_title(md: str) -> str:
    for line in md.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No title found")

def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    from_content: str
    template_content: str

    with open(from_path, "r") as f:
        from_content = f.read()
    with open(template_path, "r") as f:
        template_content = f.read()

    title = extract_title(from_content)
    from_content_html = markdown_to_html_node(from_content).to_html()

    final_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", from_content_html)

    with open(dest_path, "w") as dest_file:
        _ = dest_file.write(final_html)


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):
    for path in os.listdir(dir_path_content):
        print(path)
        if os.path.isdir(dir_path_content + "/" + path):
            os.mkdir(dest_dir_path + "/" + path)
            generate_pages_recursive(dir_path_content + "/" + path, template_path, dest_dir_path + "/" + path)
        elif os.path.splitext(path)[1] == ".md":
            generate_page(dir_path_content + "/" + path, template_path, dest_dir_path + "/" + os.path.splitext(path)[0] + ".html")


