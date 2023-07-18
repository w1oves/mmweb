from django.shortcuts import render
from .models import close_all_runner
from login.models import User
from django.http import HttpRequest
from filelist.views import get_filelist


def view_runner(request: HttpRequest, user: User):
    context = {}
    callback = {}

    runners = [user.trainrunner_set.all(), user.testrunner_set.all()]
    # 不同模型得到的QuerySet不可以进行归并
    for qs in runners:
        for runner in qs:
            callback.update(runner.get_buttons()["callback"])
    if request.POST:
        for option in request.POST.getlist("runner_buttons"):
            if option and option in callback:
                callback[option]()
        if "close_all" in request.POST:
            close_all_runner(user)
        if "jump_button" in request.POST:
            print(f'jump to {request.POST["jump_button"]}')
            filelist = get_filelist(user, "record")
            filelist.change_path(request.POST["jump_button"])
            filelist.current_file = 'None'
            filelist.save()
            context['jump_to']='/main/record'
    runners = [user.trainrunner_set.all(), user.testrunner_set.all()]
    train_info = []
    test_info = []
    for runner in user.trainrunner_set.all():
        train_info.append(runner.get_context())
    for runner in user.testrunner_set.all():
        test_info.append(runner.get_context())
    context["train_runners"] = train_info
    context["test_runners"] = test_info
    return context
