from .models import Project
from django.forms import ModelForm

class AddProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ['profile', 'post_date', 'voters', 'design_score','usability_score','content_score','average_design','average_usability','average_content','average_score']



# class RateForm(forms.Form):
#     design = forms.IntegerField(min_value= 1, max_value=10)
#     usability = forms.IntegerField(min_value= 1, max_value=10)
#     content = forms.IntegerField(min_value= 1, max_value=10)

# class EditProfileForm(ModelForm):
#     class Meta:
#         model = Profile
#         exclude = ['user']