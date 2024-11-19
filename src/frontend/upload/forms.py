from django import forms

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label='Upload CSV File')

class ColumnChoice(forms.Form):
    columns = forms.MultipleChoiceField(
        label='Select Columns',
        widget=forms.CheckboxSelectMultiple,
        required=True
    )