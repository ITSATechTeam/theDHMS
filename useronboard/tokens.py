from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from six import text_type
import six

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
	def __make_hash_value(self, user, timestamp):
		return(six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active))

account_activation_token = AccountActivationTokenGenerator()

