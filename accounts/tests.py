from django.conf import settings
from django.contrib.auth import SESSION_KEY
from django.test import TestCase
from django.urls import reverse

from .models import User


class TestSignupView(TestCase):
    def setUp(self):
        self.url = reverse("accounts:signup")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/signup.html")

    def test_success_post(self):
        valid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, valid_data)

        self.assertRedirects(
            response,
            reverse(settings.LOGIN_REDIRECT_URL),
            status_code=302,
            target_status_code=200,
        )
        self.assertTrue(User.objects.filter(username=valid_data["username"]).exists())
        self.assertIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_empty_form(self):
        invalid_data = {
            "username": "",
            "email": "",
            "password1": "",
            "password2": "",
        }
        response = self.client.post(self.url, invalid_data)
        self.assertIn("form", response.context)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("このフィールドは必須です。", form.errors["username"])
        self.assertIn("このフィールドは必須です。", form.errors["email"])
        self.assertIn("このフィールドは必須です。", form.errors["password1"])
        self.assertIn("このフィールドは必須です。", form.errors["password2"])

    def test_failure_post_with_empty_username(self):
        invalid_data = {
            "username": "",
            "email": "test@test.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, invalid_data)
        self.assertIn("form", response.context)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("このフィールドは必須です。", form.errors["username"])

    def test_failure_post_with_empty_email(self):
        invalid_data = {
            "username": "testuser",
            "email": "",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, invalid_data)
        self.assertIn("form", response.context)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("このフィールドは必須です。", form.errors["email"])

    def test_failure_post_with_empty_password(self):
        invalid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "",
            "password2": "",
        }
        response = self.client.post(self.url, invalid_data)
        self.assertIn("form", response.context)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("このフィールドは必須です。", form.errors["password2"])

    def test_failure_post_with_duplicated_user(self):
        valid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        self.client.post(self.url, valid_data)
        invalid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, invalid_data)
        self.assertIn("form", response.context)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("同じユーザー名が既に登録済みです。", form.errors["username"])

    def test_failure_post_with_invalid_email(self):
        invalid_data = {
            "username": "testuser",
            "email": "testtest.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, invalid_data)
        self.assertIn("form", response.context)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("有効なメールアドレスを入力してください。", form.errors["email"])

    def test_failure_post_with_too_short_password(self):
        invalid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "pass",
            "password2": "pass",
        }
        response = self.client.post(self.url, invalid_data)
        self.assertIn("form", response.context)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("このパスワードは短すぎます。最低 8 文字以上必要です。", form.errors["password2"])

    def test_failure_post_with_password_similar_to_username(self):
        invalid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "testuser",
            "password2": "testuser",
        }
        response = self.client.post(self.url, invalid_data)
        self.assertIn("form", response.context)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("このパスワードは ユーザー名 と似すぎています。", form.errors["password2"])

    def test_failure_post_with_only_numbers_password(self):
        invalid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "123456789",
            "password2": "123456789",
        }
        response = self.client.post(self.url, invalid_data)
        self.assertIn("form", response.context)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("このパスワードは数字しか使われていません。", form.errors["password2"])

    def test_failure_post_with_mismatch_password(self):
        invalid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "testpassword1",
            "password2": "testpassword2",
        }
        response = self.client.post(self.url, invalid_data)
        self.assertIn("form", response.context)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(password=invalid_data["password2"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("確認用パスワードが一致しません。", form.errors["password2"])


class TestLoginView(TestCase):
    def setUp(self):
        self.url = reverse(settings.LOGIN_URL)
        self.user = User.objects.create_user(username="testuser", password="testpassword")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_success_post(self):
        valid_data = {
            "username": "testuser",
            "password": "testpassword",
        }
        response = self.client.post(self.url, valid_data)

        self.assertRedirects(
            response,
            reverse(settings.LOGIN_REDIRECT_URL),
            status_code=302,
            target_status_code=200,
        )
        self.assertIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_not_exists_user(self):
        invalid_data = {
            "username": "TESTUSER",
            "password": "testpassword",
        }
        response = self.client.post(self.url, invalid_data)
        self.assertIn("form", response.context)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn(
            "正しいユーザー名とパスワードを入力してください。どちらのフィールドも大文字と小文字は区別されます。",
            form.errors["__all__"],
        )
        self.assertNotIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_empty_password(self):
        invalid_data = {
            "username": "testuser",
            "password": "",
        }
        response = self.client.post(self.url, invalid_data)
        self.assertIn("form", response.context)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("このフィールドは必須です。", form.errors["password"])
        self.assertNotIn(SESSION_KEY, self.client.session)


class TestLogoutView(TestCase):
    def setUp(self):
        self.url = reverse("accounts:logout")
        self.user = User.objects.create_user(username="tester", password="testpassword")
        self.client.login(username="tester", password="testpassword")

    def test_success_post(self):
        response = self.client.post(self.url)

        self.assertRedirects(
            response,
            reverse(settings.LOGOUT_REDIRECT_URL),
            status_code=302,
            target_status_code=200,
        )
        self.assertNotIn(SESSION_KEY, self.client.session)


# class TestUserProfileView(TestCase):
#     def test_success_get(self):


# class TestUserProfileEditView(TestCase):
#     def test_success_get(self):

#     def test_success_post(self):

#     def test_failure_post_with_not_exists_user(self):

#     def test_failure_post_with_incorrect_user(self):


# class TestFollowView(TestCase):
#     def test_success_post(self):

#     def test_failure_post_with_not_exist_user(self):

#     def test_failure_post_with_self(self):


# class TestUnfollowView(TestCase):
#     def test_success_post(self):

#     def test_failure_post_with_not_exist_tweet(self):

#     def test_failure_post_with_incorrect_user(self):


# class TestFollowingListView(TestCase):
#     def test_success_get(self):


# class TestFollowerListView(TestCase):
#     def test_success_get(self):
