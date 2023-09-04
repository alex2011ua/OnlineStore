import logging
import sys

from llama_index import (Document, DocumentSummaryIndex, GPTKeywordTableIndex,
                         StorageContext, TreeIndex, VectorStoreIndex,
                         load_index_from_storage)
from llama_index.node_parser import SimpleNodeParser
from my_apps.shop.models import Product

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

try:
    storage_context = StorageContext.from_defaults(persist_dir="./storage")
    index = load_index_from_storage(storage_context)

except Exception as ex:
    print(ex)
    products = Product.objects.all()
    documents = []
    for product in products:
        documents.append(
            Document(
                text=f"description: {product.description[0:300]}",
                metadata={
                    "slug": product.slug,
                    "name": product.name,
                    "category": product.category.name,
                },
            )
        )
        parser = SimpleNodeParser.from_defaults()
        nodes = parser.get_nodes_from_documents(documents)
        index = VectorStoreIndex(nodes)
        index.storage_context.persist()


def search_answer(text):
    query_engine = index.as_query_engine()
    response = query_engine.query(
        f"Допоможи підібрати подарунок. Цікавить таке: {text}? вибери 1 товар и напиши slug, name, category"
    )
    print(response.response)
    return response.response
