from typing import Any


from drf_spectacular.utils import extend_schema, inline_serializer

from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.response import Response
from rest_framework import serializers, mixins, status
from rest_framework.viewsets import GenericViewSet

from my_apps.accounts.models import User


@extend_schema(
    tags=["Admin user"],
)
class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """
    API endpoint that allows users to be viewed.
    """

    class UserUrlSerializer(serializers.ModelSerializer):
        class UkrPostaSerializer(serializers.Serializer):
            class Meta:
                model = User
                fields = ["town", "postOffice"]

            town = serializers.CharField(
                source="ukr_poshta_town",
            )
            postOffice = serializers.CharField(source="ukr_poshta_post_office")

            def update(self, instance, validated_data):
                instance.ukr_poshta_post_office = validated_data.get(
                    "ukr_poshta_post_office", instance.ukr_poshta_post_office
                )
                instance.ukr_poshta_town = validated_data.get(
                    "ukr_poshta_town", instance.ukr_poshta_town
                )
                instance.save()
                return instance

        class NovaPoshtaSerializer(serializers.Serializer):
            class Meta:
                model = User
                fields = ["town", "postOffice"]

            town = serializers.CharField(source="nova_poshta_town")
            postOffice = serializers.CharField(source="nova_poshta_post_office")

            def update(self, instance, validated_data):
                instance.nova_poshta_town = validated_data.get(
                    "nova_poshta_town", instance.nova_poshta_town
                )
                instance.nova_poshta_post_office = validated_data.get(
                    "nova_poshta_post_office", instance.nova_poshta_post_office
                )
                instance.save()
                return instance

        class AddressSerializer(serializers.ModelSerializer):
            class Meta:
                model = User
                fields = [
                    "town",
                    "street",
                    "building",
                    "flat",
                ]

            town = serializers.CharField(source="address_town")
            street = serializers.CharField(source="address_street")
            building = serializers.CharField(source="address_building")
            flat = serializers.CharField(source="address_flat")

            def update(self, instance, validated_data):
                instance.address_town = validated_data.get("address_town", instance.address_town)
                instance.address_street = validated_data.get(
                    "address_street", instance.address_street
                )
                instance.address_building = validated_data.get(
                    "address_building", instance.address_building
                )
                instance.address_flat = validated_data.get("address_flat", instance.address_flat)
                instance.save()
                return instance

        novaPoshta = serializers.SerializerMethodField()
        ukrPoshta = serializers.SerializerMethodField()
        address = serializers.SerializerMethodField()
        gender = serializers.CharField(source="get_gender_display")
        role = serializers.CharField(source="get_role_display")

        class Meta:
            model = User
            fields = [
                "id",
                "url",
                "email",
                "first_name",
                "last_name",
                "mobile",
                "dob",
                "address",
                "novaPoshta",
                "ukrPoshta",
                "gender",
                "role",
                "notice",
                "get_age",
            ]

        def get_novaPoshta(self, obj) -> ReturnDict[Any, Any]:
            serializer = self.NovaPoshtaSerializer(obj, context=self.context)
            return serializer.data

        def get_ukrPoshta(self, obj) -> ReturnDict[Any, Any]:
            serializer = self.UkrPostaSerializer(obj, context=self.context)
            return serializer.data

        def get_address(self, obj) -> ReturnDict[Any, Any]:
            serializer = self.AddressSerializer(obj, context=self.context)
            return serializer.data

    class OutputUserSerializer(serializers.ModelSerializer):
        novaPoshta = inline_serializer(
            name="novaPoshta",
            required=False,
            fields={
                "nova_poshta_town": serializers.CharField(required=False),
                "nova_poshta_post_office": serializers.CharField(required=False),
            },
        )
        ukrPoshta = inline_serializer(
            name="ukrPoshta",
            required=False,
            fields={
                "ukr_poshta_town": serializers.CharField(required=False),
                "ukr_poshta_post_office": serializers.CharField(required=False),
            },
        )
        address = inline_serializer(
            name="address",
            required=False,
            fields={
                "address_town": serializers.CharField(required=False),
                "address_street": serializers.CharField(required=False),
                "address_building": serializers.CharField(required=False),
                "address_flat": serializers.CharField(required=False),
            },
        )
        gender = serializers.CharField(source="get_gender_display")
        role = serializers.CharField(source="get_role_display")

        class Meta:
            model = User
            fields = [
                "id",
                "url",
                "email",
                "first_name",
                "last_name",
                "mobile",
                "dob",
                "address",
                "novaPoshta",
                "ukrPoshta",
                "gender",
                "role",
                "notice",
                "get_age",
            ]

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserUrlSerializer

    # permission_classes = [IsAuthenticated, AdminPermission]
    @extend_schema(
        request=OutputUserSerializer(),
        responses={
            200: OutputUserSerializer(),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        data = {"detail": "Deleted", "code": "deleted"}
        return Response(status=status.HTTP_204_NO_CONTENT, data=data)

    @extend_schema(
        request=OutputUserSerializer(),
        responses={
            200: OutputUserSerializer(),
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        request=OutputUserSerializer(),
        responses={
            200: OutputUserSerializer(),
        },
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.UserUrlSerializer(
            instance, data=request.data, partial=partial, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        nova_poshta_data = serializer.initial_data.get("novaPoshta")
        if nova_poshta_data:
            nova_poshta_serializer = self.UserUrlSerializer.NovaPoshtaSerializer(
                instance, data=nova_poshta_data, partial=True
            )
            if nova_poshta_serializer.is_valid():
                nova_poshta_serializer.save()

        ukr_poshta_data = serializer.initial_data.get("ukrPoshta")
        if ukr_poshta_data:
            ukr_poshta_serializer = self.UserUrlSerializer.UkrPostaSerializer(
                instance, data=ukr_poshta_data, partial=True
            )
            if ukr_poshta_serializer.is_valid():
                ukr_poshta_serializer.save()

        address_data = serializer.initial_data.get("address")
        if address_data:
            address_serializer = self.UserUrlSerializer.AddressSerializer(
                instance, data=address_data, partial=True
            )
            if address_serializer.is_valid():
                address_serializer.save()

        return Response(serializer.data)
