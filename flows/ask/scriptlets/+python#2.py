#region generated meta
import typing
from oocana import Context
class Inputs(typing.TypedDict):
    input: str
Outputs = typing.Dict[str, typing.Any]
#endregion

def main(params: Inputs, context: Context) -> Outputs:
    context.preview({
        'type': 'json',
        'data': params['input']
    })
