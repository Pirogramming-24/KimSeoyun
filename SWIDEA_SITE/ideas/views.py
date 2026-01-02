from django.shortcuts import render, redirect
from .models import Idea, DevTool
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

# Create your views here.


# 아이디어 리스트
def idea_list(request):
    sort = request.GET.get('sort')
    page = request.GET.get('page', 1)
    ideas = Idea.objects.all()

    if sort == 'star':
        ideas = ideas.order_by('-starred')
    elif sort == 'name':
        ideas = ideas.order_by('title')
    elif sort == 'register':
        ideas = ideas.order_by('created_at')
    elif sort == 'latest':
        ideas = ideas.order_by('-created_at')

    paginator = Paginator(ideas, 4)
    ideas_page = paginator.get_page(page)

    context = {
        "ideas": ideas_page,
        "current_sort": sort,
    }
    return render(request, "idea_list.html", context)


# 아이디어 상세
def idea_detail(request, pk):
    idea = Idea.objects.get(id=pk)
    context = {
        "idea": idea
    }
    return render(request, "idea_detail.html", context)


# 아이디어 작성
def idea_create(request):
    if request.method == "POST":
        Idea.objects.create(
            title=request.POST["title"],
            img=request.FILES.get("img"),
            content=request.POST["content"],
            interest=request.POST["interest"],
            devtool=request.POST["devtool"],
        )
        return redirect("ideas:idea_list")

    devtools = DevTool.objects.all()
    return render(request, "idea_create.html", {"devtools": devtools})


# 아이디어 수정
def idea_update(request, pk):
    idea = Idea.objects.get(id=pk)

    if request.method == "POST":
        idea.title = request.POST["title"]
        if request.FILES.get("img"):
            idea.img = request.FILES.get("img")
        idea.content = request.POST["content"]
        idea.interest = request.POST["interest"]
        idea.devtool = request.POST["devtool"]
        idea.save()
        return redirect("ideas:idea_detail", pk=pk)

    devtools = DevTool.objects.all()
    context = {
        "idea": idea,
        "devtools": devtools,
    }
    return render(request, "idea_update.html", context)



# 아이디어 삭제
def idea_delete(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    idea.delete()
    return redirect("ideas:idea_list")


# 개발툴 리스트
def devtool_list(request):
    devtools = DevTool.objects.all()
    context = {
        "devtools": devtools
    }
    return render(request, "devtool_list.html", context)


# 개발툴 등록
def devtool_create(request):
    if request.method == "POST":
        DevTool.objects.create(
            name = request.POST["name"],
            kind = request.POST["kind"],
            content = request.POST["content"],
        )
        return redirect("ideas:devtool_list")
    return render(request, "devtool_create.html")



# 개발툴 상세
def devtool_detail(request, pk):
    devtool = DevTool.objects.get(id=pk)
    context = {
        "devtool": devtool
    }
    return render(request, "devtool_detail.html", context)

# 개발툴 수정
def devtool_update(request, pk):
    devtool = DevTool.objects.get(id=pk)

    if request.method == "POST":
        devtool.name = request.POST["name"]
        devtool.kind = request.POST["kind"]
        devtool.content = request.POST["content"]
        devtool.save()
        return redirect("ideas:devtool_detail",pk=pk)
    context = {"devtool": devtool}
    return render(request, "devtool_update.html", context)

# 개발툴 삭제
def devtool_delete(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    devtool.delete()
    return redirect("ideas:devtool_list")


@require_POST
def change_interest(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    action = request.POST.get('action')

    if action == 'increase':
        idea.interest += 1
    elif action == 'decrease' and idea.interest > 0:
        idea.interest -= 1
    else:
        return JsonResponse({'error': '잘못된 요청입니다.'}, status=400)

    idea.save()

    return JsonResponse({'interest': idea.interest})


@require_POST
def toggle_star(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    idea.starred = not idea.starred  # 토글
    idea.save()
    return JsonResponse({'starred': idea.starred})