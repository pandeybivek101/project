from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.core.exceptions import PermissionDenied


class IsProductOwner(BasePermission):
	message = 'Permission is restricted'
	my_safe_method = ['GET',"PUT", "DELETE"]

	def has_permission(self, request, view):
		if request.method in self.my_safe_method:
			return True
		return False
	
	def has_object_permission(self, request, view, obj):
		if obj.user==request.user:
			return True
		else:
			return False



class IsCommentOwner(IsProductOwner):
	pass


class IsReplyOwner(IsProductOwner):
	
	def has_object_permission(self, request, view, obj):
		if obj.replied_user==request.user:
			return True
		else:
			return False




	
