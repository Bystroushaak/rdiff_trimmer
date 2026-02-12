import os
import sys
from shutil import rmtree
from typing import Iterable
from typing import Iterator
from typing import NamedTuple
from pathlib import Path
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


class Increment(NamedTuple):
    timestamp: int

    @staticmethod
    def from_string(line: str) -> "Increment":
        timestamp = int(line.strip().split()[0])
        return Increment(timestamp)


class RdiffAPI:
    def __init__(
        self,
        rsync_dir: str | Path,
        tmp_dir: str | Path | None = None,
        disable_compression: bool = False,
    ) -> None:
        self.rsync_dir = rsync_dir

        self._tmp_dir = tmp_dir
        if self._tmp_dir is None:
            self._tmp_dir = mkdtemp()

        self._disable_compression = disable_compression

        self._options: list[str] = []

    def __del__(self) -> None:
        if os.path.exists(self._tmp_dir):
            rmtree(self._tmp_dir)

    def yield_increments(self) -> Iterator[Increment]:
        increments = rdiff_backup(
            "--parsable-output",
            "-l",
            self.rsync_dir,
        )

        for increment_line in increments.strip().splitlines():
            if increment_line.strip():
                inc = Increment.from_string(increment_line)
                if inc.timestamp != -1:
                    yield inc

    def restore(self, out_dir: str | Path, time: int) -> None:
        rdiff_backup("-r", time, "--current-time", time, str(self.rsync_dir), out_dir)

    def add_increment(self, from_dir: str | Path, timestamp: int = 0) -> None:
        options = self._options[:]
        if timestamp != 0:
            options.extend(("--current-time", timestamp))

        if self._disable_compression:
            options.append("--no-compression")

        options.append(from_dir)
        options.append(str(self.rsync_dir))

        rdiff_backup(*options)

    def restore_into(
        self,
        out_dir: str | Path,
        increments_to_keep: Iterable[Increment],
        disable_compression: bool = False,
    ) -> "RdiffAPI":
        out_rsync = RdiffAPI(out_dir, disable_compression=disable_compression)
        for increment in sorted(increments_to_keep, key=lambda x: x.timestamp):
            rmtree(self._tmp_dir)
            os.mkdir(self._tmp_dir)

            print("Restoring", increment.timestamp)

            self.restore(self._tmp_dir, increment.timestamp)
            out_rsync.add_increment(self._tmp_dir, increment.timestamp)

        rmtree(self._tmp_dir)
        return out_rsync
