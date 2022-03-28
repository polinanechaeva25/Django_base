from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import TemplateView

from authapp.forms import ShopUserLoginForm, ShopUserEditForm, ShopUserRegisterForm
from django.contrib import auth
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from authapp.models import ShopUser
from django.db import transaction
from authapp.forms import ShopUserProfileEditForm


class UserRegisterView(TemplateView):
    template_name = 'authapp/register.html'
    register_form_class = ShopUserRegisterForm
    model = ShopUser

    def send_verify_link(self, user):
        verify_link = reverse('auth:verify', args=[user.email, user.activation_key])
        subject = f'Для активации пользователя {user.username} пройдите по ссылке'
        message = f'Для потверждения учетной записи {user.username} на портале\n' \
                  f'{settings.DOMAIN_NAME} пройдите по ссылке {settings.DOMAIN_NAME}{verify_link}'
        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

    def get_context_data(self, **kwargs):
        title = 'регистрация'
        context = super(UserRegisterView, self).get_context_data(**kwargs)
        context.update(
            title=title,
            register_form=self.register_form_class()
        )
        return context

    def post(self, request, *args, **kwargs):
        register_form = self.register_form_class(request.POST, request.FILES)

        if register_form.is_valid():
            user = register_form.save()
            self.send_verify_link(user)
            return HttpResponseRedirect(reverse('auth:login'))
        else:
            return super().get(request, *args, **kwargs)

# def register(request):
#     title = 'регистрация'
#
#     if request.method == 'POST':
#         register_form = ShopUserRegisterForm(request.POST, request.FILES)
#
#         if register_form.is_valid():
#             user = register_form.save()
#             if send_verify_mail(user):
#                 print('сообщение подтверждения отправлено')
#                 return HttpResponseRedirect(reverse('auth:login'))
#             else:
#                 print('ошибка отправки сообщения')
#                 return HttpResponseRedirect(reverse('auth:login'))
#     else:
#         register_form = ShopUserRegisterForm()
#
#     content = {'title': title, 'register_form': register_form}
#
#     return render(request, 'authapp/register.html', content)


@transaction.atomic
def edit(request):
    title = 'редактирование'
    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = ShopUserProfileEditForm(request.POST, instance=request.user.shopuserprofile)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)
        profile_form = ShopUserProfileEditForm(instance=request.user.shopuserprofile)
    content = {
        'title': title,
        'edit_form': edit_form,
        'profile_form': profile_form
    }
    return render(request, 'authapp/edit.html', content)


def login(request):
    title = 'вход'

    login_form = ShopUserLoginForm(data=request.POST or None)

    next_url = request.GET['next'] if 'next' in request.GET.keys() else ''

    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('index'))

    content = {
        'title': title,
        'login_form': login_form,
        'next': next_url
    }

    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def send_verify_mail(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])
    title = f'Подтверждение учетной записи {user.username}'
    message = f'Для подтверждения учетной записи {user.username} на портале \
    {settings.DOMAIN_NAME} перейдите по ссылке: \n{settings.DOMAIN_NAME}{verify_link}'

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'authapp/verification.html')
        else:
            print(f'error activation user: {user}')
            return render(request, 'authapp/verification.html')
    except Exception as e:
        print(f'error activation user : {e.args}')
        return HttpResponseRedirect(reverse('index'))



