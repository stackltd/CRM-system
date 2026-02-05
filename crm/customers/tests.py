from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from ads.models import Ad
from contracts.models import Contract
from leads.models import Lead
from products.models import Product

from .models import Customer

# python manage.py test  -v 2  --keepdb  --parallel
# python manage.py test customers -v 2  --keepdb
# python manage.py test customers.tests.TestCustomerViews.test_customers_list_view -v 2  --keepdb


class TestCustomerViews(TestCase):

    def fail_create_or_update_data(self, method_url):
        data = {
            "created_by": self.user.pk,
            "lead": self.lead.pk,
            "contract": self.contract.pk,
        }

        data_test = data
        for point in ("case_1", "case_2"):
            match point:
                case "case_1":
                    data_test.pop("lead")
                case "case_2":
                    data_test.pop("contract")
            response = self.client.post(method_url, data_test)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "This field is required")
            data_test = data

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

        self.contract = Contract.objects.create(
            created_by=self.user,
            product=self.product,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(hours=24),
            name="Super Contract",
            cost=444555,
            file="contracts/zxc.png",
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

        self.customer = Customer.objects.create(
            created_by=self.user, contract=self.contract, lead=self.lead
        )

        self.update_url = reverse(
            "customers:customer-update", kwargs={"pk": self.customer.pk}
        )

        self.create_url = reverse("customers:customer-create")

    @classmethod
    def tearDownClass(self):
        super().tearDownClass()
        self.product.delete()
        self.user.delete()
        self.contract.delete()
        self.lead.delete()
        self.customer.delete()
        self.ad.delete()

    def setUp(self):
        self.client = Client()
        self.client.login(username="admin", password="123")

    def test_customers_list_view(self):
        """Создание списка customers"""
        url = reverse("customers:customers-list")
        response = self.client.get(url)
        assert response.status_code == 200
        assert "Richard" in str(response.content)
        assert "Norton" in str(response.content)

    def test_get_create_view(self):
        """Форма "customer create" создания нового объекта"""
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "customers/customers-create.html")

        content = response.content.decode("utf-8")
        self.assertIn("Создание активного клиента", content)

    def test_post_create_valid(self):
        """POST "customer create" с валидными данными - создаёт объект"""
        data = {
            "created_by": self.user.pk,
            "lead": self.lead.pk,
            "contract": self.contract.pk,
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("customers:customers-list"))

        # Проверяем создание в БД
        customer = Customer.objects.filter(lead_id=self.lead.pk).first()
        self.assertEqual(customer.lead.first_name, "Richard")
        self.assertEqual(customer.contract.name, "Super Contract")

    def test_post_create_invalid_data(self):
        """POST "customer create" с ошибками - возвращает форму с ошибками"""
        self.fail_create_or_update_data(self.create_url)

    def test_only_authenticated(self):
        """Неавторизованный не может создать объект ad"""
        self.client.logout()
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 302)

        self.assertIn("/", response.url)

    def test_customer_detail_view(self):
        """Проверка детализации customer"""
        url = reverse("customers:customer-detail", kwargs={"pk": self.customer.pk})
        response = self.client.get(url)
        assert response.status_code == 200
        for text in ("Richard", "Norton", "+12125552368", "rich@nrt.com"):
            assert text in str(response.content)

    def test_get_customer_update_view(self):
        """Получение формы обновления customer"""
        url = reverse("customers:customer-update", kwargs={"pk": self.customer.pk})
        response = self.client.get(url)
        assert response.status_code == 200
        for text in ("Richard", "Norton", "Super Contract"):
            assert text in str(response.content)

    def test_post_customer_update_view(self):
        """POST "customer update"""

        self.contract = Contract.objects.create(
            created_by=self.user,
            product=self.product,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(hours=24),
            name="Mega Contract",
            cost=444555,
            file="contracts/zxc.png",
        )

        self.lead = Lead.objects.create(
            created_by=self.user,
            ad=self.ad,
            first_name="Tomas",
            last_name="Anders",
            email="rich@nrt.com",
            phone="+12125512368",
        )

        data = {
            "created_by": self.user.pk,
            "lead": self.lead.pk,
            "contract": self.contract.pk,
        }
        response = self.client.post(self.update_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            reverse("customers:customer-detail", kwargs={"pk": self.customer.pk}),
        )
        # Проверяем создание в БД
        customer = Customer.objects.filter(lead_id=self.lead.pk).first()
        self.assertEqual(customer.lead.first_name, "Tomas")
        self.assertEqual(customer.contract.name, "Mega Contract")

    def test_post_customer_update_invalid_data(self):
        """POST "customer update" с невалидными полями"""
        self.fail_create_or_update_data(self.update_url)
