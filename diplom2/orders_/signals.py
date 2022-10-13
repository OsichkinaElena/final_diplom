from django.dispatch import receiver, Signal
from django_rest_passwordreset.signals import reset_password_token_created

from auth_api.models import ConfirmEmailToken, User



@receiver(new_order)
def new_order_signal(user_id, **kwargs):
    """
    отправяем письмо при изменении статуса заказа
    """
    # send an e-mail to the user
    user = User.objects.get(id=user_id)
    title = "Обновление статуса заказа"
    message = 'Заказ сформирован'
    email = user.email
    send_email.apply_async((title, message, email), countdown=5 * 60)