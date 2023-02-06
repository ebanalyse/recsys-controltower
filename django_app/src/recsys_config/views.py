# from django.shortcuts import render
from django.forms import inlineformset_factory
from rest_framework import viewsets, status
from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from django.http import HttpResponse, JsonResponse, Http404
import json
from django.views import View
from django.views.defaults import bad_request, server_error
from django.template import loader
from django.shortcuts import render
# from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from recsys_config.serializers import ConfigurationSerializer, RecommenderVersionSerializer
from recsys_config import models
from recsys_config.forms import (
    RecommenderVersionForm,
    SegmentMatchForm,
    ModelDefinitionForm,
    CandidateListForm,
    ModelServiceForm,
    CandidateListForbiddenForm
)
from common.utils import EngageListsAPI, MimisbrunrrAPI
# Create your views here.


def index(request):
    recommender_versions = models.RecommenderVersion.objects.first()
    recommender_versions = [recommender_versions]
    template = loader.get_template('recsys_config/index.html')
    context = {
        'recommender_versions': recommender_versions,
    }
    return HttpResponse(template.render(context, request))

#######################
#  CUSTOM CRUD views  #
#######################


class RecommenderVersionView(APIView):
    def get(self, request, id):
        if id:
            template = "recsys_config/recommender-version-popup.html"
            if id < 0:
                form = RecommenderVersionForm()
            else:
                recommender_version = models.RecommenderVersion.objects.get(
                    id=id)
                form = RecommenderVersionForm(
                    instance=recommender_version, id=id)

            context = {
                "form": form
            }
        else:
            candidate_lists = models.CandidateList.objects.all()
            model_services = models.ModelService.objects.all().order_by('id')
            recommender_versions = models.RecommenderVersion.objects.all().order_by('id')
            template = "recsys_config/index.html"
            context = {
                'recommender_versions': recommender_versions,
                'candidate_lists': candidate_lists,
                'model_services': model_services,
            }

        return render(request=request,
                      template_name=template,
                      context=context)

    def post(self, request, id):
        # recommender_version = models.RecommenderVersion.objects.get(id=id)
        form = RecommenderVersionForm(
            request.data)
        if form.is_valid():
            form.save()
            template = "recsys_config/recommender-version-popup.html"
            context = {
                "form": form
            }
            resp = render(request=request,
                          template_name=template,
                          context=context)
            resp.headers["HX-Trigger"] = "reloadRecList"
            return resp

    def put(self, request, id):
        recommender_version = models.RecommenderVersion.objects.get(id=id)
        form = RecommenderVersionForm(
            request.data, instance=recommender_version, id=id)
        if form.is_valid():
            form.save()
            template = "recsys_config/recommender-version-popup.html"
            context = {
                "form": form
            }
            resp = render(request=request,
                          template_name=template,
                          context=context)
            resp.headers["HX-Trigger"] = "reloadRecList"
            return resp

        return server_error(request, template_name='500.html')

    def delete(self, request, id):
        recommender_version = models.RecommenderVersion.objects.get(id=id)
        recommender_version.delete()

        return Response(status=status.HTTP_204_NO_CONTENT, headers={"HX-Trigger": "reloadRecList"})


class SegmentMatchView(APIView):

    def get(self, request, recommender_version_id, segment_match_id):
        template = "recsys_config/segment-match-popup.html"
        if segment_match_id is not None:
            segment_match = models.SegmentMatch.objects.get(
                id=segment_match_id)
            form = SegmentMatchForm(
                instance=segment_match, recommender_version_id=recommender_version_id, segment_match_id=segment_match_id)
        else:
            print(segment_match_id, recommender_version_id)
            form = SegmentMatchForm(
                recommender_version_id=recommender_version_id)

        context = {
            "form": form
        }

        return render(request=request, template_name=template, context=context)

    def post(self, request, recommender_version_id, segment_match_id):
        # recommender_version = models.RecommenderVersion.objects.get(id=id)
        form = SegmentMatchForm(request.data)
        if form.is_valid():
            recommender_version = models.RecommenderVersion.objects.get(
                id=recommender_version_id)
            obj = form.save()
            recommender_version.segment_matches.add(obj)
            recommender_version.save()
            # template = "recsys_config/segment-match-popup.html"
            return Response(status=status.HTTP_201_CREATED, headers={"HX-Trigger": "reloadRecList"})

    def put(self, request, recommender_version_id, segment_match_id):
        segment_match = models.SegmentMatch.objects.get(id=segment_match_id)
        form = SegmentMatchForm(
            request.data,
            instance=segment_match,
            segment_match_id=segment_match_id,
            recommender_version_id=recommender_version_id
        )
        if form.is_valid():
            form.save()
            return Response(status=status.HTTP_204_NO_CONTENT, headers={"HX-Trigger": "reloadRecList"})

    def delete(self, request, recommender_version_id, segment_match_id):
        segment_match = models.SegmentMatch.objects.get(id=segment_match_id)
        segment_match.delete()
        return Response(status=status.HTTP_204_NO_CONTENT, headers={"HX-Trigger": "reloadRecList"})


