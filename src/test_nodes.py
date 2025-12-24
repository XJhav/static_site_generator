import code
from shlex import quote
from turtle import heading
from typing import Text
import unittest

from regexing import extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from blocktext import markdown_to_blocks, block_to_block_type, markdown_to_html_node

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

    def test_delimiter_split1(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN_TEXT)
        new_nodes = TextNode.split_nodes_delimiter([node], "`", TextType.CODE_TEXT)

        self.assertEqual([
            TextNode("This is text with a ", TextType.PLAIN_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" word", TextType.PLAIN_TEXT),
            ], new_nodes)

    def test_delimiter_split2(self):
        node = TextNode("This is text with another _italic word_", TextType.PLAIN_TEXT)
        new_nodes = TextNode.split_nodes_delimiter([node], "_", TextType.ITALIC_TEXT)

        expected: list[TextNode] = [TextNode("This is text with another ", TextType.PLAIN_TEXT), TextNode("italic word", TextType.ITALIC_TEXT)]

        self.assertEqual(expected, new_nodes)

    def test_markdown_image_extraction(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_markdown_link_extraction(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])
        
    def test_extract_markdown_images_and_links(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png), and two links: [link1](cool.com), [link2](cool2.com)"
        image_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], image_matches)
        self.assertListEqual([("link1", "cool.com"), ("link2", "cool2.com")], link_matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = TextNode.split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN_TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png) and [link2](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = TextNode.split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and ", TextType.PLAIN_TEXT),
                TextNode(
                    "link2", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_double_split(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png) and ![image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = TextNode.split_nodes_image(TextNode.split_nodes_links([node]))
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and ", TextType.PLAIN_TEXT),
                TextNode(
                    "image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_nodes_from_text(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("text", TextType.BOLD_TEXT),
            TextNode(" with an ", TextType.PLAIN_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" word and a ", TextType.PLAIN_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" and an ", TextType.PLAIN_TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        self.assertListEqual(TextNode.nodes_from_text(text), expected)

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

class TestBlockText(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type(self):
        unordered1 = "- Item1\n- Item2    \n- Item3"
        ordered1 = "1. Item1\n2. Item2     \n3. Item3"
        code1 = "```java\npublic static void main(String[] args) {\n\tSystem.out.println(\"Hello\")\n}```"
        quote1 = "> \"This is a quote\""
        heading1 = "# Heading1"
        heading2 = "#### Heading2"
        p1 = "-Item1\n-Item2"
        p2 = "1. Item1\n2. Item2\n1. Item3"
        p3 = ">Not a quote"
        p4 = "####### 7 Hashtaghs"
        p5 = "#1 Paragraph"
        p6 = "1.Item1\n2.Item2"

        block_list = [unordered1, ordered1, code1, quote1, heading1, heading2, p1, p2, p3, p4, p5, p6]
        expected = ["unordered_list", "ordered_list", "code", "quote", "heading", "heading", "paragraph", "paragraph", "paragraph", "paragraph", "paragraph", "paragraph"]

        self.assertListEqual(list(map(lambda s: block_to_block_type(s).value, block_list)), expected)

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
This is text that _should_ remain\nthe **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )

    def test_ordered_list(self):
        md = """1. Item1
2. Item2
3. Item3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
         "<div><ol><li>Item1</li><li>Item2</li><li>Item3</li></ol></div>"
        )

    def test_unordered_list(self):
        md = """- Item1
- Item2
- Item3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
        "<div><ul><li>Item1</li><li>Item2</li><li>Item3</li></ul></div>"
        )

    def test_quote(self):
        md = """This is regular text

> This is a quote

This is more regular text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
        "<div><p>This is regular text</p><blockquote>This is a quote</blockquote><p>This is more regular text</p></div>"
        )

    def test_headers(self):
        md = """# Title

## Header

####### Just Regular Text?
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
        "<div><h1>Title</h1><h2>Header</h2><p>####### Just Regular Text?</p></div>"
        )

if __name__ == "__main__":
    _ = unittest.main()

