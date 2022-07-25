import pytest

from genshin.module.update import check_update, get_download_url, upgrade


@pytest.mark.parametrize(
    ["info", "result"],
    [
        (
            [
                {"name": "test_win10", "url": "https://test_win10"},
                {"name": "test_win7", "url": "https://test_win7"},
            ],
            {"name": "test_win10", "url": "https://test_win10"},
        ),
        (
            [{"name": "test_win7", "url": "https://test_win7"}],
            {"name": None, "url": None},
        ),
    ],
)
def test_get_download_url(info, result):
    name, url = get_download_url(info)
    assert name == result["name"]
    assert url == result["url"]


@pytest.mark.parametrize(
    ["tag_name", "info", "result"],
    [
        ("1.0.2", [{"name": "test_win10", "url": "https://test_win10"}], None),
        (
            "1.0.0",
            [{"name": "test_win7", "url": "https://test_win7"}],
            [{"name": "test_win7", "url": "https://test_win7"}],
        ),
    ],
)
def test_check_update(mocker, tag_name, info, result):
    mocker_get_latest_version_info = "genshin.module.update.get_latest_version_info"
    get_latest_version_info = mocker.patch(mocker_get_latest_version_info, return_value=(tag_name, info))
    tag_name, info = get_latest_version_info()
    assert result == check_update()


@pytest.mark.parametrize(
    ["check", "url", "result"],
    [
        (None, ("1.0.2", [{"name": "test_win10", "url": "https://test_win10"}]), (1, 0, 0)),
        (
            ("1.0.2", [{"name": "test_win10", "url": "https://test_win10"}]),
            ("1.0.2", [{"name": "test_win10", "url": "https://test_win10"}]),
            (1, 1, 1),
        ),
    ],
)
def test_upgrade(mocker, check, url, result):
    mock_check_update = mocker.patch("genshin.module.update.check_update", return_value=check)
    mock_get_download_url = mocker.patch("genshin.module.update.get_download_url", return_value=url)
    mock_download = mocker.patch("genshin.module.update.download", return_value=None)
    upgrade()
    if result[0]:
        mock_check_update.assert_called_once()
    if result[1]:
        mock_get_download_url.assert_called_once()
    if result[2]:
        mock_download.assert_called_once()
