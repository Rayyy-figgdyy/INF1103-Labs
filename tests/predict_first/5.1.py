"""Predict: the output and result after abc, -5, then 12.50."""
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

import _support
from inventory_manager import get_positive_float


def main():
    entries = iter(["abc", "-5", "12.50"])

    def simulated_input(prompt):
        value = next(entries)
        print(prompt + value)
        return value

    output = StringIO()
    with patch("builtins.input", side_effect=simulated_input) as ask:
        with redirect_stdout(output):
            result = get_positive_float("Price: ")
    assert ask.call_count == 3
    assert result == 12.5
    assert output.getvalue().splitlines() == [
        "Price: abc", "Please enter a valid number, e.g. 12.50",
        "Price: -5", "Please enter a number greater than zero.",
        "Price: 12.50",
    ]
    print(output.getvalue(), end="")
    print(f"Returned: {result!r} ({type(result).__name__})")


if __name__ == "__main__":
    main()
