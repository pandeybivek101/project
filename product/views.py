from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product
from django.utils import timezone


# Create your views here.
def HomeView(request):
	product=Product.objects
	return render(request, "home.html", {'product':product})



@login_required
def AddProduct(request):
	if request.method=='POST':
		if request.POST['title'] and request.POST['body'] and request.POST['url'] and request.FILES['image']:
			product=Product()
			product.title=request.POST['title']
			product.body=request.POST['body']
			if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
				product.url=request.POST['url']
			else:
				product.url='http://'+ request.POST['url']
			
			product.image=request.FILES['image']
			product.pub_date=timezone.datetime.now()
			product.user=request.user
			product.save()
			return redirect('/product/'+str(product.id))
		else:
			return render(request, 'addproduct.html', {'error':'please fill all the Fields'})
	else:
	    return render(request,'addproduct.html')


def DetailView(request, product_id):
	product=get_object_or_404(Product,pk=product_id)
	return render(request, 'detailview.html', {'product':product})



def UpVote(request, product_id):
	if request.method=='POST':
		product = get_object_or_404(Product, pk=product_id)
		product.likes +=1
		product.save()
		return redirect('/product/'+str(product.id))
	else:
		return render(request, 'detailview.html')

def Search(request):
    query=request.GET.get('q','')
    if query:
	    result=Product.objects.filter(title__icontains=query).distinct()
    else:
	    result=[]
    return render(request, 'search.html', {'result':result})

	

	
    	
