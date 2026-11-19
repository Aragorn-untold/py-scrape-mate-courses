from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup, Tag

BASE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def parse_single_course(course_card: Tag) -> Course:
    return Course(
        name=course_card.select_one("h3").get_text(strip=True),
        short_description=course_card.select_one(
            "[class*='_description']"
        ).get_text(strip=True),
        duration=course_card.select_one(
            "[class*='_duration']"
        ).get_text(strip=True),
    )


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    course_cards = soup.select("a:has([data-qa='profession-card'])")

    return [parse_single_course(course_card) for course_card in course_cards]


if __name__ == "__main__":
    for course in get_all_courses():
        print(course)
