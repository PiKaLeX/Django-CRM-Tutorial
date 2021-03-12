from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect, reverse

class OrganisorAndLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated or is organisor."""
    def dispatch(self, request, *args, **kwargs):
        #print(f"{request.user.is_authenticated=}, {request.user.is_organisor=}")
        if not request.user.is_authenticated or not request.user.is_organisor:
            return redirect(reverse("leads:lead-list"))
        return super().dispatch(request, *args, **kwargs)
