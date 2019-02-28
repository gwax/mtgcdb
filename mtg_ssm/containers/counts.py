"""Helpers for tracking collection counts."""

import collections
import enum
from typing import Dict
from typing import MutableMapping
from uuid import UUID


class CountType(enum.Enum):
    """Enum for possible card printing types (nonfoil, foil)."""

    nonfoil = enum.auto()
    foil = enum.auto()


ScryfallCardCount = Dict[UUID, MutableMapping[CountType, int]]
"""Mapping from scryfall id to card printing type to count."""


def merge_print_counts(*print_counts_args: ScryfallCardCount) -> ScryfallCardCount:
    """Merge two sets of print_counts."""
    merged_counts: ScryfallCardCount = collections.defaultdict(collections.Counter)
    for print_counts in print_counts_args:
        for card_id, counts in print_counts.items():
            merged_counts[card_id].update(counts)
    return dict(merged_counts)


def diff_print_counts(
    left: ScryfallCardCount, right: ScryfallCardCount
) -> ScryfallCardCount:
    """Subtract right print counts from left print counts."""
    diffed_counts: ScryfallCardCount = collections.defaultdict(dict)
    for card_id in left.keys() | right.keys():
        left_counts = left.get(card_id, {})
        right_counts = right.get(card_id, {})
        card_counts = {
            k: left_counts.get(k, 0) - right_counts.get(k, 0)
            for k in left_counts.keys() | right_counts.keys()
        }
        card_counts = {k: v for k, v in card_counts.items() if v}
        if card_counts:
            diffed_counts[card_id] = card_counts
    return diffed_counts
