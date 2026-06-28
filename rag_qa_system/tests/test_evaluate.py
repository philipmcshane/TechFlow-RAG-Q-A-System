"""Tests for evaluate.py — judge_answer verdict parsing.

The LLM is mocked so no API calls or ChromaDB access are needed.
"""

from unittest.mock import MagicMock
from evaluate import judge_answer, TEST_CASES


def _mock_llm(response_text: str) -> MagicMock:
    llm = MagicMock()
    llm.invoke.return_value.content = response_text
    return llm


#  Verdict extraction
def test_correct_verdict_parsed():
    verdict, reason = judge_answer(
        _mock_llm("CORRECT\nThe answer matches the expected information."),
        "q", "expected", "answer",
    )
    assert verdict == "CORRECT"


def test_partial_verdict_parsed():
    verdict, _ = judge_answer(
        _mock_llm("PARTIAL\nMissing some details."),
        "q", "expected", "answer",
    )
    assert verdict == "PARTIAL"


def test_incorrect_verdict_parsed():
    verdict, _ = judge_answer(
        _mock_llm("INCORRECT\nCompletely wrong."),
        "q", "expected", "answer",
    )
    assert verdict == "INCORRECT"


def test_reason_extracted():
    _, reason = judge_answer(
        _mock_llm("CORRECT\nThe answer is accurate and complete."),
        "q", "expected", "answer",
    )
    assert reason == "The answer is accurate and complete."


def test_verdict_normalised_to_uppercase():
    verdict, _ = judge_answer(
        _mock_llm("correct\nLooks good."),
        "q", "expected", "answer",
    )
    assert verdict == "CORRECT"


def test_unrecognised_verdict_defaults_to_incorrect():
    verdict, _ = judge_answer(
        _mock_llm("UNSURE\nNot sure about this."),
        "q", "expected", "answer",
    )
    assert verdict == "INCORRECT"


def test_missing_reason_line_returns_empty_string():
    verdict, reason = judge_answer(
        _mock_llm("CORRECT"),
        "q", "expected", "answer",
    )
    assert verdict == "CORRECT"
    assert reason == ""


def test_extra_whitespace_in_verdict_tolerated():
    verdict, _ = judge_answer(
        _mock_llm("  PARTIAL  \nSome info missing."),
        "q", "expected", "answer",
    )
    assert verdict == "PARTIAL"


# Test-case suite shape 
def test_test_cases_count():
    assert len(TEST_CASES) == 13


def test_test_cases_have_required_keys():
    for tc in TEST_CASES:
        assert "question" in tc, f"Missing 'question' key: {tc}"
        assert "expected" in tc, f"Missing 'expected' key: {tc}"


def test_test_cases_non_empty_questions():
    for tc in TEST_CASES:
        assert tc["question"].strip(), "Found empty question in TEST_CASES"


def test_test_cases_non_empty_expected():
    for tc in TEST_CASES:
        assert tc["expected"].strip(), "Found empty expected answer in TEST_CASES"
