from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass
from unittest import SkipTest, TestCase
from abc import abstractmethod


class UnsupportedMethod(Exception):
    """지원하지 않는 메소드 요청 에러"""
    pass


@dataclass
class APISpec:
    """테스트를 위한 API 엔드포인트 spec. 정의"""
    title: str
    endpoint: str
    method: str
    expected_status: int
    users: Optional[List] = None
    expected_resp: Optional[Any] = None
    req_data: Optional[Dict] = None


class APISpecTestCase(TestCase):
    """
    API 엔드포인트 테스트 프레임워크
    API 엔드포인트 테스트에 필요한 케이스를 정의
    """

    @property
    @abstractmethod
    def api_specs(self) -> List[APISpec]:
        """ 테스트 대상 API 엔드포인트의 구현 스펙을 정의 """
        raise SkipTest

    @abstractmethod
    def call_api(self, api_spec: APISpec, test_user) -> Tuple[int, Any]:
        """ 테스트를 위한 API를 호출하는 추상화 메소드 """
        pass

    def assert_api_spec(self, api_spec: APISpec, test_user):
        """ 정형화된 API 테스트 케이스의 boilerplate 코드 """
        method = api_spec.method
        if method not in ['get', 'post', 'put', 'patch', 'delete', 'options']:
            raise UnsupportedMethod(
                f"{api_spec.title} 테스트가 지원하지 않는 메소드로 정의됨"
            )

        status_code, resp_data = self.call_api(api_spec, test_user)
        self.assertEqual(
            status_code, api_spec.expected_status,
            f"\n'{api_spec.title}' API endpoint spec 테스트 실패\n"
            f"\t- User: {test_user})\n"
            f"\t- API: {api_spec.method} {api_spec.endpoint}\n"
            f"\t- Data: {api_spec.req_data}\n"
            f"\t- Response: {resp_data}"
        )

        expected_resp = api_spec.expected_resp
        if expected_resp is None:
            return status_code, resp_data

        self.assert_equal(api_spec, test_user, expected_resp, resp_data, '')
        return status_code, resp_data

    def assert_equal(self, api_spec: APISpec, test_user,
                     expected_data: Any, response_data: Any,
                     field_name: str = None):
        """
        expected_data에 key값이 있는 필드만 확인
        """
        if isinstance(expected_data, Dict):
            for nested_field_name, value in expected_data.items():
                self.assertIn(
                    nested_field_name, response_data,
                    f"\n'{api_spec.title}' API endpoint spec 테스트 결과 중 "
                    f"'{nested_field_name}' 필드 없음\n"
                    f"\t- User: {test_user}\n"
                    f"\t- API: {api_spec.method} {api_spec.endpoint}\n"
                    f"\t- Requested data: {api_spec.req_data}\n"
                    f"\t- Expected response: {nested_field_name}: {value}"
                )
                self.assert_equal(api_spec, test_user,
                                  value, response_data.get(nested_field_name),
                                  f'{field_name} > {nested_field_name}')
        elif isinstance(expected_data, List):
            for idx, data in enumerate(zip(expected_data, response_data)):
                self.assert_equal(api_spec, test_user,
                                  data[0], data[1], f'{field_name}[{idx}]')
        else:
            self.assertEqual(
                expected_data, response_data,
                f"\n'{api_spec.title}' API endpoint spec 테스트 {field_name if field_name else ''} 결과값 확인 실패\n"
                f"\t- User: {test_user}\n"
                f"\t- API: {api_spec.method} {api_spec.endpoint}\n"
                f"\t- Requested data: {api_spec.req_data}\n"
                f"\t- Expected response: {expected_data}"
            )

    def test_predefined_api_specs(self):
        """
        미리 정의된 대상 API 엔드포인트 spec을 테스트
        테스트 시나리오간 연관성이 없는 단위 테스트들을 미리 정의
        """

        print(f"Starting API sepcs of the '{self.__class__.__name__}'...")

        for idx, api_spec in enumerate(self.api_specs):
            print(f" - Testing the '{api_spec.title}' API sepc...")

            users = api_spec.users
            if users is None:
                continue

            if api_spec.title is None:
                api_spec.title = str(idx)

            for test_user in users:
                self.assert_api_spec(api_spec, test_user)
