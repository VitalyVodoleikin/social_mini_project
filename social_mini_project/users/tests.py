from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import CustomUser
from .forms import RegistrationProfileForm, EditingProfileForm

User = get_user_model()


class CustomUserModelTests(TestCase):
    """
    Тестирование модели Customuser
    """
    def test_create_user(self):
        """
        Создание пользователя
        """
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="secret"
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """
        Создание суперпользователя
        """
        admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="secret"
        )
        self.assertEqual(admin.username, "admin")
        self.assertEqual(admin.email, "admin@example.com")
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_unique_email(self):
        """
        Тест на уникальность email
        """
        User.objects.create_user(
            username="user1",
            email="unique@example.com",
            password="secret"
        )
        with self.assertRaises(Exception):
            User.objects.create_user(
                username="user2",
                email="unique@example.com",
                password="secret"
            )

    def test_unique_username(self):
        """
        Тест на уникальность username
        """
        User.objects.create_user(
            username="user1",
            email="a@example.com",
            password="secret"
        )
        with self.assertRaises(Exception):
            User.objects.create_user(
                username="user1",
                email="b@example.com",
                password="secret"
            )


class RegistrationProfileFormTests(TestCase):
    """
    Тестирование формы при регистрации профиля
    """
    def test_valid_data(self):
        """
        Валидность всех данных
        """
        form = RegistrationProfileForm(data={
            "username": "newuser",
            "email": "new@example.com",
            "password1": "secret1234",
            "password2": "secret1234",
        })
        self.assertTrue(form.is_valid())

    def test_mismatched_passwords(self):
        """
        Проверка несовпадения ввода двух паролей при регистрации
        """
        form = RegistrationProfileForm(data={
            "username": "newuser",
            "email": "new@example.com",
            "password1": "secret1234",
            "password2": "different",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_duplicate_email(self):
        """
        Проверка email на уникальность в форме при регистрации
        """
        User.objects.create_user(
            username="existing",
            email="dup@example.com",
            password="secret"
        )
        form = RegistrationProfileForm(data={
            "username": "newuser",
            "email": "dup@example.com",
            "password1": "secret1234",
            "password2": "secret1234",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_duplicate_username(self):
        """
        Проверка username на уникальность в форме при регистрации
        """
        User.objects.create_user(
            username="existing",
            email="a@example.com",
            password="secret"
        )
        form = RegistrationProfileForm(data={
            "username": "existing",
            "email": "b@example.com",
            "password1": "secret1234",
            "password2": "secret1234",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)


class EditingProfileFormTests(TestCase):
    """
    Тестирование редактирования профиля
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username="editor",
            email="edit@example.com",
            password="secret"
        )

    def test_valid_data(self):
        """
        Проверка на валидность всех данных
        """
        form = EditingProfileForm(instance=self.user, data={
            "first_name": "Ivan",
            "last_name": "Petrov",
            "bio": "Hello!",
            "date_of_birth": "1990-01-01",
        })
        self.assertTrue(form.is_valid())


class UsersViewsTests(TestCase):
    """
    Тестирование представления пользователей
    """
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="secret"
        )

    def test_profile_list_view(self):
        """
        Проверка корректности списка пользователей
        """
        url = reverse("users:profiles")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/profile_list.html")
        self.assertIn("profiles", response.context)

    def test_login_view_get(self):
        """
        Тестирование пердставления для входа
        """
        url = reverse("users:login")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.html")

    def test_login_view_post_success(self):
        """
        Тестирование представления при входе
        """
        url = reverse("users:login")
        data = {
            "username": self.user.username,
            "password": "secret",
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["user"].is_authenticated)

    def test_logout_view(self):
        """
        Тестирование представления при выходе
        """
        self.client.login(username=self.user.username, password="secret")
        url = reverse("users:logout")
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["user"].is_authenticated)

    def test_profile_view_own(self):
        """
        Проверка своего профиля
        """
        self.client.login(username=self.user.username, password="secret")
        url = reverse("users:profile", kwargs={"username": self.user.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["profile_user"], self.user)

    def test_profile_edit_get_authenticated(self):
        """
        Проверка редактирования профиля аутентифицированным пользователем
        """
        self.client.login(username=self.user.username, password="secret")
        url = reverse("users:profile_edit")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/profile_edit.html")

    def test_profile_edit_post_valid(self):
        """
        Тестовое редактирование профиля
        """
        self.client.login(username=self.user.username, password="secret")
        url = reverse("users:profile_edit")
        data = {
            "first_name": "NewFirst",
            "last_name": "NewLast",
            "bio": "Updated bio",
            "date_of_birth": "1995-05-05",
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        updated_user = CustomUser.objects.get(pk=self.user.pk)
        self.assertEqual(updated_user.first_name, "NewFirst")
        self.assertEqual(updated_user.last_name, "NewLast")
        self.assertEqual(updated_user.bio, "Updated bio")

