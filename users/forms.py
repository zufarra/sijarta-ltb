import re

from django import forms


class PenggunaRegistrationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update_ids("pengguna")

        for field in self.fields:
            if field == "gender":
                self.apply_classes(field, "form-check-input")
                continue

            self.apply_classes(field, "form-control")

    name = forms.CharField(
        min_length=2,
        max_length=254,
        required=True,
    )
    password = forms.CharField(
        min_length=8,
        max_length=254,
        required=True,
    )
    gender = forms.ChoiceField(
        choices=[("M", "Male"), ("F", "Female")],
        required=True,
        widget=forms.RadioSelect(),
    )
    phone_number = forms.CharField(
        min_length=10,
        max_length=15,
        required=True,
        widget=forms.TextInput(),
    )
    birthdate = forms.DateField(
        required=True,
        widget=forms.DateInput(
            attrs={
                "type": "date",
            }
        ),
    )
    address = forms.CharField(
        min_length=10,
        max_length=254,
        required=True,
    )

    def update_ids(self, id_prefix=""):
        for fields in self.fields:
            self.fields[fields].widget.attrs.update({"id": f"{id_prefix}-{fields}"})

    def apply_classes(self, field, classes=""):
        self.fields[field].widget.attrs.update({"class": f"{classes}"})

    def clean_name(self):
        name = self.cleaned_data["name"]
        if not re.match(r"^[a-zA-Z\s]+$", name):
            raise forms.ValidationError("Name must only contain letters and spaces")
        return name

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        if not phone_number.isdigit():
            raise forms.ValidationError("Phone number must only contain numbers")
        return phone_number

    def clean_birthdate(self):
        birthdate = self.cleaned_data["birthdate"]
        if birthdate.year < 1900:
            raise forms.ValidationError("Birthdate must be after 1900")
        return birthdate


class PekerjaRegistrationForm(PenggunaRegistrationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update_ids("pekerja")
        for field in self.fields:
            if field == "gender":
                self.apply_classes(field, "form-check-input")
                continue

            if field == "bank_name":
                self.apply_classes(field, "form-select")
                continue

            self.apply_classes(field, "form-control")

    bank_name = forms.ChoiceField(
        choices=[
            ("GoPay", "GoPay"),
            ("OVO", "OVO"),
            ("Virtual Account BCA", "Virtual Account BCA"),
            ("Virtual Account BNI", "Virtual Account BNI"),
            ("Virtual Account Mandiri", "Virtual Account Mandiri"),
        ],
        required=True,
        widget=forms.Select(),
    )
    bank_account_number = forms.CharField(min_length=10, max_length=15, required=True)
    npwp = forms.CharField(min_length=15, max_length=15, required=True)
    photo_url = forms.URLField(required=True)

    def clean_bank_account(self):
        bank_account = self.cleaned_data["bank_account"]
        if not bank_account.isdigit():
            raise forms.ValidationError("Bank account must only contain numbers")
        return bank_account

    def clean_npwp(self):
        npwp = self.cleaned_data["npwp"]
        if not npwp.isdigit():
            raise forms.ValidationError("NPWP must only contain numbers")
        return npwp
