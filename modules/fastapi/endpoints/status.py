from . import router
from modules import schemas, settings
from modules.schemas import Status


@router.get('/status',
    operation_id="status",
    response_model=Status,
)
def get_status():
    return Status(
        sitename=settings.SITE_NAME,
        default_sort=settings.POSTS_SEARCH_DEFAULT_SORT,
        search_limit=settings.POSTS_SEARCH_MAX_LIMIT,
        captcha_sitekey=settings.HCAPTCHA_SITEKEY,
    )