# from django.contrib import admin


# # Register your models here.
# admin.site.register(Article)
# admin.site.register(CandidateListForbidden)
# admin.site.register(EbRecSysConfig)
# admin.site.register(ModelDefinition)
# admin.site.register(ModelService)
# admin.site.register(RecommenderVersion)

from .models import CandidateListForbidden, CandidateList, ModelService, ModelDefinition, SegmentMatch, RecommenderVersion


from django.contrib import admin

#######################
#  Custom adminviews  #
#######################


class AdminSegmentMatch(admin.ModelAdmin):
    model = SegmentMatch
    list_display = ("id", "name")


admin.site.register(CandidateListForbidden)
admin.site.register(CandidateList)
admin.site.register(ModelService)
admin.site.register(ModelDefinition)
admin.site.register(RecommenderVersion)
admin.site.register(SegmentMatch, AdminSegmentMatch)
