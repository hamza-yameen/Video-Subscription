from django.shortcuts import render
from django.views.generic import ListView
from .models import Membership, UserMembership, Subscription
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
import stripe


def get_user_membership(request):
    user_membership_qs = UserMembership.objects.filter(user=request.user)
    if user_membership_qs.exists():
        return user_membership_qs.first()
    return None


def get_user_subscription(request):
    user_subscription = Subscription.objects.filter(user_membership=get_user_membership(request))
    if user_subscription.exists():
        return user_subscription.first()
    return None


def get_selected_membership(request):
    membership_added = request.session['selected_membership_type']
    selected_membership = Membership.objects.filter(membership_type=membership_added)
    if selected_membership.exists():
        return selected_membership.first()
    return None


class membershiplistview(ListView):
    queryset = Membership.objects.all()
    template_name = "Membership/list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(membershiplistview, self).get_context_data(*args, **kwargs)
        current_membership = get_user_membership(self.request)
        context['current_membership'] = str(current_membership.member_ship)
        return context

    def post(self, request, **kwargs):
        user_membership = get_user_membership(request)
        user_subscription = get_user_subscription(request)
        selected_membership_type = request.POST.get('membership_type')
        selected_membership_qs = Membership.objects.filter(membership_type=selected_membership_type)
        selected_membership = selected_membership_qs.first()
        if user_membership.member_ship == selected_membership:
            if user_subscription is not None:
                messages.info(request, "You already have this membership. Your next payment is due {}"
                              .format('get this value from stripe'))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        request.session['selected_membership_type'] = selected_membership.membership_type
        return HttpResponseRedirect(reverse('membership:payment'))


def payment(request):
    user_membership = get_user_membership(request)
    selected_membership = get_selected_membership(request)
    publish_key = settings.STRIPE_PUBLISHABLE_KEY

    context = {
        's_membership': selected_membership
    }

    return render(request, "Membership/payment.html", context)
