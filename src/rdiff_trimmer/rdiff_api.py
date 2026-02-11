import os
import sys
from shutil import rmtree
from tempfile import mkdtemp

import sh


def _pydev_fix_fds_after_sh():
    """
    Fix for pycharm's debugger which is trying to monkeypatch stdin/out and that
    is clashing with `sh` module.
    """
    sys.stdout = os.fdopen(1, "w", buffering=1, closefd=False)
    sys.stderr = os.fdopen(2, "w", buffering=1, closefd=False)


if os.getenv("PYCHARM_HOSTED") == "1":
    rdiff_backup = sh.rdiff_backup.bake(_preexec_fn=_pydev_fix_fds_after_sh)
else:
    rdiff_backup = sh.rdiff_backup.bake()


class Increment:
    def __init__(self, timestamp):
        self.timestamp = timestamp

    @staticmethod
    def from_string(line):
        timestamp = int(line.strip().split()[0])
        return Increment(timestamp)


class RdiffAPI:
    def __init__(self, rsync_dir, tmp_dir=None, disable_compression=False):
        self.rsync_dir = rsync_dir

        self._tmp_dir = tmp_dir
        if self._tmp_dir is None:
            self._tmp_dir = mkdtemp()

        self._disable_compression = disable_compression

        self._options = []

    def __del__(self):
        if os.path.exists(self._tmp_dir):
            rmtree(self._tmp_dir)

    def yield_increments(self):
        increments = rdiff_backup(
            "--parsable-output",
            "-l",
            self.rsync_dir,
        )

        for increment_line in increments.strip().splitlines():
            if increment_line.strip():
                yield Increment.from_string(increment_line)

    def restore(self, out_dir, time):
        rdiff_backup("-r", time, "--current-time", time, str(self.rsync_dir), out_dir)

    def add_increment(self, from_dir, timestamp=0):
        options = self._options[:]
        if timestamp != 0:
            options.extend(("--current-time", timestamp))

        if self._disable_compression:
            options.append("--no-compression")

        options.append(from_dir)
        options.append(str(self.rsync_dir))

        rdiff_backup(*options)

    def restore_into(self, out_dir, increments_to_keep, disable_compression=False):
        out_rsync = RdiffAPI(out_dir, disable_compression=disable_compression)
        for increment in sorted(increments_to_keep, key=lambda x: x.timestamp):
            rmtree(self._tmp_dir)
            os.mkdir(self._tmp_dir)

            print("Restoring", increment.timestamp)

            self.restore(self._tmp_dir, increment.timestamp)
            out_rsync.add_increment(self._tmp_dir, increment.timestamp)

        rmtree(self._tmp_dir)
        return out_rsync
