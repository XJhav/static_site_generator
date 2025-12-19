from enum import Enum
from typing import override
from htmlnode import HTMLNode, LeafNode

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

def main() -> None:
    my_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(my_node)
