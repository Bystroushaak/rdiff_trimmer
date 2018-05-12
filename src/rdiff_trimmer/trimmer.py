# -*- coding: utf-8 -*-
import os
import os.path
import sys

import datetime
from collections import defaultdict

from rdiff_api import RdiffAPI
from rdiff_api import Increment


def remove_even(rsync_dir, out_dir, disable_compression=False):
    rsync = RdiffAPI(rsync_dir)

    odd_increments = [
        increment for cnt, increment in enumerate(rsync.yield_increments())
        if ((cnt + 1) % 2) != 0
    ]

    rsync.restore_into(
        out_dir,
        odd_increments,
        disable_compression=disable_compression
    )


def keep_one_for_each_month(rsync_dir, out_dir, all_from_last_3_months=True,
                            disable_compression=False):
    rsync = RdiffAPI(rsync_dir)

    def get_month_date(increment):
        date = datetime.datetime.fromtimestamp(increment.timestamp)
        return date.strftime('%Y-%m')

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

    rsync.restore_into(
        out_dir,
        sorted(last_from_each_month),
        disable_compression=disable_compression
    )


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
        args.out_dir = os.path.abspath(args.rsync_dir) + "_trimmed"

    if args.remove_even:
        remove_even(args.rsync_dir, args.out_dir, args.disable_compression)
    elif args.each_month:
        keep_one_for_each_month(
            args.rsync_dir,
            args.out_dir,
            args.disable_compression
        )
    elif args.list:
        with open(args.list) as f:
            increments_to_keep = [
                Increment.from_string(x.strip().split()[0])
                for x in f.read().splitlines()
            ]

        rdiff = RdiffAPI(args.rsync_dir)
        rdiff.restore_into(
            args.out_dir,
            increments_to_keep,
            disable_compression=args.disable_compression
        )
    else:
        sys.stderr.write("No action selected. Use --help for list.\n")
        sys.exit(1)
