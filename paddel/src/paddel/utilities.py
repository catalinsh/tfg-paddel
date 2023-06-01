import re


def contains_letters_in_order(word: str, letters: str) -> bool:
    """Check if the given word contains the given letter in order.

    Args:
        word (str): Word to check.
        letters (str): Letters to check.

    Returns:
        bool: If the word contains the letters in order.
    """
    regex = ".*".join(letters)
    return re.search(regex, word) is not None
