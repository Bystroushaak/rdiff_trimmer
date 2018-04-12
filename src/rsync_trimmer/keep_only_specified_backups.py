#! /usr/bin/env python
import os
import os.path
import sys
import argparse
from shutil import rmtree
from tempfile import mkdtemp
from collections import defaultdict

import sh


class RsyncAPI(object):
    def __init__(self, rsync_dir, tmp_dir=None):
        self.rsync_dir = rsync_dir

        self._tmp_dir = tmp_dir
        if self._tmp_dir is None:
            self._tmp_dir = mkdtemp()

    def yield_increments(self):
        increments = sh.rdiff_backup("-l", self.rsync_dir)

        for increment in increments:
            if ".dir" not in increment:
                continue
            if not increment.strip().startswith("increments."):
                continue

            yield increment.strip().split(".")[1]

    def restore(self, out_dir, time):
        sh.rdiff_backup("-r", time, self.rsync_dir, out_dir)

    def add_increment(self, from_dir):
        sh.rdiff_backup(from_dir, self.rsync_dir)

    def restore_into(self, out_dir, increments_to_keep):
        print "increments to keep", increments_to_keep

        out_rsync = RsyncAPI(out_dir)
        for increment in sorted(increments_to_keep):
            rmtree(self._tmp_dir)
            os.mkdir(self._tmp_dir)

            print "Restoring", increment

            self.restore(self._tmp_dir, increment)
            out_rsync.add_increment(self._tmp_dir)

        rmtree(self._tmp_dir)
        return out_rsync


def remove_even(rsync_dir, out_dir):
    rsync = RsyncAPI(rsync_dir)

    odd_increments = [
        increment for cnt, increment in enumerate(rsync.yield_increments())
        if ((cnt + 1) % 2) != 0
    ]

    rsync.restore_into(out_dir, odd_increments)


def keep_one_for_each_month(rsync_dir, out_dir, all_from_last_3_months=True):
    rsync = RsyncAPI(rsync_dir)

    def get_month_date(increment):
        return increment.split("T")[0].rsplit("-", 1)[0]

    month_tracker = defaultdict(list)
    for increment in rsync.yield_increments():
        month_tracker[get_month_date(increment)].append(increment)

    last_from_each_month = {
        increments[-1]
        for increments in month_tracker.itervalues()
    }

    if all_from_last_3_months:
        all_months = sorted(month_tracker.keys())

        last_from_each_month.update(month_tracker[all_months[-1]])

        if len(all_months) >= 2:
            last_from_each_month.update(month_tracker[all_months[-2]])
        if len(all_months) >= 3:
            last_from_each_month.update(month_tracker[all_months[-3]])

    rsync.restore_into(out_dir, sorted(last_from_each_month))


def _check_multiple_parameters(args):
    counter = 0

    if args.list:
        counter += 1
    if args.each_month:
        counter += 1
    if args.remove_even:
        counter += 1

    return counter > 1


def main(args):
    if args.list and not os.path.exists(args.list):
        sys.stderr.write("Increment list file `%s` not found!\n" % args.list)
        sys.exit(1)

    if not os.path.exists(args.rsync_dir):
        sys.stderr.write("rsync directory `%s` not found!\n" % args.rsync_dir)
        sys.exit(1)

    if _check_multiple_parameters(args):
        sys.stderr.write(
            "You can set only one of --keep-increments OR --one-for-each-month"
            " OR --remove-even, not all at once!\n"
        )
        sys.exit(1)

    if args.out_dir is None:
        args.out_dir = args.rsync_dir + "_trimmed"

    if args.remove_even:
        remove_even(args.rsync_dir, args.out_dir)
    elif args.each_month:
        keep_one_for_each_month(args.rsync_dir, args.out_dir)
    elif args.list:
        with open(args.list) as f:
            increments_to_keep = [
                x.strip().split()[0]
                for x in f.read().splitlines()
            ]

        RsyncAPI(args.rsync_dir).restore_into(args.out_dir, increments_to_keep)
    else:
        sys.stderr.write("No action selected. Use --help for list.\n")
        sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-k",
        "--keep-increments",
        dest="list",
        help="Keep only increments listed in this file."
    )
    parser.add_argument(
        "-o",
        "--one-for-each-month",
        dest="each_month",
        action="store_true",
        help="Keep only one backup for each month."
    )
    parser.add_argument(
        "-e",
        "--remove-even",
        action="store_true",
        help="Remove even backups. Reduce number of backups to half."
    )
    parser.add_argument(
        "rsync_dir",
        metavar="RSYNC_DIR",
        help="Path to the rsync directory."
    )
    parser.add_argument(
        "out_dir",
        default=None,
        nargs='?',
        metavar="OUT_DIR",
        help=(
            "Path to the trimmed OUTPUT rsync directory. "
            "Default `{{RSYNC_DIR}}_trimmed`."
        )
    )

    args = parser.parse_args()

    main(args)
