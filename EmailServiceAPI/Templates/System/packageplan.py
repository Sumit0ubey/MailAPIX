from EmailServiceAPI.utils import encodedUPI

def packagesPlan():
    upi_id = "sumit2003dubey@ibl"
    upi_redirect_url = "https://sumit0ubey.github.io/HelperWebPages/upi_redirect.html"
    card1 = f'{upi_redirect_url}?upi={encodedUPI(f"upi://pay?pa={upi_id}&pn=Email_Server_API&am=30&cu=INR&tn=Newbie_Pack")}'
    card2 = f'{upi_redirect_url}?upi={encodedUPI(f"upi://pay?pa={upi_id}&pn=Email_Server_API&am=300&cu=INR&tn=Veteran_Pack")}'
    card3 = f'{upi_redirect_url}?upi={encodedUPI(f"upi://pay?pa={upi_id}&pn=Email_Server_API&am=450&cu=INR&tn=Creator_Pack")}'
    card4 = f'{upi_redirect_url}?upi={encodedUPI(f"upi://pay?pa={upi_id}&pn=Email_Server_API&am=3423&cu=INR&tn=Owner_Pack")}'
    refund_policy_link = "#"
    return f"""
    <html lang="en"><head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Email Quota Packages</title>
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
        .price {{
          color: #e91e63;
          font-size: 20px;
          font-weight: bold;
          margin: 12px 0;
        }}
        .button {{
          background: linear-gradient(to right, #3b82f6, #2563eb);
          color: #ffffff;
          padding: 10px 24px;
          border-radius: 6px;
          text-decoration: none;
          font-weight: bold;
          font-size: 14px;
          display: inline-block;
          transition: background 0.3s ease;
        }}
        .button:hover {{
          background: linear-gradient(to right, #2563eb, #1d4ed8);
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
        <h2>Email Quota Packages</h2>

        <div class="card">
          <h3>Newbie Pack</h3>
          <p>Increases your email quota by 50 &amp; default by 3.</p>
          <div class="price">₹30.00</div>
          <a href="{card1}" class="button">Buy Now</a>
        </div>

        <div class="card">
          <h3>Veteran Pack</h3>
          <p>Increases your email quota by 699 &amp; default by 39.</p>
          <div class="price">₹299.99</div>
          <a href="{card2}" class="button">Buy Now</a>
        </div>

        <div class="card">
          <h3>Creator Pack</h3>
          <p>Increases default email service quota by 400.</p>
          <div class="price">₹449.99</div>
          <a href="{card3}" class="button">Buy Now</a>
        </div>

        <div class="card">
          <h3>Owner Pack</h3>
          <p>Increases your email quota by 99999.</p>
          <div class="price">₹3422.99</div>
          <a href="{card4}" class="button">Buy Now</a>
        </div>

        <div class="card">
          <p><strong>Note:</strong> After payment, please reply to this email with an attached payment receipt (screenshot) and transaction ID.</p>
        </div>

        <div class="auto-note">
          ⚠️ Please note: Any payment made is not refundable.<br>
          For more information, please review our Refund Policy.
        </div>

        <div class="footer">
          Sent by <a href="https://github.com/Sumit0ubey">Email Service API</a> • All rights reserved © 2025<br>
          <a href="{refund_policy_link}">Refund Policy</a>
        </div>
      </div>

    </body></html>
    """
