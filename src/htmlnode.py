from typing import Any, override
import unittest


class HTMLNode:
    def __init__(self, tag: str | None = None, value: str | None = None, children: list[HTMLNode] | None = [], props: dict[str, Any] = {}) -> None:
        self.tag: str | None = tag
        self.value: str | None = value
        self.children: list[HTMLNode] | None = children
        self.props: dict[str, Any] = props

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self):
        return " ".join(map(lambda key: f"{key}=\"{self.props[key]}\"", self.props.keys()))

    @override
    def __repr__(self) -> str:
        return f'HTMLNode(\n\tTag: {self.tag}\n\tValue: {self.value}\n\tChildren: {self.children}\n\t Properties: {self.props}\n)'


class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict[str, Any] = {}) -> None:
        super().__init__(tag, value, None, props)
    
    @override
    def to_html(self) -> str:
        return f'<{self.tag}{"" if not self.props else " "}{self.props_to_html()}>{self.value}</{self.tag}>'


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, Any] = {}) -> None:
        super().__init__(tag, None, children, props)

    @override
    def to_html(self) -> str:
        if self.tag == None:
            raise ValueError("No Tag Found in ParentNode")
        elif not self.children:
            raise ValueError("No Children in ParentNode")
        return f'<{self.tag}{"" if not self.props else " "}{self.props_to_html()}>{"".join(map(lambda child: child.to_html(), self.children))}</{self.tag}>'


