import yaml
from typing import Any, Union


with open("./settings.yml") as f:
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
SITE_NAME:str = get("config.site.display_name")
HOSTNAME:str = get("config.site.hostname")
PORT:int = get("config.site.port")

# SSL
SSL_ENABLED:bool = get("config.ssl.enabled")
SSL_KEY_STORE:str = get("config.ssl.key")
SSL_CERT_STORE:str = get("config.ssl.cert")

# Hcaptcha
HCAPTCHA_ENABLE:bool = get("config.hcaptcha.enabled")
HCAPTCHA_SITEKEY:str = get("config.hcaptcha.sitekey")
HCAPTCHA_SECRET:str = get("config.hcaptcha.secret")

# Email
SMTP_EMAIL:str = get("config.smtp.email")
SMTP_PASSWORD:str = get("config.smtp.password")
SMTP_HOSTNAME:str = get("config.smtp.hostname")
SMTP_PORT:int = get("config.smtp.port")
EMAIL_TEMPLATE_VERIFICATION_PATH:str = get("email.template_paths.email_verification")
EMAIL_TEMPLATE_PASSWORD_RESET_PATH:str = get("email.template_paths.password_reset")

# AWS
AWS_ID:str = get("config.aws.id")
AWS_SECRET:str = get("config.aws.secret")
AWS_REGION:str = get("config.aws.region")

# Storage
STORAGE_METHOD:str = get("storage.method")
STORAGE_LOCAL_PATH:str = get("storage.local.path")
STORAGE_S3_BUCKET:str = get("storage.s3.bucket-name")

# Tags
TAGS_MINIMUM_COUNT:int = get("tags.minimum_count")
TAGS_TAGGING_SERVICE_ENABLED:bool = get("tags.tagging_service.enabled")
TAGS_TAGGING_SERVICE_URL:str = get("tags.tagging_service.url")

# Posts
POSTS_SEARCH_DEFAULT_SORT:str = get("posts.search.default_sort")
POSTS_SEARCH_MAX_LIMIT:int = get("posts.search.max_limit")

# Database
DATABASE_CHOICE:str = get("database.choice")
WIPE_ON_STARTUP:bool = get("config.wipe_on_startup")
MONGODB_DB_NAME:str = get("config.mongodb.name")
MONGODB_HOSTNAME:str = get("config.mongodb.hostname")
MONGODB_PORT:int = get("config.mongodb.port")
MONGODB_USERNAME:int = get("config.mongodb.username")
MONGODB_PASSWORD:int = get("config.mongodb.password")

# Import
IMPORT_FILES_ENABLED:bool = get("import.local.enabled")
IMPORT_FILES_BASEPATH:str = get("import.local.local_path")

IMPORT_HYDRUS_ENABLED:bool = get("import.hydrus.enabled")
IMPORT_HYDRUS_KEY:str = get("import.hydrus.access_key")
IMPORT_HYDRUS_URL:str = get("import.hydrus.url")
IMPORT_HYDRUS_TAGS:str = get("import.hydrus.tags")

IMPORT_SAFEBOORU_ENABLED:bool = get("import.safebooru.enabled")
IMPORT_SAFEBOORU_LIMIT:Union[int,None] = get("import.safebooru.limit")
IMPORT_SAFEBOORU_SEARCHES:list[str] = get("import.safebooru.searches")

IMPORT_TUMBLR_ENABLED:bool = get("import.tumblr.enabled")
IMPORT_TUMBLR_KEY:str = get("import.tumblr.consumer_key")
IMPORT_TUMBLR_SECRET:str = get("import.tumblr.consumer_secret")

IMPORT_TWITTER_ENABLED:bool = get("import.twitter.enabled")
IMPORT_TWITTER_KEY:str = get("import.twitter.bearer_token")

# Passwords
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

# VIDEO_REENCODE:bool = get("encoding.video.full.reencode")
# VIDEO_PREVIEW_ENABLED:bool = get("encoding.video.preview.enabled")
# VIDEO_PREVIEW_DURATION:float = get("encoding.video.preview.duration")
VIDEO_THUMBNAIL_OFFSET:float = get("encoding.video.thumbnail_offset")
