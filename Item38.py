# Item 38: Accept Functions Instead of Classes for Simple Interfaces
names = ["Socrates", "Archimedes", "Plato", "Aristotle"]
names.sort(key=len)
print(names)


def log_missing():
    print(
        "key added"
    )  # if we do not increment at insertion, then it doesn't even fire off.
    return 0


from collections import defaultdict

current = {"green": 12, "blue": 3}
increments = [
    ("red", 5),
    ("blue", 17),
    ("orange", 9),
]
result = defaultdict(log_missing, current)
print(f"before: {dict(result)}")
for key, value in increments:
    result[key] += value

print(f"after: {dict(result)}")


# If I want to know the total number of keys that were missing, we can do that with a
# stateful closure (Item 21).
def increment_with_reports(current, increments):
    added_count = 0

    def missing():
        nonlocal added_count  # stateful closure
        added_count += 1
        return 0

    result = defaultdict(missing, current)
    for key, amount in increments:
        result[key] += amount

    return result, added_count


result, count = increment_with_reports(current, increments)
assert count == 2


# Stateful closures tend to be harder to read, another approach is defining a small class to encapsulate the state


class CountMissing:
    def __init__(self):
        self.added = 0

    def missing(self):
        self.added += 1
        return 0


counter = CountMissing()
result = defaultdict(counter.missing, current)  # Method reference
for key, amount in increments:
    result[key] += amount

assert counter.added == 2


# With classes, it is clearer, but it might not be as clear as we would like it.
# Perhaps making a class that is callable will inform the client the intent and
# How to use our class


class BetterCountMissing:
    def __iter__(self):
        self.added = 0

    def __call__(self, *args, **kwargs):
        self.added += 1
        return 0


counter = BetterCountMissing()
# assert counter() == 0
# assert callable(counter)

# result = defaultdict(counter, current)  # Relies on __call__
# for key, amount in increments:
#     result[key] = amount
#
# assert counter.added == 2

# Separately

from typing import Iterable, Set
import re

ARN_REGEX = "(?P<arn>\w+):(?P<partition>\w+)\:(?P<service>\w+)?\:(?P<region>\w+)\:(?P<account_id>\w+)\:(?P<resource_id>\w+)"


def collect_account_ids_from_arns(arns: Iterable[str]) -> Set[str]:
    """Given several ARNS in the form arn:partition:service:region:account-id:resource-id
    collect the unique account IDs found on those strings, and return them
    """
    collected_account_ids = set()
    for arn in arns:
        matched = re.match(ARN_REGEX, arn)
        print(f"matched: {matched}")
        if matched is not None:
            account_id = matched.groupdict()["account_id"]
            collected_account_ids.add(account_id)
    return collected_account_ids


# print(
#     collect_account_ids_from_arns(
#         [
#             "asd1:partitasdasion1:asd1:region1:account1:resource1",
#             "asd2:partitasdasion2:asd1:region2:account2:resource2",
#         ]
#     )
# )


def collect_account_ids_from_arns2(arns: Iterable[str]) -> Set[str]:
    matched = filter(None, (re.match(ARN_REGEX, arn) for arn in arns))
    return {m.groupdict()["account_id"] for m in matched}


print(
    collect_account_ids_from_arns2(
        [
            "asd1:partitasdasion1:asd1:region1:account1:resource1",
            "asd2:partitasdasion2:asd1:region2:account2:resource2",
        ]
    )
)


def collect_account_ids_from_arns3(arns: Iterable[str]) -> Set[str]:
    return {
        matched.groupdict()["account_id"]
        for arn in arns
        if (matched := re.match(ARN_REGEX, arn)) is not None
    }
