from django import forms
from rango.models import Page, Category, User, UserProfile


class CategoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically set max_length for the 'name' field
        self.fields["name"].max_length = self._meta.model._meta.get_field(
            "name"
        ).max_length
        self.fields["name"].help_text = "Please enter the category name."

    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Category
        fields = ("name",)


class PageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically set max_length for the 'name' field
        self.fields["title"].max_length = self._meta.model._meta.get_field(
            "title"
        ).max_length
        self.fields["url"].max_length = self._meta.model._meta.get_field(
            "url"
        ).max_length

    title = forms.CharField(help_text="Please enter the title of the page.")
    url = forms.URLField(help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get("url")
        # If url is not empty and doesn't start with 'http://',
        # then prepend 'http://'.
        if url and not url.startswith("http://"):
            url = f"http://{url}"
            cleaned_data["url"] = url
        return cleaned_data

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Page

        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values; we may not want to include them.
        # Here, we are hiding the foreign key.
        # we can either exclude the category field from the form,
        exclude = ("category",)


# or specify the fields to include (don't include the category field).
# fields = ('title', 'url', 'views')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
        )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            "website",
            "picture",
        )
