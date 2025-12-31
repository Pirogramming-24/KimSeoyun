from django.shortcuts import render, redirect
from .models import Review

# 리뷰 목록
def review_list(request):
    reviews = Review.objects.all()
    context = {
        "reviews": reviews
    }
    return render(request, "review_list.html", context)

# 리뷰 상세
def review_detail(request, pk):
    review = Review.objects.get(id=pk)
    context = {
        "review": review
    }
    return render(request, "review_detail.html", context)

# 리뷰 작성
def review_create(request):
    if request.method == "POST":
        Review.objects.create(
            title = request.POST["title"],
            director = request.POST["director"],
            actor = request.POST["actor"],
            genre = request.POST["genre"],
            rating = request.POST["rating"],
            runtime = request.POST["runtime"],
            release_year = request.POST["release_year"],
            content = request.POST["content"],
        )
        return redirect("reviews:review_list")
    
    return render(request, "review_create.html")


# 리뷰 수정
def review_update(request, pk):
    review = Review.objects.get(id=pk)  # 수정할 리뷰 조회
    
    if request.method == "POST":
        review.title = request.POST["title"]
        review.director = request.POST["director"]
        review.actor = request.POST["actor"]
        review.genre = request.POST["genre"]
        review.rating = request.POST["rating"]
        review.runtime = request.POST["runtime"]
        review.release_year = request.POST["release_year"]
        review.content = request.POST["content"]
        review.save()  # DB에 저장
        return redirect("reviews:review_detail", pk=pk)  # 수정 후 디테일 페이지로
    
    context = {"review": review}
    return render(request, "review_update.html", context)

# 리뷰 삭제
def review_delete(request, pk):
    if request.method == "POST":
        review = Review.objects.get(id=pk) #pk로 삭제 대상 게시글을 DB에서 조회
        review.delete() #해당 게시글을 DB에서 완전히 삭제
    return redirect("reviews:review_list") #삭제 후 게시글 목록 페이지로 리다이렉트