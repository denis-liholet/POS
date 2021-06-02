import sys
import traceback

from flask_mail import Mail, Message

from app import app
from config import RECEPIENTS


@app.errorhandler(500)
def internal_server_error(error):

    # error information collecting and preparing message body
    tb_object = sys.exc_info()[2]
    tb_info = traceback.format_tb(tb_object)
    tb_info = ''.join([str(item) for item in tb_info])
    info = str(tb_info) + str(sys.exc_info()[1])

    # sending an email with error description
    mail = Mail(app)
    msg = Message('Internal server error: 500', recipients=RECEPIENTS)
    msg.body = info
    mail.send(msg)

    message_1 = '<h1>An unexpected error has occurred</h1>'
    message_2 = '<p>The administrator has been notified. Sorry for the inconvenience!</p>'

    return message_1 + message_2, 500


@app.errorhandler(404)
def internal_server_error(error):
    message = '<h1>Sorry, but this page does not exist yet</h1>'
    return message, 404
