from collections import defaultdict
import subprocess
from rich.console import Console
from rich.table import Table
from rich.logging import RichHandler
import logging
import spacy
from anytree import Node, RenderTree, NodeMixin
from collections import defaultdict
from nltk.parse.chart import ChartParser
import nltk
from nltk import CFG
from anytree.exporter import UniqueDotExporter

console = Console()
logging.basicConfig(level=logging.INFO, format="%(message)s", handlers=[RichHandler()])
logger = logging.getLogger("rich")
nlp = spacy.load("en_core_web_sm")


def print_dictionary(list):
    # table = Table(show_header=True, header_style="bold cyan")

    # # Dynamically add columns from the first dictionary's keys
    # for key in list[0].keys():
    #     table.add_column(key)

    # # Add rows
    # for item in list:
    #     table.add_row(*[str(item[key]) for key in item])
    table = Table(title="Lexeme Table", show_lines=True)

    # Add columns to the table
    table.add_column("Token", justify="center", style="cyan", no_wrap=True)
    table.add_column("Lexeme", justify="center", style="magenta", no_wrap=True)

    # Populate the table with data
    for entry in list:
        table.add_row(entry["token"], entry["lexeme"])

    return table


class Helpers:
    def delay(self):
        trigger = input("\n \n Enter N to continue \n \n ")
        while True:
            if trigger == "n" or "N":
                break

    from anytree import Node

    def nltk_tree_to_anytree(self, nltk_tree, parent=None):
        node = Node(nltk_tree.label(), parent=parent)
        for child in nltk_tree:
            if isinstance(child, str):
                # Leaf node (token)
                Node(child, parent=node)
            else:
                Helpers.nltk_tree_to_anytree(child, parent=node)
        return node

    # Use the first parse tree (if exists)
    trees = list(parser.parse(sentence))
    if trees:
        root = nltk_tree_to_anytree(trees[0])
    else:
        root = None

    # def verb_phrase_formatting(self, lexical_table):
    #     # root = Node("S")
    #     # print(lexical_table)
    #     starting_symbol = []
    #     terminals = []
    #     non_terminals = []
    #     for i in range(len(lexical_table)):
    #         # starting_symbol = starting_symbol + lexical_table[i]["lexeme"] + " "
    #         starting_symbol.append(lexical_table[i]["lexeme"])
    #         terminals.append(lexical_table[i]["lexeme"])
    #         non_terminals.append(lexical_table[i]["token"])
    #     print(starting_symbol)
    #     print(terminals)
    #     print(non_terminals)


