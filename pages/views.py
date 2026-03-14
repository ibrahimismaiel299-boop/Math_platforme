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

# 3. عرض دروس قسم محدد (المستوى الثاني - مع نظام القفل)
@login_required
def category_lessons(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    lessons = Lesson.objects.filter(category=category)
    
    # التحقق من صلاحية الوصول (مجاني، مشترك، أو أدمن)
    user_subscriptions = [sub.category for sub in request.user.subscriptions.all()]
    is_allowed = category.is_free or category in user_subscriptions or request.user.is_superuser
    
    # معالجة كود التفعيل داخل صفحة القسم
    if request.method == "POST":
        input_code = request.POST.get('activation_code')
        try:
            code_obj = ActivationCode.objects.get(code=input_code, category=category, is_used=False)
            Subscription.objects.get_or_create(user=request.user, category=category)
            code_obj.is_used = True
            code_obj.save()
            messages.success(request, f"تم تفعيل قسم {category.name} بنجاح!")
            return redirect('category_lessons', category_id=category.id)
        except ActivationCode.DoesNotExist:
            messages.error(request, "كود التفعيل غير صحيح أو تم استخدامه مسبقاً.")

    return render(request, 'pages/lessons_list.html', {
        'category': category,
        'lessons': lessons,
        'is_allowed': is_allowed
    })

# 4. صفحة حل الاختبار وحفظ النتيجة
@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    score = None
    total = quiz.questions.count()

    if request.method == "POST":
        score = 0
        for question in quiz.questions.all():
            selected_option = request.POST.get(f'question_{question.id}')
            if selected_option and int(selected_option) == question.correct_answer:
                score += 1
        
        # حفظ النتيجة في قاعدة البيانات
        QuizResult.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            total=total
        )
        
    return render(request, 'pages/take_quiz.html', {
        'quiz': quiz,
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
