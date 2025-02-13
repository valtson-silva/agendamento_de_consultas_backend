from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
 
class UserLogarView(APIView):
    # Faz o login de usuários
    
    def get(self, request):
        # Renderiza a página de login
        return render(request, 'login.html')
            
    def post(self, request):
        # Obtém os dados do usuário
        username = request.POST['username']
        password = request.POST['password']
        # Faz a autenticação
        user = authenticate(
            request,
            username=username,
            password=password
        )
        
        if user is not None:
            # Faz o login do usuário
            login(request, user)
            
            return Response({"message": "Login realizado com sucesso."}, status=status.HTTP_200_OK)
        else:
            
            return Response({"message": "Credenciais inválidas."}, status=status.HTTP_401_UNAUTHORIZED)
        
class LogoutView(APIView):
    # Faz o logout de usuários
    
    # verifica se o usuário está logado
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Faz o logout
        logout(request)
        
        return Response({"message": "Logout realizado com sucesso."}, status=status.HTTP_200_OK)
    
