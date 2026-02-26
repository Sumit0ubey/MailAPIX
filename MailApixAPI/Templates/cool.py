from MailApixAPI.Controller.parser import plain_text_to_advanced_html

def cool(data, email_title : str = None, company_name: str = None, company_link: str = None):
    if email_title is None: email_title = "User Query"
    if company_name is None: company_name = ""
    if company_link is None: company_link = "#"

    body_content = plain_text_to_advanced_html(data)

    return f"""<!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>Email Notification</title>
      <style>
        body {{
          margin: 0;
          padding: 0;
          background-color: #f4f7fc;
          font-family: 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
          color: #333;
        }}
        .email-container {{
          max-width: 600px;
          margin: 40px auto;
          background: #ffffff;
          border-radius: 16px;
          overflow: hidden;
          box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
          border: 1px solid #dee2e6;
        }}
        .email-header {{
          background: linear-gradient(90deg, #4f46e5, #3b82f6);
          color: #ffffff;
          padding: 24px 30px;
          text-align: center;
        }}
        .email-header h1 {{
          margin: 0;
          font-size: 24px;
          font-weight: 700;
          letter-spacing: 0.5px;
        }}
        .email-body {{
          padding: 32px;
          font-size: 16px;
          line-height: 1.75;
        }}
        .email-body p {{
          margin-bottom: 18px;
        }}
        .email-body strong {{
          color: #111827;
        }}
        .email-footer {{
          background-color: #f1f5f9;
          padding: 20px 30px;
          text-align: center;
          font-size: 14px;
          color: #6b7280;
          border-top: 1px solid #e5e7eb;
        }}
        .email-footer a {{
          color: #4b5563;
          text-decoration: none;
          margin: 0 6px;
        }}
        .email-footer a:hover {{
          text-decoration: underline;
        }}
        @media (max-width: 600px) {{
          .email-container {{
            margin: 20px;
          }}
          .email-body {{
            padding: 24px;
          }}
        }}
      </style>
    </head>
    <body>
      <div class="email-container" role="article" aria-label="Email Notification">
        <div class="email-header">
          <h1>{email_title}</h1>
        </div>
        <div class="email-body">
          {body_content}
          <p style="font-size: 13px; color: #9ca3af;">⚠️ This is an automated message. Please do not reply.</p>
        </div>
        <div class="email-footer">
          <p>
            Powered by <a href="{company_link}" target="_blank">{company_name}</a> |
            <a href="#">Open Source | MailApix</a>
          </p>
        </div>
      </div>
    </body>
    </html>"""
