"""Interactive greeting script with time-aware messages, ASCII art, and multi-language support."""

import argparse
import sys
from datetime import datetime

GREETINGS = {
    "en": {
        "morning": "Good morning",
        "afternoon": "Good afternoon",
        "evening": "Good evening",
        "night": "Good night",
        "world": "World",
    },
    "es": {
        "morning": "Buenos dias",
        "afternoon": "Buenas tardes",
        "evening": "Buenas noches",
        "night": "Buenas noches",
        "world": "Mundo",
    },
    "fr": {
        "morning": "Bonjour",
        "afternoon": "Bon apres-midi",
        "evening": "Bonsoir",
        "night": "Bonne nuit",
        "world": "Monde",
    },
    "de": {
        "morning": "Guten Morgen",
        "afternoon": "Guten Tag",
        "evening": "Guten Abend",
        "night": "Gute Nacht",
        "world": "Welt",
    },
    "pt": {
        "morning": "Bom dia",
        "afternoon": "Boa tarde",
        "evening": "Boa noite",
        "night": "Boa noite",
        "world": "Mundo",
    },
}

BANNER = r"""
  _  _     ___    ____
 | || |   / _ \  |  _ \
 | || |_ | | | | | |_) |
 |__   _|| |_| | |  _ <
    |_|   \___/  |_| \_\

  Hello, {name}!
"""

PERIODS = [
    (5, 12, "morning"),
    (12, 18, "afternoon"),
    (18, 22, "evening"),
    (22, 5, "night"),
]


def get_period(hour):
    for start, end, period in PERIODS:
        if start <= end:
            if start <= hour < end:
                return period
        else:
            if hour >= start or hour < end:
                return period
    return "morning"


def greet(name, lang, show_banner, show_time):
    lang_data = GREETINGS.get(lang, GREETINGS["en"])
    hour = datetime.now().hour
    period = get_period(hour)
    greeting = lang_data[period]
    world = lang_data["world"]
    display_name = name or world

    if show_banner:
        print(BANNER.format(name=display_name))
    else:
        print(f"{greeting}, {display_name}!")

    if show_time:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"  {now}")


def main():
    parser = argparse.ArgumentParser(description="Interactive greeting script")
    parser.add_argument("--name", "-n", help="Name to greet (default: World)")
    parser.add_argument(
        "--lang",
        "-l",
        choices=list(GREETINGS.keys()),
        default="en",
        help="Language for greeting (default: en)",
    )
    parser.add_argument("--banner", "-b", action="store_true", help="Show ASCII art banner")
    parser.add_argument("--time", "-t", action="store_true", help="Show current date/time")
    args = parser.parse_args()
    greet(args.name, args.lang, args.banner, args.time)


if __name__ == "__main__":
    main()
