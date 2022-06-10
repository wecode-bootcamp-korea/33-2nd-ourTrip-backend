import jwt

from unittest.mock import patch, MagicMock
from django.test import Client, TestCase
from django.conf import settings

from users.models import User

class KakaoLoginTest(TestCase):
    def setUp(self):
        User.objects.create(
            id = 1,
            kakao_id = '12345678',
            name = '정병휘',
            email = 'wjdqudgnl@naver.com'
        )

    def tearDwon(self):
        User.objects.all().delete()

    @patch('users.views.requests')
    def test_success_kakao_exist_user(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    "id"          : 12345678,
                    "connected_at": "2022-06-10T02:08:31Z",
                    "properties"  : {
                        "nickname"   : "정병휘"
                    },
                    "kakao_account": {
                        "profile_nickname_needs_agreement": False,
                        "profile": {
                            "nickname"   : "정병휘"
                        },
                        "has_email"            : True,
                        "email_needs_agreement": False,
                        "is_email_valid"       : True,
                        "is_email_verified"    : True,
                        "email"                : "wjdqudgnl@naver.com"
                    }    
                }

        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {'HTTP_Athorization': '12345678'}
        response            = client.get('/users/kakao', **headers)
        token               = jwt.encode({'id': User.objects.get(id=1).id}, settings.SECRET_KEY, settings.ALGORITHM)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{
            'message': 'LOGIN',
            'token'  : token
        })

    @patch('users.views.requests')
    def test_success_kakao_new_user(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    "id": 12121212,
                    "connected_at": "2022-06-10T02:08:31Z",
                    "properties": {
                        "nickname": "최현민"
                    },
                    "kakao_account": {
                        "profile_nickname_needs_agreement": False,
                        "profile": {
                            "nickname": "최현민"
                        },
                        "has_email": True,
                        "email_needs_agreement": False,
                        "is_email_valid": True,
                        "is_email_verified": True,
                        "email": "hymn9611@naver.com"
                    }    
                }

        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {'HTTP_Athorization': '12345678'}
        response            = client.get('/users/kakao', **headers)
        token               = jwt.encode({'id': 2}, settings.SECRET_KEY, settings.ALGORITHM)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),{
            'message': 'FIRSTLOGIN',
            'token': token
        })