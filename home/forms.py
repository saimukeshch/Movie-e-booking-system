from django import forms
from .models import Promotion



class CreatePromo(forms.Form):
    amount = forms.IntegerField()
    valid = forms.DateField()

    class Meta():
        model = Promotion
        fields = ('amount', 'valid')

    def save(self, commit=True):
        data = self.cleaned_data
        promo = Promotion(amount=data['amount'], valid_thru=data['valid'])
        if commit:
            promo.save()
        return promo


class SendPromo(forms.Form):
    promos = forms.ModelChoiceField(queryset=Promotion.objects.all())

    class Meta():
        model = Promotion