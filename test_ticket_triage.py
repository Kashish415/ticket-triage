"""Tests for :func:`ticket_triage.triage`."""

import pytest

from ticket_triage import CATEGORIES, triage


@pytest.mark.parametrize(
    "subject,body,expected",
    [
        ("I want a refund", None, "refund"),
        ("Please reimburse my order", "It never arrived", "refund"),
        ("Order issue", "I would like my money back", "refund"),
        ("Unexpected charge", None, "billing"),
        ("Invoice question", "Can you resend the invoice?", "billing"),
        ("Question", "My card was charged twice", "billing"),
        ("App crashes on login", None, "bug"),
        ("Something is broken", "The page fails to load", "bug"),
        ("Cannot log in", "No error message shown", "bug"),
    ],
)
def test_classifies_expected_category(subject, body, expected):
    assert triage(subject, body) == expected


def test_body_is_optional():
    assert triage("Need a refund") == "refund"


def test_matching_is_case_insensitive():
    assert triage("REFUND REQUEST") == "refund"
    assert triage("Billing Problem") == "billing"


def test_refund_takes_precedence_over_billing():
    assert triage("Refund my invoice", "I was charged twice") == "refund"


def test_billing_takes_precedence_over_bug_wording():
    assert triage("Billing error", "The invoice shows a crash in totals") == "billing"


def test_keywords_match_whole_words_only():
    # "billion" contains "bill" but must not be read as a billing keyword.
    assert triage("We serve a billion users") == "bug"


def test_empty_input_defaults_to_bug():
    assert triage("") == "bug"
    assert triage("   ") == "bug"


def test_none_inputs_default_to_bug():
    assert triage(None) == "bug"
    assert triage(None, None) == "bug"


def test_result_is_always_a_known_category():
    assert set(CATEGORIES) == {"refund", "billing", "bug"}
    assert triage("random text") in CATEGORIES
