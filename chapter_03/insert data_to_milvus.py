import os
from pymilvus import DataType
from pymilvus import MilvusClient
import dotenv

dotenv.load_dotenv()

## 获取到客户端对象
client = MilvusClient(
    # uri="mivus_demo.db"
    uri=os.getenv("ZILLIZ_ENDPOINT"),
    token=os.getenv("ZILLIZ_API_KEY")
)


def create_collection():
    def build_schema():
        schema = MilvusClient.create_schema(auto_id=True)
        schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
        schema.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=768)
        schema.add_field(field_name="metadata", datatype=DataType.JSON)  # 元数据信息可以用来做检索
        schema.add_field(field_name="content", datatype=DataType.VARCHAR, max_length=1024)
        return schema

    # build_schema()
    def build_index():
        # 得到索引参数
        index_params = MilvusClient.prepare_index_params()
        # 通过调用索引参数的add_index方法，为collection当中定义的字段去构建索引
        index_params.add_index(
            field_name="vector",
            index_type="AUTOINDEX",  # milvus自动根据当前数据量大小选择合适的索引,
            metric_type="COSINE"  # 衡量两个向量之间距离的方式，L2表示的是向量之间的欧式距离
        )
        return index_params

    # build_index()
    client.create_collection("demo_collection", dimension=768,
                             primary_field_name="id",
                             schema=build_schema(),
                             index_params=build_index())


def get_document():
    """
    准备Document，将Document交给embedding model 来进行嵌入
    :return:
    """
    from langchain_community.document_loaders import UnstructuredWordDocumentLoader
    data_loader = UnstructuredWordDocumentLoader(
        file_path="assets/sample.docx",
        mode="elements"
    )
    return data_loader.load()


def get_embeddings(document_list):
    """
    通过嵌入模型来得到向量
    :param document_list:
    :return:
    """
    from langchain_huggingface import HuggingFaceEmbeddings
    model = HuggingFaceEmbeddings(
        model_name=r"D:\cache\modelscope\hub/models\Xorbits\bge-base-zh-v1___5"
    )
    return model.embed_documents(document_list)


# 往集合当中插入数据
def get_data_to_insert_into_milvus():
    documents = get_document()
    document_embeddings = get_embeddings([document.page_content for document in documents])
    list_dict = [
        {
            "vector": document_embedding,
            "metadata": document.metadata,
            "content": document.page_content,
        }
        for document, document_embedding in zip(documents, document_embeddings)
    ]  # 构造数据
    return list_dict


print("1. 正在检查/创建集合...")
create_collection()
print("2. 正在加载文档并生成向量数据 (这可能需要几秒钟)...")
datas = get_data_to_insert_into_milvus()
print(f"3. 准备将 {len(datas)} 条数据插入 Zilliz Cloud...")
client.insert(collection_name="demo_collection", data=datas)
