from typing import Any
from rest_framework import serializers
from __seedwork.domain.validators import DRFValidator, StrictBooleanField, StrictCharField


class CategoryRules(serializers.Serializer):
    name = StrictCharField(max_length=255)
    description = StrictCharField(
        required=False, allow_null=True, allow_blank=True)
    is_active = StrictBooleanField(required=False)
    created_at = serializers.DateTimeField(required=False)


class CategoryValidator(DRFValidator):

    def validate(self, data: Any) -> bool:
        rules = CategoryRules(data=data)
        return super().validate(rules)


class CategoryValidatorFactory:

    @staticmethod
    def create():
        return CategoryValidator()
