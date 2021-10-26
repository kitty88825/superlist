import re

from django.core import mail

from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


TEST_EMAIL = 'kitty@example.com'
SUBJECT = 'Your login link for Superlists'


class LoginTest(FunctionalTest):

    def test_can_get_email_link_to_log_in(self):
        # Edith 前往很棒的超級清單網站
        # 並且在第一次來到時，發現一個 "Log in" 連結
        # 並顯示輸入她的 email address，所以他輸入了
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # 出現一條訊息，告訴她一封電子郵件已發送
        self.wait_for(lambda: self.assertIn(
            'Check your email',
            self.browser.find_element_by_tag_name('body').text,
        ))

        # 她檢查她的電子郵件並找到一條訊息
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # 裡面有一個 url 連結
        self.assertIn('Use this link to log in', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n{email.body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # 她點擊連結
        self.browser.get(url)

        # 她已登入!
        self.wait_to_be_logged_in(email=TEST_EMAIL)

        # 現在她要登出
        self.browser.find_element_by_link_text('Log out').click()

        # 她已經登出
        self.wait_to_be_logged_out(email=TEST_EMAIL)
