from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Intervention, TYPE_PARAM, Param
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect


# Create your views here.
def interv_list(request):
    intervs = Intervention.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'project/interv_list.html', {'intervs': intervs})


def interv_detail(request, pk):
    interv = get_object_or_404(Intervention, pk=pk)
    return render(request, 'project/interv_detail.html', {'interv': interv})


def interv_add(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            interv = form.save(commit=False)
            interv.author = request.user
            interv.published_date = timezone.now()
            interv.save()
            post_text = request.POST.get('the_post')
            interv = get_object_or_404(Intervention, pk=interv.pk)
            return redirect('add_parameters', pk=interv.pk)
        else:
            form = PostForm
            return render(request, 'project/interv_add.html', {'form': form, 'types': TYPE_PARAM})
    else:
        form = PostForm
        return render(request, 'project/interv_add.html', {'form': form, 'types': TYPE_PARAM})


def add_parameters(request, pk):
    interv = Intervention.objects.get(pk=pk)
    if request.method == "GET":
        form = PostForm
        return render(request, 'project/add_parameters.html', {'form': form, 'types': TYPE_PARAM, 'interv': interv})
    else:
        k = 0
        while True:
            try:
                name_subparam = request.POST["%s[%s][%s]" % ("subparams", k, "name")]
                type_subparam = request.POST["%s[%s][%s]" % ("subparams", k, "type_subparam")]
                interv = Intervention.objects.get(pk=pk)
                subparam = Param(intervention=interv, name=name_subparam, type=type_subparam)
                subparam.save()
                k += 1
            except Exception as e:
                print(e)
                break
        return redirect('fill_params', pk=interv.pk)


# @login_required(login_url="login/")
def fill_params(request, pk):
    # return render(request, 'project/fill_params.html')
    if request.method == "GET":
        interv = Intervention.objects.get(pk=pk)
        params = Param.objects.filter(intervention=interv)
        return render(request, 'project/fill_params.html', {'interv': interv, 'params':params})




def interv_edit(request, pk):
    interv = get_object_or_404(Intervention, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=interv)
        if form.is_valid():
            interv = form.save(commit=False)
            interv.author = request.user
            interv.published_date = timezone.now()
            interv.save()
            return redirect('interv_detail', pk=interv.pk)
    else:
        form = PostForm(instance=interv)
    return render(request, 'project/interv_edit.html', {'form': form, 'types': TYPE_PARAM})
