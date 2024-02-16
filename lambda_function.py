import smtplib
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# --- Configuration Section ---
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
USERNAME = 'your_email@gmail.com'  # Replace with your email address
PASSWORD = 'your_password'  # Replace with your password
SENDER = 'Your Name or Bot Name'  # Sender name
RECIPIENTS = ['example1@example.com', 'example2@example.com']  # Recipient email addresses

# --- Utility Functions ---


def round_if_not_none(val):
    return round(val, 2) if val is not None else None


def get_last_trading_day_data(data, offset):
    if len(data) > offset:
        return round_if_not_none(data['Close'].iloc[-1-offset])
    return None


# --- Email Sending Function ---
def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = SENDER
    msg['To'] = ', '.join(RECIPIENTS)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(USERNAME, PASSWORD)
            server.sendmail(SENDER, RECIPIENTS, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")


def index_collector():
    indexes = {
        'Dow Jones Industrial Average': '^DJI',  # Dow Jones
        'S&P 500': '^GSPC',  # S&P 500
        'NASDAQ Composite': '^IXIC',  # NASDAQ
        'Crude Oil': 'CL=F',  # Crude Oil futures
        'Gold': 'GC=F',  # Gold futures
        'Silver': 'SI=F',  # Silver futures
        'CBOE Interest Rate 10 Year T No': '^TNX'  # 10 Year Treasury Note
    }

    data_dict = {
        'Index': [],
        'Current Price': [],
        'Prev. Close': [],
        "Today's Change": [],
        'L.W. Close': [],
        '1-Week Change': []
    }

    end_date = datetime.now()
    start_date = end_date - timedelta(days=14)  # Extend to two weeks

    for name, symbol in indexes.items():
        ticker = yf.Ticker(symbol)
        historical_data = ticker.history(start=start_date, end=end_date)

        current_price = round_if_not_none(historical_data['Close'].iloc[-1]) if not historical_data[
            'Close'].empty else None
        prev_close = get_last_trading_day_data(historical_data, 1)
        todays_change = round_if_not_none(
            current_price - prev_close) if prev_close is not None and current_price is not None else None
        price_last_week = get_last_trading_day_data(historical_data, 5)
        one_week_change = round_if_not_none(
            current_price - price_last_week) if current_price is not None and price_last_week is not None else None

        data_dict['Index'].append(name)
        data_dict['Current Price'].append(f"{current_price:.2f}")
        data_dict['Prev. Close'].append(f"{prev_close:.2f}")
        data_dict["Today's Change"].append(f"{todays_change:.2f}")
        data_dict['L.W. Close'].append(f"{price_last_week:.2f}")
        data_dict['1-Week Change'].append(f"{one_week_change:.2f}")

    # Create DataFrame
    df = pd.DataFrame(data_dict)

    # Apply Styling
    styled_df = df.style.set_table_styles(
        [{
            'selector': 'th',
            'props': [
                ('background-color', '#f4f4f4'),
                ('color', '#0c0c0d'),
                ('font-family', 'Arial, sans-serif'),
                ('font-size', '16px'),
                ('font-weight', '600'),
                ('text-align', 'center')  # center text in header cells
            ]
        },
            {
                'selector': 'td',
                'props': [
                    ('font-family', 'Arial, sans-serif'),
                    ('font-size', '14px'),
                    ('font-weight', '500'),
                    ('text-align', 'center')  # center text in data cells
                ]
            }]
    ).set_properties(**{
        'border-color': 'black',
        'border-width': '2px',
        'border-style': 'solid'
    }).set_table_attributes('style="border-collapse: collapse; width:100%;"')

    # Convert styled DataFrame to HTML
    html_body = styled_df.to_html()

    return html_body


# --- Execution Point ---
def lambda_handler(event, context):
    try:
        data = index_collector()
        current_date = datetime.now().strftime("%m/%d/%Y")
        subject = f"Index Report ({current_date})"

        send_email(subject, data)

    except Exception as e:
        error_message = f"Failed to gather data: {str(e)}"
        send_email('Stock Data Gathering Error', error_message)
