from django.urls import path
from .views import membershiplistview, payment

app_name = 'membership'

urlpatterns = [
    path('', membershiplistview.as_view(), name='select'),
    path('payment', payment, name='payment'),
]