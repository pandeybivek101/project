from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product
from django.utils import timezone
from django.core.paginator import Paginator
from .forms import *
from django.views.generic import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
def HomeView(request):
	product=Product.objects.all().order_by('-pub_date')
	paginator=Paginator(product, 3)
	page=request.GET.get('page')
	product=paginator.get_page(page)
	return render(request, "home.html", {'product':product})



"""@login_required
def AddProductItem(request):
	if request.method == 'POST':
		form = AddProductForm(request.POST, request.FILES)
		if form.is_valid():
			user = request.user
			form.save()
			return redirect("home")
	else:
		form = AddProductForm()
	return render(request,'addproduct.html', {"form":form})"""
		
class AddProductItem(LoginRequiredMixin, CreateView):
	form_class = AddProductForm
	template_name = 'addproduct.html'
	success_url = reverse_lazy("home")

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)


def DetailView(request, product_id):
	product=get_object_or_404(Product,pk=product_id)
	return render(request, 'detailview.html', {'product':product})



def UpVote(request, product_id):
	if request.method=='POST':
		product = get_object_or_404(Product, pk=product_id)
		product.likes += 1
		product.save()
		return redirect('/product/'+str(product.id))
	else:
		return render(request, 'detailview.html')



def Search(request):
    query=request.GET.get('q')
    if query:
	    result=Product.objects.filter(title__icontains=query)
    else:
	    result=[]
    return render(request, 'search.html', {'result':result})

    	