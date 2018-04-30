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


``-o`` / ``--one-for-each-month``
+++++++++++++++++++++++++++++++++

Keep **last** increment from each month, and all increments from the last three months.

Great if you want to trim really old incremental backups.

Example
'''''''

``-e`` / ``--remove-even``
++++++++++++++++++++++++++

Reduce number of increments to half by keeping only odd increments.

Example
'''''''

Installation
------------


Help
----
