#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import sys

import base64
import json

def main():
    """Run administrative tasks."""   

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
 #   logger_provider.shutdown()


if __name__ == '__main__':

#with tracer.start_as_current_span("my_span_name"):
    
    main()
    # logger_provider.shutdown()
