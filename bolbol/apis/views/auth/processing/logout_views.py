# from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status


# class LogoutAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     http_method_names = ["post"]

#     def post(self, request):
#         # Blacklist all tokens for the user
#         user = request.user
#         tokens = OutstandingToken.objects.filter(user=user)
#         for token in tokens:
#             BlacklistedToken.objects.get_or_create(token=token)

#         return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
    

# class LogoutAPIView(APIView):
#     def post(self, request):
#         try:
#             # Blacklist the refresh token if provided in the request
#             refresh_token = request.data.get("refresh")
#             if refresh_token:
#                 token = RefreshToken(refresh_token)
#                 token.blacklist()

#             # Log the user out of the session
#             logout(request)
#             return Response({"detail": "Logged out successfully."}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)