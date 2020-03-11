import cexprtk as cexprtk
from .models import Intervention, TYPE_PARAM, Param, ParamValue, TemplParam, Template, ResearchParamValue, Research
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
from py_expression_eval import Parser
from .models import SPHERE

parser = Parser()


# Create your views here.
def interv_list(request):
    intervs = Intervention.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    speheres = []
    for s in SPHERE:
        speheres.append(s[1])

    return render(request, 'project/interv_list.html', {'intervs': intervs, 'activate': 'intervs', 'sphere': speheres})


def interv_detail(request, pk):
    interv = get_object_or_404(Intervention, pk=pk)
    params = Param.objects.filter(intervention=interv)
    subvalues = []
    for sb in params:
        sbvalue = ParamValue.objects.get(param=sb)
        subvalues.append(sbvalue)
    template = Template.objects.filter(intervention=interv)
    templ = False
    if len(template) != 0:
        templ = True

    researches = Research.objects.filter(intervention=interv)
    return render(request, 'project/interv_detail.html',
                  {'interv': interv, 'params': params, 'subvalues': subvalues, 'templ': templ,
                   'researches': researches})


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
        return render(request, 'project/interv_add.html', {'form': form, 'types': TYPE_PARAM, 'activate': 'intervs'})


def add_parameters(request, pk):
    interv = Intervention.objects.get(pk=pk)
    if request.method == "GET":
        form = PostForm
        return render(request, 'project/add_parameters.html',
                      {'form': form, 'types': TYPE_PARAM, 'interv': interv, 'activate': 'intervs'})
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
    interv = Intervention.objects.get(pk=pk)
    if request.method == "GET":
        params = Param.objects.filter(intervention=interv)
        return render(request, 'project/fill_params.html', {'interv': interv, 'params': params})
    # POST-method
    else:
        k = 0
        while True:
            collection = []
            params = Param.objects.filter(intervention=interv)
            collection.append({"params": params})
            for c in collection:
                for param in c["params"]:
                    # ParamValue
                    param_val = ParamValue(param=param)
                    if param.type == 3 or param.type == 4:
                        print(request.FILES)
                        instance = ParamValue(param=param, file=request.FILES["file_%s" % param.id])
                        instance.save()
                    else:
                        # print('sp_%s' % param.id)
                        val = request.POST["sp_%s" % param.id]
                        # val = request.POST.get("sp_%s" % param.id)
                        # print(val)
                        # value = request.POST.get("sp_%s" % param.id)
                        if param.type == 1:
                            param_val.value = val
                        elif param.type == 2:
                            # print(val)
                            param_val.text = val
                        param_val.save()
                        # ParamValue.objects.all().delete()
                return redirect('interv_detail', pk=interv.pk)


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


def create_templ(request, pk):
    interv = Intervention.objects.get(pk=pk)
    if request.method == "GET":
        # form = PostForm
        return render(request, 'project/template_create.html', {'types': TYPE_PARAM, 'interv': interv})
    else:
        k = 0
        template = Template(intervention=interv)
        template.save()
        while True:
            try:
                name_templ_param = request.POST["%s[%s][%s]" % ("templ_params", k, "name")]
                # print(name_templ_param)
                type_templ_param = request.POST["%s[%s][%s]" % ("templ_params", k, "type_templ_param")]
                interv = Intervention.objects.get(pk=pk)
                templ_param = TemplParam(template=template, name=name_templ_param, type=type_templ_param)
                templ_param.save()
                k += 1
            except Exception as e:
                print(e)
                break
        return redirect('create_formula', pk=interv.pk)


def template_detail(request, pk):
    interv = Intervention.objects.get(pk=pk)
    if request.method == "GET":
        # form = PostForm
        templ = Template.objects.get(intervention=interv)
        templ_params = TemplParam.objects.filter(template=templ)
        researches = Research.objects.filter(template=templ)
        return render(request, 'project/template_detail.html',
                      {'types': TYPE_PARAM, 'interv': interv, 'template': templ, 'templ_params': templ_params,
                       'researches': researches})


FUNCTIONS = ["log", "ln", "x!", "sqrt", "abs"]


def create_formula(request, pk):
    interv = Intervention.objects.get(pk=pk)
    templ = Template.objects.get(intervention=interv)

    if request.method == "GET":
        params = TemplParam.objects.filter(template=templ)

        return render(request, 'project/create_formula.html', {'params': params, 'funcs': FUNCTIONS})
    else:
        formula = request.POST["formula"]
        templ.formula = formula
        templ.save()
        return redirect('template_detail', pk=interv.pk)


def add_research(request, pk):
    interv = Intervention.objects.get(pk=pk)
    if request.method == "GET":
        template = Template.objects.get(intervention=interv)
        templ_params = TemplParam.objects.filter(template=template)
        return render(request, 'project/add_research.html', {'interv': interv, 'params': templ_params})
    else:
        k = 0
        while True:
            collection = []
            templ = Template.objects.get(intervention=interv)
            templ_params = TemplParam.objects.filter(template=templ)
            name_research = request.POST["name_research"]
            research = Research(intervention=interv, template=templ, name=name_research)
            research.save()
            collection.append({"params": templ_params})
            for c in collection:
                for param in c["params"]:
                    # ParamValue
                    templ_param = TemplParam.objects.get(template=templ, name=param.name)
                    param_val = ResearchParamValue(research=research, param=templ_param)

                    if param.type == 3 or param.type == 4:
                        # print(request.FILES)
                        instance = ResearchParamValue(research=research, param=templ_param,
                                                      file=request.FILES["file_%s" % param.id])
                        instance.save()
                    else:
                        val = request.POST["sp_%s" % param.id]
                        # val = request.POST.get("sp_%s" % param.id)
                        # print(val)
                        # value = request.POST.get("sp_%s" % param.id)
                        if param.type == 1:
                            param_val.value = val
                            param_val.save()
                        elif param.type == 2:
                            param_val.text = val
                            param_val.save()
                        # ParamValue.objects.all().delete()
            research.effect = calculate_effect(research)
            research.save()
            return redirect('interv_detail', pk=interv.pk)


def calculate_effect(research):
    params = ResearchParamValue.objects.filter(research=research)
    formula = research.template.formula

    vars = ['a', 'b', 'c', 'd', 'e', 'x', 'y', 'z']
    var_val = {}
    k = 0
    print("ДО  " + formula)
    for p in params:
        if p.is_number():
            print(p.param.name + ' ' + str(p.value))
            name_p = p.param.name
            if name_p in formula:
                formula = formula.replace(name_p, vars[k])
                var_val[vars[k]] = p.value
                k = k + 1
    print("ПОСЛЕ  " + formula)

    result = parser.parse(formula).evaluate(var_val)
    print(result)
    return result
    # ОБРАБОТАТЬ ФУНКЦИИ


def research_detail(request, interv_pk, res_pk):
    research = Research.objects.get(pk=res_pk)
    interv = Intervention.objects.get(pk = interv_pk)
    params = TemplParam.objects.filter(template=Template.objects.get(intervention=interv))
    res_params_value = ResearchParamValue.objects.filter(research = research)
    researches = Research.objects.filter(intervention=interv)
    return render(request, 'project/research_detail.html', {'research': research, 'interv': interv,
                                                            'params': params,
                                                            'params_value': res_params_value,
                                                            'researches': researches})
