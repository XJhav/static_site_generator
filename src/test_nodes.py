from typing import Text
import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)


    def test_noteq(self):
        node = TextNode("This is also text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertNotEqual(node, node2)

    def test_noteq2(self):
        node = TextNode("This is a text node", TextType.IMAGE, "cool.com")
        node2 = TextNode("This is a text node", TextType.IMAGE, "uncool.com")
        self.assertNotEqual(node, node2)

    def test_text1(self):
        node = TextNode("This is a text node", TextType.PLAIN_TEXT)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text2(self):
        node = TextNode("This is an image text node", TextType.IMAGE, "cool.com")
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props_to_html(), 'src="cool.com" alt="This is an image text node"')

    def text_delimiter_split1(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN_TEXT)
        new_nodes = TextNode.split_nodes_delimiter([node], "`", TextType.CODE_TEXT)

        self.assertEqual([
            TextNode("This is text with a ", TextType.PLAIN_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" word", TextType.PLAIN_TEXT),
            ], new_nodes)

    def text_delimiter_split2(self):
        node = TextNode("This is text with anoter _italic word_", TextType.PLAIN_TEXT)
        new_nodes = TextNode.split_nodes_delimiter([node], "_", TextType.ITALIC_TEXT)

        expected: list[TextNode] = [TextNode("This is text with another ", TextType.PLAIN_TEXT), TextNode("italic block", TextType.ITALIC_TEXT), TextNode("", TextType.PLAIN_TEXT)]

        self.assertEqual([
            TextNode("This is text with a ", TextType.PLAIN_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" word", TextType.PLAIN_TEXT),
            ], new_nodes)



class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        html_node = HTMLNode(props = {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(html_node.props_to_html(), 'href="https://www.google.com" target="_blank"')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Hello, world!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Hello, world!</a>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()

