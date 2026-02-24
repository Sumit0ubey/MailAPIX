from EmailServiceAPI.Controller.parser import plain_text_to_advanced_html


def impressive(data, subject: str | None, company_name: str | None, company_link: str | None):
    project_info: str
    if company_name is None:
        company_name = "Sumit Dubey"
        project_info = "Open Source Project"
    else:
        project_info = "© All rights reserved"

    if company_link is None:
        company_link = "https://github.com/Sumit0ubey"

    if subject is None:
        subject = "You've Got a New Update"

    body_content = plain_text_to_advanced_html(data)
    return f"""<!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>Notification</title>
      <style>
        body {{
          margin: 0;
          padding: 0;
          background-color: #f3f4f6;
          font-family: 'Inter', sans-serif;
          color: #111827;
        }}
        .container {{
          max-width: 640px;
          margin: 50px auto;
          background-color: #ffffff;
          display: flex;
          border-radius: 12px;
          overflow: hidden;
          box-shadow: 0 12px 24px rgba(0,0,0,0.06);
        }}
        .sidebar {{
          background-color: #4b5563;
          width: 10px;
        }}
        .content {{
          padding: 40px;
          width: 100%;
        }}
        .title {{
          font-size: 20px;
          font-weight: 600;
          color: #1f2937;
          margin-bottom: 24px;
        }}
        .message {{
          font-size: 16px;
          line-height: 1.7;
          color: #374151;
          margin-bottom: 30px;
        }}
        .footer-note {{
          font-size: 13px;
          color: #9ca3af;
          text-align: right;
        }}
        .footer {{
          text-align: center;
          padding: 20px;
          font-size: 13px;
          color: #6b7280;
          border-top: 1px solid #e5e7eb;
          margin-top: 30px;
        }}
        .footer a {{
          color: #4b5563;
          text-decoration: none;
          margin: 0 6px;
        }}
        .footer a:hover {{
          text-decoration: underline;
        }}
        @media (max-width: 640px) {{
          .container {{
            flex-direction: row;
            flex-wrap: nowrap;
            margin: 10px;
            border-radius: 8px;
          }}
          .sidebar {{
            width: 6px;
            height: auto;
          }}
          .content {{
            padding: 20px;
          }}
        }}
      </style>
    </head>
    <body>
      <div class="container" role="article" aria-label="User Email">
        <div class="sidebar"></div>
        <div class="content">
          <div class="title">{subject}</div>
          <div class="message">
            {body_content}
          </div>
          <div class="footer-note">
            ⚠️ This is an automated email. No reply is needed.
          </div>
          <div class="footer">
            Sent via <a href={company_link} target="_blank">{company_name}</a> • 
            {project_info}
          </div>
        </div>
      </div>
    </body>
    </html>"""
