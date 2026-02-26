from dotenv import load_dotenv
from os import getenv

load_dotenv()

WEBSITE_LINK = getenv("WEBSITE_LINK", "#")

def tokenRevert(token: str):
    return f"""
    <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <title>Registration Successful - Email Service API</title>
      <style>
        body {{
          font-family: Arial, sans-serif;
          background-color: #f4f4f4;
          margin: 0;
          padding: 0;
        }}
        .email-container {{
          max-width: 600px;
          margin: auto;
          background-color: #ffffff;
          padding: 24px;
          border-radius: 10px;
          box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
        }}
        .email-container h2 {{
          text-align: center;
          color: #111827;
          font-size: 22px;
          margin-bottom: 30px;
        }}
        .card {{
          background-color: #ffffff;
          border-radius: 10px;
          box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
          padding: 20px;
          margin-bottom: 20px;
          text-align: center;
        }}
        .card h3 {{
          margin-top: 0;
          color: #1f2937;
          font-size: 18px;
        }}
        .card p {{
          color: #4b5563;
          font-size: 14px;
          margin: 10px 0;
        }}
        .credentials {{
          color: #e91e63;
          font-size: 16px;
          font-weight: bold;
          margin: 12px 0;
          line-height: 1.6;
        }}
        .auto-note {{
          font-size: 12px;
          color: #9ca3af;
          text-align: center;
          margin: 20px 0;
        }}
        .footer {{
          text-align: center;
          font-size: 13px;
          color: #6b7280;
          border-top: 1px solid #e0e0e0;
          padding-top: 16px;
          margin-top: 30px;
        }}
        .footer a {{
          color: #3b82f6;
          text-decoration: none;
        }}
        .footer a:hover {{
          text-decoration: underline;
        }}
        @media only screen and (max-width: 620px) {{
          .email-container {{
            padding: 16px;
          }}
          .card {{
            padding: 16px;
          }}
        }}
      </style>
    </head>
    <body>
      <div class="email-container">
        <h2>Revert/Change Token </h2>

        <div class="card">
          <h3>Welcome to MailApix API</h3>
          <p>Thanks for sticking with us. Below is your new token:</p>
          <div class="credentials">
            Token: {token}
          </div>
        </div>

        <div class="card">
          <p><strong>Important:</strong> Do not share your token or this mail with anyone.</p>
        </div>

        <div class="auto-note">
          ⚠️ This is an automated email. Please do not reply.
        </div>

        <div class="footer">
          Sent by <a href="{WEBSITE_LINK}"> MailApix API </a> • All rights reserved © 2025<br />
        </div>
      </div>
    </body>
    </html>
    """
