import random
from http import HTTPStatus
import jsonschema

import allure
import pytest
import requests
from faker import Faker
from requests import Response
from selenium import webdriver

from api import constant
from api.api_calls import ApiRequests





#---------------GET----------------------------
# test for getting all books:
@allure.description("getting all the books")
def test_get_all_books():
    response=requests.get(constant.FULL_URL)
    response_body = response.json()
    print(len(response_body))
    assert response.status_code == HTTPStatus.OK
    assert len(response_body) > 0
    assert response_body[0]['title'] == "Book 1"
    # list_null_titles=[]
    # for item in response_body:
    #     if item['title'] is None:
    #         list_null_titles.append(item)
    #
    # print(list_null_titles)

@allure.description("testing schema of getting all the books")
def test_schema_of_get_all_books():
    EXPECTED_SCHEMA = {
        'type': 'object',
        'properties': {
            'id': {'type': 'integer'},
            'title': {'type': 'string'},
            'description': {'type': 'string'},
            'pageCount': {'type': 'integer'},
            'excerpt': {'type': 'integer'},
            'publishDate': {'type': 'string'}
        }, 'required': ['id', 'title', 'description', 'pageCount', 'excerpt', 'publishDate']
    }

    response=requests.get(constant.FULL_URL)
    response_body = response.json()
    try:
        jsonschema.validate(response_body,EXPECTED_SCHEMA)
        print("API response schema is valid")
    except jsonschema.ValidationError as e:
        print(f"API response schema is invalid: {e}")


@allure.description("get a specific book")
def test_get_specific_book():
    response = requests.get(constant.FULL_URL)
    response_body=response.json()
    tracked_fifth_book = {
        'id': response_body[5]['id'],
        'title': response_body[5]['title']
    }

    # get the fifth book:
    response = requests.get(f"{constant.FULL_URL}/{tracked_fifth_book['id']}")
    response_body=response.json()
    assert response.status_code == HTTPStatus.OK , "request fail"
    assert response_body['id'] == tracked_fifth_book['id'], "not the same book as expected"
    assert response_body['title'] == tracked_fifth_book['title'], "not the same book as expected"



# Testing with DDT:

data = [
    #(id, statusCode)
    (100, HTTPStatus.OK),
    (250, HTTPStatus.NOT_FOUND)
]
@allure.description("DDT - test response status code with a specific book that exists / NOT exists")
@pytest.mark.parametrize("id, statusCode", data)
def test_response_with_DDT(id, statusCode):
    response = requests.get(f"{constant.FULL_URL}/{id}")
    assert response.status_code == statusCode , "something wrong with status code"
    print(statusCode)


#---------------POST----------------------------

@allure.description("Testing POST of a new book")
def test_post_new_book():
    json={
        "id": 201,
        "title": "my title",
        "description": "my description",
        "pageCount": 120,
        "excerpt": "my book writings",
        "publishDate": "2024-01-27T12:34:27.122Z"
    }

    response = requests.post(constant.FULL_URL, json=json)
    assert response.status_code == HTTPStatus.OK

@allure.description("Testing POST of a new book with FAKE")
def test_post_new_book():
    fake = Faker()

    json={
        "id": random.randint(201,1000),
        "title": fake.name(),
        "description": fake.address(),
        "pageCount": random.randint(50,1000),
        "excerpt": fake.text(),
        "publishDate": fake.date()
    }

    response = requests.post(constant.FULL_URL, json=json)
    print(json)
    assert response.status_code == HTTPStatus.OK



data = [
    (None, HTTPStatus.BAD_REQUEST),
    ("1bb", HTTPStatus.BAD_REQUEST)
]
@allure.description("Testing INVALID POST of a new book without ID")
@pytest.mark.parametrize("id, statusCode", data)
def test_invalid_id_post_new_book(id, statusCode):
    fake = Faker()

    json={
        "id": id,
        "title": fake.name(),
        "description": fake.address(),
        "pageCount": random.randint(50,1000),
        "excerpt": fake.text(),
        "publishDate": fake.date()
    }

    response = requests.post(constant.FULL_URL, json=json)
    print(json)
    print(response.status_code)
    assert response.status_code == HTTPStatus.BAD_REQUEST


@allure.description("Testing INVALID POST of a new book without pageCount")
def test_invalid_post_new_book():
    fake = Faker()

    json={
        "id": random.randint(201,1000),
        "title": fake.name(),
        "description": fake.address(),
        "pageCount": None,
        "excerpt": fake.text(),
        "publishDate": fake.date()
    }

    response = requests.post(constant.FULL_URL, json=json)
    print(json)
    print(response.status_code)
    assert response.status_code == HTTPStatus.BAD_REQUEST

@allure.description("Testing INVALID POST of a new book without publishDate")
def test_invalid_post_without_date_new_book():
    fake = Faker()

    json={
        "id": random.randint(201,1000),
        "title": fake.name(),
        "description": fake.address(),
        "pageCount": random.randint(50,1000),
        "excerpt": fake.text(),
        "publishDate": None
    }

    response = requests.post(constant.FULL_URL, json=json)
    response_body = response.json()
    print(response_body)
    print(response.status_code)
    assert response.status_code == HTTPStatus.BAD_REQUEST

