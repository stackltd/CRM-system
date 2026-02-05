from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ads.models import Ad
from products.models import Product

from .models import Lead

# python manage.py test  -v 2  --keepdb  --parallel
# python manage.py test leads -v 2  --keepdb
# python manage.py test leads.tests.TestLeadViews.test_leads_list_view -v 2  --keepdb


class TestLeadViews(TestCase):

    def fail_create_or_update_data(self, method_url):
        data = {
            "created_by": self.user.pk,
            "ad": self.ad.pk,
            "first_name": "Dmitry",
            "last_name": "Malikov",
            "email": "aaa@bb.asd",
            "phone": "+12125552308",
        }
        data_test = data
        for point in ("case_1", "case_2", "case_3", "case_4"):
            match point:
                case "case_1":
                    data_test.pop("ad")
                case "case_2":
                    data_test["first_name"] = ""
                case "case_3":
                    data_test["last_name"] = ""
                case "phone":
                    data_test.pop("phone")
            response = self.client.post(method_url, data_test)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "This field is required")
            data_test = data
        else:
            data_test["phone"] = "4505666"
            response = self.client.post(method_url, data_test)
            self.assertContains(
                response, "Enter a valid phone number (e.g. +12125552368)."
            )

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

        self.lead = Lead.objects.create(
            created_by=self.user,
            ad=self.ad,
            first_name="Richard",
            last_name="Norton",
            email="rich@nrt.com",
            phone="+12125552368",
        )

        self.update_url = reverse("leads:lead-update", kwargs={"pk": self.lead.pk})

        self.create_url = reverse("leads:lead-create")

    @classmethod
    def tearDownClass(self):
        super().tearDownClass()
        self.product.delete()
        self.user.delete()
        self.ad.delete()
        self.lead.delete()

    def setUp(self):
        self.client = Client()
        self.client.login(username="admin", password="123")

    def test_leads_list_view(self):
        """Создание списка leads"""
        url = reverse("leads:leads-list")
        response = self.client.get(url)
        assert response.status_code == 200
        assert "Richard" in str(response.content)
        assert "Norton" in str(response.content)

    def test_get_create_view(self):
        """Форма "lead create" создания нового объекта"""
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "leads/leads-create.html")

        content = response.content.decode("utf-8")
        self.assertIn("Создание лида", content)

    def test_post_create_valid(self):
        """POST "lead create" с валидными данными - создаёт объект"""
        data = {
            "created_by": self.user.pk,
            "ad": self.ad.pk,
            "first_name": "Dmitry",
            "last_name": "Malikov",
            "email": "aaa@bb.asd",
            "phone": "+12125552308",
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("leads:leads-list"))

        # Проверяем создание в БД
        lead = Lead.objects.get(email="aaa@bb.asd")
        self.assertEqual(lead.ad, self.ad)
        self.assertEqual(lead.created_by, self.user),
        self.assertEqual(lead.first_name, "Dmitry")
        self.assertEqual(lead.last_name, "Malikov")
        self.assertEqual(lead.email, "aaa@bb.asd"),
        self.assertEqual(lead.phone, "+12125552308"),

    def test_post_create_invalid_data(self):
        """POST "lead create" с ошибками - возвращает форму с ошибками"""
        self.fail_create_or_update_data(self.create_url)

    def test_only_authenticated(self):
        """Неавторизованный не может создать объект lead"""
        self.client.logout()
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 302)

        self.assertIn("/", response.url)

    def test_ad_detail_view(self):
        """Проверка детализации lead"""
        url = reverse("leads:lead-detail", kwargs={"pk": self.lead.pk})
        response = self.client.get(url)
        assert response.status_code == 200
        for text in ("Richard", "+12125552368", "reclame", "rich@nrt.com"):
            assert text in str(response.content)

    def test_get_ad_update_view(self):
        """Получение формы обновления lead"""
        url = reverse("leads:lead-update", kwargs={"pk": self.lead.pk})
        response = self.client.get(url)
        assert response.status_code == 200
        for text in ("Richard", "+12125552368", "reclame", "rich@nrt.com"):
            assert text in str(response.content)

    def test_post_ad_update_view(self):
        """POST "lead update"""
        data = {
            "created_by": self.user.pk,
            "ad": self.ad.pk,
            "first_name": "Nik",
            "last_name": "Nolty",
            "email": "nikky@leads.com",
            "phone": "+12125556368",
        }
        response = self.client.post(self.update_url, data)
        self.assertEqual(response.status_code, 302)  # редирект
        self.assertEqual(
            response.url,
            reverse("leads:lead-detail", kwargs={"pk": self.lead.pk}),
        )

        # Проверяем обновление в БД
        self.lead.refresh_from_db()
        self.assertEqual(self.lead.ad, self.ad)
        self.assertEqual(self.lead.created_by, self.user),
        self.assertEqual(self.lead.first_name, "Nik")
        self.assertEqual(self.lead.last_name, "Nolty")
        self.assertEqual(self.lead.email, "nikky@leads.com"),
        self.assertEqual(self.lead.phone, "+12125556368"),

    def test_post_ad_update_invalid_data(self):
        """POST "ad update" с невалидными полями"""
        self.fail_create_or_update_data(self.update_url)
