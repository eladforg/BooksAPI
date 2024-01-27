import random
from http import HTTPStatus

import allure
import pytest
from faker import Faker
from requests import Response
from selenium import webdriver

import constant
from api_calls import ApiRequests

data = [(900, HTTPStatus.OK), (7, HTTPStatus.NOT_FOUND)]

fake = Faker()









@allure.description("Get all hotels")
def test_get_hotels():
    driver = webdriver.Chrome()
    response = ApiRequests.get(constant.BASE_URL)
    assert response.status_code == HTTPStatus.OK
    assert "application/json" in response.headers["Content-Type"]
    response_body = response.json()
    if response_body["totalElements"] > 0:
        driver.get("https://www.ynet.co.il")
    else:
        driver.get("https://www.walla.co.il")


@allure.description("Get specified hotel")
def test_get_hotel(create_hotels):
    response = ApiRequests.get(constant.BASE_URL)
    response_body = response.json()
    response = ApiRequests.get(
        f"{constant.BASE_URL}/{response_body['content'][0]['id']}"
    )
    response_body = response.json()
    assert response_body["name"] == "nir"

