import logging
import sys

from llama_index import (
    Document,
    DocumentSummaryIndex,
    GPTKeywordTableIndex,
    StorageContext,
    TreeIndex,
    VectorStoreIndex,
    load_index_from_storage,
)
from llama_index.node_parser import SimpleNodeParser
from my_apps.shop.models import Product

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


class LlamaSearch:
    def __init__(self):
        try:
            print("load index")
            self.storage_context = StorageContext.from_defaults(persist_dir="./storage")
            self.index = load_index_from_storage(self.storage_context)

        except FileNotFoundError as ex:
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
            self.index = VectorStoreIndex(nodes)
            self.index.storage_context.persist()

    def search_answer(self, text):
        query_engine = self.index.as_query_engine()
        response = query_engine.query(
            f"Help to choose product. Interested in: {text}? choose 1 product and write slug, name, category"
        )
        print(response.response)
        return response.response
