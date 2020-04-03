from .models import Catagory

def CatagoryList(request):
	name = Catagory.objects.all()
	return {'name':name}

