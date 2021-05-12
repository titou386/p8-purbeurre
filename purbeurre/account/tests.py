from django.test import TestCase
from selenium import webdriver
from account.models import User
from search.models import Product


class RegisterPageTestCase(TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_01_register_firefox(self):
        self.driver.get("http://localhost:8000/account/register/")
        self.driver.find_element_by_id('id_username').send_keys('Test')
        self.driver.find_element_by_id('id_email').send_keys('test@test.fr')
        self.driver.find_element_by_id('id_password1').send_keys('1234')
        self.driver.find_element_by_id('id_password2').send_keys('1234')
        self.driver.find_element_by_name('submit').click()
        self.assertIn("http://localhost:8000/account/",
                      self.driver.current_url)

    def test_02_login_firefox(self):
        self.driver.get("http://localhost:8000/account/")
        self.driver.find_element_by_id('id_username').send_keys('test@test.fr')
        self.driver.find_element_by_id('id_password').send_keys('1234')
        self.assertEquals("http://localhost:8000/account/",
                          self.driver.current_url)

    def tearDown(self):
        self.driver.quit()


class RegisterViewTestCase(TestCase):

    def setUp(self):
        u = User.objects.create(username='Pauline', email='pauline@free.fr')
        u.set_password('1234')
        u.save()

    def test_register_success(self):
        response = self.client.post('/account/register/',
                                    {'username': "Jacques",
                                     'email': "jacques@free.fr",
                                     'password1': '1234',
                                     'password2': '1234'})

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, "/account/")

    def test_register_email_fail(self):
        response = self.client.post('/account/register/',
                                    {'username': "Paulinette",
                                     'email': "pauline@free.fr",
                                     'password1': '2345',
                                     'password2': '2345'})

        self.assertContains(response, "L'email est déjà enregistré", html=True)

    def test_register_mismatch_password(self):
        response = self.client.post('/account/register/',
                                    {'username': "Vincent",
                                     'email': "vincent@free.fr",
                                     'password1': '1234',
                                     'password2': '2345'})
        self.assertContains(response, "Le mot de passe ne correspond pas",
                            html=True)

    def test_no_register_if_logged(self):
        self.client.post('/account/',
                         {'username': 'pauline@free.fr',
                          'password': '1234'})
        response = self.client.get('/account/register/')
        self.assertEquals(response.status_code, 302)


class LoginViewTestCase(TestCase):

    def setUp(self):
        u = User.objects.create(username='Michelle', email='michelle@free.fr')
        u.set_password('1234')
        u.save()

    def test_login_success(self):

        response = self.client.login(username='michelle@free.fr',
                                     password='1234')
        self.assertTrue(response)


class SaveAndMySubstitionsViewTestCase(TestCase):

    def setUp(self):
        u = User.objects.create(username='Pauline', email='pauline@free.fr')
        u.set_password('1234')
        u.save()
        self.p = Product.objects.create(name="Nutella 650g",
                                        code="758511125439",
                                        image_url="https://nut.fr/prod.jpg",
                                        nutriscore='e')

    def test_save_substitution(self):

        self.client.post('/account/',
                         {'username': 'pauline@free.fr',
                          'password': '1234'})
        response = self.client\
            .post(f'/account/substitutions/{self.p.id}/save/')
        response = self.client.get(response.url)
        self.assertContains(response, "Nutella 650g", html=True)
