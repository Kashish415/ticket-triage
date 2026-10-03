"""Rule-based triage for support tickets.

Classifies an incoming ticket as ``"refund"``, ``"billing"`` or ``"bug"``
based on keywords found in its subject and body.

Precedence is intentional: a refund request is a specific kind of billing
issue, so refund keywords win over billing ones, and anything that is not
clearly a refund or billing issue is treated as a bug report by default.
"""

from __future__ import annotations

import re

CATEGORIES = ("refund", "billing", "bug")

REFUND_KEYWORDS = (
    "refund",
    "refunded",
    "refunds",
    "reimburse",
    "reimbursement",
    "money back",
    "chargeback",
    "return my money",
)

BILLING_KEYWORDS = (
    "bill",
    "billed",
    "billing",
    "invoice",
    "invoiced",
    "charge",
    "charged",
    "charges",
    "payment",
    "paid",
    "pay",
    "subscription",
    "receipt",
    "overcharge",
    "overcharged",
    "price",
    "pricing",
)


def _contains_keyword(text: str, keywords: tuple[str, ...]) -> bool:
    """Return True if any keyword appears in *text* as a whole word/phrase.

    Word boundaries prevent substring false positives such as ``"debug"``
    matching the ``"bug"`` keyword.
    """
    return any(
        re.search(rf"\b{re.escape(keyword)}\b", text) is not None
        for keyword in keywords
    )


def triage(subject: str | None, body: str | None = None) -> str:
    """Classify a ticket as ``"refund"``, ``"billing"`` or ``"bug"``.

    ``subject`` and ``body`` are matched case-insensitively. Refund requests
    take precedence over billing issues, which take precedence over bugs.
    When no keyword matches, the ticket is treated as a bug report, since
    unexpected behaviour is the safest default for a support queue.
    """
    text = f"{subject or ''} {body or ''}".lower()

    if _contains_keyword(text, REFUND_KEYWORDS):
        return "refund"
    if _contains_keyword(text, BILLING_KEYWORDS):
        return "billing"
    return "bug"
