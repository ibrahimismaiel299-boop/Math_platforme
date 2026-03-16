from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Lesson, Quiz, QuizResult, Subscription, Category, ActivationCode

# 1. الصفحة الرئيسية (اختيار الصف الدراسي)
def home(request):
    return render(request, 'pages/index.html')

# 2. عرض الأقسام التابعة للصف الدراسي (المستوى الأول)
@login_required
def grade_categories(request, grade_code):
    # جلب الأقسام المرتبطة بهذا الصف (مثل: جبر 1 ثانوي، هندسة 1 ثانوي)
    categories = Category.objects.filter(grade=grade_code)
    grade_name = dict(Lesson.GRADES).get(grade_code)
    
    return render(request, 'pages/categories_list.html', {
        'categories': categories,
        'grade_name': grade_name,
        'grade_code': grade_code
    })

@login_required
def category_lessons(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    lessons = Lesson.objects.filter(category=category)
    
    # جلب قائمة بـ IDs الاختبارات التي حلها الطالب بنجاح في هذا القسم
    completed_quizzes = QuizResult.objects.filter(
        user=request.user, 
        quiz__lesson__category=category
    ).values_list('quiz_id', flat=True)

    user_subscriptions = [sub.category for sub in request.user.subscriptions.all()]
    is_allowed = category.is_free or category in user_subscriptions or request.user.is_superuser
    
    # ... (باقي كود الـ POST كما هو) ...

    return render(request, 'pages/lessons_list.html', {
        'category': category,
        'lessons': lessons,
        'is_allowed': is_allowed,
        'completed_quizzes': completed_quizzes, # أضفنا هذا السطر
    })


# 4. صفحة حل الاختبار وحفظ النتيجة
import random # أضف هذا السطر في أعلى ملف views.py

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    # تحويل الأسئلة لقائمة وعمل "خلط" عشوائي لها
    questions = list(quiz.questions.all())
    # ملاحظة: لو مش عايز الترتيب يتغير في كل Refresh، ممكن نشيل السطر ده
    random.shuffle(questions) 

    score = None
    total = len(questions)

    if request.method == "POST":
        score = 0
        for question in questions:
            selected_option = request.POST.get(f'question_{question.id}')
            if selected_option and int(selected_option) == question.correct_answer:
                score += 1
        
        QuizResult.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            total=total
        )
        
    return render(request, 'pages/take_quiz.html', {
        'quiz': quiz,
        'questions': questions, # نرسل الأسئلة المرتتبة عشوائياً
        'score': score,
        'total': total
    })

# 5. صفحة البروفايل الشخصي للنتائج والاشتراكات
@login_required
def profile(request):
    subscriptions = request.user.subscriptions.all() 
    results = QuizResult.objects.filter(user=request.user).order_by('-date')
    
    return render(request, 'pages/profile.html', {
        'subscriptions': subscriptions,
        'results': results
    })
