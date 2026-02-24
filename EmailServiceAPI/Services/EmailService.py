from __future__ import annotations

import re
import ssl
import socket
import logging
from dataclasses import dataclass
from typing import Iterable, Optional, Union, List, Literal

from smtplib import (
    SMTP, SMTP_SSL, SMTPException, SMTPAuthenticationError,
    SMTPSenderRefused, SMTPRecipientsRefused
)
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

from EmailServiceAPI.Templates.cool import cool
from EmailServiceAPI.Templates.amazing import Amazing
from EmailServiceAPI.Templates.simple import simple

from EmailServiceAPI.Templates.System.tokenrevert import tokenRevert
from EmailServiceAPI.Templates.System.packageplan import packagesPlan
from EmailServiceAPI.Templates.System.mailapix import mailApix_Email_Format
from EmailServiceAPI.Templates.System.registration import registrationEmail


logger = logging.getLogger("EmailService")
if not logger.handlers:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler()],
    )

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass(frozen=True)
class SMTPConfig:
    host: str
    port: int
    use_ssl: bool = False
    use_starttls: bool = True

def _plain_text_to_basic_html(text: str) -> str:
    safe = (text or "").replace("\r\n", "\n").replace("\r", "\n")
    safe = safe.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    parts = re.split(r"\n{2,}", safe)
    return "".join("<p>" + "<br/>".join(p.split("\n")) + "</p>" for p in parts)


