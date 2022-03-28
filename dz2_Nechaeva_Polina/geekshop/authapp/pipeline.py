from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse
import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden
from authapp.models import ShopUserProfile, ShopUser


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return
    # api_url = urlunparse(('https',
    #                       'api.vk.com',
    #                       '/method/users.get',
    #                       None,
    #                       urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about')),
    #                                             access_token=response['access_token'], v='5.92')),
    #                       None
    #                       ))

    fields = ','.join(('sex', 'about', 'bdate', 'city', 'personal', 'country', 'domain', 'languages'))
    access_token = response['access_token']
    version = '5.131'
    api_url = f'http://api.vk.com/method/users.get?fields={fields}&access_token={access_token}&v={version}'

    resp = requests.get(api_url)
    if resp.status_code != 200:
        return
    data = resp.json()['response'][0]
    if data['sex']:
        user.shopuserprofile.gender = ShopUserProfile.MALE if data['sex'] == 2 else ShopUserProfile.FEMALE
    if data['country']:
        user.country = data['country']['title']
    if data['personal']:
        user.shopuserprofile.languages = ', '.join(data['personal']['langs'])
    if data['domain']:
        user.shopuserprofile.other_social_media = f"https://vk.com/{data['domain']}"
    if data['about']:
        user.shopuserprofile.aboutMe = data['about']
    if data['bdate']:
        bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()
        age = timezone.now().date().year - bdate.year
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')
        user.shopuserprofile.age = age
    user.save()
