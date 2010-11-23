""" Testing gitwash dumper
"""

import os
from os.path import join as pjoin, dirname, split as psplit
import shutil
from tempfile import mkdtemp
from subprocess import call

from nose.tools import assert_true, assert_false, assert_equal, assert_raises

_downpath, _ = psplit(dirname(__file__))
_downpath = os.path.abspath(_downpath)
EXE_PTH = pjoin(_downpath, 'gitwash_dumper.py')
DOC_DIR = pjoin(_downpath, 'gitwash')
TMPDIR = None

def setup():
    global TMPDIR
    TMPDIR = mkdtemp()


def teardown():
    #shutil.rmtree(TMPDIR)
    print TMPDIR


def test_dumper():
    call([EXE_PTH,
          TMPDIR,
          'my_project'])
    gitwdir = pjoin(TMPDIR, 'gitwash')
    assert_true(os.path.isdir(gitwdir))
    for dirpath, dirnames, filenames in os.walk(gitwdir):
        if not dirpath.endswith('gitwash'):
            raise RuntimeError('I only know about the gitwash directory')
        for filename in filenames:
            print filename
            old_fname = pjoin(DOC_DIR, filename)
            new_fname = pjoin(dirpath, filename)
            old_contents = file(old_fname, 'rt').readlines()
            new_contents = file(new_fname, 'rt').readlines()
            for old, new in zip(old_contents, new_contents):
                if 'PROJECT' in old and not filename.endswith('.inc'):
                    assert_false('PROJECT' in new)
                    assert_true('my_project' in new)


