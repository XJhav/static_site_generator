from enum import Enum
from pydoc import text
from typing import override
from htmlnode import HTMLNode, LeafNode
from regexing import extract_markdown_images, extract_markdown_links

class TextType(Enum):
    PLAIN_TEXT = "plain"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text: str = text
        self.text_type: TextType = text_type
        self.url: str | None = url

    @override
    def __eq__(self, value: object, /) -> bool:
        if type(value) != TextNode:
            return False
        return self.text == value.text and self.text_type == value.text_type and self.url == value.url

    @override
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

    def to_html_node(self) -> HTMLNode:
        match self.text_type:
            case TextType.PLAIN_TEXT:
                return LeafNode(None, self.text)
            case TextType.BOLD_TEXT:
                return LeafNode("b", self.text)
            case TextType.ITALIC_TEXT:
                return LeafNode("i", self.text)
            case TextType.CODE_TEXT:
                return LeafNode("code", self.text)
            case TextType.LINK:
                return LeafNode("a", self.text, {"href": self.url})
            case TextType.IMAGE:
                return LeafNode("img", "", {"src": self.url, "alt": self.text})

    @staticmethod
    def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
        node_list: list[TextNode] = []

        for node in old_nodes:
            if node.text_type != TextType.PLAIN_TEXT:
                node_list.append(node)
                continue

            split_text = node.text.split(delimiter)
            node_list_extension = list(map(lambda data: TextNode(data[1], text_type if data[0] % 2 == 1 else TextType.PLAIN_TEXT), enumerate(split_text)))

            if node_list_extension[-1].text == "":
                _ = node_list_extension.pop()
            if len(node_list_extension) <= 0:
                continue
            if node_list_extension[0].text == "":
                _ = node_list_extension.pop(0)
            
            node_list.extend(node_list_extension)


        return node_list

    @staticmethod
    def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
        node_list: list[TextNode] = []

        for node in old_nodes:
            if node.text_type != TextType.PLAIN_TEXT:
                node_list.append(node)
                continue

            images = extract_markdown_images(node.text)
            current_split_text_nodes = [TextNode(node.text, TextType.PLAIN_TEXT)]

            for image in images:
                current_text = current_split_text_nodes.pop().text
                image_str = f"![{image[0]}]({image[1]})"

                split_text_list = current_text.split(image_str)
                current_split_text_nodes += [TextNode(split_text_list[0], TextType.PLAIN_TEXT),
                                     TextNode(image[0], TextType.IMAGE, image[1]),
                                     TextNode(split_text_list[1], TextType.PLAIN_TEXT)]

            if current_split_text_nodes[-1].text == "":
                _ = current_split_text_nodes.pop()
            if current_split_text_nodes[0].text == "":
                _ = current_split_text_nodes.pop(0)

            node_list += current_split_text_nodes

        return node_list

    @staticmethod
    def split_nodes_links(old_nodes: list[TextNode]) -> list[TextNode]:
        node_list: list[TextNode] = []

        for node in old_nodes:
            if node.text_type != TextType.PLAIN_TEXT:
                node_list.append(node)
                continue

            links = extract_markdown_links(node.text)
            current_split_text_nodes = [TextNode(node.text, TextType.PLAIN_TEXT)]

            for link in links:
                current_text = current_split_text_nodes.pop().text
                link_str = f"[{link[0]}]({link[1]})"

                split_text_list = current_text.split(link_str)
                current_split_text_nodes += [TextNode(split_text_list[0], TextType.PLAIN_TEXT),
                                     TextNode(link[0], TextType.LINK, link[1]),
                                     TextNode(split_text_list[1], TextType.PLAIN_TEXT)]

            if current_split_text_nodes[-1].text == "":
                _ = current_split_text_nodes.pop()
            if current_split_text_nodes[0].text == "":
                _ = current_split_text_nodes.pop(0)

            node_list += current_split_text_nodes

        return node_list

    @staticmethod
    def nodes_from_text(text: str) -> list[TextNode]:
        text = strip_and_replace_newlines(text)
        nodes = [TextNode(text, TextType.PLAIN_TEXT)]

        # Add Links and Images
        nodes = TextNode.split_nodes_image(
            TextNode.split_nodes_links(
                nodes
            )
        )

        # Add Code
        nodes = TextNode.split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
        # Add Bold
        nodes = TextNode.split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
        # Add Italics
        nodes = TextNode.split_nodes_delimiter(nodes, "_", TextType.ITALIC_TEXT)

        return nodes

def strip_and_replace_newlines(text: str) -> str:
    return " ".join(filter(lambda s: s.strip() != "", map(lambda s: s.strip(), text.splitlines())))



