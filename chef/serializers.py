from rest_framework.serializers import Serializer, ModelSerializer
from chef.models import Application


class ApplicationSerializer(ModelSerializer):

    class Meta:
        model = Application
        fields = '__all__'

    def create(self, validated_data):

        return Application(**validated_data)