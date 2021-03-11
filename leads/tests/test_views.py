from django.test import TestCase
from django.shortcuts import reverse

class LandingPageTest(TestCase):
    
    def test_status_code(self):
        # TODO Some sort of test
        response = self.client.get(reverse("landing-page"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 200)
     
