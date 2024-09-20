import requests
from bs4 import BeautifulSoup
from dateutil import parser
import re

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
    
    @staticmethod
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
    
    @staticmethod
    def get_website_html(url) -> BeautifulSoup:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        return soup
    
    @staticmethod
    def remove_text_within_parentheses(text):
        return re.sub(r"\([^)]*\)", "", text)
    
    @staticmethod
    def convert_odds(odds, from_type="american", to_type="decimal"):
        """
        Converts betting odds between different formats.

        Args:
            odds: The odds to convert.
            from_type: The type of odds to convert from. Supported types: "american", "decimal", "fractional".
            to_type: The type of odds to convert to. Supported types: "american", "decimal", "fractional".

        Returns:
            The converted odds.

        Raises:
            ValueError: If an invalid odds type or an invalid odds value is provided.
        """
        odds = odds.replace("(", "").replace(")", "").strip()
        odds = int(odds)
        # Convert from_type to decimal
        if from_type == "american":
            if odds < 0:
                decimal_odds = -odds / 100 + 1
            else:
                decimal_odds = odds / 100 + 1
        elif from_type == "decimal":
            decimal_odds = odds
        elif from_type == "fractional":
            numerator, denominator = map(int, odds.split("/"))
            decimal_odds = numerator / denominator + 1
        else:
            raise ValueError("Invalid 'from_type'")

        # Convert decimal to to_type
        if to_type == "american":
            if decimal_odds < 2:
                converted_odds = -100 / (decimal_odds - 1)
            else:
                converted_odds = 100 * (decimal_odds - 1)
            # Round to nearest integer for American odds
            converted_odds = round(converted_odds)
        elif to_type == "decimal":
            converted_odds = decimal_odds
        elif to_type == "fractional":
            # Find closest fractional representation
            int_part = int(decimal_odds)
            decimal_part = decimal_odds - int_part
            numerator, denominator = 1, 1
            while abs(numerator / denominator - decimal_part) > 0.001:  # Adjust precision if needed
                if numerator / denominator < decimal_part:
                    numerator += 1
            else:
                denominator += 1
            converted_odds = f"{int_part + numerator}/{denominator}" if int_part else f"{numerator}/{denominator}"
        else:
            raise ValueError("Invalid 'to_type'")

        return converted_odds
    
    @staticmethod
    def convert_datetime_format(datetime_str):
        """Converts a datetime string of any format (attempts to infer) to the specified format.

        Args:
            datetime_str: The datetime string to convert.

        Returns:
            The converted datetime string in the format 'Month day, year @ hours:minutes:seconds'.
            or None if the format could not be inferred
        """

        try:
            # Attempt to parse the datetime string, inferring the format
            dt_object = parser.parse(datetime_str)

            # Format the datetime object to the desired output format
            formatted_datetime = dt_object.strftime("%B %d, %Y")

            return formatted_datetime
        except ValueError:
            # Handle cases where the format could not be inferred
            print(f"Could not infer datetime format for: {datetime_str}")
            return None
        
    @staticmethod
    def get_unique_objects_by_title(objects):
        """
        Returns a list of objects with unique titles, keeping only the first occurrence of each title.

        Args:
            objects: A list of objects, each expected to have a 'title' attribute.

        Returns:
            A list of objects with unique titles.
        """

        seen_titles = set()
        unique_objects = []
        for obj in objects:
            if hasattr(obj, 'title') and obj.title not in seen_titles:
                seen_titles.add(obj.title)
            unique_objects.append(obj)
        return unique_objects