import os

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from settings import MEDIA_ROOT
from gallery.forms import *


log = logging.getLogger(__name__)


@login_required
def home(request):
    gallery = __get_gallery(request)
    context = __get_basic_home_context(gallery)

    if request.POST:
        if request.POST['action'] == 'create_image':
            form = ImageCreateForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                form.set_gallery(gallery)
                form.save()
            else:
                log.error(form.errors.as_data())
        return HttpResponseRedirect('home')

    context["image_create_form"] = ImageCreateForm()

    return render(request, "home.html", context)


@login_required
def home_image_id(request, selected_image_id):
    gallery = __get_gallery(request)
    context = __get_basic_home_context(gallery)

    if request.POST and request.POST['action'] == 'delete_image':
        form = ImageDeleteForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.delete()
        else:
            log.error(form.errors.as_data())
        return HttpResponseRedirect('home')

    context["selected_image_id"] = selected_image_id

    return render(request, "home.html", context)


@login_required
def home_image_id_action(request, selected_image_id, image_action):
    gallery = __get_gallery(request)
    context = __get_basic_home_context(gallery)

    if request.POST:
        if image_action == 'delete' and request.POST['action'] == 'confirm_delete_image':
            form = ImageDeleteForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                form.delete()
            else:
                log.error(form.errors.as_data())
            return HttpResponseRedirect('home')
        if image_action == 'edit' and request.POST['action'] == 'confirm_edit_image':
            form = ImageDeleteForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                form.delete()
            else:
                log.error(form.errors.as_data())
            return HttpResponseRedirect('home')

    context["selected_image"] = Image.objects.get(id=selected_image_id)
    context["selected_image_id"] = selected_image_id
    context["image_action"] = image_action

    return render(request, "home.html", context)


def __get_gallery(request):
    if not Gallery.objects.filter(owner=request.user.pk).exists():
        gallery = Gallery(owner_id=request.user.pk)
        gallery.save()
    else:
        gallery = Gallery.objects.get(owner=request.user.pk)

    return gallery


def __get_basic_home_context(gallery):
    context = dict()

    context["image_delete_form"] = ImageDeleteForm()
    context["media_root"] = os.sep + os.path.basename(os.path.normpath(MEDIA_ROOT)) + os.sep
    context["images"] = Image.objects.filter(gallery=gallery).values()

    # TODO: make slider
    # paginator = Paginator(images, 8)
    #
    # page_number = request.GET.get('page')
    # main_compilation = paginator.get_page(page_number)
    # context["main_compilation"] = main_compilation

    return context
