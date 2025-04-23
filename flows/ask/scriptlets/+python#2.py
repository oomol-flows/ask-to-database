#region generated meta
import typing
class Inputs(typing.TypedDict):
    input: str
Outputs = typing.Dict[str, typing.Any]
#endregion

from oocana import Context

def main(params: Inputs, context: Context) -> Outputs:
    context.preview({
        'type': 'json',
        'data': params['input']
    })
