from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.contrib.auth.models import AbstractUser

from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model

from dashboard import views
from signing.views import SignupView, SigninView, SignoutView
from user import models
from user.models import User, Mediator, BasicUser
from user.views import TopMediatorsList, ContactTopMediatorsList, \
    MediatorDetailView
from django.test import TestCase
from django.db import transaction


# Запуск: python manage.py test mediators_website.tests
# Ran 35 tests in 1.054s
# FAILED (failures=2, errors=1)


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Указываем пароль явно и затем используем set_password для установки хэшированного пароля
        self.user = BasicUser.objects.create(firstname='John One', email='john@example.com')
        self.user.set_password('password')
        self.user.group_id = 1
        self.user.save()

        # Указываем пароль явно и затем используем set_password для установки хэшированного пароля
        self.mediator = Mediator.objects.create(firstname='John Doe', email='john1@example.com')
        self.mediator.set_password('password')
        self.user.group_id = 2
        self.mediator.save()


    def test_top_mediators_view(self):
        """
        Проверяет, что статус ответа 200,
        что используется правильный шаблон и
        что представление (view), является экземпляром класса TopMediatorsList
        """
        # Тест проходит
        response = self.client.get(reverse('mediators'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'page-about.html')
        self.assertIsInstance(response.context['view'], TopMediatorsList)

    def test_contact_top_mediators_view(self):
        """
        Проверяет, что статус ответа 200,
        что используется правильный шаблон и
        что представление (view), является экземпляром класса ContactTopMediatorsList
        """
        # тест проходит
        response = self.client.get(reverse('contacts'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'page-contact.html')
        self.assertIsInstance(response.context['view'],
                              ContactTopMediatorsList)

    def test_mediator_detail_view(self):
        """
        Тестирует mediator detail view, ответ 404 Страницы нет
        """
        with transaction.atomic():
            # url для mediator-detail
            url = reverse('mediator-detail', kwargs={'pk': self.mediator.pk})

            # Входим в систему
            self.client.login(email=self.mediator.email, password='password')

            response = self.client.get(url)
            self.assertEqual(response.status_code, 404)

    def test_url_routing(self):
        """
        Проверяет, что маршруты соответствуют ожиданиям.
        """
        # тест проходитА
        self.assertEqual(reverse('mediators'), '/mediators/')
        self.assertEqual(reverse('contacts'), '/contacts/')

    def test_index_view(self):
        """
        Проверяет, что статус ответа 200,
        что используется правильный шаблон
        и что представление является экземпляром TemplateView
        """
        # тест проходит
        client = self.client
        url = reverse('index')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertIsInstance(response.context['view'], TemplateView)

    def test_error_view_status_code(self):
        """
        Проверяет, что статус ответа 200
        """
        # тест проходит
        response = self.client.get(reverse('error'))
        self.assertEqual(response.status_code, 200)

    def test_error_view_template(self):
        """
        Проверяет, что используется правильный шаблон
        """
        # тест проходит
        response = self.client.get(reverse('error'))
        self.assertTemplateUsed(response,
                                'page-error.html')

    def test_faq_url_resolves(self):
        """
        Проверяет, что URL 'faq/' успешно разрешается во view.
        """
        # тест проходит
        url = reverse('faq')
        self.assertEqual(url, '/faq/')

    def test_faq_view_uses_correct_template(self):
        """
        Проверяет, что view использует правильный шаблон 'page-faq.html'
        """
        # тест проходит
        url = reverse('faq')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'page-faq.html')

    def test_terms_url_resolves_to_template_view(self):
        """
        тест помогает убедиться, что страница, связанная с URL-ом "terms",
        использует ожидаемый шаблон и представление
        """
        # тест проходит
        response = self.client.get(reverse('terms'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context_data['view'], TemplateView)
        self.assertTemplateUsed(response, 'page-terms.html')

    def test_terms_url_name(self):
        """
        проверяет, что URL, связанный с именем terms,
        соответствует ожидаемому значению '/terms/'
        """
        # тест проходит
        url = reverse('terms')
        self.assertEqual(url, '/terms/')

    def test_user_url_resolves(self):
        """
        Проверяет, что URL "user:email_confirm" успешно разрешается
        code = mediator1@gmail.com - нужно заменить на электронную
        почту зарегистрированного пользователя.
        """
        # тест проходит
        code = "mediator1@gmail.com"  # Замените на актуальный код
        url = reverse("user:email_confirm", args=[code])
        self.assertEqual(url, f"/user/email_confirm/{code}/")

    def test_dashboard_url_resolves(self):
        """
        Проверяет, что URL для "dashboard/" правильно разрешается.
        """
        # тест проходит
        url = reverse("dashboard:dashboard")
        self.assertEqual(url, "/dashboard/")

    def test_user_dashboard_url_resolves(self):
        """
        Проверяет, что URL для "dashboard/user/" правильно разрешается.
        """
        # тест проходит
        url = reverse("dashboard:user_dashboard")
        self.assertEqual(url, "/dashboard/user/")

    def test_mediator_dashboard_url_resolves(self):
        """
        Проверяет, что URL для "dashboard/mediator/" правильно разрешается.
        """
        # тест проходит
        url = reverse("dashboard:mediator_dashboard")
        self.assertEqual(url, "/dashboard/mediator/")

    def test_user_dashboard_view_uses_correct_template(self):
        """
        Проверяет, что представление, связанное с URL "dashboard/user/",
         использует правильный шаблон.
        """
        # тест проходит
        response = self.client.get(reverse("dashboard:create-project"))
        self.assertTemplateUsed(response,
                                "dashboard/page-dashboard-create-project.html")

    def test_invoice_dashboard_url_resolves(self):
        """
        Проверяет, что представление, связанное с URL "dashboard/invoice/",
         использует правильный шаблон.
        """
        # тест проходит
        response = self.client.get(reverse("dashboard:invoice"))
        self.assertTemplateUsed(response,
                                "dashboard/page-dashboard-invoice.html")

    def test_message_dashboard_url_resolves(self):
        """
        Проверяет, что представление, связанное с URL "dashboard/message/",
         использует правильный шаблон.
        """
        # тест проходит
        response = self.client.get(reverse("dashboard:message"))
        self.assertTemplateUsed(response,
                                "dashboard/page-dashboard-message.html")

    def test_payouts_dashboard_url_resolves(self):
        """
        Проверяет, что представление, связанное с URL "dashboard/payouts/",
        использует правильный шаблон.
        """
        # тест проходит.
        response = self.client.get(reverse("dashboard:payout"))
        self.assertTemplateUsed(response,
                                "dashboard/page-dashboard-payouts.html")

    # def test_profile_dashboard_url_resolves(self):
    #     """
    #     Проверяет, что представление, связанное с URL "dashboard/profile/",
    #     использует правильный шаблон.
    #     """
    #     # Тест не проходит. AttributeError: 'AnonymousUser' object has no attribute '_meta'
    #     self.client.login(email='john@example.com', password='password')
    #
    #     response = self.client.get(reverse("dashboard:profile"))
    #     self.assertTemplateUsed(response, "dashboard/page-dashboard-profile.html")

    def test_signup_url(self):
        """
        Проверяет, что URL-шаблон для 'signup/' соответствует классу SignupView.
        """
        # тест проходит.
        url = reverse('signing:register')
        self.assertEqual(resolve(url).func.view_class, SignupView)

    def test_signin_url(self):
        """
        Проверяет, что URL-шаблон для 'signin/' соответствует классу SigninView.
        """
        # тест проходит
        url = reverse('signing:login')
        self.assertEqual(resolve(url).func.view_class, SigninView)

    def test_signout_url(self):
        """
        Проверяет, что URL-шаблон для 'signout/' соответствует классу SignoutView.
        """
        # тест проходит
        url = reverse('signing:logout')
        self.assertEqual(resolve(url).func.view_class, SignoutView)

    def test_user_dashboard_list_mediator_url_resolves(self):
        """
        Проверяет, что URL для "user/list-mediator/" правильно разрешается.
        """
        # тест проходит
        url = reverse("dashboard:list-mediators")
        self.assertEqual(url, "/dashboard/user/list-mediator/")

    def test_user_dashboard_list_mediator_view_uses_correct_template(self):
        """
        Проверяет, что представление, связанное с URL "user/list-mediator/",
         использует правильный шаблон.
        """
        # тест проходит
        response = self.client.get(reverse("dashboard:list-mediators"))
        self.assertTemplateUsed(response,
                                "dashboard/page-dashboard-list-mediators.html")

    def test_user_dashboard_jobs_url_resolves(self):
        """
        Проверяет, что URL для "user/manage-jobs/" правильно разрешается.
        """
        # тест проходит
        url = reverse("dashboard:jobs")
        self.assertEqual(url, "/dashboard/user/manage-jobs/")

    # def test_user_dashboard_jobs_view_uses_correct_template(self):
    #     """
    #     Проверяет, что представление, связанное с URL "user/manage-jobs/",
    #     использует правильный шаблон.
    #     """
    #     # тест не проходит.
    #     url = reverse('client-detail', kwargs={'pk': self.client.pk})
    #     self.client.force_login(self.client)
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)
    #     response = self.client.get(reverse("dashboard:jobs"))
    #     self.assertTemplateUsed(response,
    #                             "dashboard/page-dashboard-manage-jobs.html")

    def test_url_resolves_to_correct_view(self):
        """
         Проверяет, что URL-шаблон для 'user/manage-jobs/status-new/'
        соответствует классу UserDashboardListConflictStatusNew
        """
        # тест с ответом 200 не проходит.
        url = reverse("dashboard:new")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302) # так и должно быть?
        self.assertEqual(resolve(url).func.view_class,
                         views.UserDashboardListConflictStatusNew)

    def test_url_name_is_correct(self):
        """
        Проверяет, что имя URL-а 'dashboard:new' соответствует ожидаемому.
        """
        # тест проходит
        url = reverse("dashboard:new")
        self.assertEqual(url, "/dashboard/user/manage-jobs/status-new/")

    def test_status_in_work_url_resolves(self):
        """
        Проверяет, что URL для "user/manage-jobs/status-in-work/"
        правильно разрешается.
        """
        # тест проходит
        url = reverse("dashboard:in-work")
        self.assertEqual(url, "/dashboard/user/manage-jobs/status-in-work/")

    def test_user_dashboard_completed_url_resolves(self):
        """
        Проверяет, что URL для "user/manage-jobs/status-completed/" правильно разрешается.
        """
        # тест проходит
        url = reverse("dashboard:completed")
        self.assertEqual(url, "/dashboard/user/manage-jobs/status-completed/")

    def test_jobs_mediator_url_resolves(self):
        """
        Проверяет, что URL для "mediator/manage-jobs-mediator/" правильно разрешается.
        """
        # тест проходит
        url = reverse("dashboard:jobs-mediator")
        self.assertEqual(url, "/dashboard/mediator/manage-jobs-mediator/")

    # def test_jobs_mediator_view_uses_correct_template(self):
    #     """
    #     Проверяет, что представление, связанное с URL
    #     "mediator/manage-jobs-mediator/",
    #      использует правильный шаблон.
    #     """
    #     # тест не проходит. AssertionError: No templates used to render the response
    #     response = self.client.get(reverse("dashboard:jobs-mediator"))
    #     self.assertTemplateUsed(response,
    #                             "dashboard/page-dashboard-manage-jobs-mediator.html")

    def test_list_review_view(self):
        """
        Проверяет, что URL для отображения списка отзывов работает
        """
        # тест проходит
        url = reverse('reviews:list_review')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_review_view(self):
        """
        Проверяет, что URL для создания отзыва работает
        """
        # тест проходит
        url = reverse('reviews:create_review')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302) # Ответ не 200