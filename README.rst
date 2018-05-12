Rdiff trimmer
=============

Tool designed to trim old increments from the `rdiff-backup <https://www.nongnu.org/rdiff-backup/>`_.

Rdiff-backup can't remove old increments and this script can't do that either. What it can is to create new directory with only selected increments by restoring old increments and adding them into the new storage.

This may be potentially time and disk-space consuming operation, so be aware before you try it.

Modes
-----

So far, I've implemented following strategies:

``-k`` / ``--keep-increments`` ``FILE``
+++++++++++++++++++++++++++++++++++++++

Keep only increments specified in ``FILE``. It should be a list of timestamps (see ``rdiff-backup --parsable-output -l dir`` for list of timestamps).

Example
'''''''

::

    rdiff-backup -k backups_to_keep.txt my_delta_dir

This will automatically create directory named ``my_delta_dir_trimmed`` with only increments specified in file ``backups_to_keep.txt``.

``-o`` / ``--one-for-each-month``
+++++++++++++++++++++++++++++++++

Keep **last** increment from each month, and all increments from the last three months.

Great if you want to trim really old incremental backups.

Example
'''''''

::

    rdiff_trimmer -o my_delta_dir

This will automatically create directory named ``my_delta_dir_trimmed``.


``-e`` / ``--remove-even``
++++++++++++++++++++++++++

Reduce number of increments to half by keeping only odd increments.

Example
'''''''

::

    rdiff_trimmer -e my_delta_dir


This will automatically create directory named ``my_delta_dir_trimmed``.


Installation
------------

This project may be installed using PIP:

::

    pip install --user -U rdiff_trimmer


Help
----

::

    usage: rdiff_trimmer [-h] [-k LIST] [-o] [-e] [-d] RSYNC_DIR [OUT_DIR]

    positional arguments:
      RSYNC_DIR             Path to the rsync directory.
      OUT_DIR               Path to the trimmed OUTPUT rsync directory. Default
                            `{{RSYNC_DIR}}_trimmed`.

    optional arguments:
      -h, --help            show this help message and exit
      -k LIST, --keep-increments LIST
                            Keep only increments listed in this file.
      -o, --one-for-each-month
                            Keep only one backup for each month.
      -e, --remove-even     Remove even backups. Reduce number of backups to half.
      -d, --disable-compression
                            Disable default gzip compression used by rdiff.


Real example
------------