class ModelDefinitionView(APIView):

    def get(self, request, recommender_version_id, segment_match_id, model_definition_id):
        template = "recsys_config/model-definition-popup.html"
        if model_definition_id is not None:
            model_definition = models.ModelDefinition.objects.get(
                id=model_definition_id)
            form = ModelDefinitionForm(
                instance=model_definition,
                recommender_version_id=recommender_version_id,
                segment_match_id=segment_match_id,
                model_definition_id=model_definition_id
            )
        else:
            form = ModelDefinitionForm(
                recommender_version_id=recommender_version_id, segment_match_id=segment_match_id)

        context = {
            "form": form
        }

        return render(request=request, template_name=template, context=context)

    def post(self, request, recommender_version_id, segment_match_id, model_definition_id):
        # recommender_version = models.RecommenderVersion.objects.get(id=id)
        form = ModelDefinitionForm(
            request.data,
            recommender_version_id=recommender_version_id,
            segment_match_id=segment_match_id
        )
        if form.is_valid():
            segment_match = models.SegmentMatch.objects.get(
                id=segment_match_id)
            obj = form.save()
            segment_match.models.add(obj)
            segment_match.save()
            return Response(status=status.HTTP_201_CREATED, headers={"HX-Trigger": "reloadRecList"})

    def put(self, request, recommender_version_id, segment_match_id, model_definition_id):
        model_definition = models.ModelDefinition.objects.get(
            id=model_definition_id)
        form = ModelDefinitionForm(
            request.data,
            instance=model_definition,
            segment_match_id=segment_match_id,
            recommender_version_id=recommender_version_id,
            model_definition_id=model_definition_id
        )
        if form.is_valid():
            form.save()
            return Response(status=status.HTTP_204_NO_CONTENT, headers={"HX-Trigger": "reloadRecList"})

    def delete(self, request, recommender_version_id, segment_match_id, model_definition_id):
        model_definition = models.ModelDefinition.objects.get(
            id=model_definition_id)
        model_definition.delete()
        return Response(status=status.HTTP_204_NO_CONTENT, headers={"HX-Trigger": "reloadRecList"})


class CandidateListView(APIView):

    def get(self, request, candidate_list_name):
        template = "recsys_config/candidatelist-popup.html"
        if candidate_list_name is not None:
            candidate_list = models.CandidateList.objects.get(
                name=candidate_list_name)
            form = CandidateListForm(
                instance=candidate_list,
                candidate_list_name=candidate_list_name,
            )
        else:
            form = CandidateListForm()

        context = {
            "form": form
        }

        return render(request=request, template_name=template, context=context)
    # def get(self, request, candidate_list_name):
        # template = "recsys_config/candidatelist-popup.html"
        # # CandidateListFormSet = inlineformset_factory(
            # # CandidateListForbiddenForm,
            # # CandidateListForm
        # # )

        # if candidate_list_name is not None:
            # candidate_list = models.CandidateList.objects.get(
                # name=candidate_list_name)
            # form = CandidateListFormSet(instance=candidate_list, candidate_list_name=candidate_list_name)
            # # form = CandidateListForm(
                # # instance=candidate_list,
                # # candidate_list_name=candidate_list_name
            # # )
        # else:
            # # form = CandidateListForm()
            # form = CandidateListFormSet()

        # context = {
            # "form": form
        # }

        # return render(request=request, template_name=template, context=context)

    def post(self, request, candidate_list_name):
        # CandidateListFormSet = inlineformset_factory(
            # CandidateListForm, CandidateListForbiddenForm)
        # form = CandidateListFormSet(request.data)
        form = CandidateListForm(
            request.data
        )
        if form.is_valid():
            obj = form.save()

            return Response(status=status.HTTP_201_CREATED, headers={"HX-Trigger": "reloadRecList"})

    def put(self, request, candidate_list_name):
        candidate_list = models.CandidateList.objects.get(
            name=candidate_list_name)
        form = CandidateListForm(
            request.data,
            instance=candidate_list,
            candidate_list_name=candidate_list_name
        )
        if form.is_valid():
            form.save()
            return Response(status=status.HTTP_204_NO_CONTENT, headers={"HX-Trigger": "reloadRecList"})

    def delete(self, request, candidate_list_name):
        candidate_list = models.CandidateList.objects.get(
            name=candidate_list_name)
        candidate_list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT, headers={"HX-Trigger": "reloadRecList"})


