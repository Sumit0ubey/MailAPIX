from MailApixAPI.Controller.parser import plain_text_to_advanced_html


def simple(data):
    body_content = plain_text_to_advanced_html(data)
    return f"""<!DOCTYPE html>
    <html lang="en">
    <head>
      <style>
        body {{
          margin: 0; padding: 0; background: #f4f6f8; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #333;
        }}
        .container {{
          max-width: 640px;
          margin: 40px auto;
          background: #ffffff;
          border-radius: 8px;
          padding: 30px 40px;
          box-shadow: 0 0 20px rgba(0,0,0,0.08);
          box-sizing: border-box;
          word-wrap: break-word;
        }}
        h1, h2, h3 {{
          color: #222;
          margin-bottom: 12px;
        }}
        p {{
          line-height: 1.6;
          font-size: 16px;
          margin-bottom: 1.25em;
        }}
        ul, ol {{
          margin: 1em 0 1.25em 20px;
          padding: 0;
        }}
        li {{
          margin-bottom: 8px;
        }}
        a {{
          color: #1a73e8;
          text-decoration: none;
        }}
        a:hover {{
          text-decoration: underline;
        }}
        @media (max-width: 640px) {{
          .container {{
            margin: 20px;
            padding: 20px;
          }}
        }}
      </style>
    </head>
    <body>
      <div class="container" role="main" aria-label="Email content">
        {body_content}
      </div>
    </body>
    </html>"""
