from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Application
from .serializers import ApplicationSerializer
from .permissions import IsJobSeeker

class ApplyToJobView(generics.CreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsJobSeeker]

    def create(self, request, *args, **kwargs):
        job_id = request.data.get("job")

        # Prevent duplicate application
        if Application.objects.filter(user=request.user, job_id=job_id).exists():
            return Response(
                {"error": "You have already applied to this job"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)