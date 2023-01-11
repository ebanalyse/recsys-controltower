# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from recsys_config.serializers import RecommenderVersionSerializer
from recsys_config.models import RecommenderVersion
from djangorestframework_camel_case.render import CamelCaseJSONRenderer
# Create your views here.


def index(request):
    return HttpResponse("Test response")


@api_view(['GET', 'PUT'])
def recsys_configuration(request):
    recommender_versions = RecommenderVersion.objects.all()
    if request.method == 'GET':
        serializer = RecommenderVersionSerializer(
            recommender_versions, many=True)
        # return JsonResponse(serializer.data, safe=False)
        print(serializer.data)
        return HttpResponse(CamelCaseJSONRenderer().render(serializer.data), headers={"Content-Type": "application/json"})

    # elif request.method == 'PUT':
        # # serializer = SnippetSerializer(snippet, data=request.data)
        # # if serializer.is_valid():
        # # serializer.save()
        # # return Response(serializer.data)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
