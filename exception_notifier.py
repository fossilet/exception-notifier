"""Mail uncaught exceptions to developers.
"""

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import socket
import traceback
import cgitb
import sys
import os
import os.path

# Stolen from six: https://bitbucket.org/gutworth/six
# Useful for very coarse version differentiation.
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
if PY3:
    from io import StringIO
else:
    from StringIO import StringIO

__version__ = '0.3.1'

_log_name = os.getenv('USERNAME' if sys.platform == 'win32' else 'USER')


def _send_email(sender, receivers, subject, body, mail_server):
    """Send email to addresses.
    Note: authentication to SMTP server is currently not support yet.

    sender: sender's email address
    receivers: list of receivers email addresses
    body: string of email body
    mail_server: host of SMTP server

    This function should be robust.
    """
    msg = MIMEMultipart('alternative')
    if PY3:
        msg['subject'] = str(subject, encoding='utf-8')
    else:
        msg['subject'] = str(subject).decode('utf-8')
    msg['From'] = sender
    msg['To'] = ','.join(receivers)
    msg.attach(MIMEText(body, 'html', 'utf-8'))

    s = smtplib.SMTP(mail_server)
    s.sendmail(msg['From'], receivers, msg.as_string())
    # Print to stderr to facilitate doctest.
    sys.stderr.write("'%s' sent to %s" % (subject, ','.join(receivers)))
    s.quit()


def mail_exception(sender=_log_name, receivers=[_log_name],
                   mail_server='localhost', callback=None, args=(), kwargs={},
                   both=False):
    """Notify user when an exception is raised in the wrapped function.

    sender: sender's email address. Defaults to the name of the current user.
    receivers: list of receivers' email addresses. Defaults to the name of the
    current user.
    mail_server: host of SMTP server. Defaults to 'localhost'.
    callback: callback function when an exception is encountered. Defaults to
    None, then the exception information is mailed.
    args: argument tuple for the callback function invocation. Defaults to ().
    kwargs: keyword arguments dictionary for the callback function invocation.
    Defaults to {}.
    both: if True, both the mail routine and callback function will be called.
    Defaults to False.
    """
    def decorator(func):
        def wrapper(*fargs, **fkwargs):
            try:
                return func(*fargs, **fkwargs)
            except Exception:
                return _notify(sender, receivers, mail_server, callback, args,
                               kwargs, both)
        return wrapper
    return decorator


def _get_subject(evalue):
    """ Returns email subject.
    """
    hostname = socket.gethostname()
    # RFC 2822's hard limit is 998 characters per line. So, minus
    # "Subject: " the actual subject must be no longer than 989
    # characters. (Copied from Django source).
    subject = ('%s: %s: %s' % (hostname, os.path.basename(__file__),
                               evalue))[:989]
    return subject


def _get_body(exc_info=None):
    """ Returns email body.
    """
    # Write cgitb output to a variable
    bodyf = StringIO()
    sys_stderr_orig = sys.stderr
    sys.stderr = bodyf
    cgitb.Hook(file=bodyf, context=7, format='html').handle(exc_info)
    sys.stderr = sys_stderr_orig
    body = bodyf.getvalue()
    bodyf.close()
    return body


def _notify(sender, receivers, mail_server, callback, args, kwargs, both):
    """ Returns exception email suject and body formatted by cgitb module.
    """
    traceback.print_exc()

    evalue = sys.exc_info()[1]
    subject = _get_subject(evalue)
    body = _get_body()

    if callback is None:
        _send_email(sender, receivers, subject, body, mail_server)
    elif both:
        _send_email(sender, receivers, subject, body, mail_server)
        return callback(*args, **kwargs)
    else:
        return callback(*args, **kwargs)


def _notifiy_hook(etype, evalue, etb):
    """ Exception hook that notifies exception info.
    sys.exc_info() is empty here, while the latest exception info is
    available in etype, evalue and etb.
    XXX: coverage does not count this function as covered.
    """
    # Default exception hook to display exception info.
    sys.__excepthook__(etype, evalue, etb)

    subject = _get_subject(evalue)
    body = _get_body((etype, evalue, etb))

    t = _notifiy_hook  # this function
    if t.callback is None:
        _send_email(t.sender, t.receivers, subject, body, t.mail_server)
    elif t.both:
        _send_email(t.sender, t.receivers, subject, body, t.mail_server)
        return t.callback(*t.args, **t.kwargs)
    else:
        return t.callback(*t.args, **t.kwargs)


def _hook_wrapper(sender, receivers, mail_server, callback,
                  args, kwargs, both):
    """ Returns a dummy exception hook, before it notifies exceptions.
    """
    # An (awkward) way to avoid unnecessary class.
    hook = _notifiy_hook
    setattr(hook, 'sender', sender)
    setattr(hook, 'receivers', receivers)
    setattr(hook, 'mail_server', mail_server)
    setattr(hook, 'callback', callback)
    setattr(hook, 'args', args)
    setattr(hook, 'kwargs', kwargs)
    setattr(hook, 'both', both)
    return hook


def enable(sender=_log_name, receivers=[_log_name], mail_server='localhost',
           callback=None, args=(), kwargs={}, both=False):
    """ Override default exception hook with our new hook.
    Arguments meaning are the same with mail_exception.

    Note that if both enable and mail_exception are in effect, enable will be
    shadowed by mail_exception, since exceptions are caught by
    mail_exception first.
    """
    sys.excepthook = _hook_wrapper(sender, receivers, mail_server, callback,
                                   args, kwargs, both)


def disable():
    """ Disable our exception hook and restore to the system default.
    """
    sys.excepthook = sys.__excepthook__
