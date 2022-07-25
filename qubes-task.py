#
# The Qubes OS Project, https://www.qubes-os.org/
#
# Copyright (C) 2022  unman <unman@thirdeyesecurity.org>
#
# Reuses code from qvm-template.py
# Copyright (C) 2019  WillyPillow <wp@nerde.pw>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2.1 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""Tool for managing Tasks."""

import argparse
import collections
import configparser
import datetime
import enum
import fcntl
import fnmatch
import functools
import glob
import itertools
import operator
import os
import re
import rpm
import subprocess
import sys
import typing
import qubesadmin

from qubesadmin.tools.qvm_template import is_match_spec
from qubesadmin.tools.qvm_template import qrexec_popen
from qubesadmin.tools.qvm_template import qubes_release
from qubesadmin.tools.qvm_template import Template as Package

DATE_FMT = '%Y-%m-%d %H:%M:%S'
LOCK_FILE = '/var/tmp/qvm-task.lck'
UPDATEVM = str('global UpdateVM')
PACKAGE_NAME_PREFIX = '3isec-qubes-'
REPO_FILE = ['/etc/yum.repos.d/3isec-dom0.repo']























if __name__ == '__main__':
    sys.exit(main())
