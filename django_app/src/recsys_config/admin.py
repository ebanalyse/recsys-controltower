# from django.contrib import admin

# from .models import Article, CandidateListForbidden, EbRecSysConfig, ModelDefinition, ModelService, RecommenderVersion

# # Register your models here.
# admin.site.register(Article)
# admin.site.register(CandidateListForbidden)
# admin.site.register(EbRecSysConfig)
# admin.site.register(ModelDefinition)
# admin.site.register(ModelService)
# admin.site.register(RecommenderVersion)

from django.contrib import admin
from django.apps import apps

app = apps.get_app_config('recsys_config')

for model_name, model in app.models.items():
    admin.site.register(model)
