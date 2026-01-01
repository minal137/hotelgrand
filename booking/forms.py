from django import forms
from .models import Booking, Room

class PrivateBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["room", "check_in", "check_out","special_requests", "rating", "review"]
        widgets = {
            "check_in": forms.DateInput(attrs={"type": "date"}),
            "check_out": forms.DateInput(attrs={"type": "date"}),
            "special_requests": forms.Textarea(attrs={"rows": 3}),
            "review": forms.Textarea(attrs={"rows": 3}),
        }
    def clean(self):
        cleaned_data = super().clean()
        room = cleaned_data.get("room")
        check_in = cleaned_data.get("check_in")
        check_out = cleaned_data.get("check_out")

        if room and check_in and check_out:
            conflict = Booking.objects.filter(
                room=room,
                check_in__lt=check_out,
                check_out__gt=check_in
            )
            if conflict.exists():
                raise forms.ValidationError("❌ This room is already booked for the selected dates.")
        return cleaned_data
    
    from django import forms
from .models import Booking, Room

class PrivateBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["room", "check_in", "check_out","special_requests", "rating", "review"]
        widgets = {
            "check_in": forms.DateInput(attrs={"type": "date"}),
            "check_out": forms.DateInput(attrs={"type": "date"}),
            "special_requests": forms.Textarea(attrs={"rows": 3}),
            "review": forms.Textarea(attrs={"rows": 3}),
        }
    def clean(self):
        cleaned_data = super().clean()
        room = cleaned_data.get("room")
        check_in = cleaned_data.get("check_in")
        check_out = cleaned_data.get("check_out")

        if room and check_in and check_out:
            conflict = Booking.objects.filter(
                room=room,
                check_in__lt=check_out,
                check_out__gt=check_in
            )
            if conflict.exists():
                raise forms.ValidationError("❌ This room is already booked for the selected dates.")
        return cleaned_data
    
    def clean_rating(self):
        rating = self.cleaned_data.get("rating")
        if rating and (rating < 1 or rating > 5):
            raise forms.ValidationError("Rating must be between 1 and 5 stars.")
        return rating

    







class AvailabilityForm(forms.Form):
    check_in = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    check_out = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    

