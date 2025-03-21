from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from phonenumber_field.phonenumber import PhoneNumber
from rest_framework import exceptions, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from profiles.models import *
from profiles.serializers import ClientSerializer

from .tokens import account_activation_token


class EmailLogin(ObtainAuthToken):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        print(f"eddamail => {email}\tpassword=>{password}")

        if email is None or password is None:
            raise exceptions.AuthenticationFailed("Email and password required")

        if email and password:
            user = authenticate(request=request, email=email, password=password)
            print("passed 2")

            if user is not None:
                login(
                    request, user, backend="django.contrib.auth.backends.ModelBackend"
                )
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key})

        return Response({"error": "Invalid email/password"}, status=400)


class RegisterUserView(APIView):
    permission_classes = (permissions.AllowAny,)

    @extend_schema(
        request={
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "email": {"type": "string"},
                "password": {"type": "string"},
                "password2": {"type": "string"},
                "phone": {"type": "string"},
                "company": {"type": "string"},
                "url": {"type": "string"},
            },
        
        },
        responses={
            status.HTTP_201_CREATED: {'error': {'type': 'string'}},
            status.HTTP_400_BAD_REQUEST: {'error': {'type': 'string'}},
            status.HTTP_500_INTERNAL_SERVER_ERROR: {'error': {'type': 'string'}},
            status.HTTP_200_OK: {'error': {'type': 'string'}},
            },
        operation_id="register_user",
        tags=["User"],
    )
    def post(self, request):
        try:
            print("passed 0")
            data = request.data

            name = data["name"] if data["name"] != None else ""
            email = data["email"]
            password = data["password"]
            password2 = data["password2"]
            phone = data["phone"] if data["phone"] != None else ""
            company = data["company"] if data["company"] != None else ""
            company_url = data["url"] if data["url"] != None else ""
            role = "Client"
            username = email

            print("passed")

            if User.objects.filter(email=email).exists():
                return Response(
                    {"error": "Email already exists"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if password != password2:
                return Response(
                    {"error": "Passwords do not match"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if len(password) >= 8:
                print("passed 1")
                try:
                    user = User.objects.create_user(
                        first_name=name,
                        username=username,
                        password=password,
                        email=email,
                    )

                    print(f"{company} {company_url} {phone}")
                    client = Client(user=user, email=email, name=name)

                    phone = '"{}"'.format(phone)
                    client.phone = PhoneNumber.from_string(str(phone))
                    print(f"client phone {client.phone}")
                    client.company = company
                    client.save()

                    role = Role(user=user, role=role)
                    role.save()

                except IntegrityError as e:
                    # handle the case where a user with the same email already exists
                    print("Error creating client: ", e)

                subject = "Account Activation"
                activate_url = (
                    "https://api.orangewaves.tech/"
                    + "activate/"
                    + str(user.pk)
                    + "/"
                    + account_activation_token.make_token(user)
                    + "/"
                )
                message = f"""
                   Hey there{name},
                   Thank you for signing up for NSNCO,
                      Please click on the link below to activate your account
                        {activate_url}
                    Regards,
                    Team NsN
                    """
                return Response(
                    {"message": "User created successfully"},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"error": "Password must be at least 8 characters"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            print(e)
            if str(e) == "User has no client.":
                return Response(
                    {"success": "User is created successfully"},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"error": "Something went wrong", "error_message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ValidateToken(APIView):
    """verify token

    Args:
        APIView (POST): Validate user by token

    Returns:
        User: User details along with message
    """

    permission_classes = (permissions.AllowAny,)

    @extend_schema(
        request={
            "type": "object",
            "properties": {
                "token": {"type": "string"},
            },
            "required": ["token"],
        },
        responses={
            status.HTTP_200_OK: {'user': {'type': 'object'}, 'status': {'type': 'string'}, 'msg': {'type': 'string'}},
            status.HTTP_400_BAD_REQUEST: {'status': {'type': 'string'}, 'msg': {'type': 'string'}}
        },
        operation_id="validate_token",
        tags=["User"],
    )
    def post(self, request):
        data = request.data
        token = data["token"]

        if Token.objects.filter(key=token).exists():
            token = get_object_or_404(Token, key=token)
            user = User.objects.get(email=token.user.email)

            response = {
                "name": user.first_name + " " + user.last_name,
                "email": user.email,
            }

            try:
                role = Role.objects.get(user=user)
            except:
                role = None

            if role:
                if role.role == "Client":
                    client = Client.objects.get(user=user)
                    response["role"] = "Client"
                    response["phone"] = str(client.phone)
                    response["company"] = client.company
                    response["image"] = f"{client.image.url}"
                elif role.role == "PM":
                    response["role"] = "PM"
                elif role.role == "AM":
                    response["role"] = "AM"
                else:
                    response["role"] = "Unknown"

            return Response(
                {
                    "user": response,
                    "status": "success",
                    "msg": "Token is valid",
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "status": "failed",
                    "msg": "Token is invalid",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserDetailsView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses={
            status.HTTP_200_OK: {'user': {'type': 'object'}, 'role': {'type': 'string'}},
            status.HTTP_400_BAD_REQUEST: {'message': {'type': 'string'}}
        },
        operation_id="get_user_details",
        tags=["User"],
    )
    def get(self, request, *args, **kwargs):
        try:
            role = get_object_or_404(Role, user=request.user)
            if role.role == "Client":
                client = get_object_or_404(Client, user=request.user)
                client_serializer = ClientSerializer(instance=client, many=False)
                return Response(
                    {"user": client_serializer.data, "role": role.role},
                    status=status.HTTP_200_OK,
                )
            elif role.role == "AM":
                user = {
                    "name": request.user.first_name + " " + request.user.last_name,
                    "email": request.user.email,
                }
                return Response(
                    {"user": user, "role": role.role}, status=status.HTTP_200_OK
                )
            elif role.role == "Product Manager":
                user = {
                    "name": request.user.first_name + " " + request.user.last_name,
                    "email": request.user.email,
                }
                return Response(
                    {"user": user, "role": role.role}, status=status.HTTP_200_OK
                )
        except Exception as e:
            return Response(
                {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )
