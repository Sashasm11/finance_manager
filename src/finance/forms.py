from django import forms


# Валидация данных, перед их поступлением в Views
class CSVImportForm(forms.Form):
    csv_file = forms.FileField(
        widget=forms.FileInput(attrs={'accept': '.csv'})
    )
