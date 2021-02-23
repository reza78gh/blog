from weblog.models import Comment,Post,LikePost
from weblog.serializers import *
from rest_framework.generics import ListAPIView ,CreateAPIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView


class LikePostList(generics.ListAPIView):
    serializer_class = LikePostSerializer
    
    def get_queryset(self):
        post_id = self.kwargs.get('pk')
        return LikePost.objects.filter(post_id=post_id)


class DetailLikePost(generics.RetrieveUpdateDestroyAPIView):
    queryset = LikePost.objects.all()
    serializer_class = LikePostSerializer

class AddLikePost(generics.CreateAPIView):
    queryset = LikePost.objects.all()
    serializer_class = LikePostSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
   

class CommentCreateVeiw(APIView):
    def post(self, request):
        print('her post')
        comment = CommentSerializer(data=request.data)
        print(comment)
        if comment.is_valid():
            print('valid')
            post = Post.objects.get(pk=comment.data['post'])
            print('post find',post)
            Comment.objects.create(text=comment.data['text'], post=post, user=request.user)
            print('comment create')
            return Response(status=status.HTTP_201_CREATED)
        print('after vlaid')
        return Response(status=status.HTTP_400_BAD_REQUEST)
