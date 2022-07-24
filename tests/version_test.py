import pytest

from genshin.utils.version import get_version


@pytest.mark.parametrize(
    ["version_tuple", "version"],
    [
        ((1, 4, 0, "alpha", 1), "1.4a1"),
        ((1, 4, 0, "beta", 1), "1.4b1"),
        ((1, 4, 0, "rc", 1), "1.4rc1"),
        ((1, 4, 1, "rc", 2), "1.4.1rc2"),
        ((1, 4, 0, "final", 0), "1.4"),
        ((1, 4, 1, "final", 0), "1.4.1"),
    ],
)
def test_release_version(version_tuple, version):
    assert version == get_version(version_tuple)
