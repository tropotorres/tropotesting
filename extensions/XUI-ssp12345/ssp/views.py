import os

from django.shortcuts import render
from django.templatetags.static import static
from extensions.views import mfe_app_extension
from utilities.models import GlobalPreferences


@mfe_app_extension
def view(request):
    gp = GlobalPreferences.objects.first()

    return render(
        request,
        "ssp/templates/index.html",
        {
            "data": {
                "cmpUser": request.user.is_authenticated,
                "inactivityTimeoutMinutes": gp.inactivity_timeout_minutes,
                "staticUrl": static("ssp"),
            }
        },
    )
