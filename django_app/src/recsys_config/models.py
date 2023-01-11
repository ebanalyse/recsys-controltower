from django.db import models
from rest_framework import serializers
from django.contrib.postgres.fields import ArrayField

# Create your models here.


class CandidateListForbidden(models.Model):
    articles = ArrayField(models.IntegerField(), default=list)
    max_rate = models.FloatField()


class CandidateList(models.Model):
    ENGAGE = 'EN'
    STATIC = 'ST'
    LIST_TYPES = (
        (ENGAGE, 'engage'),
        (STATIC, 'static')
    )
    type = models.CharField(
        max_length=2,
        choices=LIST_TYPES,
        default=ENGAGE
    )
    cid = models.CharField(max_length=255, null=True)  # Id
    name = models.CharField(primary_key=True, max_length=255)
    articles = ArrayField(models.IntegerField(), default=list)
    # articles = models.ManyToManyField(
    # Article,
    # related_name="candidate_list_articles",
    # )
    shuffle = models.BooleanField()
    forbidden = models.ForeignKey(
        CandidateListForbidden,
        models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return str(self.name)


class ModelService(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    health_check_url = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)


class ModelDefinition(models.Model):
    model = models.ForeignKey(
        ModelService,
        on_delete=models.DO_NOTHING,
        null=True,
    )
    candidate_list = models.ForeignKey(
        CandidateList,
        on_delete=models.DO_NOTHING,
        null=True
    )  # CandidateListName
    fallback_model = models.ForeignKey(
        ModelService,
        on_delete=models.DO_NOTHING,
        related_name="fallback_model",
        null=True,
    )
    split = models.IntegerField()
    wait_for_reply = models.BooleanField()
    use_context = models.BooleanField()
    cache_minutes = models.IntegerField()
    candidate_list_limit = models.IntegerField()
    use_user_id = models.BooleanField()
    use_global_cache_key = models.BooleanField()
    remove_read = models.BooleanField()
    remove_exposed = models.BooleanField()
    throttling_timeout_sec = models.IntegerField()

    def __str__(self):
        return f"{self.model}---{self.candidate_list}"


# TODO: create custom "callable" segments, fixed segment for testing
#       ex. does id start with: a-c
class SegmentMatch(models.Model):
    SSO_ID_USER = 'SSO_ID'
    EB_ID_USER = 'EB_ID'
    ALL = 'ALL'
    NO_ID_USER = 'NO_CONSENT'
    USER_CHOICES = (
        (ALL, 'All'),
        (SSO_ID_USER, 'SSO id user'),
        (EB_ID_USER, 'EB id user'),
        (NO_ID_USER, 'No consent'),
    )

    name = models.CharField(max_length=255)
    user_type = models.CharField(max_length=20,
                                 choices=USER_CHOICES,
                                 default=ALL)
    relevance_segment = models.CharField(max_length=255, null=True)
    models = models.ManyToManyField(
        ModelDefinition,
        related_name="models"
    )

    def __str__(self):
        return str(self.name)


# TODO move cache_key and model_selection_timeout_min to segmentMatches to allow doing experiments at a segment
class RecommenderVersion(models.Model):
    name = models.CharField(max_length=255)
    api_id = models.CharField(max_length=255)
    cache_key = models.CharField(max_length=255)
    model_selection_timeout_min = models.IntegerField()
    allow_unhealthy = models.BooleanField()
    segment_matches = models.ManyToManyField(
        SegmentMatch,
        related_name="segment_matches"
    )

    def __str__(self):
        return str(self.name)

#################
#  Serializers  #
#################


class ModelDefinitionSerializer(serializers.ModelSerializer):
    model = serializers.StringRelatedField(many=False)
    candidate_list = serializers.StringRelatedField(many=False)
    fallback_model = serializers.StringRelatedField(many=False)

    class Meta:
        model = ModelDefinition
        fields = '__all__'


class SegmentMatchSerializer(serializers.ModelSerializer):
    models = ModelDefinitionSerializer(many=True)

    class Meta:
        model = SegmentMatch
        fields = '__all__'


class RecommenderVersionSerializer(serializers.ModelSerializer):
    segment_matches = SegmentMatchSerializer(many=True)

    class Meta:
        model = RecommenderVersion
        fields = '__all__'


# TODO: Create this at dump
# class EbRecSysConfig(models.Model):
    # recommender_versions = models.ManyToManyField(
        # RecommenderVersion,
        # related_name="recommender_versions",
    # )
    # candidate_lists = models.ManyToManyField(
        # CandidateList,
        # related_name="candidate_lists",
    # )
    # _models = models.ManyToManyField(
        # ModelService,
        # related_name="model_services",
    # )
    # inview_api_endpoint = models.CharField(max_length=255)
    # # s3_bucket = models.CharField(max_length=255)
    # # model_auth_header = models.CharField(max_length=255)
    # # environment = models.CharField(max_length=255)

    # articles = models.

    # type CandidateListForbidden struct {
    # Articles []int   `yaml:"articles"`
    # MaxRate  float64 `yaml:"max_rate"`
    # }

    # // CandidateLists
    # type CandidateLists struct {
    # Id        string                 `yaml:"id"`
    # Name      string                 `yaml:"name"`
    # Type      string                 `yaml:"type"`
    # Articles  []int                  `yaml:"articles"`
    # Shuffle   *bool                  `yaml:"shuffle" omitempty`
    # Forbidden CandidateListForbidden `yaml:"forbidden,omitempty"`
    # }


"""

type EbRecSysConfig struct {
	RecommenderVersions []RecommenderVersions `yaml:"recommenderVersions"`
	CandidateLists      []CandidateLists      `yaml:"candidateLists"`
	Models              []ModelServices       `yaml:"models"`
	InviewAPIEndpoint   string                `yaml:"inviewAPIEndpoint"`
	S3Bucket            string
	ModelAuthHeader     string
	Environment         string
}

// Models
type ModelServices struct {
	Name           string `yaml:"name"`
	Url            string `yaml:"url"`
	HealthCheckUrl string `yaml:"health"`
}

// Models
type ModelDefinitions struct {
	ModelName            string `yaml:"modelName"`
	FallbackModelName    string `yaml:"fallbackModelName"`
	ModelNamePostfix     string `yaml:"modelNamePostfix"`
	Split                int    `yaml:"split"`
	WaitForReply         *bool  `yaml:"wait_for_reply" omitempty`
	CandidateListName    string `yaml:"candidateListName"`
	UseContext           *bool  `yaml:"useContext" omitempty`
	CacheMinutes         int    `yaml:"cacheMinutes" omitempty`
	CandidateListLimit   int    `yaml:"candidateListLimit" omitempty`
	UseUserId            *bool  `yaml:"useUserId" omitempty`
	UseGlobalCacheKey    *bool  `yaml:"useGlobalCacheKey" omitempty`
	RemoveRead           *bool  `yaml:"removeRead" omitempty`
	RemoveExposed        *bool  `yaml:"removeExposed" omitempty`
	ThrottlingTimeoutSec int    `yaml:"throttlingTimeoutSec"`
}

// RecommenderVersions
type RecommenderVersions struct {
	Name                     string             `yaml:"name"`
	ApiId                    string             `yaml:"apiId"`
	CacheKey                 *string            `yaml:"cacheKey" omitempty`
	ModelSelectionTimeoutMin int                `yaml:"model_selection_timeout_min"`
	AllowUnhealthy           *bool              `yaml:"allow_unhealthy_selection" omitempty`
	Models                   []ModelDefinitions `yaml:"models"`
}

type CandidateListForbidden struct {
	Articles []int   `yaml:"articles"`
	MaxRate  float64 `yaml:"max_rate"`
}

// CandidateLists
type CandidateLists struct {
	Id        string                 `yaml:"id"`
	Name      string                 `yaml:"name"`
	Type      string                 `yaml:"type"`
	Articles  []int                  `yaml:"articles"`
	Shuffle   *bool                  `yaml:"shuffle" omitempty`
	Forbidden CandidateListForbidden `yaml:"forbidden,omitempty"`
}

"""
