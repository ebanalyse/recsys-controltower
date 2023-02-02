from django.urls import register_converter, path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
# router.register(r'recommender-versions', views.RecommenderVersionViewSet)


class NegativeIntConverter:
    regex = r'-?\d+'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '%d' % value


register_converter(NegativeIntConverter, 'uint')

urlpatterns = [
    path('', include(router.urls)),
    path('recsys-config',
         views.recsys_configuration),
    path('model-services',
         views.ModelServiceView.as_view(),
         {"model_service_id": None},
         name="model-services"),
    path('model-services/<int:model_service_id>/',
         views.ModelServiceView.as_view(),
         name="model-services"),
    path('candidate-lists',
         views.CandidateListView.as_view(),
         {"candidate_list_name": None},
         name="candidate-lists"),
    path('candidate-lists/<str:candidate_list_name>/',
         views.CandidateListView.as_view(),
         name="candidate-lists"),
    path('recommender-versions',
         views.RecommenderVersionView.as_view(),
         {"id": None},
         name="recommender-versions"),
    path('recommender-versions/<uint:id>/',
         views.RecommenderVersionView.as_view(),
         name="recommender-versions"),
    path('recommender-versions/<int:recommender_version_id>/segment-matches/',
         views.SegmentMatchView.as_view(),
         {"segment_match_id": None},
         name="segment-matches"),
    path('recommender-versions/<int:recommender_version_id>/segment-matches/<int:segment_match_id>/',
         views.SegmentMatchView.as_view(),
         name="segment-matches"),
    path('recommender-versions/<int:recommender_version_id>/segment-matches/<int:segment_match_id>/model-definitions',
         views.ModelDefinitionView.as_view(),
         {"model_definition_id": None},
         name="model-definitions"),
    path('recommender-versions/<int:recommender_version_id>/segment-matches/<int:segment_match_id>/model-definitions/<int:model_definition_id>',
         views.ModelDefinitionView.as_view(),
         name="model-definitions"),
    path('visualize-engage-list/<str:list_name>',
         views.EngageListVisualView.as_view(),
         name="visualize-engage-list"),
    # path('model-definitions',
    # views.ModelDefinitionView.as_view(),
    # name="model-definitions")
]
