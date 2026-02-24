from datetime import datetime
from EmailServiceAPI.Controller.parser import plain_text_to_advanced_html


def Amazing(data, email_title: str = None, company_name: str = None, company_link: str = None):
    now = datetime.now()
    if email_title is None: email_title = "You got new message"
    if company_name is None: company_name = ""
    if company_link is None: company_link = "#"
    body_content = plain_text_to_advanced_html(data)
    return f"""<!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>Notification Email</title>
      <style>
        body {{
          margin: 0;
          padding: 0;
          background-color: #eef2f6;
          font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
          color: #333;
        }}
        .wrapper {{
          width: 100%;
          padding: 40px 20px;
          display: flex;
          justify-content: center;
        }}
        .card {{
          background: #fff;
          max-width: 620px;
          width: 100%;
          border-radius: 12px;
          box-shadow: 0 10px 30px rgba(0, 0, 0, 0.06);
          overflow: hidden;
        }}
        .header {{
          background-color: #0d9488;
          color: white;
          padding: 24px;
          text-align: left;
        }}
        .header h2 {{
          margin: 0;
          font-size: 22px;
          font-weight: 600;
        }}
        .content {{
          padding: 28px 32px;
          font-size: 16px;
          line-height: 1.65;
          background-color: #ffffff;
        }}
        .content p {{
          margin-bottom: 18px;
        }}
        .note {{
          font-size: 13px;
          color: #6b7280;
          margin-top: 28px;
          text-align: right;
        }}
        .footer {{
          background-color: #f1f5f9;
          text-align: center;
          font-size: 14px;
          padding: 20px;
          color: #6b7280;
          border-top: 1px solid #e5e7eb;
        }}
        .footer a {{
          color: #0f766e;
          text-decoration: none;
          font-weight: 500;
        }}
        .footer a:hover {{
          text-decoration: underline;
        }}
        @media (max-width: 640px) {{
          .card {{
            border-radius: 8px;
          }}
          .content {{
            padding: 24px;
          }}
        }}
      </style>
    </head>
    <body>
      <div class="wrapper">
        <div class="card" role="article" aria-label="User Message">
          <div class="header">
            <h2>{email_title}</h2>
          </div>
          <div class="content">
            {body_content}
            <div class="note">
              📬 This email was generated automatically. Please do not reply.
            </div>
          </div>
          <div class="footer">
            <p>
              © {now.year} <a href="{company_link}" target="_blank">{company_name}</a> — All rights reserved.
            </p>
          </div>
        </div>
      </div>
    </body>
    </html>"""

