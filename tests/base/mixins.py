from django.contrib.auth import get_user_model
UserModel = get_user_model()

from legal_map.legal_auth.models import LegalUser
# It was return LegalUser.objects.create


class LegalTestUtils:
    def create_user(self, **kwargs):
        return UserModel.objects.create(**kwargs)
