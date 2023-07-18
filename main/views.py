from django.shortcuts import render
from login.models import User
from utils import get_gpu_info
from django.http import HttpResponseRedirect
from django.urls import reverse
from filelist.views import view_filelist
from tdb.views import view_tdb
from runner.views import view_runner
view_fn = dict(
    gpu=lambda request, user: {"gpu_info": get_gpu_info()},
    config=lambda request, user: view_filelist(request, user, "config"),
    record=lambda request, user: view_filelist(request, user, "record"),
    tdb=view_tdb,
    process=view_runner,
)


# Create your views here.
def index(request, option="gpu"):
    if option == "gpu":
        return render(request, "main/gpu.html", view_fn["gpu"](None, None))
    if "user_name" in request.COOKIES:
        user_name = request.COOKIES["user_name"]
    else:
        return HttpResponseRedirect(reverse("signin"))
    try:
        user = User.objects.get(name=user_name)
    except:
        return HttpResponseRedirect(reverse("signin"))
    if option in view_fn:
        context = view_fn[option](request, user=user)
        template = f"main/{option}.html"
    else:
        context = {"error": f"not find context about option {option}"}
        template = f"main/main.html"
    context["user_name"] = user_name
    if 'jump_to' in context:
        return HttpResponseRedirect(context['jump_to'])
    return render(request, template, context)
