#!/usr/bin/env python
import os
import sys


def main():
    if 'DJANGO_SETTINGS_MODULE' not in os.environ:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError('Could not load Django') from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
