from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import Product

# python manage.py test  -v 2  --keepdb  --parallel
# python manage.py test products -v 2  --keepdb
# python manage.py test products.tests.TestProductViews.test_products_list_view -v 2  --keepdb


class TestProductViews(TestCase):
    @classmethod
    def setUpClass(self):
        super().setUpClass()
        User = get_user_model()
        self.user = User.objects.create_user(
            username="admin",
            password="123",
            email="admin@test.com",
            is_staff=True,
            is_active=True,
            is_superuser=True,
        )
        self.product = Product.objects.create(
            created_by=self.user,
            name="service",
            description="desc",
            cost=1000,
        )

        self.update_url = reverse(
            "products:product-update", kwargs={"pk": self.product.pk}
        )

        self.create_url = reverse("products:product-create")

    @classmethod
    def tearDownClass(self):
        super().tearDownClass()
        self.product.delete()
        self.user.delete()

    def setUp(self):
        self.client = Client()
        self.client.login(username="admin", password="123")

    def test_product_list_view(self):
        """Создание списка products"""
        url = reverse("products:products-list")
        response = self.client.get(url)
        assert response.status_code == 200
        assert "service" in str(response.content)

    def test_get_create_view(self):
        """Форма создания нового объекта product"""
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/products-create.html")

        content = response.content.decode("utf-8")
        self.assertIn("Создание услуги", content)

    def test_post_create_valid(self):
        """POST с валидными данными - создаёт объект product"""
        data = {
            "name": "новая услуга",
            "description": "отличная услуга",
            "cost": 1500,
        }

        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, 302)  # редирект
        self.assertEqual(response.url, reverse("products:products-list"))

        # Проверяем создание в БД
        product = Product.objects.get(name="новая услуга")
        self.assertEqual(product.description, "отличная услуга")
        self.assertEqual(product.cost, 1500)
        self.assertEqual(product.created_by, self.user)

    def test_post_create_invalid_data(self):
        """POST с ошибками - возвращает форму создания product с ошибками"""
        data = {
            "name": "",
            "cost": "abc",
        }

        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required")
        self.assertContains(response, "Enter a number")

    def test_only_authenticated(self):
        """Неавторизованный не может создать объект product"""
        self.client.logout()
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 302)

        self.assertIn("/", response.url)

    def test_product_detail_view(self):
        """Проверка детализации product"""
        url = reverse("products:product-detail", kwargs={"pk": self.product.pk})
        response = self.client.get(url)
        assert response.status_code == 200
        for text in ("service", "desc", "1000"):
            assert text in str(response.content)

    def test_get_product_update_view(self):
        """Получение формы обновления product"""
        url = reverse("products:product-update", kwargs={"pk": self.product.pk})
        response = self.client.get(url)
        assert response.status_code == 200
        for text in ("service", "desc", "1000"):
            assert text in str(response.content)

    def test_post_product_update_view(self):
        """POST для обновления данных product"""
        data = {
            "name": "new-service",
            "description": "new-description",
            "cost": 999,
        }
        response = self.client.post(self.update_url, data)
        self.assertEqual(response.status_code, 302)  # редирект
        self.assertEqual(
            response.url,
            reverse("products:product-detail", kwargs={"pk": self.product.pk}),
        )

        # Проверяем обновление в БД
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "new-service")
        self.assertEqual(self.product.description, "new-description")
        self.assertEqual(self.product.cost, 999)

    def test_post_product_update_invalid_data(self):
        """POST с невалидными данными для обновления product"""
        data = {
            "name": "",
            "description": "super",
            "cost": "сто пятьсот",
        }
        response = self.client.post(self.update_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required")
        self.assertContains(response, "Enter a number")
