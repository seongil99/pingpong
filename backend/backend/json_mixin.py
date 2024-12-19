import re
from rest_framework import serializers


class CamelCaseSerializerMixin:
    def to_representation(self, instance):
        """Convert snake_case keys to camelCase for the frontend."""
        data = super().to_representation(instance)
        return {self.snake_to_camel(key): value for key, value in data.items()}

    def to_internal_value(self, data):
        """Convert camelCase keys back to snake_case for the backend."""
        converted_data = {
            self.camel_to_snake(key): value for key, value in data.items()
        }
        return super().to_internal_value(converted_data)

    @staticmethod
    def camel_to_snake(camel_str):
        """Convert camelCase to snake_case."""
        return re.sub(r"(?<!^)(?=[A-Z])", "_", camel_str).lower()

    @staticmethod
    def snake_to_camel(snake_str):
        """Convert snake_case to camelCase."""
        components = snake_str.split("_")
        return components[0] + "".join(x.title() for x in components[1:])
