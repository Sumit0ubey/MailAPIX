from os import getenv
from dotenv import load_dotenv

from EmailServiceAPI.utils import encodedUPI

load_dotenv()

WEBSITE_LINK = getenv("WEBSITE_LINK", "#")
REFUND_POLICY_LINK = getenv("REFUND_POLICY_LINK", "#")
UPI_REDIRECT_URL = getenv("UPI_REDIRECT_URL", "https://sumit0ubey.github.io/HelperWebPages/upi_redirect.html")
UPI_ID = getenv("UPI_ID", "#")
NEWBIE_PACK_PRICE = getenv("NEWBIE_PACK", "30")
VETERAN_PACK_PRICE = getenv("VETERAN_PACK", "300")
CREATOR_PACK_PRICE = getenv("CREATOR_PACK", "450")
OWNER_PACK_PRICE = getenv("OWNER_PACK", "3423")
CURRENCY = getenv("CURRENCY", "INR")

def packagesPlan():
    card1 = f'{UPI_REDIRECT_URL}?upi={encodedUPI(f"upi://pay?pa={UPI_ID}&pn=MailApix_API&am={NEWBIE_PACK_PRICE}&cu={CURRENCY}&tn=Newbie_Pack")}'
    card2 = f'{UPI_REDIRECT_URL}?upi={encodedUPI(f"upi://pay?pa={UPI_ID}&pn=MailApix_API_API&am={VETERAN_PACK_PRICE}&cu={CURRENCY}&tn=Veteran_Pack")}'
    card3 = f'{UPI_REDIRECT_URL}?upi={encodedUPI(f"upi://pay?pa={UPI_ID}&pn=MailApix_API_API&am={CREATOR_PACK_PRICE}&cu={CURRENCY}&tn=Creator_Pack")}'
    card4 = f'{UPI_REDIRECT_URL}?upi={encodedUPI(f"upi://pay?pa={UPI_ID}&pn=MailApix_API_API&am={OWNER_PACK_PRICE}&cu={CURRENCY}&tn=Owner_Pack")}'
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
          Sent by <a href="{WEBSITE_LINK}">MailApix API</a> • All rights reserved © 2025<br>
          <a href="{REFUND_POLICY_LINK}">Refund Policy</a>
        </div>
      </div>

    </body></html>
    """
