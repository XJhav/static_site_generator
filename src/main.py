from textnode import TextNode, TextType

def main() -> None:
    node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.PLAIN_TEXT,
    )
    new_nodes = TextNode.split_nodes_image([node])
    print(new_nodes)

main()