class EmailService:
    SMTP_SETTINGS = {
        "gmail.com":   SMTPConfig("smtp.gmail.com", 587, use_ssl=False, use_starttls=True),
        "yahoo.com":   SMTPConfig("smtp.mail.yahoo.com", 587, use_ssl=False, use_starttls=True),
        "outlook.com": SMTPConfig("smtp.office365.com", 587, use_ssl=False, use_starttls=True),
        "hotmail.com": SMTPConfig("smtp.office365.com", 587, use_ssl=False, use_starttls=True),
        "live.com":    SMTPConfig("smtp.office365.com", 587, use_ssl=False, use_starttls=True),
        "icloud.com":  SMTPConfig("smtp.mail.me.com", 587, use_ssl=False, use_starttls=True),
        "zoho.com":    SMTPConfig("smtp.zoho.com", 587, use_ssl=False, use_starttls=True),
        "yandex.com":  SMTPConfig("smtp.yandex.com", 587, use_ssl=False, use_starttls=True),
        "mail.com":    SMTPConfig("smtp.mail.com", 587, use_ssl=False, use_starttls=True),
    }

    _USER_ALLOWED_TEMPLATES = {0, 1, 2, 3, 4}

    SystemTemplate = Literal["mailapix", "packages", "registration", "tokenrevert"]

    @staticmethod
    def _is_valid_email(addr: str) -> bool:
        return bool(_EMAIL_RE.match(addr or ""))

    @classmethod
    def get_smtp_config(cls, email: str) -> SMTPConfig:
        domain = (email or "").lower().split("@")[-1].strip()
        if not domain:
            return SMTPConfig("localhost", 25, use_ssl=False, use_starttls=False)
        if domain in cls.SMTP_SETTINGS:
            return cls.SMTP_SETTINGS[domain]
        return SMTPConfig(f"smtp.{domain}", 587, use_ssl=False, use_starttls=True)

    @classmethod
    def _connect(cls, username: str, password: str, timeout: int = 20) -> Union[SMTP, SMTP_SSL]:
        cfg = cls.get_smtp_config(username)
        ssl_ctx = ssl.create_default_context()

        try:
            if cfg.use_ssl:
                server: Union[SMTP, SMTP_SSL] = SMTP_SSL(cfg.host, cfg.port, timeout=timeout, context=ssl_ctx)
            else:
                server = SMTP(cfg.host, cfg.port, timeout=timeout)

            server.ehlo()

            if cfg.use_starttls and not cfg.use_ssl:
                server.starttls(context=ssl_ctx)
                server.ehlo()

            server.login(username, password)
            logger.info(
                "Connected to SMTP server: %s:%s (ssl=%s starttls=%s)",
                cfg.host, cfg.port, cfg.use_ssl, cfg.use_starttls
            )
            return server

        except SMTPAuthenticationError as e:
            logger.error("SMTP auth failed for %s: %s", username, e)
            raise
        except (SMTPException, socket.timeout, OSError) as e:
            logger.error("SMTP connection failed for %s (%s:%s): %s", username, cfg.host, cfg.port, e)
            raise

    @staticmethod
    def create_mail(
        from_email: str,
        to_list: List[str],
        subject: str,
        html_body: str,
        text_fallback: Optional[str] = None,
        from_name: Optional[str] = None,
        reply_to: Optional[str] = None,
    ) -> MIMEMultipart:
        msg = MIMEMultipart("alternative")
        msg["From"] = formataddr((from_name, from_email)) if from_name else from_email
        msg["To"] = ", ".join(to_list)
        msg["Subject"] = subject
        if reply_to:
            msg["Reply-To"] = reply_to

        if text_fallback is not None:
            msg.attach(MIMEText(text_fallback, "plain", "utf-8"))
        msg.attach(MIMEText(html_body, "html", "utf-8"))
        return msg


    @staticmethod
    def _render_user_template(
        template_id: int,
        data: str,
        *,
        company_name: Optional[str] = None,
        company_link: Optional[str] = None,
        email_title: Optional[str] = None,
        custom_html: Optional[str] = None,
    ) -> tuple[str, str]:

        if template_id == 0:
            text = data or ""
            return _plain_text_to_basic_html(text), text

        if template_id == 4:
            html_body = custom_html if custom_html is not None else (data or "")
            return html_body, (data or "")

        if template_id == 1:
            html_body = cool(data=data, email_title=email_title, company_name=company_name, company_link=company_link)
            return html_body, (data or "")

        if template_id == 2:
            html_body = Amazing(data=data, company_name=company_name)
            return html_body, (data or "")

        html_body = simple(data=data)
        return html_body, (data or "")


    @staticmethod
    def _render_system_template(
        system_template: "EmailService.SystemTemplate",
        *,
        data: str = "",
        company_name: Optional[str] = None,
        company_link: Optional[str] = None,
        email_title: Optional[str] = None,
        iD: Optional[int] = None,
        token: Optional[str] = None,
    ) -> str:
        st = system_template

        if st == "mailapix":
            return mailApix_Email_Format(
                data=data,
                subject=email_title,
                company_name=company_name,
                company_link=company_link,
            )

        if st == "packages":
            return packagesPlan()

        if st == "registration":
            return registrationEmail(iD=iD, token=token)

        if st == "tokenrevert":
            return tokenRevert(token=token)

        return simple(data=data)


    @classmethod
    def send_mail(
        cls,
        username: str,
        password: str,
        to: Union[str, Iterable[str]],
        subject: str,
        data: str,
        template_id: int = 3,
        company_name: Optional[str] = None,
        company_link: Optional[str] = None,
        email_title: Optional[str] = None,
        timeout: int = 20,
        text_fallback: Optional[str] = None,
        custom_html: Optional[str] = None,
        from_name: Optional[str] = None,
        reply_to: Optional[str] = None,
    ) -> bool:
        if template_id not in cls._USER_ALLOWED_TEMPLATES:
            logger.error("template_id=%s is not allowed for user send_mail()", template_id)
            return False

        if isinstance(to, str):
            to_list = [to]
        else:
            to_list = [x for x in to if x]

        if not cls._is_valid_email(username):
            logger.error("Invalid sender email: %s", username)
            return False

        to_list = [addr.strip() for addr in to_list if cls._is_valid_email(addr.strip())]
        if not to_list:
            logger.error("No valid recipient emails.")
            return False

        if not subject or not subject.strip():
            logger.error("Subject is required.")
            return False

        try:
            html_body, default_text = cls._render_user_template(
                template_id=template_id,
                data=data,
                company_name=company_name,
                company_link=company_link,
                email_title=email_title,
                custom_html=custom_html,
            )

            final_text = text_fallback if text_fallback is not None else default_text
            msg = cls.create_mail(
                from_email=username,
                to_list=to_list,
                subject=subject.strip(),
                html_body=html_body,
                text_fallback=final_text,
                from_name=from_name,
                reply_to=reply_to,
            )

            server = None
            try:
                server = cls._connect(username, password, timeout=timeout)
                server.sendmail(username, to_list, msg.as_string())
                logger.info("Email sent successfully to %s", ", ".join(to_list))
                return True
            finally:
                if server:
                    try:
                        server.quit()
                    except Exception:
                        pass

        except (SMTPRecipientsRefused, SMTPSenderRefused) as e:
            logger.error("SMTP refused sender/recipients: %s", e)
            return False
        except SMTPAuthenticationError:
            return False
        except SMTPException as e:
            logger.error("Failed to send email (SMTP): %s", e)
            return False
        except Exception as e:
            logger.exception("Unexpected error while sending email: %s", e)
            return False


    @classmethod
    def send_system_mail(
        cls,
        username: str,
        password: str,
        to: Union[str, Iterable[str]],
        subject: str,
        system_template: "EmailService.SystemTemplate",
        *,
        data: str = "",
        company_name: Optional[str] = None,
        company_link: Optional[str] = None,
        email_title: Optional[str] = None,
        iD: Optional[int] = None,
        token: Optional[str] = None,
        timeout: int = 20,
        text_fallback: Optional[str] = None,
        from_name: Optional[str] = None,
        reply_to: Optional[str] = None,
    ) -> bool:
        if isinstance(to, str):
            to_list = [to]
        else:
            to_list = [x for x in to if x]

        if not cls._is_valid_email(username):
            logger.error("Invalid sender email: %s", username)
            return False

        to_list = [addr.strip() for addr in to_list if cls._is_valid_email(addr.strip())]
        if not to_list:
            logger.error("No valid recipient emails.")
            return False

        if not subject or not subject.strip():
            logger.error("Subject is required.")
            return False

        try:
            html_body = cls._render_system_template(
                system_template=system_template,
                data=data,
                company_name=company_name,
                company_link=company_link,
                email_title=email_title,
                iD=iD,
                token=token,
            )

            final_text = text_fallback if text_fallback is not None else (data or "")
            msg = cls.create_mail(
                from_email=username,
                to_list=to_list,
                subject=subject.strip(),
                html_body=html_body,
                text_fallback=final_text,
                from_name=from_name,
                reply_to=reply_to,
            )

            server = None
            try:
                server = cls._connect(username, password, timeout=timeout)
                server.sendmail(username, to_list, msg.as_string())
                logger.info("System email sent successfully to %s", ", ".join(to_list))
                return True
            finally:
                if server:
                    try:
                        server.quit()
                    except Exception:
                        pass

        except (SMTPRecipientsRefused, SMTPSenderRefused) as e:
            logger.error("SMTP refused sender/recipients: %s", e)
            return False
        except SMTPAuthenticationError:
            return False
        except SMTPException as e:
            logger.error("Failed to send System email (SMTP): %s", e)
            return False
        except Exception as e:
            logger.exception("Unexpected error while sending System email: %s", e)
            return False
