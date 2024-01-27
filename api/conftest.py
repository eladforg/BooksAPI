import pytest
import requests
from _pytest.config import Config
from pytest import fixture
from faker import Faker
from faker.generator import random
from api import constant

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json

import allure
from allure_commons.types import AttachmentType
from requests import Response

fake = Faker()
@fixture
# create hotels random data
def create_hotels():
    global fake
    requests.post(
        constant.BASE_URL,
        json={
            "city": fake.city(),
            "description": fake.text(),
            "name": fake.name(),
            "rating": random.randint(0, 9),
        },
    )


# to create allure results report after every run:
def pytest_configure(config: Config) -> None:
    config.option.allure_report_dir = "allure-results"



# # screenshot for failing test:
# def pytest_exception_interact(report):
#     if report.failed:
#         allure.attach(body=driver.get_screenshot_as_png(), name="screenshot",
#                       attachment_type=allure.attachment_type.PNG)
