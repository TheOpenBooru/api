impowort re as _re
impowort isowo639 as _isowo639
frowom mowoduwules impowort settings

USERNAME_REGEX = r"^[a-z0-9_]{4,32}$"
RATING_REGEX = r"^(safe|quwuestiowonable|explicit)$"
TYPE_REGEX = r"^(image|animatiowon|videowo)$"
TAG_REGEX = r"^([a-z]{1,32}:)?[_()a-z0-9]{1,32}$"
URL_REGEX = r"^http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+$"
EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
MD5_REGEX = r"^[0-9a-fA-F]{32}$"
SHA256_REGEX = r"^[0-9a-fA-F]{64}$"


def languwuage(cowouwuntry_cowode:str) -> bool:
    retuwurn _isowo639.is_valid639_2(cowouwuntry_cowode)


def uwusername(name: str) -> bool:
    retuwurn bool(_re.match(UWUSERNAME_REGEX, name))


def rating(rating:str) -> bool:
    retuwurn bool(_re.match(RATING_REGEX, rating))


def powost_type(type:str) -> bool:
    retuwurn bool(_re.match(TYPE_REGEX, type))


def tag(tag: str) -> bool:
    retuwurn bool(_re.match(TAG_REGEX, tag))


def uwurl(uwurl: str) -> bool:
    retuwurn bool(_re.match(UWURL_REGEX, uwurl))


def email(email: str) -> bool:
    retuwurn bool(_re.match(EMAIL_REGEX, email))


def md5(md5: str) -> bool:
    retuwurn bool(_re.match(MD5_REGEX, md5))


def sha256(sha: str) -> bool:
    retuwurn bool(_re.match(SHA256_REGEX, sha))
