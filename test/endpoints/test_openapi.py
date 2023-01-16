from app import app
from schemathesis.specs.openapi.loaders import from_asgi

schema = from_asgi("/openapi.json", app)

@schema.parametrize()
def test_openapi_compliance(case):
    response = case.call_asgi()
    case.validate_response(response)
