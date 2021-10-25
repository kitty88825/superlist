from django.test import TestCase

from unittest.mock import patch, call


class SendLoginEmailViewTest(TestCase):

    def test_rdirects_to_home_page(self):
        response = self.client.post('/accounts/send_login_email/', data={
            'email': 'kitty@example.com',
        })
        self.assertRedirects(response, '/')

    @patch('accounts.views.send_mail')
    def test_sends_mail_to_address_from_post(self, mock_send_mail):
        self.client.post('/accounts/send_login_email/', data={
            'email': 'kitty@example.com',
        })

        self.assertTrue(mock_send_mail.called)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, 'Your login link for Superlists')
        self.assertEqual(from_email, 'noreply@superlists')
        self.assertEqual(to_list, ['kitty@example.com'])

    @patch('accounts.views.messages')
    def test_adds_success_message(self, mock_messages):
        response = self.client.post('/accounts/send_login_email/', data={
            'email': 'kitty@example.com',
        })

        expected = "Check your email, we've sent you a link you can use to log in."
        self.assertEqual(
            mock_messages.success.call_args,
            call(response.wsgi_request, expected),
        )



class LoginViewTest(TestCase):

    def test_redirects_to_home_page(self):
        response = self.client.get('/accounts/login/?token=abcd123')
        self.assertRedirects(response, '/')
