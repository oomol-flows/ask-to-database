from oocana import Context

#region generated meta
import typing
class Inputs(typing.TypedDict):
    input: str
Outputs = typing.Dict[str, typing.Any]
#endregion

def main(params: Inputs, context: Context) -> Outputs:
    context.preview(payload={
        "type": 'text',
        "data": params['input']
    })
