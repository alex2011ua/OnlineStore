from llama_index import Document
from llama_index.node_parser import SimpleNodeParser
from llama_index import VectorStoreIndex, GPTKeywordTableIndex
from my_apps.shop.models import Product

import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

products = Product.objects.all()

text_list = []
for product in products:
    text_list.append(f"title: {product.name}, description: {product.description[0:200]}")

documents = [Document(text=t) for t in text_list]

parser = SimpleNodeParser.from_defaults()
nodes = parser.get_nodes_from_documents(documents)
index = GPTKeywordTableIndex(nodes)

query_engine = index.as_query_engine(response_mode='tree_summarize')


def search_answer(text):

    response = query_engine.query(f"какой подарок подходящий: {text}? выбрать один товар")
    print(response.response)
    return response.response