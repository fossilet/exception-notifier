'''Mail uncaught exceptions to developers.

Copyright (C) Yongzhi Pan 2012 <panyongzhi@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from email.mime.text import MIMEText
import smtplib
import socket
import traceback


def send_email(sender, receivers, subject, body, mail_server):
    '''Send email to addresses.
    Note: authentication to SMTP server is currently not support yet.

    sender: sender's email address
    receivers: list of receivers email addresses
    body: string of email body
    mail_server: host of SMTP server

    This function should be robust.
    '''
    msg = MIMEText(body)
    msg['subject'] = str(subject).decode('utf-8')
    msg['From'] = sender
    msg['To'] = ','.join(receivers)

    s = smtplib.SMTP(mail_server)
    s.sendmail(msg['From'], receivers, msg.as_string())
    print "'%s' sent to %s" % (subject, ','.join(receivers))
    s.quit()


def mail_exception(sender, receivers, mail_server='localhost'):
    '''Notify user when an exception is raised in the wrapped function.

    sender: sender's email address
    receivers: list of receivers email addresses
    mail_server: host of SMTP server
    '''
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except Exception as e:
                hostname = socket.gethostname()
                subject = '%s:%s: %s' % (hostname, __file__, e)
                body = traceback.format_exc()
                print body
                send_email(sender, receivers, subject, body, mail_server)
        return wrapper
    return decorator
