from django.shortcuts import render,redirect, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from django.utils import timezone
from django.core.paginator import Paginator
from .forms import *
from django.views.generic import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import *
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.
def HomeView(request):
	name = Catagory.objects.all()
	product=Product.objects.all().order_by('-pub_date')
	paginator=Paginator(product, 3)
	page=request.GET.get('page')
	product=paginator.get_page(page)
	return render(request, "home.html", {'product':product, 'name':name})

		
class AddProductItem(LoginRequiredMixin, CreateView):
	form_class = AddProductForm
	template_name = 'addproduct.html'
	success_url = reverse_lazy("home")

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)


def DetailView(request, pk):
	product=get_object_or_404(Product,pk=pk)
	commentlist = product.comment_set.all().order_by('-commented_date')
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit = False)
			comment.user = request.user
			comment.product = product
			comment.save()
			messages.success(request, f'Comment SuccessFully Added')
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	else:
		form = CommentForm()
	return render(request,
	 'detailview.html', 
	 {'product':product, "form":form, 'commentlist':commentlist})


@login_required
def LikeProduct(request,pk):
	product=get_object_or_404(Product,pk=pk)
	user=request.user
	if request.method=='POST':
		if product.likes.filter(id=user.id).exists():
			product.likes.remove(user)
		else:
			product.likes.add(user)
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))   
	return render(request , 'home.html' ,{'product':product})


def Search(request):
    query=request.GET.get('q')
    if query:
	    result=Product.objects.filter(title__icontains = query)
    else:
	    result=[]
	    messages.error(request, f'Please enter item title to search')
    return render(request, 'search.html', {'result':result})


class UpdateProductview(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Product
	form_class = AddProductForm
	template_name = "updateproduct.html"
	success_url = "/product/{id}" 

	def form_valid(self, form):
		form.instance.user == self.request.user
		return super().form_valid(form)

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



class DeleteComment(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
	model = Comment
	template_name = 'commentdelete.html'
	context_object_name = 'comment'
	success_message = "Object deleted"
	
	def get_success_url(self):
		return reverse_lazy('detailview', kwargs={'pk':self.object.product.id})

	def test_func(self):
		comment = self.get_object()
		if comment.user == self.request.user or comment.product.user == self.request.user:
			return True
		else:
			return False


@login_required
def EditComment(request,pk):
	comment = Comment.objects.get(pk = pk )
	id = comment.product.pk
	form=CommentForm(request.POST or None, instance=comment)
	if request.method == 'POST':
		if form.is_valid():
			if comment.user == request.user:
				form.save()
				messages.info(request, f'Your comment Successfully Edited')
				return redirect("/product/{}".format(id))
	return render(request, 'commentupdate.html', {'form':form, 'comment':comment})


@login_required
def AddReply(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	all_replies = comment.replies_set.all().order_by('-replied_date')
	if request.method == 'POST':
		form = ReplyForm(request.POST)
		if form.is_valid():
			data = form.save(commit = False)
			data.comment = comment
			data.replied_user = request.user
			data.save()
			return redirect(request.META.get('HTTP_REFERER'))
	else:
		form = ReplyForm()
	return render(request, 'replycomment.html', {'form':form, 'comment':comment, 'all_replies':all_replies})



class DeleteReplyView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
	model = Replies
	template_name = 'replydelete.html'
	context_object_name = 'replies'
	success_url=reverse_lazy("home")

	def get_success_url(self):
		return reverse_lazy('addreply', kwargs={'pk':self.object.comment.id})

	def test_func(self):
		replies = self.get_object()
		if replies.replied_user == self.request.user:
			return True
		else:
			return False


class EditReplyView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Replies
	form_class = ReplyForm
	template_name = "editreply.html"
	context_object_name='replies'
	
	def get_success_url(self):
		return reverse_lazy('addreply', kwargs={'pk':self.object.comment.id})

	def test_func(self):
		replies = self.get_object()
		if replies.replied_user == self.request.user:
			return True
		else:
			return False


