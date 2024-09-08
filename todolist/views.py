from rest_framework import status
from django.http import Http404
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.authtoken.models import Token
from todolist.models import TodoItem
from todolist.serializers import TodoItemSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class TodoItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
 # GET request to fetch todos assigned to the authenticated user
    def get(self, request, format=None):
        todos = TodoItem.objects.filter(author=request.user)
        serializer = TodoItemSerializer(todos, many=True)
        return Response(serializer.data)
  # POST request to create & save new todos assigned to the authenticated user
    def post(self, request, format=None):
        data = request.data
        data['author'] = request.user.id  
        serializer = TodoItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()  
        return Response(serializer.data)
    # DELETE request to delete a todos assigned to the authenticated user
    def delete(self, request, format=None):
        data = request.data
        try:
            todo_id = data.get('id')
            todo = TodoItem.objects.get(pk=todo_id, author=request.user)
        except TodoItem.DoesNotExist:
            raise Http404

        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
class LoginView(ObtainAuthToken):
   def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })