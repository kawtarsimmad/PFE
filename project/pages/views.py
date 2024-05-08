from django.shortcuts import render
from publications.models import Publication
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from users.models import Association



# Create your views here.
def index(request):
    publications = Publication.objects.all()  # Fetch all publications
    return render(request, 'pages/index.html', {'publications': publications})

@require_GET
def get_nearby_associations(request):
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')

    user_location = Point(float(longitude), float(latitude), srid=4326)  # Create Point object
    associations = Association.objects.annotate(distance=Distance('location', user_location)).order_by('distance')[:10]

    data = [{
        'name': association.name,
        'distance': association.distance.km,
        'address': association.address,
        # Add more fields as needed
    } for association in associations]

    return JsonResponse(data, safe=False)
