from django.urls import path

from . import views

app_name = 'community'

urlpatterns = [
    # /events/ : 이벤트(미구현)
    # /questions/ : 질문게시판(구현 중)

    # 질문 게시판 메인 페이지(복수의 질문리스트이기 때문에 questions 복수 형태로 사용
    path('questions/', views.questions, name='questions'),
    # 질문 게시판 디테일 페이지(question 은 단수로 사용)
    path('question/<int:pk>/', views.question_detail, name='question-detail'),
    # 질문 게시판에 글 생성
    path('question/new/', views.question_create, name='question-create'),
    # 질문 게시판 글 수정
    path('question/update/<int:pk>/', views.question_update, name='question-update'),
    # 질문 게시판에 글 삭제
    path('question/del/<int:pk>/', views.question_delete, name='question-delete'),

    # 질문 게시판 디테일의 댓글 작성
    path('question/comment/new/detail/<int:question_pk>/', views.comment_create, name='comment-create'),
]


# https://mht.kr/community/questions # 질문 게시판 메인 페이지
# https://mht.kr/community/questions/<int:commiunity_pk>/ # 질문 게시판 디테일 페이지
# https://mht.kr/community/questions/new/ # 질문 게시판에 글 생성
# https://mht.kr/community/questions/del/<int:pk>/ # 질문 게시판 글 삭제
#
# https://mht.kr/community/questions/comment/new/<int:community_pk>/ # 질문 게시판의 댓글 생성
