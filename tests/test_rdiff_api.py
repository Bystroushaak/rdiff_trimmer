#! /usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
import os
import shutil
import os.path
import tempfile

from rdiff_trimmer.rdiff_api import RdiffAPI
from rdiff_trimmer.rdiff_api import Increment


DIR_PATH = os.path.abspath(os.path.dirname(__file__))


class TestIncrement(object):
    def test_increment_from_string(self):
        inc_line = "   1524336818 directory   "

        inc = Increment.from_string(inc_line)

        assert inc.timestamp == 1524336818.0


class TestRdiffAPI(object):
    def setup(self):
        self.ra = RdiffAPI(os.path.join(DIR_PATH, "test_data"))
        self.tmp_dir = tempfile.mkdtemp()
        self.out_ra = RdiffAPI(self.tmp_dir)

    def teardown(self):
        shutil.rmtree(self.tmp_dir)

    def test_yield_increments(self):
        increments = list(self.ra.yield_increments())

        assert len(increments) == 3

        assert increments[1].timestamp == 1524342591.0
        assert increments[2].timestamp == 1524342605.0

    def test_restore_into(self):
        increments = list(self.ra.yield_increments())

        self.ra.restore_into(self.tmp_dir, increments_to_keep=[increments[0]])

        kept_increments = list(self.out_ra.yield_increments())

        assert len(kept_increments) == 1
        assert kept_increments[0].timestamp == increments[0].timestamp

        assert os.path.exists(os.path.join(self.tmp_dir, "content"))
        assert not os.path.exists(os.path.join(self.tmp_dir, "and_more_content"))
