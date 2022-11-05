from . import router
from fastapi.responses import RedirectResponse


@router.get('/', include_in_schema=False)
def docs_redirect():
    return RedirectResponse('/docs')
