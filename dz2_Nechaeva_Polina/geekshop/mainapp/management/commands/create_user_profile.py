from django.core.management.base import BaseCommand
from authapp.models import ShopUser
from authapp.models import ShopUserProfile


class Command(BaseCommand):
    def handle(self, *args, **options):
        exclude_user_idx = ShopUserProfile.objects.all().values_list('user__id', flat=True)
        users = ShopUser.objects.exclude(id__in=exclude_user_idx).only('id')
        if users.exists():
            create_profiles = [ShopUserProfile(user=user) for user in users]
            ShopUserProfile.objects.bulk_create(create_profiles)
