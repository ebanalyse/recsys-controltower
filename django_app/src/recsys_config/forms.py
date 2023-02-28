from crispy_forms.layout import Submit, Button, Field, BaseInput, Fieldset, Layout
from django.contrib.postgres.forms import SimpleArrayField
from crispy_forms.helper import FormHelper
from django.forms import ModelForm
from django import forms
from django.forms.utils import ValidationError
from django.urls import reverse_lazy, reverse
from rest_framework.utils.model_meta import _get_fields
from .models import RecommenderVersion, SegmentMatch, ModelDefinition, CandidateList, ModelService, CandidateListForbidden
from typing import Optional


class RecommenderVersionForm(ModelForm):
    class Meta:
        model = RecommenderVersion
        exclude = ["segment_matches"]

    def __init__(self, *args, **kwargs):
        recommender_version_id = kwargs.pop("id", None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        # self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.form_id = "recommender-version-form"
        helper_attrs = {
            'hx-target': '#recommender-version-form',
            'hx-swap': 'outerHTML'
        }

        # if id is set set action url to: PUT /recommender_versions/<id>
        # otherwise: POST /recommender_versions
        if recommender_version_id is not None:
            helper_attrs['hx-put'] = f"{reverse_lazy('recommender-versions')}/{recommender_version_id}/"
        else:
            helper_attrs['hx-post'] = f"{reverse_lazy('recommender-versions')}"

        self.helper.attrs = helper_attrs

        self.helper.add_input(
            Submit('submit',
                   'Submit',
                   data_bs_dismiss="modal",
                   style="margin-top:10px")
        )
        if recommender_version_id is not None:
            self.helper.add_input(
                Button('delete',
                       'Delete',
                       css_class="btn btn-danger",
                       style="margin-top:10px",
                       hx_delete=f"{reverse_lazy('recommender-versions')}/{recommender_version_id}/",
                       data_bs_dismiss="modal"))

        self.helper.add_input(
            Button('close',
                   'Close',
                   css_class="btn btn-secondary",
                   style="margin-top:10px",
                   data_bs_dismiss="modal")
        )


class SegmentMatchForm(ModelForm):
    class Meta:
        model = SegmentMatch
        exclude = ["model_definitions"]

    def __init__(self, *args, **kwargs):
        recommender_version_id = kwargs.pop("recommender_version_id", None)
        segment_match_id = kwargs.pop("segment_match_id", None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        # self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.form_id = "segment-match-form"
        helper_attrs = {
            'hx-target': '#segment-match-form',
            'hx-swap': 'outerHTML'
        }

        # if id is set set action url to: PUT /recommender_versions/<id>
        # otherwise: POST /recommender_versions
        if segment_match_id is not None:
            helper_attrs['hx-put'] = reverse_lazy(
                'segment-matches', args=(recommender_version_id, segment_match_id))
        else:
            helper_attrs['hx-post'] = reverse_lazy(
                'segment-matches', args=(recommender_version_id,))

        self.helper.attrs = helper_attrs

        self.helper.add_input(
            Submit('submit',
                   'Submit',
                   data_bs_dismiss="modal",
                   style="margin-top:10px")
        )
        if segment_match_id is not None:
            self.helper.add_input(
                Button('delete',
                       'Delete',
                       css_class="btn btn-danger",
                       style="margin-top:10px",
                       hx_delete=reverse('segment-matches',
                                         args=(recommender_version_id, segment_match_id)),
                       data_bs_dismiss="modal"))

        self.helper.add_input(
            Button('close',
                   'Close',
                   css_class="btn btn-secondary",
                   style="margin-top:10px",
                   data_bs_dismiss="modal")
        )


class ModelDefinitionForm(ModelForm):
    class Meta:
        model = ModelDefinition
        exclude = ["segment_match"]

    def __init__(self, *args, **kwargs):
        self.recommender_version_id = kwargs.pop("recommender_version_id", None)
        self.segment_match_id = kwargs.pop("segment_match_id", None)
        self.model_definition_id = kwargs.pop("model_definition_id", None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        # self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.form_id = "model-definition-form"
        helper_attrs = {
            'hx-target': '#model-definition-form',
            'hx-swap': 'outerHTML'
        }

        # if id is set set action url to: PUT /recommender_versions/<id>
        # otherwise: POST /recommender_versions
        if self.model_definition_id is not None:
            helper_attrs['hx-put'] = reverse_lazy(
                'model-definitions', args=(self.recommender_version_id, self.segment_match_id, self.model_definition_id))
        else:
            helper_attrs['hx-post'] = reverse_lazy(
                'model-definitions', args=(self.recommender_version_id, self.segment_match_id))

        self.helper.attrs = helper_attrs

        self.helper.add_input(
            Submit('submit',
                   'Submit',
                   data_bs_dismiss="modal",
                   style="margin-top:10px")
        )
        if self.model_definition_id is not None:
            self.helper.add_input(
                Button('delete',
                       'Delete',
                       css_class="btn btn-danger",
                       style="margin-top:10px",
                       hx_delete=reverse('model-definitions',
                                         args=(self.recommender_version_id, self.segment_match_id, self.model_definition_id)),
                       data_bs_dismiss="modal"))

        self.helper.add_input(
            Button('close',
                   'Close',
                   css_class="btn btn-secondary",
                   style="margin-top:10px",
                   data_bs_dismiss="modal")
        )


    def save(self):
        data = self.cleaned_data
        # __import__('pdb').set_trace()

        if self.instance:
            obj = self.instance
        else:
            obj = ModelDefinition()

        obj.segment_match_id = self.segment_match_id

        obj.update(commit=True, **data)

        obj.save()
        return obj


class CandidateListForbiddenForm(ModelForm):
    articles = SimpleArrayField(forms.IntegerField(), widget=forms.Textarea, required=False)

    class Meta:
        model = CandidateListForbidden
        fields = "__all__"

class CandidateListForm(forms.Form):
    type = CandidateList._meta.get_field('type').formfield()
    name = CandidateList._meta.get_field('name').formfield()
    cid = CandidateList._meta.get_field('cid').formfield()
    shuffle = CandidateList._meta.get_field('shuffle').formfield()
    articles = SimpleArrayField(forms.IntegerField(), widget=forms.Textarea, required=False)
    forbidden = SimpleArrayField(forms.IntegerField(), widget=forms.Textarea, required=False)
    max_rate = CandidateListForbidden._meta.get_field('max_rate').formfield()

    def __init__(self, *args, **kwargs):
        self.instance :Optional[CandidateList] = kwargs.pop("instance", None)
        candidate_list_name = kwargs.pop("candidate_list_name", None)
        super().__init__(*args, **kwargs)

        self.fields['max_rate'].required = False

        if self.instance:
            self.fields['type'].initial = self.instance.type
            self.fields['name'].initial = self.instance.name
            self.fields['name'].widget.attrs['readonly'] = True
            self.fields['cid'].initial = self.instance.cid
            self.fields['shuffle'].initial = self.instance.shuffle
            self.fields['articles'].initial = self.instance.articles
            if self.instance.forbidden:
                self.fields['forbidden'].initial = self.instance.forbidden.articles
                self.fields['max_rate'].initial = self.instance.forbidden.max_rate


        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_id = "candiate-list-form"

        helper_attrs = {
            'hx-target': '#candiate-list-form',
            'hx-swap': 'outerHTML'
        }

        if candidate_list_name is not None:
            helper_attrs['hx-put'] = reverse_lazy(
                'candidate-lists', args=(candidate_list_name,))
        else:
            helper_attrs['hx-post'] = reverse_lazy(
                'candidate-lists')

        self.helper.attrs = helper_attrs

        self.helper.layout = Layout(
            Fieldset(
                '',
                'type',
                'name',
                'cid',
                'articles',
                'shuffle',
                Fieldset(
                'Forbidden articles',
                'forbidden',
                'max_rate',
                )
            ))

        self.helper.add_input(
            Submit('submit',
                   'Submit',
                   data_bs_dismiss="modal",
                   style="margin-top:10px")
        )
        if candidate_list_name is not None:
            self.helper.add_input(
                Button('delete',
                       'Delete',
                       css_class="btn btn-danger",
                       style="margin-top:10px",
                       hx_delete=reverse('candidate-lists',
                                         args=(candidate_list_name,)),
                       data_bs_dismiss="modal"))

        self.helper.add_input(
            Button('close',
                   'Close',
                   css_class="btn btn-secondary",
                   style="margin-top:10px",
                   data_bs_dismiss="modal")
        )

    def save(self):
        data = self.cleaned_data
        max_rate = data.pop("max_rate", 0.0)
        if max_rate is None: max_rate = 0.0
        forbidden_data = {
            'articles': data.pop("forbidden", []),
            'max_rate': max_rate
        }

        print(forbidden_data)

        if self.instance:
            obj = self.instance
        else:
            obj = CandidateList()

        obj.update(commit=True, **data)

        ## Store forbidden obj
        if self.instance:
            forbidden = self.instance.forbidden
        else:
            forbidden = CandidateListForbidden(**forbidden_data)

        forbidden.update(commit=True, **forbidden_data)

        # forbidden = for.save()
        obj.forbidden = forbidden
        # Saving your obj
        obj.save()

        return obj


class DCandidateListForm(ModelForm):
    articles = SimpleArrayField(forms.IntegerField(), widget=forms.Textarea, required=False)
    forbidden = SimpleArrayField(forms.IntegerField(), widget=forms.Textarea, required=False)
    max_rate = forms.FloatField(required=False)

    class Meta:
        model = CandidateList
        exclude = ["models", "forbidden"]

    def __init__(self, *args, **kwargs):
        candidate_list_name = kwargs.pop("candidate_list_name", None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.form_id = "candiate-list-form"
        helper_attrs = {
            'hx-target': '#candiate-list-form',
            'hx-swap': 'outerHTML',

        }

        # if id is set set action url to: PUT /recommender_versions/<id>
        # otherwise: POST /recommender_versions
        if candidate_list_name is not None:
            helper_attrs['hx-put'] = reverse_lazy(
                'candidate-lists', args=(candidate_list_name,))
        else:
            helper_attrs['hx-post'] = reverse_lazy(
                'candidate-lists')

        self.helper.attrs = helper_attrs

        # self.helper[] = Layout(
            # Fieldset("Forbidden articles",
                     # )
        # )

        self.helper.add_input(
            Submit('submit',
                   'Submit',
                   data_bs_dismiss="modal",
                   style="margin-top:10px")
        )
        if candidate_list_name is not None:
            self.helper.add_input(
                Button('delete',
                       'Delete',
                       css_class="btn btn-danger",
                       style="margin-top:10px",
                       hx_delete=reverse('candidate-lists',
                                         args=(candidate_list_name,)),
                       data_bs_dismiss="modal"))

        self.helper.add_input(
            Button('close',
                   'Close',
                   css_class="btn btn-secondary",
                   style="margin-top:10px",
                   data_bs_dismiss="modal")
        )

    def clean(self, *args, **kwargs):
        super().clean()
        forbidden = self.cleaned_data.get("forbidden", [])
        max_rate = self.cleaned_data.get("max_rate")

        if len(forbidden) > 0 and not max_rate:
            raise ValidationError("max_rate is not set")


    def save(self, commit=True):
        obj = super().save(commit=False)

        if commit:

            ## Store forbidden obj
            forbidden_form = CandidateListForbiddenForm(self.data)
            forbidden = forbidden_form.save()
            obj.forbidden = forbidden

            # Saving your obj
            obj.save()

        return obj


class ModelServiceForm(ModelForm):
    class Meta:
        model = ModelService
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        model_service_id = kwargs.pop("model_service_id", None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        # self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.form_id = "model-service-form"
        helper_attrs = {
            'hx-target': '#model-service-form',
            'hx-swap': 'outerHTML'
        }

        # if id is set set action url to: PUT /recommender_versions/<id>
        # otherwise: POST /recommender_versions
        if model_service_id is not None:
            helper_attrs['hx-put'] = reverse_lazy(
                'model-services', args=(model_service_id,))
        else:
            helper_attrs['hx-post'] = reverse_lazy(
                'model-services')

        self.helper.attrs = helper_attrs

        self.helper.add_input(
            Submit('submit',
                   'Submit',
                   data_bs_dismiss="modal",
                   style="margin-top:10px")
        )
        if model_service_id is not None:
            self.helper.add_input(
                Button('delete',
                       'Delete',
                       css_class="btn btn-danger",
                       style="margin-top:10px",
                       hx_delete=reverse('model-services',
                                         args=(model_service_id,)),
                       data_bs_dismiss="modal"))

        self.helper.add_input(
            Button('close',
                   'Close',
                   css_class="btn btn-secondary",
                   style="margin-top:10px",
                   data_bs_dismiss="modal")
        )
