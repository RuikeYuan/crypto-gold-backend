from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
import time

class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]



    def post(self, request, *args, **kwargs):
        start_time = time.time()

        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not old_password or not new_password:
            return Response({'error': 'Old password and new password are required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        print(f"Time before check_password: {time.time() - start_time}s")

        # Check if the old password is correct
        if not check_password(old_password, user.password):
            return Response({'error': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

        print(f"Time after check_password: {time.time() - start_time}s")

        # Update the password
        user.set_password(new_password)
        user.save()

        print(f"Time after saving user: {time.time() - start_time}s")

        # Update the session authentication hash to prevent the user from being logged out
        update_session_auth_hash(request, user)

        print(f"Time after update_session_auth_hash: {time.time() - start_time}s")

        return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)

