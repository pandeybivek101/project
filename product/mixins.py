from django.views import View
from .forms import *
from django.shortcuts import render, get_object_or_404
from .models import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin

class AboutViewMixin(View):
	form_class=MessageForm
	template_name='about.html'

	def get(self, request):
		form=self.form_class()
		context={'form':form}
		return render(request, self.template_name, context)


class AddMixin(View, ):
	template_name=''
	model=None
	context_object_name=''
	form_class=None

	def get_object(self, *args, **kwargs):
		return get_object_or_404(self.model, pk=self.kwargs.get('pk'))



class DeleteCommentURLMixin:
	def get_success_url(self):
		return reverse_lazy('detailview', kwargs={'pk':self.object.product.id})


class ADDReplySuccessURLMixin:
	def get_success_url(self):
		return reverse_lazy('addreply', kwargs={'pk':self.object.comment.id})



class FormValidMixin:
	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)


class ReplyAutorityMixin(UserPassesTestMixin):

	def test_func(self):
		replies = self.get_object()
		if replies.replied_user == self.request.user:
			return True
		else:
			return False


		



