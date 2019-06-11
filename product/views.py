from django.shortcuts import render,redirect, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product
from django.utils import timezone
from django.core.paginator import Paginator
from .forms import *
from django.views.generic import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import *
from django.urls import reverse_lazy, reverse


# Create your views here.
def HomeView(request):
	name = Catagory.objects.all()
	product=Product.objects.all().order_by('-pub_date')
	paginator=Paginator(product, 3)
	page=request.GET.get('page')
	product=paginator.get_page(page)
	return render(request, "home.html", {'product':product, 'name':name})


"""@login_required
def AddProductItem(request):
	if request.method == 'POST':
		form = AddProductForm(request.POST, request.FILES)
		if form.is_valid():
			data = form.save(commit = False)
			data.user = request.user
			data.save()
			messages.success(request, f'Item added successfully')
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


def DetailView(request, pk):
	product=get_object_or_404(Product,pk=pk)
	return render(request, 'detailview.html', {'product':product})


'''def UpVote(request, pk):
	if request.method=='POST':
		product = get_object_or_404(Product, pk=id)
		product.likes += 1
		product.save()
		return redirect('/product/'+str(product.id))
	else:
		return render(request, 'detailview.html')'''

@login_required
def UpVote(request,pk):
	like=get_object_or_404(Product,pk=pk)
	user=request.user
	if request.method=='POST':
		if like.likes.filter(id=user.id).exists():
			like.likes.remove(user)
		else:
			like.likes.add(user)
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))   
	return render(request , 'home.html' ,{'like':like})



def Search(request):
    query=request.GET.get('q')
    if query:
	    result=Product.objects.filter(title__icontains=query)
    else:
	    result=[]
	    messages.error(request, f'Please enter item title to search')
    return render(request, 'search.html', {'result':result})


class UpdateProductview(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Product
	form_class = AddProductForm
	template_name = "updateproduct.html"
	success_url = reverse_lazy('home')

	def form_valid(self, form):
		form.instance.user == self.request.user
		return super().form_valid(form)

	def test_func(self):
		product = self.get_object()
		if product.user == self.request.user:
			return True
		else:
			return False


class DeleteProductView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Product
	template_name = "deleteproduct.html"
	success_url = reverse_lazy('home')

	def test_func(self):
		product = self.get_object()
		if product.user == self.request.user:
			return True
		else:
			return False



class UserProductlistView(ListView):
	model = Product
	template_name = 'userproduct.html'
	context_object_name = 'product'
	paginate_by = 3

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Product.objects.filter(user=user).order_by('-pub_date')


class productcatagorylist(UserProductlistView, ListView):
	model = Product
	template_name = 'catagorylist.html'
	context_object_name = 'product'
	paginate_by = 3

	def get_queryset(self):
		catagory = get_object_or_404(Catagory, catagory=self.kwargs.get('catagory'))
		return Product.objects.filter(catagory = catagory).order_by('-pub_date')




