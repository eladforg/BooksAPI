import requests
from requests import Response

from allure_attachments import AllureAttachments


class ApiRequests:
    """
    wrapper class for api requests that includes built in allure logging.
    """

    @staticmethod
    def get(url: str, params=None) -> Response:
        AllureAttachments.attach_request(url, request_method="GET")
        response = requests.get(url, params=params)

        try:
            AllureAttachments.attach_response(response)
        except Exception as e:
            print(e)

        return response

    @staticmethod
    def post(url: str, data=None, params=None) -> Response:
        AllureAttachments.attach_request(url, request_method="POST", payload=data)
        response = requests.post(url, params=params, json=data)

        try:
            AllureAttachments.attach_response(response)
        except Exception as e:
            print(e)

        return response

    @staticmethod
    def delete(url: str) -> Response:
        AllureAttachments.attach_request(url, request_method="DELETE")
        response = requests.delete(url)

        try:
            AllureAttachments.attach_response(response)
        except Exception as e:
            print(e)

        return response

    @staticmethod
    def put(url: str, data=None, params=None) -> Response:
        AllureAttachments.attach_request(url, request_method="PUT", payload=data)
        response = requests.put(url, params=params, json=data)

        try:
            AllureAttachments.attach_response(response)
        except Exception as e:
            print(e)

        return response
