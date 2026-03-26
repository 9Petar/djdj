from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from AppGuests.models import ContactMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def is_staff(user):
	return bool(user.is_staff)


@login_required(login_url='/admin/login/')
@user_passes_test(is_staff, login_url='/admin/login/')
def reply_message(request):
	if request.method == 'POST':
		recipient = request.POST.get('recipient_email')
		subject = request.POST.get('subject')
		message = request.POST.get('message')
		message_id = request.POST.get('message_id')
		name = get_object_or_404(ContactMessage, id=message_id).name
		base_url = request.build_absolute_uri('/')
		if base_url.endswith('/'):
			base_url = base_url[:-1]
		context = {
			'message_body': message,
			'subject': subject,
			'recipient': recipient,
			'name': name,
			'base_url': base_url,
		}
		
		try:
			html_message = render_to_string('AppStaff/email.html', context)
			plain_message = strip_tags(html_message)

			send_mail(
				subject=subject,
				message=plain_message,
				from_email=settings.EMAIL_HOST_USER,
				recipient_list=[recipient],
				fail_silently=False,
				html_message=html_message
			)
		except Exception as e:
			pass

		if message_id:
			try:
				contact_msg = ContactMessage.objects.get(id=message_id)
				contact_msg.replied = True
				contact_msg.reply = message
				contact_msg.save()
			except Exception as e:
				pass

		return redirect('staff_messages')

	return redirect('staff_messages')
