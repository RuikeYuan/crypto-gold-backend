#!/usr/bin/env python3
"""Django's command-line utility for administrative tasks."""
import os
import sys
import logging

from django.core.management import execute_from_command_line

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    # try:
    execute_from_command_line()
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Starting Django setup")
    execute_from_command_line(sys.argv)
    logging.debug("Django setup complete")
    # except ImportError as exc:
    #     raise ImportError(
    #         "Couldn't import Django. Are you sure it's installed and "
    #         "available on your PYTHONPATH environment variable? Did you "
    #         "forget to activate a virtual environment?"
    #     ) from exc


if __name__ == '__main__':
    main()
