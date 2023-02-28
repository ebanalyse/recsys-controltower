from rest_framework import serializers
from . import models


class ModelDefinitionSerializer(serializers.ModelSerializer):
    # model = serializers.StringRelatedField(many=False)
    model_name = serializers.StringRelatedField(source="model")
    candidate_list_name = serializers.StringRelatedField(
        source="candidate_list", many=False)
    fallback_model = serializers.StringRelatedField(many=False)

    class Meta:
        model = models.ModelDefinition
        exclude = ['id', 'candidate_list']


class SegmentMatchSerializer(serializers.ModelSerializer):
    models = ModelDefinitionSerializer(source="model_definitions", many=True)

    class Meta:
        model = models.SegmentMatch
        fields = [
            "name",
            "user_type",
            "relevance_segment",
            "models",
        ]


class RecommenderVersionSerializer(serializers.ModelSerializer):
    segment_matches = SegmentMatchSerializer(many=True)

    class Meta:
        model = models.RecommenderVersion
        fields = [
            "name",
            "api_id",
            "cache_key",
            "model_selection_timeout_min",
            "allow_unhealthy",
            "segment_matches"
        ]


class CandidateListForbiddenSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CandidateListForbidden
        exclude = ['id']


class CandidateListSerializer(serializers.ModelSerializer):
    forbidden = CandidateListForbiddenSerializer(many=False)

    class Meta:
        model = models.CandidateList
        fields = '__all__'


class ModelServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ModelService
        exclude = ['id']


class ConfigurationSerializer(serializers.Serializer):
    recommender_versions = RecommenderVersionSerializer(many=True)
    candidate_lists = CandidateListSerializer(many=True)
    models = ModelServiceSerializer(many=True)
    inviewAPIEndpoint = serializers.CharField(source="inview_api_endpoint")

    class Meta:
        fields = ('recommender_versions',
                  'candidate_lists',
                  'models',
                  'inviewAPIEndpoint')


if __name__ == "__main__":
    recommender_versions = models.RecommenderVersion.objects.all()
    candidate_lists = models.CandidateList.objects.all()
    models = models.ModelService.objects.all()

    data = {
        "recommender_versions": recommender_versions,
        "candidate_lists": candidate_lists,
        "models": models,
        "inview_api_endpoint": "https://eb-ml-pipeline-prod.com/inview-api/get-user-blacklist"
    }

    class ConfigurationSerializer(serializers.Serializer):
        recommender_versions = RecommenderVersionSerializer(many=True)
        candidate_lists = CandidateListSerializer(many=True)
        models = ModelServiceSerializer(many=True)
        inviewAPIEndpoint = serializers.CharField(source="inview_api_endpoint")

        class Meta:
            fields = ('recommender_versions',
                      'candidate_lists',
                      'models',
                      'inviewAPIEndpoint')

    from rest_framework.renderers import JSONRenderer
    JSONRenderer().render(ConfigurationSerializer(data).data)
    # pprint.pprint(str(YAMLRenderer().render(RecommenderVersionSerializer(
    # recommender_versions[0]).data)))
