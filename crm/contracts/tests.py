import os
from datetime import timedelta
from logging import Logger

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from products.models import Product

from .models import Contract

logger = Logger("test")

# python manage.py test  -v 2  --keepdb  --parallel
# python manage.py test contracts -v 2  --keepdb
# python manage.py test contract.tests.TestContractViews.test_contracts_list_view -v 2  --keepdb


class TestContractViews(TestCase):

    def fail_create_or_update_data(self, method_url):
        file_name = "contract.doc"
        test_image = SimpleUploadedFile(
            name=file_name,
            content=b"text content",
        )
        start_date = timezone.now()
        end_date = start_date + timedelta(hours=24)
        data = {
            "created_by": self.user.pk,
            "product": self.product.pk,
            "name": "Maker some fakes",
            "start_date": start_date.strftime("%Y-%m-%d %H:%M"),
            "end_date": end_date.strftime("%Y-%m-%d %H:%M"),
            "cost": 888222,
            "file": test_image,
        }

        data_test = data
        for point in ("case_1", "case_2", "case_3", "case_4", "case_5"):
            match point:
                case "case_1":
                    data_test.pop("product")
                case "case_2":
                    data_test.pop("name")
                case "case_3":
                    data_test.pop("start_date")
                case "case_4":
                    data_test.pop("end_date")
                case "case_5":
                    data_test.pop("file")
            response = self.client.post(method_url, data_test)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "This field is required")
            data_test = data
        else:
            data_test["cost"] = "fff"
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

        self.contract = Contract.objects.create(
            created_by=self.user,
            product=self.product,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(hours=24),
            name="Super Contract",
            cost=444555,
            file="contracts/zxc.png",
        )

        self.update_url = reverse(
            "contracts:contract-update", kwargs={"pk": self.contract.pk}
        )

        self.create_url = reverse("contracts:contract-create")

    @classmethod
    def tearDownClass(self):
        super().tearDownClass()
        self.product.delete()
        self.user.delete()
        self.contract.delete()

    def setUp(self):
        self.client = Client()
        self.client.login(username="admin", password="123")

    def test_contracts_list_view(self):
        """Создание списка contracts"""
        url = reverse("contracts:contracts-list")
        response = self.client.get(url)
        assert response.status_code == 200
        assert "Super Contract" in str(response.content)

    def test_get_create_view(self):
        """Форма "contract create" создания нового объекта"""
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contracts/contracts-create.html")

        content = response.content.decode("utf-8")
        self.assertIn("Создание контракта", content)

    def test_post_create_valid(self):
        """POST "contract create" с валидными данными - создаёт объект"""
        # Создаём тестовый файл
        file_name = "contract.doc"
        test_image = SimpleUploadedFile(
            name=file_name,
            content=b"text content",
        )
        start_date = timezone.now()
        end_date = start_date + timedelta(hours=24)
        data = {
            "created_by": self.user.pk,
            "product": self.product.pk,
            "name": "Maker some fakes",
            "start_date": start_date.strftime("%Y-%m-%d %H:%M"),
            "end_date": end_date.strftime("%Y-%m-%d %H:%M"),
            "cost": 888222,
            "file": test_image,
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("contracts:contracts-list"))

        # Проверяем создание в БД
        contract = Contract.objects.get(name="Maker some fakes")

        curr_dir = os.getcwd()
        folder_path = os.path.join(curr_dir, "uploads", "contracts")
        os.chdir(folder_path)

        # тест загрузки файла
        self.assertTrue(contract.file)
        self.assertTrue(os.path.exists(contract.file.path))
        file_name_test = f'{"_".join(contract.name.split())}_{file_name}'
        self.assertEqual(contract.file.name, f"contracts/{file_name_test}")
        # удаление файла
        for file in os.listdir():
            if file == file_name_test:
                os.remove(file)
        os.chdir(curr_dir)

        self.assertEqual(contract.name, "Maker some fakes")
        self.assertEqual(contract.cost, 888222)
        self.assertEqual(contract.start_date.date(), start_date.date())
        self.assertEqual(contract.end_date.date(), end_date.date()),
        self.assertEqual(contract.product, self.product),
        self.assertEqual(contract.created_by, self.user),

    def test_post_create_invalid_data(self):
        """POST "contract create" с ошибками - возвращает форму с ошибками"""
        self.fail_create_or_update_data(self.create_url)

    def test_only_authenticated(self):
        """Неавторизованный не может создать объект ad"""
        self.client.logout()
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 302)

        self.assertIn("/", response.url)

    def test_ad_detail_view(self):
        """Проверка детализации contract"""
        url = reverse("contracts:contract-detail", kwargs={"pk": self.contract.pk})
        response = self.client.get(url)
        assert response.status_code == 200
        for text in ("service", "Super Contract", "444555"):
            assert text in str(response.content)

    def test_get_ad_update_view(self):
        """Получение формы обновления contract"""
        url = reverse("contracts:contract-update", kwargs={"pk": self.contract.pk})
        response = self.client.get(url)
        assert response.status_code == 200
        for text in ("service", "Super Contract", "444555"):
            assert text in str(response.content)

    def test_post_ad_update_view(self):
        """POST "contract update"""
        # Создаём тестовый файл
        file_name = "contract_updated.doc"
        test_image = SimpleUploadedFile(
            name=file_name,
            content=b"text for updated content",
        )
        start_date = timezone.now()
        end_date = start_date + timedelta(hours=24)
        data = {
            "created_by": self.user.pk,
            "product": self.product.pk,
            "name": "Maker no fakes",
            "start_date": start_date.strftime("%Y-%m-%d %H:%M"),
            "end_date": end_date.strftime("%Y-%m-%d %H:%M"),
            "cost": 111222,
            "file": test_image,
        }
        response = self.client.post(self.update_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            reverse("contracts:contract-detail", kwargs={"pk": self.contract.pk}),
        )

        # Проверяем создание в БД
        contract = Contract.objects.get(name="Maker no fakes")

        curr_dir = os.getcwd()
        folder_path = os.path.join(curr_dir, "uploads", "contracts")
        os.chdir(folder_path)

        # тест загрузки файла
        self.assertTrue(contract.file)
        self.assertTrue(os.path.exists(contract.file.path))
        file_name_test = f'{"_".join(contract.name.split())}_{file_name}'
        self.assertEqual(contract.file.name, f"contracts/{file_name_test}")
        # удаление файла
        for file in os.listdir():
            if file == file_name_test:
                os.remove(file)
        os.chdir(curr_dir)

        self.assertEqual(contract.name, "Maker no fakes")
        self.assertEqual(contract.cost, 111222)
        self.assertEqual(contract.start_date.date(), start_date.date())
        self.assertEqual(contract.end_date.date(), end_date.date()),
        self.assertEqual(contract.product, self.product),
        self.assertEqual(contract.created_by, self.user)

    def test_post_ad_update_invalid_data(self):
        """POST "ad update" с невалидными полями"""
        self.fail_create_or_update_data(self.update_url)
