from django.db import models

class Review(models.Model):
    title = models.CharField(max_length=200)  # 영화 제목
    director = models.CharField(max_length=200)  # 감독
    actor = models.CharField(max_length=200)  # 주연
    genre = models.CharField(max_length=100)  # 장르
    rating = models.DecimalField(max_digits=2, decimal_places=1)  # 별점 (0.0~5.0)
    runtime = models.IntegerField()  # 개봉 년도
    release_year = models.IntegerField()  # 개봉 년도
    content = models.TextField()  # 리뷰 내용

