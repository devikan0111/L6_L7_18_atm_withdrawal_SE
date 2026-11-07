def notes_needed(amount):
    """Number of 100 notes for an amount string like '2,500'.
    Returns None for any invalid input."""
    if not isinstance(amount, str):
        return None
    cleaned = amount.replace(',', '').strip()
    if not (cleaned.isascii() and cleaned.isdigit()):
        return None
    return int(cleaned) // 100


def mask_card(card_number):
    """Mask '1234 5678 9012 3456' -> 'XXXX XXXX XXXX 3456'.
    Returns None for any invalid input."""
    if not isinstance(card_number, str):
        return None
    groups = card_number.split()
    if len(groups) != 4 or not all(
        g.isascii() and g.isdigit() and len(g) == 4 for g in groups
    ):
        return None
    return "XXXX XXXX XXXX " + groups[3]


def average_withdrawal(amounts_csv):
    """Average of a CSV of whole amounts, e.g. '500,1000,2000'.
    Returns None for any invalid input."""
    if not isinstance(amounts_csv, str):
        return None
    parts = [p.strip() for p in amounts_csv.split(',')]
    if not all(p.isascii() and p.isdigit() for p in parts):
        return None
    amounts = [int(p) for p in parts]
    return sum(amounts) // len(amounts)


def main():
    print("==== Running notes_needed ====")
    user_input = input("Enter an amount (e.g. 2,500): ")
    result = notes_needed(user_input)
    print("Number of 100 Notes:", "Invalid input" if result is None else result)

    print("\n==== Running mask_card ====")
    user_input = input("Enter a card number (e.g. 1234 5678 9012 3456): ")
    result = mask_card(user_input)
    print("Masked Card:", "Invalid input" if result is None else result)

    print("\n==== Running average_withdrawal ====")
    user_input = input("Enter withdrawals as CSV (e.g. 500,1000,2000): ")
    result = average_withdrawal(user_input)
    print("Average Withdrawal:", "Invalid input" if result is None else result)


if __name__ == "__main__":
    main()
