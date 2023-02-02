from crispy_forms.layout import Submit, Button, Field, BaseInput, Fieldset, Layout
from crispy_forms.helper import FormHelper
from django.forms import ModelForm
from django.urls import reverse_lazy, reverse
from .models import RecommenderVersion, SegmentMatch, ModelDefinition, CandidateList, ModelService, CandidateListForbidden


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
        exclude = ["models"]

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
        exclude = ["models"]

    def __init__(self, *args, **kwargs):
        recommender_version_id = kwargs.pop("recommender_version_id", None)
        segment_match_id = kwargs.pop("segment_match_id", None)
        model_definition_id = kwargs.pop("model_definition_id", None)
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
        if model_definition_id is not None:
            helper_attrs['hx-put'] = reverse_lazy(
                'model-definitions', args=(recommender_version_id, segment_match_id, model_definition_id))
        else:
            helper_attrs['hx-post'] = reverse_lazy(
                'model-definitions', args=(recommender_version_id, segment_match_id))

        self.helper.attrs = helper_attrs

        self.helper.add_input(
            Submit('submit',
                   'Submit',
                   data_bs_dismiss="modal",
                   style="margin-top:10px")
        )
        if model_definition_id is not None:
            self.helper.add_input(
                Button('delete',
                       'Delete',
                       css_class="btn btn-danger",
                       style="margin-top:10px",
                       hx_delete=reverse('model-definitions',
                                         args=(recommender_version_id, segment_match_id, model_definition_id)),
                       data_bs_dismiss="modal"))

        self.helper.add_input(
            Button('close',
                   'Close',
                   css_class="btn btn-secondary",
                   style="margin-top:10px",
                   data_bs_dismiss="modal")
        )


class CandidateListForbiddenForm(ModelForm):
    class Meta:
        model = CandidateListForbidden
        fields = "__all__"


class CandidateListForm(ModelForm):
    class Meta:
        model = CandidateList
        exclude = ["models"]

    def __init__(self, *args, **kwargs):
        candidate_list_name = kwargs.pop("candidate_list_name", None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        # self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.form_id = "candiate-list-form"
        helper_attrs = {
            'hx-target': '#candiate-list-form',
            'hx-swap': 'outerHTML'
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
