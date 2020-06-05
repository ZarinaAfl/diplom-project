from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from .models import Intervention, TYPE_PARAM, Param, ParamValue, TemplParam, Template, ResearchParamValue, Research, \
    StageResearch, TaskStage, CustomUser, ResponsTask
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
from py_expression_eval import Parser
from .models import SPHERE, STATUS

parser = Parser()


def logout_view(request):
    logout(request)
    return redirect("login_view")

def home_view(request):
    return render(request, 'project/home.html')


def login_view(request):
    # if not request.user.is_anonymous:
    # return redirect("project:profile")
    if request.method == 'POST':
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is not None:
            login(request, user, backend=None)
            return redirect("interv_list")
        else:
            error_message = 'Пользователь не найден' if not User.objects.filter(
                username=request.POST['username']).count() \
                else 'Неверный пароль'
            return render(request, 'project/login.html', {'error': error_message,
                                                          'email': request.POST['username']})
    return render(request, 'project/login.html')


@login_required(login_url="/login")
def profile_view(request):
    return render(request, 'project/profile.html', {'activate': 'profile'})

@csrf_exempt
def tasks_view(request):
    user = CustomUser.objects.get(user=request.user)
    if request.method == 'GET':
        tasks = ResponsTask.objects.filter(responsible=user)
        return render(request, 'project/my_tasks.html', {'activate': 'tasks', 'tasks': tasks})
    else:
        report = request.FILES['report']
        print(report)
        task_pk = request.POST.get('task_pk')
        task = ResponsTask.objects.get(pk=task_pk)
        task.report = report
        task.save()
        return HttpResponse(task_pk)




@login_required(login_url="/login")
def interv_list(request):
    if request.method == 'GET':
        title_contains = request.GET.get('title_contains')
        intervs = Intervention.objects.all()
        if title_contains is not None:
            intervs = Intervention.objects.filter(name__icontains=title_contains).order_by('created_date')

        return render(request, 'project/interv_list.html',
                      {'intervs': intervs, 'activate': 'intervs', 'spheres': SPHERE})

    if request.method == 'POST':
        req = request.POST
        print(req)
        name = req.get('interv_name')
        desc = req.get('interv_desc')
        sphere = req.get('sphere')
        interv = Intervention(name=name, annotation=desc, sphere=sphere, author=request.user)
        interv.save()
        return HttpResponse(interv.pk)


def interv_detail(request, pk):
    interv = Intervention.objects.get(pk=pk)
    params = Param.objects.filter(intervention=interv)
    subvalues = []
    stages = []
    tasks = []

    if request.method == 'GET':
        for sb in params:
            sbvalue = ParamValue.objects.get(param=sb)
            subvalues.append(sbvalue)
        template = Template.objects.filter(intervention=interv)
        templ = False
        if len(template) != 0:
            template = template[0]
            templ = True

            stages = StageResearch.objects.filter(template=template)
            if len(stages) != 0:
                for s in stages:
                    task = TaskStage.objects.filter(stage=s)
                    for t in task:
                        tasks.append(t)

        researches = Research.objects.filter(intervention=interv)

        current_user = CustomUser.objects.get(user=request.user)
        organization = current_user.organization
        close_users = CustomUser.objects.filter(organization=organization)
        return render(request, 'project/interv_detail.html',
                      {'interv': interv, 'params': params, 'subvalues': subvalues, 'templ': templ, 'template': template,
                       'researches': researches, 'stages': stages, 'tasks': tasks, 'users': close_users, 'activate': 'intervs',})

    if request.method == 'POST':
        req = request.POST
        current_user = CustomUser.objects.get(user=request.user)
        organization = current_user.organization
        templ = Template.objects.get(intervention=interv)
        research = Research(intervention=interv, template=templ, organization=organization,
                            name=req.get('research_name'))
        research.save()

        for i in range(int(req.get('tasks_count'))):
            task = TaskStage.objects.get(pk=req["%s[%s][%s]" % ("tasks", i, "pk")])
            responsible = CustomUser.objects.get(pk=req["%s[%s][%s]" % ("tasks", i, "executor")])
            t = ResponsTask(research=research, taskstage=task, responsible=responsible)
            t.save()

        researches = Research.objects.filter(organization=organization)
        print(researches)
        return redirect('our_researches')


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


