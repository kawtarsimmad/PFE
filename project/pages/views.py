from django.shortcuts import render
from publications.models import Publication
from categories.models import Category
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from users.models import Association,User



# Create your views here.
def index(request):
    #publications = Publication.objects.all()  # Fetch all publications
    #publications = Publication.objects.order_by('category')[:2]
     #######admin_user = User.objects.filter(is_superuser=True).first()
    #if admin_user:
        # Filtrer les publications créées par l'administrateur
        #publications = Publication.objects.filter(user=admin_user)
    #else:
        #publications = []  # Aucun administrateur trouvé, donc aucune publication à afficher

    children_category = Category.objects.filter(id="1").first()

    if children_category:
        # Filtrer les publications appartenant à la catégorie "children"
        publications = Publication.objects.filter(category_id=children_category)
    else:
        publications = []  # Aucune catégorie "children" trouvée, donc aucune publication à afficher

    return render(request, 'pages/index.html', {'publications': publications})