::

    bystrousak:/media/bystrousak/Internal/Backup/delta,0$ rdiff-backup -l xlit_delta
    Found 100 increments:
        increments.2016-10-06T21:46:49+02:00.dir   Thu Oct  6 21:46:49 2016
        increments.2016-10-09T18:00:21+02:00.dir   Sun Oct  9 18:00:21 2016
        increments.2016-10-18T00:34:36+02:00.dir   Tue Oct 18 00:34:36 2016
        increments.2016-10-22T03:44:59+02:00.dir   Sat Oct 22 03:44:59 2016
        increments.2016-10-29T23:20:03+02:00.dir   Sat Oct 29 23:20:03 2016
        increments.2016-11-05T21:19:54+01:00.dir   Sat Nov  5 21:19:54 2016
        increments.2016-11-12T12:46:04+01:00.dir   Sat Nov 12 12:46:04 2016
        increments.2016-11-14T00:22:04+01:00.dir   Mon Nov 14 00:22:04 2016
        increments.2016-11-16T00:09:38+01:00.dir   Wed Nov 16 00:09:38 2016
        increments.2016-11-21T00:24:46+01:00.dir   Mon Nov 21 00:24:46 2016
        increments.2016-11-22T21:02:35+01:00.dir   Tue Nov 22 21:02:35 2016
        increments.2016-12-09T23:13:37+01:00.dir   Fri Dec  9 23:13:37 2016
        increments.2016-12-12T00:55:07+01:00.dir   Mon Dec 12 00:55:07 2016
        increments.2016-12-12T20:42:38+01:00.dir   Mon Dec 12 20:42:38 2016
        increments.2016-12-25T18:48:13+01:00.dir   Sun Dec 25 18:48:13 2016
        increments.2016-12-28T18:25:13+01:00.dir   Wed Dec 28 18:25:13 2016
        increments.2017-01-03T20:26:22+01:00.dir   Tue Jan  3 20:26:22 2017
        increments.2017-01-12T18:53:19+01:00.dir   Thu Jan 12 18:53:19 2017
        increments.2017-01-15T16:42:42+01:00.dir   Sun Jan 15 16:42:42 2017
        increments.2017-01-23T20:32:09+01:00.dir   Mon Jan 23 20:32:09 2017
        increments.2017-01-25T03:02:03+01:00.dir   Wed Jan 25 03:02:03 2017
        increments.2017-01-31T22:44:00+01:00.dir   Tue Jan 31 22:44:00 2017
        increments.2017-02-05T18:04:52+01:00.dir   Sun Feb  5 18:04:52 2017
        increments.2017-02-08T17:24:05+01:00.dir   Wed Feb  8 17:24:05 2017
        increments.2017-02-12T03:16:53+01:00.dir   Sun Feb 12 03:16:53 2017
        increments.2017-02-16T19:21:32+01:00.dir   Thu Feb 16 19:21:32 2017
        increments.2017-02-18T01:03:35+01:00.dir   Sat Feb 18 01:03:35 2017
        increments.2017-02-24T18:08:07+01:00.dir   Fri Feb 24 18:08:07 2017
        increments.2017-02-26T22:43:35+01:00.dir   Sun Feb 26 22:43:35 2017
        increments.2017-02-28T03:25:32+01:00.dir   Tue Feb 28 03:25:32 2017
        increments.2017-03-04T00:29:03+01:00.dir   Sat Mar  4 00:29:03 2017
        increments.2017-03-07T16:31:02+01:00.dir   Tue Mar  7 16:31:02 2017
        increments.2017-03-15T16:08:05+01:00.dir   Wed Mar 15 16:08:05 2017
        increments.2017-03-20T00:32:52+01:00.dir   Mon Mar 20 00:32:52 2017
        increments.2017-03-26T17:44:46+02:00.dir   Sun Mar 26 17:44:46 2017
        increments.2017-03-28T01:24:43+02:00.dir   Tue Mar 28 01:24:43 2017
        increments.2017-04-04T00:18:42+02:00.dir   Tue Apr  4 00:18:42 2017
        increments.2017-04-10T22:26:01+02:00.dir   Mon Apr 10 22:26:01 2017
        increments.2017-04-13T02:05:35+02:00.dir   Thu Apr 13 02:05:35 2017
        increments.2017-04-17T03:53:13+02:00.dir   Mon Apr 17 03:53:13 2017
        increments.2017-04-23T00:16:43+02:00.dir   Sun Apr 23 00:16:43 2017
        increments.2017-04-24T20:28:38+02:00.dir   Mon Apr 24 20:28:38 2017
        increments.2017-04-28T17:48:13+02:00.dir   Fri Apr 28 17:48:13 2017
        increments.2017-05-01T17:05:54+02:00.dir   Mon May  1 17:05:54 2017
        increments.2017-05-06T14:53:45+02:00.dir   Sat May  6 14:53:45 2017
        increments.2017-05-08T01:18:36+02:00.dir   Mon May  8 01:18:36 2017
        increments.2017-05-12T21:21:06+02:00.dir   Fri May 12 21:21:06 2017
        increments.2017-05-15T01:50:22+02:00.dir   Mon May 15 01:50:22 2017
        increments.2017-05-20T18:36:21+02:00.dir   Sat May 20 18:36:21 2017
        increments.2017-05-21T23:17:01+02:00.dir   Sun May 21 23:17:01 2017
        increments.2017-05-26T14:27:02+02:00.dir   Fri May 26 14:27:02 2017
        increments.2017-06-01T00:41:23+02:00.dir   Thu Jun  1 00:41:23 2017
        increments.2017-06-04T19:54:44+02:00.dir   Sun Jun  4 19:54:44 2017
        increments.2017-06-05T01:46:51+02:00.dir   Mon Jun  5 01:46:51 2017
        increments.2017-06-05T01:50:49+02:00.dir   Mon Jun  5 01:50:49 2017
        increments.2017-06-10T12:55:40+02:00.dir   Sat Jun 10 12:55:40 2017
        increments.2017-06-15T02:05:46+02:00.dir   Thu Jun 15 02:05:46 2017
        increments.2017-06-15T17:49:10+02:00.dir   Thu Jun 15 17:49:10 2017
        increments.2017-06-19T02:26:20+02:00.dir   Mon Jun 19 02:26:20 2017
        increments.2017-06-23T17:47:04+02:00.dir   Fri Jun 23 17:47:04 2017
        increments.2017-07-02T01:43:56+02:00.dir   Sun Jul  2 01:43:56 2017
        increments.2017-07-07T14:25:32+02:00.dir   Fri Jul  7 14:25:32 2017
        increments.2017-07-14T20:56:14+02:00.dir   Fri Jul 14 20:56:14 2017
        increments.2017-07-23T18:29:51+02:00.dir   Sun Jul 23 18:29:51 2017
        increments.2017-07-27T00:55:34+02:00.dir   Thu Jul 27 00:55:34 2017
        increments.2017-08-03T19:56:02+02:00.dir   Thu Aug  3 19:56:02 2017
        increments.2017-08-12T23:55:28+02:00.dir   Sat Aug 12 23:55:28 2017
        increments.2017-08-18T21:26:34+02:00.dir   Fri Aug 18 21:26:34 2017
        increments.2017-08-21T01:22:28+02:00.dir   Mon Aug 21 01:22:28 2017
        increments.2017-08-25T12:39:03+02:00.dir   Fri Aug 25 12:39:03 2017
        increments.2017-08-26T00:28:28+02:00.dir   Sat Aug 26 00:28:28 2017
        increments.2017-08-28T01:34:57+02:00.dir   Mon Aug 28 01:34:57 2017
        increments.2017-09-04T04:12:11+02:00.dir   Mon Sep  4 04:12:11 2017
        increments.2017-09-10T21:32:15+02:00.dir   Sun Sep 10 21:32:15 2017
        increments.2017-09-21T21:39:00+02:00.dir   Thu Sep 21 21:39:00 2017
        increments.2017-09-24T05:01:10+02:00.dir   Sun Sep 24 05:01:10 2017
        increments.2017-09-30T18:45:00+02:00.dir   Sat Sep 30 18:45:00 2017
        increments.2017-10-09T03:26:08+02:00.dir   Mon Oct  9 03:26:08 2017
        increments.2017-10-26T00:32:24+02:00.dir   Thu Oct 26 00:32:24 2017
        increments.2017-10-30T02:22:21+01:00.dir   Mon Oct 30 02:22:21 2017
        increments.2017-11-02T00:51:45+01:00.dir   Thu Nov  2 00:51:45 2017
        increments.2017-11-06T02:53:23+01:00.dir   Mon Nov  6 02:53:23 2017
        increments.2017-11-06T20:54:10+01:00.dir   Mon Nov  6 20:54:10 2017
        increments.2017-11-13T22:38:19+01:00.dir   Mon Nov 13 22:38:19 2017
        increments.2017-11-18T18:13:39+01:00.dir   Sat Nov 18 18:13:39 2017
        increments.2017-11-19T23:45:23+01:00.dir   Sun Nov 19 23:45:23 2017
        increments.2017-12-01T00:45:18+01:00.dir   Fri Dec  1 00:45:18 2017
        increments.2017-12-10T23:40:29+01:00.dir   Sun Dec 10 23:40:29 2017
        increments.2017-12-24T00:52:04+01:00.dir   Sun Dec 24 00:52:04 2017
        increments.2017-12-28T23:40:24+01:00.dir   Thu Dec 28 23:40:24 2017
        increments.2017-12-30T11:56:06+01:00.dir   Sat Dec 30 11:56:06 2017
        increments.2018-01-13T22:40:59+01:00.dir   Sat Jan 13 22:40:59 2018
        increments.2018-01-25T22:27:24+01:00.dir   Thu Jan 25 22:27:24 2018
        increments.2018-01-30T23:19:17+01:00.dir   Tue Jan 30 23:19:17 2018
        increments.2018-02-11T22:43:29+01:00.dir   Sun Feb 11 22:43:29 2018
        increments.2018-02-22T16:48:26+01:00.dir   Thu Feb 22 16:48:26 2018
        increments.2018-03-17T11:31:46+01:00.dir   Sat Mar 17 11:31:46 2018
        increments.2018-03-18T15:35:24+01:00.dir   Sun Mar 18 15:35:24 2018
        increments.2018-03-19T19:53:36+01:00.dir   Mon Mar 19 19:53:36 2018
        increments.2018-04-18T22:01:28+02:00.dir   Wed Apr 18 22:01:28 2018
    Current mirror: Fri May 11 23:49:17 2018
    bystrousak:/media/bystrousak/Internal/Backup/delta,1$ rdiff_trimmer -d -o xlit_delta
    Restoring 1477776003
    Restoring 1479844955
    Restoring 1482945913
    Restoring 1485899040
    Restoring 1488248732
    Restoring 1490657083
    Restoring 1493394493
    Restoring 1495801622
    Restoring 1498232824
    Restoring 1501109734
    Restoring 1503876897
    Restoring 1506789900
    Restoring 1509326541
    Restoring 1511131523
    Restoring 1514631366
    Restoring 1517350757
    Restoring 1519314506
    Restoring 1521282706
    Restoring 1521383724
    Restoring 1521485616
    Restoring 1524081688
    Restoring 1526075357
    bystrousak:/media/bystrousak/Internal/Backup/delta,0$ rdiff-backup -l xlit_delta_trimmed/
    Found 21 increments:
        increments.2016-10-29T23:20:03+02:00.dir   Sat Oct 29 23:20:03 2016
        increments.2016-11-22T21:02:35+01:00.dir   Tue Nov 22 21:02:35 2016
        increments.2016-12-28T18:25:13+01:00.dir   Wed Dec 28 18:25:13 2016
        increments.2017-01-31T22:44:00+01:00.dir   Tue Jan 31 22:44:00 2017
        increments.2017-02-28T03:25:32+01:00.dir   Tue Feb 28 03:25:32 2017
        increments.2017-03-28T01:24:43+02:00.dir   Tue Mar 28 01:24:43 2017
        increments.2017-04-28T17:48:13+02:00.dir   Fri Apr 28 17:48:13 2017
        increments.2017-05-26T14:27:02+02:00.dir   Fri May 26 14:27:02 2017
        increments.2017-06-23T17:47:04+02:00.dir   Fri Jun 23 17:47:04 2017
        increments.2017-07-27T00:55:34+02:00.dir   Thu Jul 27 00:55:34 2017
        increments.2017-08-28T01:34:57+02:00.dir   Mon Aug 28 01:34:57 2017
        increments.2017-09-30T18:45:00+02:00.dir   Sat Sep 30 18:45:00 2017
        increments.2017-10-30T02:22:21+01:00.dir   Mon Oct 30 02:22:21 2017
        increments.2017-11-19T23:45:23+01:00.dir   Sun Nov 19 23:45:23 2017
        increments.2017-12-30T11:56:06+01:00.dir   Sat Dec 30 11:56:06 2017
        increments.2018-01-30T23:19:17+01:00.dir   Tue Jan 30 23:19:17 2018
        increments.2018-02-22T16:48:26+01:00.dir   Thu Feb 22 16:48:26 2018
        increments.2018-03-17T11:31:46+01:00.dir   Sat Mar 17 11:31:46 2018
        increments.2018-03-18T15:35:24+01:00.dir   Sun Mar 18 15:35:24 2018
        increments.2018-03-19T19:53:36+01:00.dir   Mon Mar 19 19:53:36 2018
        increments.2018-04-18T22:01:28+02:00.dir   Wed Apr 18 22:01:28 2018
    Current mirror: Fri May 11 23:49:17 2018
    bystrousak:/media/bystrousak/Internal/Backup/delta,0$ 
