import urllib
from datetime import datetime
from uuid import uuid4
from secrets import choice
from string import ascii_letters, digits
from passlib.context import CryptContext


def serialize_timestamp(dt: datetime) -> str:
    return dt.strftime("%d-%m-%Y")


def generate_key(suffix_length=12):
    uuid_part = str(uuid4())
    alphabet = ascii_letters + digits
    random_part = ''.join(choice(alphabet) for _ in range(suffix_length))
    return uuid_part.replace("-", "") + random_part


pwt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwt_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwt_context.verify(password, hashed_password)


def encodedUPI(upi_url):
    return urllib.parse.quote(upi_url, safe='')

def get_email_service(email):
    known_services = {
        "gmail.com": "Gmail",
        "googlemail.com": "Gmail",
        "outlook.com": "Outlook",
        "hotmail.com": "Outlook",
        "live.com": "Outlook",
        "msn.com": "Outlook",
        "yahoo.com": "Yahoo",
        "yahoo.co.uk": "Yahoo UK",
        "yahoo.co.in": "Yahoo India",
        "icloud.com": "iCloud",
        "me.com": "iCloud",
        "mac.com": "iCloud",
        "aol.com": "AOL",
        "protonmail.com": "ProtonMail",
        "zoho.com": "Zoho Mail",
        "mail.com": "Mail.com",
        "gmx.com": "GMX",
        "gmx.net": "GMX",
        "yandex.com": "Yandex",
        "yandex.ru": "Yandex",
        "tutanota.com": "Tutanota",
        "hey.com": "HEY",
        "fastmail.com": "Fastmail",
        "hushmail.com": "Hushmail",
        "qq.com": "QQ Mail",
        "naver.com": "Naver Mail",
        "daum.net": "Daum Mail",
        "rediffmail.com": "Rediffmail",
        "seznam.cz": "Seznam",
        "web.de": "Web.de",
        "mail.ru": "Mail.ru",
        "126.com": "126 Mail",
        "163.com": "163 Mail",
    }

    try:
        domain = email.strip().lower().split('@')[1]
        return known_services.get(domain, domain)
    except (IndexError, AttributeError):
        return 'Invalid email'
