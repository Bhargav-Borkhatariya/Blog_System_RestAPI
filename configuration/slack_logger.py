import requests
import json
import time
from copy import copy
from django.conf import settings
from django.utils.log import AdminEmailHandler
from django.views.debug import ExceptionReporter

# from django_slack_logger.logger import SlackExceptionHandler
print("slack_logger")


class SlackExceptionHandler(AdminEmailHandler):
    print("SlackExceptionHandler")

    # replacing default django emit (https://github.com/django/django/blob/master/django/utils/log.py)
    def emit(self, record, *args, **kwargs):
        print("emit(record, *args, **kwargs")
        # original AdminEmailHandler "emit" method code (but without actually sending email)
        if not getattr(self, "_emitted", False):
            self._emitted = True
            try:
                request = record.request
                subject = "%s (%s IP): %s" % (
                    record.levelname,
                    (
                        "internal"
                        if request.META.get("REMOTE_ADDR") in settings.INTERNAL_IPS
                        else "EXTERNAL"
                    ),
                    record.getMessage(),
                )
            except Exception:
                subject = "%s: %s" % (record.levelname, record.getMessage())
                request = None
            subject = self.format_subject(subject)

            no_exc_record = copy(record)
            no_exc_record.exc_info = None
            no_exc_record.exc_text = None

            if record.exc_info:
                exc_info = record.exc_info
            else:
                exc_info = (None, record.getMessage(), None)

            reporter = ExceptionReporter(request, is_email=True, *exc_info)
            message = "%s\n\n%s" % (
                self.format(no_exc_record),
                reporter.get_traceback_text(),
            )
            html_message = reporter.get_traceback_html() if self.include_html else None

            user_info = {
                "username": request.user.username
                if request.user.is_authenticated
                else "Anonymous",
                "id": str(request.user.pk) if request.user.is_authenticated else "N/A",
            }

            attachments = [
                {
                    "title": subject,
                    "color": "danger",
                    "fields": [
                        {
                            "title": "Level",
                            "value": record.levelname,
                            "short": True,
                        },
                        {
                            "title": "Method",
                            "value": request.method if request else "No Request",
                            "short": True,
                        },
                        {
                            "title": "Path",
                            "value": request.path if request else "No Request",
                            "short": True,
                        },
                        {
                            "title": "User",
                            "value": (
                                (
                                    user_info["username"] + " (" + user_info["id"] + ")"
                                    if request.user.is_authenticated
                                    else "Anonymous"
                                )
                                if request
                                else "No Request"
                            ),
                            "short": True,
                        },
                        {
                            "title": "Status Code",
                            "value": record.status_code,
                            "short": True,
                        },
                        {
                            "title": "UA",
                            "value": (
                                request.META["HTTP_USER_AGENT"]
                                if request and request.META
                                else "No Request"
                            ),
                            "short": False,
                        },
                        {
                            "title": "GET Params",
                            "value": json.dumps(request.GET)
                            if request
                            else "No Request",
                            "short": False,
                        },
                        {
                            "title": "POST Data",
                            "value": json.dumps(request.POST)
                            if request
                            else "No Request",
                            "short": False,
                        },
                        {
                            "title": "Exception Type",
                            "value": record.exc_info[0].__name__
                            if record.exc_info
                            else "N/A",
                            "short": True,
                        },
                        {
                            "title": "Exception Value",
                            "value": str(record.exc_info[1])
                            if record.exc_info
                            else "N/A",
                            "short": True,
                        },
                        {
                            "title": "Exception Location",
                            "value": f"{record.pathname}, line {record.lineno}",
                            "short": True,
                        },
                        {
                            "title": "Raised During",
                            "value": record.funcName,
                            "short": True,
                        },
                        {
                            "title": "Python Executable",
                            "value": record.pathname,
                            "short": True,
                        },
                        {
                            "title": "Python Version",
                            "value": record.module,
                            "short": True,
                        },
                        {
                            "title": "Python Path",
                            "value": record.pathname,
                            "short": False,
                        },
                    ],
                },
            ]

            main_text = "Error at " + time.strftime(
                "%A, %d %b %Y %H:%M:%S +0000", time.gmtime()
            )

            data = {
                "payload": json.dumps(
                    {"main_text": main_text, "attachments": attachments}
                ),
            }
            # setup channel webhook
            webhook_url = "https://hooks.slack.com/services/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"

            # send it
            r = requests.post(webhook_url, data=data)
