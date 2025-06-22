from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class LogoutView(APIView):

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"detail": "Logout realizado com sucesso."}, status=status.HTTP_200_OK)
