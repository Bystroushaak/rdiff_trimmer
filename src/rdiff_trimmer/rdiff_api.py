# -*- coding: utf-8 -*-
import os
from shutil import rmtree
from tempfile import mkdtemp

import sh


class Increment(object):
    def __init__(self, timestamp):
        self.timestamp = timestamp

    @staticmethod
    def from_string(line):
        timestamp = int(line.strip().split()[0])
        return Increment(timestamp)


class RdiffAPI(object):
    def __init__(self, rsync_dir, tmp_dir=None, disable_compression=False):
        self.rsync_dir = rsync_dir

        self._tmp_dir = tmp_dir
        if self._tmp_dir is None:
            self._tmp_dir = mkdtemp()

        self._disable_compression = disable_compression

        self._options = []

    def yield_increments(self):
        increments = sh.rdiff_backup("--parsable-output", "-l", self.rsync_dir)

        for increment_line in increments:
            yield Increment.from_string(increment_line)

    def restore(self, out_dir, time):
        sh.rdiff_backup("-r", time, self.rsync_dir, out_dir)

    def add_increment(self, from_dir, timestamp=0):
        options = self._options[:]
        if timestamp != 0:
            options.extend(("--current-time", timestamp))

        if self._disable_compression:
            options.append("--no-compression")

        options.append(from_dir)
        options.append(self.rsync_dir)

        sh.rdiff_backup(*options)

    def restore_into(self, out_dir, increments_to_keep,
                     disable_compression=False):
        out_rsync = RdiffAPI(out_dir, disable_compression=disable_compression)
        for increment in sorted(increments_to_keep, key=lambda x: x.timestamp):
            rmtree(self._tmp_dir)
            os.mkdir(self._tmp_dir)

            print "Restoring", increment.timestamp

            self.restore(self._tmp_dir, increment.timestamp)
            out_rsync.add_increment(self._tmp_dir, increment.timestamp)

        rmtree(self._tmp_dir)
        return out_rsync
