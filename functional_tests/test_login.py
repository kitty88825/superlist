import poplib
import re
import time

from django.core import mail
from django.conf import settings

from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


SUBJECT = 'Your login link for Superlists'


class LoginTest(FunctionalTest):

    def wait_for_email(self, test_email, subject):
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body

        email_id = None
        start = time.time()
        inbox = poplib.POP3_SSL('pop.gmail.com')
        try:
            inbox.user(test_email)
            inbox.pass_(settings.EMAIL_HOST_PASSWORD)
            while time.time() - start < 60:
                # get 10 newest messages
                count, _ = inbox.stat()
                for i in reversed(range(max(1, count - 10), count + 1)):
                    print('getting msg', i)
                    _, lines, __ = inbox.retr(i)
                    lines = [line.decode('utf8') for line in lines]
                    if f'Subject: {subject}' in lines:
                        email_id = i
                        body = '\n'.join(lines)
                        return body
                time.sleep(5)
        finally:
            if email_id:
                inbox.dele(email_id)
            inbox.quit()

    def test_can_get_email_link_to_log_in(self):
        # Edith 前往很棒的超級清單網站
        # 並且在第一次來到時，發現一個 "Log in" 連結
        # 並顯示輸入她的 email address，所以他輸入了
        if self.staging_server:
            test_email = settings.EMAIL_HOST_USER
        else:
            test_email = 'kitty@example.com'

        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(test_email)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # 出現一條訊息，告訴她一封電子郵件已發送
        self.wait_for(lambda: self.assertIn(
            'Check your email',
            self.browser.find_element_by_tag_name('body').text,
        ))

        # 她檢查她的電子郵件並找到一條訊息
        body = self.wait_for_email(test_email, SUBJECT)

        # 裡面有一個 url 連結
        self.assertIn('Use this link to log in', body)
        url_search = re.search(r'http://.+/.+$', body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n{body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # 她點擊連結
        self.browser.get(url)

        # 她已登入!
        self.wait_to_be_logged_in(email=test_email)

        # 現在她要登出
        self.browser.find_element_by_link_text('Log out').click()

        # 她已經登出
        self.wait_to_be_logged_out(email=test_email)
