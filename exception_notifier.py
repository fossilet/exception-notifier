'''Mail uncaught exceptions to developers.
'''

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import socket
import traceback
import cgitb
import sys
import os.path


def send_email(sender, receivers, subject, body, mail_server):
    '''Send email to addresses.
    Note: authentication to SMTP server is currently not support yet.

    sender: sender's email address
    receivers: list of receivers email addresses
    body: string of email body
    mail_server: host of SMTP server

    This function should be robust.
    '''
    msg = MIMEMultipart('alternative')
    msg['subject'] = str(subject).decode('utf-8')
    msg['From'] = sender
    msg['To'] = ','.join(receivers)
    msg.attach(MIMEText(body, 'html', 'utf-8'))

    s = smtplib.SMTP(mail_server)
    s.sendmail(msg['From'], receivers, msg.as_string())
    print "'%s' sent to %s" % (subject, ','.join(receivers))
    s.quit()


class WriteableObject(file):
    def __init__(self):
        self.content = ''

    def write(self, string):
        self.content += string


def mail_exception(sender, receivers, mail_server='localhost', callback=None,
                   args=(), kwargs=None, both=False):
    '''Notify user when an exception is raised in the wrapped function.

    sender: sender's email address
    receivers: list of receivers email addresses
    mail_server: host of SMTP server. Defaults to 'localhost'.
    callback: callback function when an exception is encountered. Defaults to
    None, then the exception information is mailed.
    args: argument tuple for the callback function invocation. Defaults to ().
    kwargs: keyword arguments dictionary for the callback function invocation.
    Defaults to {}.
    both: if True, both the mail routine and callback function will be called.
    Defaults to False.
    '''
    if not kwargs:
        kwargs = {}

    def decorator(func):
        def wrapper(*fargs, **fkwargs):
            try:
                return func(*fargs, **fkwargs)
            except Exception as e:
                hostname = socket.gethostname()
                # RFC 2822's hard limit is 998 characters per line. So, minus
                # "Subject: " the actual subject must be no longer than 989
                # characters. (Copied from Django source).
                subject = '%s: %s: %s' % (hostname,
                        os.path.basename(__file__), e)[:989]
                traceback.print_exc()

                # Write cgitb output to a variable
                bodyf = WriteableObject()
                sys_stderr_orig = sys.stderr
                sys.stderr = bodyf
                cgitb.Hook(file=bodyf, context=7, format='html').handle()
                sys.stderr = sys_stderr_orig
                body = bodyf.content

                if callback is None:
                    send_email(sender, receivers, subject, body, mail_server)
                elif both:
                    callback(*args, **kwargs)
                    send_email(sender, receivers, subject, body, mail_server)
                else:
                    callback(*args, **kwargs)
        return wrapper
    return decorator
