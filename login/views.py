from urllib import response
from django.http.response import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import generic
from django.urls import reverse
from .forms import UserForm
from .models import User
from django.http import HttpRequest


def index(request):
    return signin(request)


class SignIn(generic.ListView):
    template_name = "login/signin.html"
    context_object_name = "Users"
    model = User


def get_queryset(self):
    return User.objects.order_by("-name")


def signin(request:HttpRequest, user_name=None):
    if user_name is not None:
        try:
            User.objects.get(name=user_name)
            response=HttpResponseRedirect(reverse('main:main'))
            response.set_cookie('user_name',user_name)
            return response
        except:
            return HttpResponse(f"Fail! {user_name} is not in users")
    else:
        return SignIn.as_view()(request)


def signup(request):
    # 如果form通过POST方法发送数据
    context = {}
    if request.method == "POST":
        # 接受request.POST参数构造form类的实例
        form = UserForm(request.POST)
        # 验证数据是否合法
        if form.is_valid():
            # 处理form.cleaned_data中的数据
            # ...
            # 重定向到一个新的URL
            # form.save()
            form.save()
            return redirect(reverse("index"))
        else:
            context["message"] = "输入信息不正确"

    # 如果是通过GET方法请求数据，返回一个空的表单
    else:
        form = UserForm()
    context["form"] = form

    return render(request, "login/signup.html", context)
