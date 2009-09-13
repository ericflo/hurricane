from django import forms
 
class SearchForm(forms.Form):
    """
    A simple search form with a query input.
    """
    q = forms.CharField(max_length=50)