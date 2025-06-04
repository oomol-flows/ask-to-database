#region generated meta
import typing
from oocana import Context
class Inputs(typing.TypedDict):
    training_data_path: str
    training_data_id: str
Outputs = typing.Dict[str, typing.Any]
#endregion

from vanna.openai import OpenAI_Chat
from vanna.chromadb import ChromaDB_VectorStore

class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, ai_client, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, ai_client, config=config)

def main(params: Inputs, context: Context):
    vn: MyVanna = MyVanna(ai_client =None,  config={
        'path': params['training_data_path'],
        'model': "oomol-chat",
    })

    vn.remove_training_data(params['training_data_id'])
