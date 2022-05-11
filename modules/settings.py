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

# Webserver Config

SITE_NAME:str = get("config.site.name")
HOSTNAME:str = get("config.site.hostname")
PORT:int = get("config.site.port")

SSL_ENABLED:bool = get("config.ssl.enabled")
SSL_KEY_STORE:str = get("config.ssl.key")
SSL_CERT_STORE:str = get("config.ssl.cert")

# Hcaptcha

HCAPTCHA_SITEKEY:str = get("config.hcaptcha.sitekey")
HCAPTCHA_SECRET:str = get("config.hcaptcha.secret")

# Email

SMTP_EMAIL:str = get("config.smtp.email")
SMTP_PASSWORD:str = get("config.smtp.password")
SMTP_HOSTNAME:str = get("config.smtp.hostname")
SMTP_PORT:int = get("config.smtp.port")
EMAIL_TEMPLATE_EMAIL_VERIFICATION_PATH:str = get("email.template_paths.email_verification")
EMAIL_TEMPLATE_PASSWORD_RESET_PATH:str = get("email.template_paths.password_reset")

# AWS

AWS_ID:str = get("config.aws.id")
AWS_SECRET:str = get("config.aws.secret")
AWS_REGION:str = get("config.aws.region")

# Storage

STORAGE_METHOD:str = get("storage.method")
STORAGE_LOCAL_PATH:str = get("storage.local.path")
STORAGE_S3_BUCKET:str = get("storage.s3.bucket-name")

# Posts

MAX_SEARCH_LIMIT:int = get("posts.search_max_limit")

# Database
DATABASE_CHOICE:str = get("database.choice")
MONGODB_WIPE_ON_STARTUP:bool = get("database.mongodb.wipe_on_startup")
MONGODB_DB_NAME:str = get("database.mongodb.name")
MONGODB_HOSTNAME:str = get("database.mongodb.host")
MONGODB_PORT:int = get("database.mongodb.port")

# Import

IMPORT_LOCAL_ENABLED:bool = get("posts.import.local.enabled")
IMPORT_GELBOORU_ENABLED:bool = get("posts.import.gelbooru.enabled")
IMPORT_GELBOORU_WEBSITE:str = get("posts.import.gelbooru.website")
IMPORT_GELBOORU_LIMIT:int|None = get("posts.import.gelbooru.limit")
IMPORT_GELBOORU_SEARCHES:list[str] = get("posts.import.gelbooru.searches")

# Password

PASSWORD_PEPPER:int = get("config.password_pepper")
DEFAULT_TOKEN_EXPIRATION:int = get("authentication.token_expiration")
PASSWORD_MIN_LENGTH:int = get("authentication.password_requirements.min_length")
PASSWORD_MAX_LENGTH:int = get("authentication.password_requirements.max_length")
PASSWORD_REQUIRED_SCORE:int = get("authentication.password_requirements.score")

# Encoding

THUMBNAIL_LOSSLESS:bool = get("encoding.thumbnail.lossless")
THUMBNAIL_QUALITY:int = get("encoding.thumbnail.quality")
THUMBNAIL_WIDTH:int = get("encoding.thumbnail.max_width")
THUMBNAIL_HEIGHT:int = get("encoding.thumbnail.max_height")

IMAGE_FULL_LOSSLESS:bool = get("encoding.image.full.lossless")
IMAGE_FULL_QUALITY:int = get("encoding.image.full.quality")
IMAGE_FULL_WIDTH:int = get("encoding.image.full.max_width")
IMAGE_FULL_HEIGHT:int = get("encoding.image.full.max_height")

IMAGE_PREVIEW_LOSSLESS:bool = get("encoding.image.preview.lossless")
IMAGE_PREVIEW_QUALITY:int = get("encoding.image.preview.quality")
IMAGE_PREVIEW_WIDTH:int = get("encoding.image.preview.max_width")
IMAGE_PREVIEW_HEIGHT:int = get("encoding.image.preview.max_height")

ANIMATION_LOSSLESS:bool = get("encoding.animation.lossless")
ANIMATION_QUALITY:int = get("encoding.animation.quality")
ANIMATION_WIDTH:int = get("encoding.animation.max_width")
ANIMATION_HEIGHT:int = get("encoding.animation.max_height")

VIDEO_REENCODE:bool = get("encoding.video.full.reencode")
VIDEO_PREVIEW_ENABLED:bool = get("encoding.video.preview.enabled")
VIDEO_PREVIEW_DURATION:float = get("encoding.video.preview.duration")
VIDEO_THUMBNAIL_OFFSET:float = get("encoding.video.thumbnail_offset")
