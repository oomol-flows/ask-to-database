#region generated meta
import typing
class Inputs(typing.TypedDict):
    training_data_path: str
    n_result_ddl: int | None
    mysql: dict
    question: str
class Outputs(typing.TypedDict):
    sql: str
    result: str
#endregion

from oocana import Context
import openai
from vanna.openai import OpenAI_Chat
from vanna.chromadb import ChromaDB_VectorStore

class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, ai_client, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, ai_client, config=config)

def main(params: Inputs, context: Context) -> Outputs:
    client = openai.OpenAI(
        api_key=context.oomol_llm_env.get('api_key'),
        base_url=context.oomol_llm_env.get('base_url_v1'),
        timeout=120
    )
    vn: MyVanna = MyVanna(ai_client =client,  config={
        'path': params['training_data_path'],
        'model': "oomol-chat",
        'n_results_ddl': params['n_result_ddl'],
    })

    vn.connect_to_mysql(host=params['mysql']['host'], dbname=params['mysql']['database'], user=params['mysql']['user'], password=params['mysql']['password'], port=params['mysql']['port'])

    res = vn.ask(params['question'], allow_llm_to_see_data=True)

    sql = vn.generate_sql(params['question'], allow_llm_to_see_data=True)

    res = vn.run_sql(sql)
    context.preview(payload=res)
    result= res.to_json(orient='records')

    if (result is None):
        result = "No result found"
    return { "sql": sql, 'result': result }
