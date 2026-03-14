from django.urls import path
from . import views

urlpatterns = [
    # الصفحة الرئيسية (الصفوف الدراسية)
    path('', views.home, name='home'),

    # المستوى الأول: عرض الأقسام التابعة للصف (جبر، هندسة...)
    path('grade/<str:grade_code>/', views.grade_categories, name='grade_categories'),

    # المستوى الثاني: عرض دروس قسم محدد (فيديو، مذكرات...)
    path('category/<int:category_id>/', views.category_lessons, name='category_lessons'),

    # صفحة حل الاختبار
    path('quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),

    # صفحة البروفايل (النتائج والاشتراكات)
    path('profile/', views.profile, name='profile'),
]
