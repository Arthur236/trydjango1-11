from django import forms

from .models import Item
from restaurants.models import RestaurantLocation


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'restaurant',
            'name',
            'contents',
            'excludes',
            'public'
        ]

    def __init__(self, user=None, **kwargs):
        """
        Pass in user to form and update querysets
        """
        super(ItemForm, self).__init__(**kwargs)
        self.fields['restaurant'].queryset = RestaurantLocation.objects.filter(owner=user)
        # .exclude(item__isnull=False)
