import yaml
from typing import Any, Union
from os import environ


with open("./settings.yml") as f:
    _config:dict = yaml.full_load(f)

def _check_env(setting: str) -> Union[Any, None]:
    env_name = (setting
        .upper()
        .replace(".","_")
    )
    return environ.get(env_name, default=None)


def get(setting: str) -> Any:
    """Raises:
    - KeyError: Invalid Setting Name
    """
    env_setting = _check_env(setting)
    if env_setting:
        return env_setting
    else:
        config = _config.copy()
        for key in setting.split("."):
            if key not in config:
                raise KeyError(f"Invalid Setting in settings.yml: {setting}")
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
TAGS_REGEN_COUNT_EVERY:Union[int, None] = get("tags.time_between_count_regen")
TAGS_MINIMUM_COUNT:int = get("tags.minimum_count")
TAGS_NAMESPACES:list[str] = get("tags.valid_namespaces")
TAGS_TAGGING_SERVICE_ENABLED:bool = get("tags.tagging_service.enabled")
TAGS_TAGGING_SERVICE_URL:str = get("tags.tagging_service.url")

# Posts
POSTS_SEARCH_DEFAULT_SORT:str = get("posts.search.default_sort")
POSTS_SEARCH_MAX_LIMIT:int = get("posts.search.max_limit")
POSTS_SEARCH_USE_SIBLINGS_AND_PARENTS:bool = False

# Database
WIPE_ON_STARTUP:bool = get("config.wipe_on_startup")
MONGODB_DB_NAME:str = get("config.mongodb.name")
MONGODB_HOSTNAME:str = get("config.mongodb.hostname")
MONGODB_PORT:int = get("config.mongodb.port")
MONGODB_USERNAME:int = get("config.mongodb.username")
MONGODB_PASSWORD:int = get("config.mongodb.password")

# Importers
IMPORTER_FILES_ENABLED:bool = get("importers.local.enabled")
IMPORTER_FILES_RETRY_AFTER:Union[int, None] = get("importers.local.run_every")
IMPORTER_FILES_BASEPATH:str = get("importers.local.local_path")

IMPORTER_HYDRUS_ENABLED:bool = get("importers.hydrus.enabled")
IMPORTER_HYDRUS_RETRY_AFTER:Union[int, None] = get("importers.hydrus.run_every")
IMPORTER_HYDRUS_KEY:str = get("importers.hydrus.access_key")
IMPORTER_HYDRUS_URL:str = get("importers.hydrus.url")
IMPORTER_HYDRUS_TAGS:str = get("importers.hydrus.tags")

IMPORTER_SAFEBOORU_ENABLED:bool = get("importers.safebooru.enabled")
IMPORTER_SAFEBOORU_RETRY_AFTER:Union[int, None] = get("importers.safebooru.run_every")
IMPORTER_SAFEBOORU_REENCODE:bool = get("importers.safebooru.limit")
IMPORTER_SAFEBOORU_LIMIT:Union[int,None] = get("importers.safebooru.limit")
IMPORTER_SAFEBOORU_SEARCHES:list[str] = get("importers.safebooru.searches")

IMPORTER_E621_ENABLED:bool = get("importers.e621.enabled")
IMPORTER_E621_RETRY_AFTER:Union[int, None] = get("importers.e621.run_every")
IMPORTER_E621_DUMP:str = get("importers.e621.dump_location")

IMPORTER_RULE34_ENABLED:bool = get("importers.rule34.enabled")
IMPORTER_RULE34_RETRY_AFTER:Union[int, None] = get("importers.rule34.run_every")
IMPORTER_RULE34_DUMP:str = get("importers.rule34.dump_location")
IMPORTER_RULE34_PROXY_FORMAT:str = get("importers.rule34.proxy_format")

# Downloader
DOWNLOADER_SAFEBOORU_ENABLED:bool = get("downloaders.safebooru.enabled")
DOWNLOADER_E621_ENABLED:bool = get("downloaders.e621.enabled")
DOWNLOADER_RULE34_ENABLED:bool = get("downloaders.rule34.enabled")
DOWNLOADER_YOUTUBE_ENABLED:bool = get("downloaders.youtube.enabled")
DOWNLOADER_FILE_ENABLED:bool = get("downloaders.file.enabled")

DOWNLOADER_TUMBLR_ENABLED:bool = get("downloaders.tumblr.enabled")
DOWNLOADER_TUMBLR_KEY:str = get("downloaders.tumblr.consumer_key")
DOWNLOADER_TUMBLR_SECRET:str = get("downloaders.tumblr.consumer_secret")

DOWNLOADER_TWITTER_ENABLED:bool = get("downloaders.twitter.enabled")
DOWNLOADER_TWITTER_KEY:str = get("downloaders.twitter.bearer_token")

# Passwords
DEFAULT_TOKEN_EXPIRATION:int = get("authentication.token_expiration")
PASSWORD_MIN_LENGTH:int = get("authentication.password_policy.min_length")
PASSWORD_MAX_LENGTH:int = get("authentication.password_policy.max_length")
PASSWORD_REQUIRED_SCORE:int = get("authentication.password_policy.score")

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
