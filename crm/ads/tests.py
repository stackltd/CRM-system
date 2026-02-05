from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from products.models import Product

from .models import Ad

# python manage.py test  -v 2  --keepdb  --parallel
# python manage.py test ads -v 2  --keepdb
# python manage.py test ads.tests.TestAdViews.test_ads_list_view -v 2  --keepdb


class TestAdViews(TestCase):

    def fail_create_or_update_data(self, method_url):
        data = {
            "created_by": self.user.pk,
            "product": self.product.pk,
            "name": "new reclame",
            "promotionChannel": "#asd",
            "budget": 888,
        }
        data_test = data
        for point in ("case_1", "case_2", "case_3"):
            match point:
                case "case_1":
                    data_test.pop("product")
                case "case_2":
                    data_test["name"] = ""
                case "case_3":
                    data_test.pop("budget")
            response = self.client.post(method_url, data_test)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "This field is required")
            data_test = data
        else:
            data_test["budget"] = "fff"
            response = self.client.post(method_url, data_test)
            self.assertContains(response, "Enter a number")

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

        self.ad = Ad.objects.create(
            created_by=self.user,
            product=self.product,
            promotionChannel="#qwerty",
            name="reclame",
            budget=19000,
        )

        self.update_url = reverse("ads:ad-update", kwargs={"pk": self.ad.pk})

        self.create_url = reverse("ads:ad-create")

    @classmethod
    def tearDownClass(self):
        super().tearDownClass()
        self.product.delete()
        self.user.delete()
        self.ad.delete()

    def setUp(self):
        self.client = Client()
        self.client.login(username="admin", password="123")

    def test_ads_list_view(self):
        """Создание списка ads"""
        url = reverse("ads:ads-list")
        response = self.client.get(url)
        assert response.status_code == 200
        assert "reclame" in str(response.content)

    def test_get_create_view(self):
        """Форма "ad create" создания нового объекта"""
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "ads/ads-create.html")

        content = response.content.decode("utf-8")
        self.assertIn("Создание рекламной компании", content)

    def test_post_create_valid(self):
        """POST "ad create" с валидными данными - создаёт объект"""
        data = {
            "created_by": self.user.pk,
            "product": self.product.pk,
            "name": "new reclame",
            "promotionChannel": "#asd",
            "budget": 888,
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("ads:ads-list"))

        # Проверяем создание в БД
        ad = Ad.objects.get(name="new reclame")
        self.assertEqual(ad.name, "new reclame")
        self.assertEqual(ad.promotionChannel, "#asd")
        self.assertEqual(ad.created_by, self.user),
        self.assertEqual(ad.product, self.product),

    def test_post_create_invalid_data(self):
        """POST "ad create" с ошибками - возвращает форму с ошибками"""
        self.fail_create_or_update_data(self.create_url)

    def test_only_authenticated(self):
        """Неавторизованный не может создать объект ad"""
        self.client.logout()
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 302)

        self.assertIn("/", response.url)

    def test_ad_detail_view(self):
        """Проверка детализации ad"""
        url = reverse("ads:ad-detail", kwargs={"pk": self.ad.pk})
        response = self.client.get(url)
        assert response.status_code == 200
        for text in ("service", "reclame", "19000"):
            assert text in str(response.content)

    def test_get_ad_update_view(self):
        """Получение формы обновления ad"""
        url = reverse("ads:ad-update", kwargs={"pk": self.ad.pk})
        response = self.client.get(url)
        assert response.status_code == 200
        for text in ("service", "reclame", "19000", "#qwerty"):
            assert text in str(response.content)

    def test_post_ad_update_view(self):
        """POST "ad update"""
        data = {
            "created_by": self.user.pk,
            "product": self.product.pk,
            "name": "new-advert",
            "promotionChannel": "#qwertasdzxc",
            "budget": 65555,
        }
        response = self.client.post(self.update_url, data)
        self.assertEqual(response.status_code, 302)  # редирект
        self.assertEqual(
            response.url,
            reverse("ads:ad-detail", kwargs={"pk": self.ad.pk}),
        )

        # Проверяем обновление в БД
        self.ad.refresh_from_db()
        self.assertEqual(self.ad.name, "new-advert")
        self.assertEqual(self.ad.promotionChannel, "#qwertasdzxc")
        self.assertEqual(self.ad.budget, 65555)

    def test_post_ad_update_invalid_data(self):
        """POST "ad update" с невалидными полями"""
        self.fail_create_or_update_data(self.update_url)
