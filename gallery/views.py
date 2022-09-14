import os

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

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

    context["selected_image"] = Image.objects.get(id=selected_image_id)

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
                return HttpResponseRedirect('home')
            else:
                log.error(form.errors.as_data())

        if image_action == 'edit' and request.POST['action'] == 'confirm_edit_image':
            old_image = Image.objects.get(id=selected_image_id)
            form = ImageEditForm(request.POST or None, instance=old_image)
            if form.is_valid():
                if 'image_field' in request.FILES:
                    os.remove(os.path.join(os.path.basename(os.path.normpath(MEDIA_ROOT)), str(old_image.image_field)))
                    old_image.image_field = request.FILES['image_field']
                if 'text' in form.data and len(form.data["text"]) > 0:
                    old_image.text = form.data["text"]
                old_image.save()
                return HttpResponseRedirect('home')
            else:
                log.error(form.errors.as_data())

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

    context["image_create_form"] = ImageCreateForm()
    context["image_edit_form"] = ImageEditForm()
    context["image_delete_form"] = ImageDeleteForm()
    context["media_root"] = os.sep + os.path.basename(os.path.normpath(MEDIA_ROOT)) + os.sep
    context["images"] = Image.objects.filter(gallery=gallery).values()

    return context
