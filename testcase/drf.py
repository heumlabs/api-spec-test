from abc import ABC
from typing import Tuple, Any

from rest_framework.test import APITestCase

from . import APISpecTestCase, APISpec


class DRFAPISpecTestCase(APISpecTestCase, APITestCase, ABC):
    """
    Django Rest Framework의 APITestCase를 활용한 테스트
    """

    def call_api(self, api_spec: APISpec, test_user) -> Tuple[int, Any]:
        self.client.force_authenticate(test_user)
        method_handler = getattr(self.client, api_spec.method)
        resp = method_handler(api_spec.endpoint, api_spec.req_data)
        return resp.status_code, resp.data
