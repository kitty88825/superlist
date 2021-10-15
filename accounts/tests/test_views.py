from django.test import TestCase


class SendLoginEmailViewTest(TestCase):

    def test_rdirects_to_home_page(self):
        response = self.client.post('/accounts/send_login_email/', data={
            'email': 'kitty@example.com',
        })
        self.assertRedirects(response, '/')
