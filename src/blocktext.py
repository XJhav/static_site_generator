from enum import Enum
import re

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, strip_and_replace_newlines

def markdown_to_blocks(md: str) -> list[str]:
    return list(filter(lambda s: s != "", map(lambda s: s.strip(), md.split("\n\n"))))

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block: str) -> BlockType:
    if re.search(r"^#{1,6} ", block):
        return BlockType.HEADING
    elif re.search(r"^```[\s\S]*```$", block):
        return BlockType.CODE
    elif re.search(r"^> ", block):
        return BlockType.QUOTE
    elif re.search(r"^(?:- .*(?:\n|$))+$", block):
        return BlockType.UNORDERED_LIST
    
    ordered_list: bool = True
    for i, line in enumerate(block.splitlines(), start = 1):
        if not line.startswith(f"{i}. "):
            ordered_list = False

    if ordered_list:
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def markdown_to_html_node(md: str)-> HTMLNode:
    blocks: list[str] = markdown_to_blocks(md)

    final_node: ParentNode = ParentNode("div", [])

    for block in blocks:
        current_node: ParentNode = ParentNode("", [])

        block_type = block_to_block_type(block)

        match block_type.value:
            case "paragraph":
                current_node.tag = "p"

            case "heading":
                hash_count = 0
                while block[0] == "#":
                    hash_count += 1
                    block = block[1:]

                block = block.strip()
                current_node.tag = f"h{hash_count}"

            case "unordered_list":
                current_node.tag = "ul"

                block = "".join(map(lambda s: "<li>" + s[2:].strip() + "</li>", block.splitlines()))

            case "ordered_list":
                current_node.tag = "ol"

                block = "".join(map(lambda s: "<li>" + s[3:].strip() + "</li>", block.splitlines()))

            case "quote":
                current_node.tag = "blockquote"
                block = block[2:].strip()

            case "code":
                current_node.tag = "pre"
                block = "\n".join(filter(lambda s: s, map(lambda s: s.rstrip(), block[3:-3].splitlines())))
                _ = current_node.add_child(LeafNode("code", block))
                _ = final_node.add_child(current_node)
                continue

        current_node.children = list(map(lambda node: node.to_html_node(), TextNode.nodes_from_text(block)))
        _ = final_node.add_child(current_node)

    return final_node
