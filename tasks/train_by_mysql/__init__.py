#region generated meta
import typing
from oocana import Context
class Inputs(typing.TypedDict):
    training_data_path: str
    mysql: dict
    db_description: str
class Outputs(typing.TypedDict):
    training_record: str
#endregion

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
    })

    vn.connect_to_mysql(host=params['mysql']['host'], dbname=params['mysql']['database'], user=params['mysql']['user'], password=params['mysql']['password'], port=params['mysql']['port'])

    df_information_schema = vn.run_sql('SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = "%s"' % params['mysql']['database'])

    plan = vn.get_training_plan_generic(df_information_schema)

    vn.train(plan=plan, documentation=params['db_description'])

    r = vn.run_sql("show tables;")
    t = r['Tables_in_cnpmcore'].to_list()

    for table in t:
        r = vn.run_sql('show create table `%s`;' % table)
        rs = r['Create Table'].to_list()

        vn.train(ddl=rs[0])

    training_data = vn.get_training_data()
    context.preview(training_data)


    td = training_data.to_json(orient='records')
    if td is None:
        return { "training_record": "" }
    return { "training_record": td }
