from django.test import TestCase

# Create your tests here.



from django.test import TestCase
from django.urls import reverse
from .models import LivePost, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class BlogTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.post = LivePost.objects.create(title='Test', content='Some content', author=self.user, status='Ongoing')

    def test_post_list_view(self):
        self.client.login(username='testuser', password='pass')
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test')
