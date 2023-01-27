from recsys_config import models
from urllib3.util import url
import random
import factory
import faker
from os import name
from rest_framework_yaml.renderers import YAMLRenderer
import pprint
from rest_framework import serializers
# from rest_framework.renderers import JSONRenderer, YAMLRenderer


class CandidateListForbiddenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.CandidateListForbidden

    max_rate = factory.Faker("pyfloat", min_value=0.0, max_value=1.0)

    @factory.post_generation
    def articles(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for article in extracted:
                self.articles.add(article)


class StaticCandidateListFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.CandidateList

    type = models.CandidateList.STATIC
    cid = None
    shuffle = True
    name = factory.Sequence(lambda n: f'static-candidate-list-{n}')
    forbidden = factory.SubFactory(
        CandidateListForbiddenFactory
    )

    @factory.post_generation
    def articles(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for article in extracted:
                self.articles.append(article)


class EngageCandidateListFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.CandidateList

    articles = None
    type = models.CandidateList.ENGAGE
    shuffle = False
    # articles = models.Article.set()
    cid = factory.Iterator(
        ["most_read_last_24_hours",
         "recsys_latest_published_premium",
         "most_read_plus_7_days"]
    )
    name = factory.Sequence(lambda n: f"engage-candidatelist-{n}")
    # name = models.CharField(max_length=240)

    @factory.post_generation
    def articles(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for article in extracted:
                self.articles.add(article)


class ModelServiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ModelService

    name = factory.Iterator(["nrms-app-spot", "nrms-app"])
    url = factory.Iterator([
        "https://eb-ml-pipeline-prod.com/ebnrmsapp-spot/predict/",
        "https://eb-ml-pipeline-prod.com/ebnrmsapp/predict/"
    ])
    health_check_url = factory.Iterator([
        "https://eb-ml-pipeline-prod.com/ebnrmsapp-spot/health/",
        "https://eb-ml-pipeline-prod.com/ebnrmsapp/health/"
    ])


# class ModelDefinitionFactory(factory.django.DjangoModelFactory):
    # class Meta:
    # model = models.ModelDefinition
    # inline_args = ('model', 'candidate_list', 'fallback_model')

    # model = factory.SubFactory(ModelServiceFactory)
    # candidate_list = factory.SubFactory(models.CandidateList)
    # fallback_model = factory.SubFactory(ModelServiceFactory)
    # split = 1
    # wait_for_reply = False
    # use_context = False
    # cache_minutes = 10080
    # candidate_list_limit = 100
    # use_user_id = True
    # use_global_cache_key = False
    # remove_read = True
    # remove_exposed = True
    # throttling_timeout_sec = 0


# class SegmentMatchFactory(factory.django.DjangoModelFactory):
    # class Meta:
    # model = models.SegmentMatch


# class RecommenderVersionFactory(factory.django.DjangoModelFactory):
    # class Meta:
    # model = models.RecommenderVersion


my_faker = faker.Faker()

########################
#  Create article ids  #
########################

article_ids = []
for _ in range(40):
    article_ids.append(my_faker.pyint(min_value=9500000, max_value=9576903))

##################################
#  Create CandidateListForbidden #
##################################

candidate_list_forbidden = models.CandidateListForbidden.objects.first()
if not candidate_list_forbidden:
    candidate_list_forbidden = CandidateListForbiddenFactory.create()

    sample_articles = random.sample(article_ids, 10)
    for aid in sample_articles:
        candidate_list_forbidden.articles.append(aid)
    candidate_list_forbidden.save()


##########################
#  Create CandidateList  #
##########################

# Create candidatelist both: engage and static
candidatelists = models.CandidateList.objects.all()
if not candidatelists.exists():
    candidatelists_engage = EngageCandidateListFactory.create_batch(2)

    candidatelist_static = StaticCandidateListFactory.create(articles=article_ids,
                                                             forbidden=candidate_list_forbidden)
    candidatelist_static = StaticCandidateListFactory.create(
        articles=article_ids)
    candidatelists = models.CandidateList.objects.all()


#########################
#  Create ModelService  #
#########################

model_services = models.ModelService.objects.all()
if not model_services.exists():
    model_services = ModelServiceFactory.create_batch(2)

#############################
#  Create ModelDefinitions  #
#############################
model_definitions = models.ModelDefinition.objects.all()
if not model_definitions.exists():
    model_definition = models.ModelDefinition(
        model=model_services[0],
        candidate_list=candidatelists[0],
        fallback_model=None,
        split=1,
        wait_for_reply=False,
        use_context=False,
        cache_minutes=10080,
        candidate_list_limit=100,
        use_user_id=True,
        use_global_cache_key=False,
        remove_read=True,
        remove_exposed=True,
        throttling_timeout_sec=0,
    )
    model_definition.save()

    model_definition = models.ModelDefinition(
        model=model_services[0],
        candidate_list=candidatelists[1],
        fallback_model=None,
        split=1,
        wait_for_reply=False,
        use_context=False,
        cache_minutes=10080,
        candidate_list_limit=100,
        use_user_id=True,
        use_global_cache_key=False,
        remove_read=True,
        remove_exposed=True,
        throttling_timeout_sec=0,
    )
    model_definition.save()

    model_definition = models.ModelDefinition(
        model=model_services[1],
        candidate_list=candidatelists.first(),
        fallback_model=None,
        split=1,
        wait_for_reply=False,
        use_context=False,
        cache_minutes=10080,
        candidate_list_limit=100,
        use_user_id=True,
        use_global_cache_key=False,
        remove_read=True,
        remove_exposed=True,
        throttling_timeout_sec=0,
    )
    model_definition.save()

    model_definitions = models.ModelDefinition.objects.all()


################################
#  Create RecommenderVersions  #
#   and SegmentMatch'es        #
################################

# segment_match = models.SegmentMatch(
    # name="sso brugere",
    # user_type=models.SegmentMatch.SSO_ID_USER,
    # relevance_segment=None,
# )
# segment_match.save()
# segment_match.models.set([model_definitions[0], model_definitions[1]])

# Relevance segments name and id
relevance_segments = {
    "Recommender - Evige gratisbrugere": "4MiIr70MH8D8A2RvYroM1i",
    "Recommender - Abonnenter": "7mTj9c9cfqXIXbweHzZ6JE",
    "Recommender - Potentielle abonnenter": "4K0a51PHdpxbaFXtPW8Db8"
}

# positions and their API keys
positions = {
    "position1": "POS1",
    "position2": "POS2",
    "position3": "POS3",
    "position4": "POS4",
    "position5": "POS5",
    "position6": "POS6"
}

recommender_versions = models.RecommenderVersion.objects.all()
if not recommender_versions.exists():
    for position_name, cache_key in positions.items():
        recommender_version = models.RecommenderVersion(
            name=f"recom-{position_name}",
            api_id=f"recom-{position_name}",
            cache_key=cache_key,
            model_selection_timeout_min=10080,  # 1 week
            allow_unhealthy=False
        )
        recommender_version.save()

        segments = []

        for segment_name, relevance_segment in relevance_segments.items():
            segment_match = models.SegmentMatch(
                name=segment_name,
                user_type=models.SegmentMatch.ALL,
                relevance_segment=relevance_segment)
            segment_match.save()
            # sample 1-2 random models
            sample_models = random.sample(
                list(model_definitions), random.randint(1, 2))
            segment_match.models.set(sample_models)
            segments.append(segment_match)

        recommender_version.segment_matches.set(segments)
