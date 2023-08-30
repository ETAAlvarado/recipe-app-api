"""
Tests for models.
"""

# Base Class for tests
from django.test import TestCase
# The get_user_model helper function provided by django in order to get \
# the default user model for the project
# get_user_model is best practice so that anytime you use a custom user \
# model, it is referenced throughout all your code
from django.contrib.auth import get_user_model


class ModelTest(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        # When testing, reccomended to use @example.com for a test email as \
        # that is a reserved domain specifically for testing
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        # Here we define a list of email addresses
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            # The reason we don;t normalize the firstc character is bc in \
            # theory, the first part of an email address is unique
            # This is mostly the main standard of email for simplicity
            # Essentially, anything in the first part of the email can be \
            # capitalized, but the domain names cannot be at all
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        # Here we make a loop to iterate through our expected email addresses \
        # and expected outcomes
        # We make a user with the entered email and assert whether or not it \
        # matches the expected email
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)


    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