class Compiler:
    def __init__(self, starting_statement):
        self.starting_statement = starting_statement

    def lexical_analysis(self, starting_statement):
        alphabets = [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "o",
            "p",
            "q",
            "r",
            "s",
            "t",
            "u",
            "v",
            "w",
            "x",
            "y",
            "z",
        ]
        punctuation_symbol_table = {
            ".": "<PERIOD>",
            ",": "<COMMA>",
            "!": "<EXCLAMATION MARK>",
            "?": "<QUESTION MARK>",
            ":": "<COLON>",
            ";": "<SEMICOLON>",
            "'": "<APOSTROPHE>",
            '"': "<QUOTATION MARK>",
            "-": "<HYPHEN>",
            "_": "<UNDERSCORE>",
            "(": "<LEFT PARENTHESIS>",
            ")": "<RIGHT PARENTHESIS>",
            "[": "<LEFT BRACKET>",
            "]": "<RIGHT BRACKET>",
            "{": "<LEFT BRACE>",
            "}": "<RIGHT BRACE>",
            "/": "<SLASH>",
            "\\": "<BACKSLASH>",
            "@": "<AT SYMBOL>",
            "#": "<HASH>",
            "$": "<DOLLAR SIGN>",
            "%": "<PERCENT>",
            "^": "<CARET>",
            "&": "<AMPERSAND>",
            "*": "<ASTERISK>",
            "+": "<PLUS>",
            "=": "<EQUALS>",
            "<": "<LESS THAN>",
            ">": "<GREATER THAN>",
            "`": "<BACKTICK>",
            "~": "<TILDE>",
            "|": "<VERTICAL BAR>",
        }
        current_str_token = ""
        lexical_table = []
        for i in range(len(starting_statement)):
            if starting_statement[i] in punctuation_symbol_table:
                lexical_table.append(
                    {
                        "token": starting_statement[i],
                        "lexeme": punctuation_symbol_table[starting_statement[i]],
                    }
                )
            elif starting_statement[i] == " ":
                pass
            else:
                current_str_token = current_str_token + starting_statement[i]
                if not (starting_statement[i + 1] in alphabets):
                    # tokens = nltk.word_tokenize(current_str_token)
                    # pos = nltk.pos_tag(tokens)
                    # Load the English model

                    # Process a word (or sentence)
                    doc = nlp(current_str_token)

                    pos_tags = [token.pos_ for token in doc]
                    lexical_table.append(
                        {
                            "token": current_str_token,
                            "lexeme": f"<{pos_tags[0]}>",
                        }
                    )

                    current_str_token = ""
        logger.info(print_dictionary(lexical_table))
        console.print(print_dictionary(lexical_table))
        return lexical_table

    def syntax_analysis(self, lexical_table):

        root = Node("S")
        # for i in range(len(starting_symbol)):
        #     Node(starting_symbol[i], parent=root)
        for i in range(len(lexical_table)):
            parent_node = Node(lexical_table[i]["lexeme"], parent=root)
            Node(lexical_table[i]["token"], parent=parent_node)

        for pre, fill, node in RenderTree(root):
            print(f"{pre}{node.name}")

        exporter = UniqueDotExporter(
            root,
            graph="digraph",
            name="tree",
        )
        exporter.to_dotfile("syntax_tree.dot")  # Save to a known location
        # exporter.to_picture("syntaxanalysis.png")

        subprocess.run(
            ["dot", "syntax_tree.dot", "-Tpng", "-o", "syntaxanalysis.png"], check=True
        )
        console.log(root)
        return root

    # def semantic_analysis(self, ast):
    #     terminals = [node.name for node in ast.descendants if node.depth == 1]
    #     non_termminals = [node.name for node in ast.descendants if node.depth == 2]
    #     print(terminals)
    #     print(non_termminals)
    #     # Every sentence must have a subject and a verb (predicate)
    #     has_verb = False
    #     has_noun = False
    #     if ("<AUX>" or "<VERB>") and ("<NOUN>" or "<PRON>") in terminals:
    #         has_noun = True
    #         has_verb = True
    #     # Adjectives Describe Nouns; Adverbs Describe Verbs
    #     if "<ADJ>" in terminals :
    #         noun_before_adj = False
    #         adj_index = terminals.index('<ADJ>')
    #         if terminals[adj_index - 1] == "<NOUN>":
    #             noun_before_adj = True

    #     # Subject-verb agreement
    #     # if noun_before_adj and has_noun
    #     # Sentences must start with a capital letter and end with proper punctuation
    #     verified_ast = ast
    #     return verified_ast

    def intermediate_code_generation(self, ast):
        non_termminals = [node.name for node in ast.descendants if node.depth == 2]
        #

        doc = nlp(" ".join(non_termminals))
        ir = []
        for token in doc:
            if token.dep_:
                10 != ROOT
            print(
                f"{token.text:10} {token.dep_:10} {token.head.text:10} {token.pos_:6}"
            )
            print(token)

        pass

    def run_compiler(self):
        helpers = Helpers()
        # temp = [
        #     {"token": "The", "lexeme": "<PRON>"},
        #     {"token": "big", "lexeme": "<ADJ>"},
        #     {"token": "red", "lexeme": "<ADJ>"},
        #     {"token": "ball", "lexeme": "<NOUN>"},
        #     {"token": "is", "lexeme": "<AUX>"},
        #     {"token": "yours", "lexeme": "<NOUN>"},
        #     {"token": ".", "lexeme": "<PERIOD>"},
        # ]
        # print(temp)
        # helpers.verb_phrase_formatting(temp)
        starting_statement = self.starting_statement
        lexical_table = self.lexical_analysis(starting_statement)
        print(lexical_table)
        helpers.delay()
        abstract_syntax_tree = self.syntax_analysis(lexical_table)
        # abstract_syntax_tree = self.syntax_analysis(temp)
        helpers.delay()
        verified_ast = self.semantic_analysis(abstract_syntax_tree)
        helpers.delay()
        self.intermediate_code_generation(abstract_syntax_tree)

        helpers.delay()
        self.semantic_analysis(abstract_syntax_tree)


if __name__ == "__main__":
    t = Compiler("The quick red fox jumps over the lazy dog.")
    t.run_compiler()

logger = [
    [
        {"token": "Hello", "lexeme": "STRING"},
        {"token": ",", "lexeme": "<COMMA>"},
        {"token": " ", "lexeme": "<SPACE>"},
        {"token": "HelloWorld", "lexeme": "STRING"},
        {"token": "!", "lexeme": "<EXCLAMATION MARK>"},
    ]
]


# def lexical_analysis():
#     # Lexical analysis code would go here
#     punctuation_symbol_table = {
#         ".": "<PERIOD>",
#         ",": "<COMMA>",
#         "!": "<EXCLAMATION MARK>",
#         "?": "<QUESTION MARK>",
#         ":": "<COLON>",
#         ";": "<SEMICOLON>",
#         "'": "<APOSTROPHE>",
#         '"': "<QUOTATION MARK>",
#         "-": "<HYPHEN>",
#         "_": "<UNDERSCORE>",
#         "(": "<LEFT PARENTHESIS>",
#         ")": "<RIGHT PARENTHESIS>",
#         "[": "<LEFT BRACKET>",
#         "]": "<RIGHT BRACKET>",
#         "{": "<LEFT BRACE>",
#         "}": "<RIGHT BRACE>",
#         "/": "<SLASH>",
#         "\\": "<BACKSLASH>",
#         "@": "<AT SYMBOL>",
#         "#": "<HASH>",
#         "$": "<DOLLAR SIGN>",
#         "%": "<PERCENT>",
#         "^": "<CARET>",
#         "&": "<AMPERSAND>",
#         "*": "<ASTERISK>",
#         "+": "<PLUS>",
#         "=": "<EQUALS>",
#         "<": "<LESS THAN>",
#         ">": "<GREATER THAN>",
#         "`": "<BACKTICK>",
#         "~": "<TILDE>",
#         "|": "<VERTICAL BAR>",
#         " ": "<SPACE>",
#     }
