from django.shortcuts import render,redirect, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from django.utils import timezone
from django.core.paginator import Paginator
from .forms import *
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import *
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.views import View
from django.contrib.messages.views import SuccessMessageMixin
from .mixins import *
import geocoder
from math import sin, cos, sqrt, atan2, radians

# Create your views here.

def getLocation():
	g = geocoder.ip('me')
	if g:
		lat1=g.lat
		lng1=g.lng
	else:
		lat1=24.2213
		lng1=87.4444
	lst=[lat1, lng1]
	return lst


class HomeView(ListView):
	#template_name='product/home.html'
	template_name='home.html'
	context_object_name='product'
	model=Product
	paginate_by=3

		
class AddProductItem(LoginRequiredMixin, CreateView):
	form_class = AddProductForm
	template_name = 'addproduct.html'
	success_url = reverse_lazy("home")

	def form_valid(self, form):
		form.instance.user = self.request.user
		form.instance.pro_lat=getLocation()[0]
		form.instance.pro_lng=getLocation()[1]
		return super().form_valid(form)


class ProductDetailView(AddMixin, ):
	#template_name='detailview.html'
	template_name='product/product_detail.html'
	model=Product
	context_object_name='product'
	form_class=CommentForm

	def compute_distance(self):
		product=self.get_object()
		R = 6373.0
		if product.pro_lat and product.pro_lng:
			lat1 = radians(product.pro_lat)
			lng1 = radians(product.pro_lng)
		else:
			lat1=radians(abs(27.00332))
			lng1=radians(abs(82.44231))
		lat2 = radians(getLocation()[0])
		lng2 = radians(getLocation()[1])
		dlat = lat2-lat1
		dlng = lng2-lng1
		a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlng / 2)**2
		c = 2 * atan2(sqrt(a), sqrt(1 - a))
		distance = R * c
		return int(distance)


	def get(self, request, *args, **kwargs):
		user=request.user
		product=self.get_object()
		if request.user.is_authenticated:
			if not product.views.filter(id=user.id).exists():
				product.views.add(request.user)
		distance=self.compute_distance()
		commentlist = product.comment_set.all().order_by('-commented_date')
		form = self.form_class()
		context={
		    'distance':distance,
			'product':product,
			'commentlist':commentlist,
			'form':form
			}
		return render(request, self.template_name, context)


class LikeProduct(LoginRequiredMixin, AddMixin, View):
	model=Product
	template_name='home.html'
	context_object_name='product'

	def post(self, request, *args, **kwargs):
		user=request.user
		product=self.get_object()
		if request.method=='POST':
			if product.likes.filter(id=user.id).exists():
				product.likes.remove(user)
			else:
				product.likes.add(user)
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))   
		return render(request , 'home.html' ,{'product':product})



class Search(View):
	template_name='search.html'
	model=Product

	def get(self, request):
		query=request.GET.get('q')
		print(query)
		if query:
			result=self.model.objects.filter(Q(title__icontains = query) | Q(
				catagory__catagory__icontains = query)).order_by('-pub_date')
		else:
			result=[]
			messages.error(request, f'Please enter item title to search')
		context={'result':result}
		return render(request, self.template_name, context)



class UpdateProductview(LoginRequiredMixin, UserPassesTestMixin, FormValidMixin, UpdateView):
	model = Product
	form_class = AddProductForm
	template_name = "updateproduct.html"
	success_url = "/product/{id}" 


	def test_func(self):
		product = self.get_object()
		if product.user == self.request.user:
			return True
		else:
			return False


class DeleteProductView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
	model = Product
	template_name = "deleteproduct.html"
	success_message = 'Item Deleted Successfully'

	def get_success_url(self):
		return reverse_lazy("home")

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



class DeleteComment(LoginRequiredMixin, UserPassesTestMixin, DeleteCommentURLMixin, SuccessMessageMixin, DeleteView):
	model = Comment
	template_name = 'commentdelete.html'
	context_object_name = 'comment'
	success_message = "Object deleted"
	

	def test_func(self):
		comment = self.get_object()
		if comment.user == self.request.user or comment.product.user == self.request.user:
			return True
		else:
			return False


class AddComment(LoginRequiredMixin, AddMixin, View, ):
	template_name='detailview.html'
	model=Product
	context_object_name='product'
	form_class=CommentForm

	def get(self, request, *args, **kwargs):
		form=self.form_class
		product = self.get_object()
		context={'form':form, 'product':product}
		return render(request, self.template_name, context)


	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			comment = form.save(commit = False)
			comment.user = request.user
			comment.product = self.get_object()
			comment.save()
			messages.success(request, f'Comment SuccessFully Added')
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
		return render(request, self.template_name, {'form':form})


class EditComment(LoginRequiredMixin, SuccessMessageMixin, DeleteCommentURLMixin, UpdateView, ):
	template_name='commentupdate.html'
	model= Comment
	form_class=CommentForm
	success_url=reverse_lazy("home")
	success_message='Your comment Successfully Updated'



class DeleteReplyView(LoginRequiredMixin, SuccessMessageMixin, ADDReplySuccessURLMixin, ReplyAutorityMixin, DeleteView):
	model = Replies
	template_name = 'replydelete.html'
	context_object_name = 'replies'
	success_url=reverse_lazy("home")


class EditReplyView(LoginRequiredMixin, ADDReplySuccessURLMixin, ReplyAutorityMixin, UpdateView):
	model = Replies
	form_class = ReplyForm
	template_name = "editreply.html"
	context_object_name='replies'
	


class AboutView(LoginRequiredMixin, AboutViewMixin):
	pass

		
class AddMessage(LoginRequiredMixin, AboutViewMixin, View):

	def post(self, request):
		form=self.form_class(request.POST)
		if form.is_valid():
			Msg=form.save(commit = False)
			Msg.message_user = request.user
			Msg.save()
			messages.success(request, f'ThankYou four Feedback')
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
		return render(request, self.template_name, context)



class AddReply(LoginRequiredMixin, AddMixin, View, ):
	template_name='replycomment.html'
	model=Comment
	context_object_name='comment'
	form_class=ReplyForm

	def get(self, request, *args, **kwargs):
		form=self.form_class
		comment = self.get_object()
		context={'form':form, 'comment':comment}
		return render(request, self.template_name, context)


	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			data = form.save(commit = False)
			data.comment = self.get_object()
			data.replied_user = request.user
			data.save()
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
		context={'form':form}
		return render(request, self.template_name, context)


def ChatView(request, username):
	return redirect('/dialogs/{}'.format(username))




