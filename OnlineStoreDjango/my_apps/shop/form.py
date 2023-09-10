from django import forms


class gpt_Form(forms.Form):
    search_gpt = forms.CharField(label="Опишить що шукаєте.", max_length=200)
