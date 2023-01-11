from rest_framework import serializers
from . import models


class ModelDefinitionSerializer(serializers.ModelSerializer):
    model = serializers.StringRelatedField(many=False)
    candidate_list = serializers.StringRelatedField(many=False)
    fallback_model = serializers.StringRelatedField(many=False)

    class Meta:
        model = models.ModelDefinition
        exclude = ['id']


class SegmentMatchSerializer(serializers.ModelSerializer):
    models = ModelDefinitionSerializer(many=True)

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
    forbidden = CandidateListForbiddenSerializer()

    class Meta:
        model = models.CandidateList
        exclude = ['id']
