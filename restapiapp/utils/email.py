from django.core.mail import send_mail


class Sender:

	def send(self, msg, recipients):
		send_mail(
		    'Token Received!',
		    msg,
		    'mailer@example.com',
		    (recipients,)
		)