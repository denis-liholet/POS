from pos import app


@app.errorhandler(500)
def internal_server_error(error):
    message_1 = '<h1>An unexpected error has occured</h1>'
    message_2 = '<p>The administrator has been notified. Sorry for the inconvenience!</p>'
    return message_1 + message_2, 500


@app.errorhandler(404)
def internal_server_error(error):
    message = '<h1>Sorry, but this page does not exist yet</h1>'
    return message, 404