@csrf_exempt
def create_templ(request, pk):
    interv = Intervention.objects.get(pk=pk)
    if request.method == "GET":
        # form = PostForm
        return render(request, 'project/template_create.html', {'types': TYPE_PARAM, 'interv': interv})
    else:
        k = 0
        template = Template(intervention=interv, protocol=request.FILES['protocol'])
        template.save()
        while True:
            try:
                name_templ_param = request.POST["name_%s" % (k)]
                print(name_templ_param)
                template.save()
                type_templ_param = request.POST["type_%s" % (k)]
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
        stages = StageResearch.objects.filter(template=templ)
        tasks = []
        for s in stages:
            task = TaskStage.objects.filter(stage=s)
            for t in task:
                tasks.append(t)
        return render(request, 'project/template_detail.html',
                      {'types': TYPE_PARAM, 'interv': interv, 'template': templ, 'templ_params': templ_params,
                       'researches': researches,
                       'stages': stages,
                       'tasks': tasks})


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
        return redirect('research_tasks', interv_pk=interv.pk)


def fill_research(request, pk, res_pk):
    interv = Intervention.objects.get(pk=pk)
    if request.method == "GET":
        template = Template.objects.get(intervention=interv)
        templ_params = TemplParam.objects.filter(template=template)
        research = Research.objects.get(pk=res_pk)
        return render(request, 'project/fill_research.html', {'interv': interv, 'params': templ_params, 'research': research})
    else:
        k = 0
        while True:
            collection = []
            templ = Template.objects.get(intervention=interv)
            templ_params = TemplParam.objects.filter(template=templ)
            research = Research.objects.get(pk=res_pk)
            collection.append({"params": templ_params})
            for c in collection:
                for param in c["params"]:
                    # ParamValue
                    templ_param = TemplParam.objects.get(template=templ, name=param.name)
                    param_val = ResearchParamValue(research=research, param=templ_param)

                    if param.type == 3:
                        instance = ResearchParamValue(research=research, param=templ_param,
                                                      file=request.FILES["file_%s" % param.id])
                        instance.save()
                    elif param.type == 4:
                        instance = ResearchParamValue(research=research, param=templ_param,
                                                          image=request.FILES["file_%s" % param.id])
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
            research.status = STATUS[1][0]
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


def our_researches(request):
    current_user = CustomUser.objects.get(user=request.user)
    organization = current_user.organization
    researches = Research.objects.filter(organization=organization)
    print(researches)
    if request.method == "GET":
        return render(request, 'project/our_researches.html', {'researches': researches, 'activate': 'researches'})


def research_detail(request, interv_pk, res_pk):
    research = Research.objects.get(pk=res_pk)
    interv = Intervention.objects.get(pk=interv_pk)
    params = TemplParam.objects.filter(template=Template.objects.get(intervention=interv))
    res_params_value = ResearchParamValue.objects.filter(research=research)
    researches = Research.objects.filter(intervention=interv)
    tasks = ResponsTask.objects.filter(research=research).order_by('id')

    print(tasks)

    return render(request, 'project/research_detail.html', {'research': research, 'interv': interv,
                                                            'params': params,
                                                            'params_value': res_params_value,
                                                            'researches': researches,
                                                            'tasks': tasks})


@login_required(login_url="login/")
def research_tasks(request, interv_pk):
    interv = Intervention.objects.get(pk=interv_pk)
    if request.method == "GET":
        return render(request, 'project/research_tasks.html', {'interv': interv})
    else:
        template = Template.objects.get(intervention=interv)  # получаем шаблон исследования
        stages_kol = int(request.POST['stages_kol'])
        tasks_kol = int(request.POST['tasks_kol'])
        req = request.POST
        for k in range(0, stages_kol):
            stage_number = req.get("%s[%s][%s]" % ("data_stages", k, "stage_number"))
            stage_value = req.get("%s[%s][%s]" % ("data_stages", k, "stage_value"))
            stage = StageResearch(template=template, number=stage_number, name=stage_value)
            stage.save()

        for k in range(0, tasks_kol):
            task_r = req.get("%s[%s][%s]" % ("data_tasks", k, "task_number")).split('_')
            task_number = task_r[2]
            task_stage = task_r[1]
            stage = StageResearch.objects.get(template=template, number=task_stage)
            task_value = req.get("%s[%s][%s]" % ("data_tasks", k, "task_value"))
            task = TaskStage(stage=stage, number=task_number, name=task_value)
            task.save()

        return HttpResponse(interv.pk)
