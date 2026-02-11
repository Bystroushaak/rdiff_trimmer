import os
import os.path

from pytest import fixture

from rdiff_trimmer.trimmer import keep_one_for_each_month

from rdiff_trimmer.rdiff_api import RdiffAPI
from rdiff_trimmer.rdiff_api import Increment


DIR_PATH = os.path.abspath(os.path.dirname(__file__))


@fixture
def test_data_rdiff_api():
    return RdiffAPI(os.path.join(DIR_PATH, "test_data"))


@fixture
def tmpdir_rdiff_api(tmp_path):
    return RdiffAPI(tmp_path)


def test_increment_from_string():
    inc_line = "   1524336818 directory   "

    inc = Increment.from_string(inc_line)

    assert int(inc.timestamp) == 1524336818


def test_yield_increments(test_data_rdiff_api):
    increments = list(test_data_rdiff_api.yield_increments())

    assert len(increments) == 4

    assert int(increments[1].timestamp) == 1524342591
    assert int(increments[2].timestamp) == 1524342605


def test_restore_into(test_data_rdiff_api, tmpdir_rdiff_api):
    increments = list(test_data_rdiff_api.yield_increments())

    tmp_dir = tmpdir_rdiff_api.rsync_dir
    test_data_rdiff_api.restore_into(tmp_dir, increments_to_keep=[increments[0]])

    kept_increments = list(tmpdir_rdiff_api.yield_increments())

    assert len(kept_increments) == 1
    assert kept_increments[0].timestamp == increments[0].timestamp

    assert os.path.exists(os.path.join(tmp_dir, "content"))
    assert not os.path.exists(os.path.join(tmp_dir, "and_more_content"))


def test_keep_one_for_each_month(test_data_rdiff_api, tmp_path):
    keep_one_for_each_month(test_data_rdiff_api.rsync_dir, tmp_path, False)

    trimmed = RdiffAPI(tmp_path)
    kept_increments = list(trimmed.yield_increments())
    assert len(kept_increments) == 2
