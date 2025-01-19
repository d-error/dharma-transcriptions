from dharma_transcriptions.utils import format_time, sanitize_filename


def test_sanitize_filename():
    # Test replacing invalid characters
    assert sanitize_filename('test<file>') == 'test_file_'
    assert sanitize_filename('file:name') == 'file_name'
    assert sanitize_filename('file\\path') == 'file_path'
    assert sanitize_filename('file|name') == 'file_name'
    assert (
        sanitize_filename(
            'Alan Wallace ｜ Conselho para quem deseja superar as aflições'
        )
        == 'Alan Wallace _ Conselho para quem deseja superar as aflições'
    )

    # Test with no invalid characters
    assert sanitize_filename('valid_filename') == 'valid_filename'

    # Test with empty filename
    assert not sanitize_filename('')


def test_format_time():
    # Test standard cases
    assert format_time(0) == '00:00:00,000'
    assert format_time(1) == '00:00:01,000'
    assert format_time(60) == '00:01:00,000'
    assert format_time(3600) == '01:00:00,000'
    assert format_time(3661.123) == '01:01:01,123'

    # Test fractional seconds rounding
    assert format_time(3661.126) == '01:01:01,126'
    assert format_time(3661.999) == '01:01:01,999'

    # Test large time values
    assert format_time(86461.5) == '24:01:01,500'
