import yaml
from typing import Any



with open("./config.yml") as f:
    _config = yaml.full_load(f)

def get(setting: str) -> Any:
    """Raises:
    - KeyError: Invalid Setting Name
    """
    config = _config
    for key in setting.split("."):
        if key not in config:
            raise KeyError(f"Invalid Setting: {setting}")
        else:
            config = config[key]
    return config

SITE_NAME:str = get("config.site.name")
HOSTNAME:str = get("config.site.hostname")
PORT:str = get("config.site.port")

SSL_KEY_STORE:str = get("config.ssl.key")
SSL_CERT_STORE:str = get("config.ssl.cert")

HCAPTCHA_SITEKEY:str = get("config.hcaptcha.sitekey")
HCAPTCHA_SECRET:str = get("config.hcaptcha.secret")

SMTP_EMAIL:str = get("config.smtp.email")
SMTP_PASSWORD:str = get("config.smtp.password")
SMTP_HOSTNAME:str = get("config.smtp.hostname")
SMTP_PORT:int = get("config.smtp.port")
EMAIL_TEMPLATE_EMAIL_VERIFICATION_PATH:str = get("email.template_paths.email_verification")
EMAIL_TEMPLATE_PASSWORD_RESET_PATH:str = get("email.template_paths.password_reset")

AWS_ID:str = get("config.aws.id")
AWS_SECRET:str = get("config.aws.secret")
AWS_REGION:str = get("config.aws.region")

STORAGE_METHOD:str = get("storage.method")
STORAGE_S3_BUCKET:str = get("storage.s3.bucket-name")

MAX_SEARCH_LIMIT:int = get("search.max_limit")
POST_IMPORT_LOCAL:int = get("posts.sources.local")
POST_IMPORT_SAFEBOORU:int = get("posts.sources.safebooru")

PASSWORD_PEPPER:int = get("config.password_pepper")
DEFAULT_TOKEN_EXPIRATION:int = get("token_expiration")
PASSWORD_MIN_LENGTH:int = get("password_requirements.min_length")
PASSWORD_MAX_LENGTH:int = get("password_requirements.max_length")
PASSWORD_REQUIRED_SCORE:int = get("password_requirements.score")

THUMBNAIL_LOSSLESS:bool = get("thumbnail.lossless")
THUMBNAIL_QUALITY:int = get("thumbnail.quality")
THUMBNAIL_WIDTH:int = get("thumbnail.max_width")
THUMBNAIL_HEIGHT:int = get("thumbnail.max_height")

IMAGE_FULL_LOSSLESS:bool = get("image.full.lossless")
IMAGE_FULL_QUALITY:int = get("image.full.quality")
IMAGE_FULL_WIDTH:int = get("image.full.max_width")
IMAGE_FULL_HEIGHT:int = get("image.full.max_height")

IMAGE_PREVIEW_LOSSLESS:bool = get("image.preview.lossless")
IMAGE_PREVIEW_QUALITY:int = get("image.preview.quality")
IMAGE_PREVIEW_WIDTH:int = get("image.preview.max_width")
IMAGE_PREVIEW_HEIGHT:int = get("image.preview.max_height")

ANIMATION_LOSSLESS:bool = get("animation.lossless")
ANIMATION_QUALITY:int = get("animation.quality")
ANIMATION_WIDTH:int = get("animation.max_width")
ANIMATION_HEIGHT:int = get("animation.max_height")

VIDEO_REENCODE:bool = get("video.full.reencode")
VIDEO_PREVIEW_ENABLED:bool = get("video.preview.enabled")
VIDEO_PREVIEW_DURATION:float = get("video.preview.duration")
VIDEO_THUMBNAIL_OFFSET:float = get("video.thumbnail_offset")
