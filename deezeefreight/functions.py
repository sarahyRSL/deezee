import re
import os
import traceback
import mailtrap as mt
from dotenv import load_dotenv

load_dotenv(override=True)

def validate_phone_number(phone_number):
    match = re.search(pattern, phone_number)
    if match:
        return True
    return False

pattern = re.compile(r"(\+\d{1,3})?\s?\(?\d{1,4}\)?[\s.-]?\d{3}[\s.-]?\d{4}")

def send_email(type, entry):
    sender = str(os.getenv('SENDER'))
    token = str(os.getenv('TOKEN'))
    recipient = os.getenv('RECIPIENT').strip('"').strip("'")
    host = str(os.getenv('HOST_URL'))
    if type == 'vendor':
        template = os.getenv('VENDOR_TEMPLATE')
        template_variables={
            "name": str(entry['name']),
            "email": str(entry['email']),
            "company": str(entry['company']),
            "phone": str(entry['phone']),
            "address": f"{entry.get('address', '')}, {entry.get('address2', '')}",
            "city": str(entry['city']),
            "zip": str(entry['zip']),
            "country": str(entry['country']),
            "addresses": '\n'.join(entry['addresses'])
        }
    else :
        template = os.getenv('EMPLOYEE_TEMPLATE')
        template_variables={
            "name": str(entry['name']),
            "email": str(entry['email']),
            "phone": str(entry['phone'])
        }
    
    print('sender:', sender, '\nrecipient:', recipient, '\ntemplate:', template, '\nvars:', template_variables)
    try:
        mail = mt.MailFromTemplate(
            sender=mt.Address(email=sender, name="DeeZee New Vendor"),
            to=[mt.Address(email=recipient)],
            template_uuid=template,
            template_variables=template_variables
        )   
        client = mt.MailtrapClient(token=token, api_host=host)
        response = client.send(mail)
        print('recipient', recipient)

        print(response)
        return 'success'
    except Exception as e:
        traceback.print_exc()
        print('Mailing Error:', e)
        return 'error'
