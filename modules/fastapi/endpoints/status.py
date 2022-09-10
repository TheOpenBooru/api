from . import router
from modules import settings, fastapi
from modules.schemas import Status
from fastapi import Depends


@router.get('/status',
    operation_id="status",
    response_model=Status,
    dependencies=[
        Depends(fastapi.RateLimit("1/second")),
    ],
)
def get_status():
    return Status(
        sitename=settings.SITE_NAME,
        default_sort=settings.POSTS_SEARCH_DEFAULT_SORT,
        search_limit=settings.POSTS_SEARCH_MAX_LIMIT,
        captcha_sitekey=settings.HCAPTCHA_SITEKEY,
    )