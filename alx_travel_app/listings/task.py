from rest_framework.viewsets import ModelViewSet
from .models import Booking
from .serializers import BookingSerializer
from .tasks import send_booking_confirmation_email

class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        booking = serializer.save()
        user_email = booking.user.email  # Ensure user has an email field
        booking_details = f"Booking ID: {booking.id}, Date: {booking.date}"
        
        # Trigger the Celery task
        send_booking_confirmation_email.delay(user_email, booking_details)
