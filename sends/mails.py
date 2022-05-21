import logging
import smtplib
import email.encoders as encoders
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from os.path import join, dirname, realpath
from datetime import datetime

def send_email ( valuation_data,  result_path ):

    logging.info("Sending Email for Ticker" )

    img_paths = valuation_data.report_paths
    now = datetime.now()
    date_str = now.strftime("%d, %B %Y'")


    smtp_port = 587
    smtp_server = "smtp.gmail.com"
    login = "mart.cuent@gmail.com" # paste your login generated by Mailtrap
    password = "rpfglzmbmzmcxtqb"

    sender_email = "relatio.sa@gmail.com"
    receiver_email = "relatio.sa@gmail.com"
    message = MIMEMultipart("alternative")
    stock_info = " Ticker " + valuation_data.ticker + " "+ valuation_data.valuation + " Margin: "+valuation_data.margin_value +" Growth:"+ valuation_data.growth_rank
    message["Subject"] = "Stock Report "+ stock_info
    message["From"] = sender_email
    message["To"] = receiver_email

    templateLoader = FileSystemLoader(searchpath=dirname(realpath(__file__)))
    env = Environment(loader=templateLoader)
    template = env.get_template('template.html')

    html = template.render(img_paths=img_paths, stock_info=stock_info)  # this is where to put args to the template renderer

    logging.info(html)

    part = MIMEText(html, "html")
    message.attach(part)

    for image_name in img_paths:
        fp = open(image_name, 'rb')
        image = MIMEImage(fp.read())
        
        # Specify the  ID according to the img src in the HTML part
        image.add_header('Content-ID', '<'+image_name+'>')
        message.attach(image)
        mime = MIMEBase('image', 'png', filename=image_name)
        # add required header data:
        mime.add_header('Content-Disposition', 'attachment', filename=image_name)
        mime.add_header('X-Attachment-Id', image_name+'-attch')
        mime.add_header('Content-ID', '<'+image_name+'-attch>')
        # read attachment file content into the MIMEBase object
        mime.set_payload(fp.read())
        # encode with base64
        encoders.encode_base64(mime)
        message.attach(mime)
        fp.close()

    # send your email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.ehlo()
        server.starttls()
        server.login(login, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
            )
    logging.info('Sent')


