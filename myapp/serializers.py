from rest_framework.serializers import ModelSerializer

# Serializers define the API representation.
class UploadSerializer(ModelSerializer):
    class Meta:
        fields = ['file']