# AutoMarket Reports


## Project Overview
This project automates the collection, analysis, and reporting of financial market data. Utilizing Python and libraries such as `smtplib` for email delivery, `yfinance` for data retrieval, and `pandas` for data manipulation, the system is designed to send daily or weekly financial market reports via email. These reports provide valuable insights into market trends and performances, making it an invaluable tool for investors and financial analysts.

## Features
- **Automated Data Collection:** Fetches data for major financial indices and commodities using `yfinance`.
- **Data Analysis:** Calculates key metrics such as current price, daily change, and weekly trends.
- **Email Reporting:** Sends formatted email reports to a predefined list of recipients with the latest market data.
- **AWS Lambda Deployment:** Hosted on AWS Lambda, allowing for scheduled execution without the need for dedicated server infrastructure.

## Prerequisites
- AWS account
- Python 3.x
- Access to SMTP server credentials for email sending

## Setup and Deployment

### AWS Lambda Configuration
1. **Create a Lambda Function:**
   - Navigate to the AWS Lambda console and create a new function.
   - Choose Python 3.x as the runtime environment.

2. **Add Environment Variables:**
   - Store sensitive information such as SMTP credentials and recipient emails as environment variables in the Lambda function configuration.

3. **Deploy the Script:**
   - Zip your Python script along with any dependencies.
   - Upload the zip file to your Lambda function.

### AWS CloudWatch Event Trigger
1. **Create a CloudWatch Rule:**
   - Go to the CloudWatch console and create a new rule.
   - Define a schedule expression (e.g., `rate(1 day)` for daily execution).

2. **Set the Lambda Function as the Target:**
   - Select your Lambda function as the target for the rule.

3. **Configure Input:**
   - Choose "Constant (JSON text)" and enter `{}` as the input if no specific input is required.

### Email Configuration
- Configure `SMTP_SERVER`, `SMTP_PORT`, `USERNAME`, and `PASSWORD` environment variables in AWS Lambda with your SMTP server details.
- Update the `SENDER` and `RECIPIENTS` variables as necessary.

## Usage
Once deployed and configured, the AWS CloudWatch event will trigger the Lambda function according to the schedule you've set. The function will collect the latest financial market data, generate a report, and send it to the specified recipients.

## Security Considerations
Ensure that SMTP credentials and other sensitive information are securely stored as environment variables and not hardcoded into the script.

## Contributing
Contributions to this project are welcome! Please refer to the contributing guidelines for more details.
