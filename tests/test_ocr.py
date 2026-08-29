from src.ocr import _mean_confidence


def test_mean_confidence_ignores_negative_and_invalid_values():
    data = {"conf": ["90", "70.5", "-1", "invalid"]}
    assert _mean_confidence(data) == 80.25


def test_mean_confidence_handles_empty_input():
    assert _mean_confidence({"conf": []}) == 0.0
