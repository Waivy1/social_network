import logging

from django_nose import NoseTestSuiteRunner
from django.conf import settings

class CustomTestSuiteRunner(NoseTestSuiteRunner):
    def run_tests(self, test_labels, extra_tests=None, **kwargs):

        # Don't show logging messages while testing
        logging.disable(logging.CRITICAL)

        return super().run_tests(test_labels, extra_tests, **kwargs)
