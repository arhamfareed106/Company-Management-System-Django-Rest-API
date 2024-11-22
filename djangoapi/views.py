from django.http import HttpResponse,JsonResponse

def home_page(request):
    print("home page requested")
    friends= [
        'ali',
        'ahmad',
        'raza',
    ]
    return JsonResponse(friends, safe=False)
    





    



