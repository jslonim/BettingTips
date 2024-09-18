class BetUtilities:

    def __init__(self):  # Private constructor
        raise RuntimeError("Cannot instantiate StringUtils")
    
    @staticmethod
    def kelly_criterion(win_probability, odds):
        """
        Calculates the optimal bet size using the Kelly criterion.

        Args:
            win_probability: The probability of winning the bet (between 0 and 1).
            odds: The decimal odds offered for the bet (e.g., 2.0 for even odds).

        Returns:
            The optimal fraction of your bankroll to bet (between 0 and 1).
        """
        if not (0 <= win_probability <= 1):
            raise ValueError("win_probability must be between 0 and 1")
        if odds <= 1:
            raise ValueError("odds must be greater than 1")

        edge = (win_probability * odds) - 1  # Calculate the expected value advantage
        kelly_fraction = edge / (odds - 1)  # Apply the Kelly formula

        return round(kelly_fraction * 10, 1)
    
    def extract_first_number(text):
        """
        Extracts the first number found in a string.

        Args:
            text: The string to search for a number.

        Returns:
            The first number found in the string, or None if no number is found.
        """
        digits = []
        for char in text:
            if char.isdigit():
                digits.append(char)
            elif digits:
                break  # Stop after finding the first sequence of digits
        if digits:
            return int("".join(digits))
        else:
            return None