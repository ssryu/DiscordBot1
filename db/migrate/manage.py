#!/usr/bin/env python
import os

from migrate.versioning.shell import main

if __name__ == '__main__':
    main(debug='False', url=os.environ.get('DATABASE_URL'), repository='.')