class ModelServiceView(APIView):

    def get(self, request, model_service_id):
        template = "recsys_config/crispy-form-popup.html"
        if model_service_id is not None:
            model_service = models.ModelService.objects.get(
                id=model_service_id)
            form = ModelServiceForm(
                instance=model_service, model_service_id=model_service_id)
        else:
            form = ModelServiceForm()

        context = {
            "form": form
        }

        return render(request=request, template_name=template, context=context)

    def post(self, request, model_service_id):
        form = ModelServiceForm(request.data)
        if form.is_valid():
            obj = form.save()
            return Response(status=status.HTTP_201_CREATED, headers={"HX-Trigger": "reloadRecList"})

    def put(self, request, model_service_id):
        model_service = models.ModelService.objects.get(id=model_service_id)
        print(model_service)
        form = ModelServiceForm(request.data,
                                instance=model_service,
                                model_service_id=model_service_id)
        print(form.is_valid(), form.errors)
        if form.is_valid():
            form.save()
            return Response(status=status.HTTP_204_NO_CONTENT, headers={"HX-Trigger": "reloadRecList"})

    def delete(self, request, model_service_id):
        model_service = models.ModelService.objects.get(id=model_service_id)
        model_service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT, headers={"HX-Trigger": "reloadRecList"})

#######################
#  CUSTOM CRUD views  #
#######################


class EngageListVisualView(APIView):
    def get(self, request, list_name):
        template = "recsys_config/article-list.html"
        article_ids = EngageListsAPI().get_list(list_name)
        article_data = MimisbrunrrAPI().get_articles(article_ids)
        for idx, article in enumerate(article_data):
            # if article["image_ids"]
            if idx == 0:
                print(article)
            if article['image_ids'] and len(article['image_ids']) > 0:
                article_data[idx]["image_url"] = \
                    f"https://ekstrabladet.dk/svc/next/image/{article['id']}/p300/"

        context = {
            "articles": article_data
        }

        return render(request=request, template_name=template, context=context)


class RecommenderVersionDetail(APIView):

    def get_object(self, pk):
        try:
            return models.RecommenderVersion.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk, format=None):
        recommender_version = self.get_object(pk)
        serializer = RecommenderVersionSerializer(recommender_version)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        recommender_version = self.get_object(pk)
        serializer = RecommenderVersionSerializer(
            recommender_version, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        recommender_version = self.get_object(pk)
        recommender_version.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecommenderVersionList(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """

    def get(self, request, format=None):
        recommender_versions = models.RecommenderVersion.objects.all()
        serializer = RecommenderVersionSerializer(
            recommender_versions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RecommenderVersionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@ api_view(['GET', 'PUT'])
def recsys_configuration(request):
    recommender_versions = models.RecommenderVersion.objects.all()
    candidate_lists = models.CandidateList.objects.all()
    model_services = models.ModelService.objects.all()

    data = {
        "recommender_versions": recommender_versions,
        "candidate_lists": candidate_lists,
        "models": model_services,
        "inview_api_endpoint": "https://eb-ml-pipeline-prod.com/inview-api/get-user-blacklist"
    }

    if request.method == 'GET':
        serializer = ConfigurationSerializer(data)
        # serializer = RecommenderVersionSerializer(
        # recommender_versions, many=True)
        # return JsonResponse(serializer.data, safe=False)
        return HttpResponse(CamelCaseJSONRenderer().render(serializer.data), headers={"Content-Type": "application/json"})


def recsys_config_admin_view(request):
    recommender_versions = models.RecommenderVersion.objects.all()
    candidate_lists = models.CandidateList.objects.all()
    model_services = models.ModelService.objects.all()

    data = {
        "recommender_versions": recommender_versions,
        "candidate_lists": candidate_lists,
        "models": model_services,
        "inview_api_endpoint": "https://eb-ml-pipeline-prod.com/inview-api/get-user-blacklist"
    }

    if request.method == 'GET':
        serializer = ConfigurationSerializer(data)
        return HttpResponse(CamelCaseJSONRenderer().render(serializer.data), headers={"Content-Type": "application/json"})
