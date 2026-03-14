from django.db import models
from django.contrib.auth.models import User

# 1. موديل الأقسام (يحتوي الآن على السعر والقفل)
class Category(models.Model):
    # خيارات الصفوف (يجب أن تكون هنا داخل الكلاس الرئيسي)
    GRADES = [
        ('1G', 'الأول الإعدادي'), ('2G', 'الثاني الإعدادي'), ('3G', 'الثالث الإعدادي'),
        ('1S', 'الأول الثانوي'), ('2S', 'الثاني الثانوي'), ('3S', 'الثالث الثانوي'),
    ]

    name = models.CharField(max_length=100, verbose_name="اسم القسم")
    # حقل الصف الدراسي (هنا مكانه الصحيح)
    grade = models.CharField(max_length=2, choices=GRADES, default='1G', verbose_name="الصف الدراسي التابع له")
    is_free = models.BooleanField(default=False, verbose_name="هل القسم مجاني؟")
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, verbose_name="سعر القسم")

    def __str__(self):
        return f"{self.name} - {self.get_grade_display()}"

    class Meta:
        verbose_name = "قسم"
        verbose_name_plural = "الأقسام"

# 2. موديل الدرس
class Lesson(models.Model):
    GRADES = [
        ('1G', 'الأول الإعدادي'), ('2G', 'الثاني الإعدادي'), ('3G', 'الثالث الإعدادي'),
        ('1S', 'الأول الثانوي'), ('2S', 'الثاني الثانوي'), ('3S', 'الثالث الثانوي'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="عنوان الدرس")
    grade = models.CharField(max_length=2, choices=GRADES, verbose_name="الصف الدراسي")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="الفرع / القسم")
    video_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="رابط فيديو اليوتيوب")
    pdf_file = models.FileField(upload_to='lessons_pdfs/', blank=True, null=True, verbose_name="ملف المذكرة (PDF)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.category.name}"

    class Meta:
        verbose_name = "درس"
        verbose_name_plural = "الدروس"

# 3. موديل الاختبار
class Quiz(models.Model):
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, related_name='quiz', verbose_name="الدرس التابع له")
    title = models.CharField(max_length=200, verbose_name="عنوان الاختبار")

    def __str__(self):
        return f"اختبار: {self.lesson.title}"

    class Meta:
        verbose_name = "اختبار"
        verbose_name_plural = "الاختبارات"

# 4. موديل الأسئلة
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(verbose_name="نص السؤال")
    option1 = models.CharField(max_length=200, verbose_name="الخيار الأول")
    option2 = models.CharField(max_length=200, verbose_name="الخيار الثاني")
    option3 = models.CharField(max_length=200, verbose_name="الخيار الثالث")
    option4 = models.CharField(max_length=200, verbose_name="الخيار الرابع")
    correct_answer = models.IntegerField(
        choices=[(1, 'الخيار الأول'), (2, 'الخيار الثاني'), (3, 'الخيار الثالث'), (4, 'الخيار الرابع')], 
        verbose_name="الإجابة الصحيحة"
    )

    def __str__(self):
        return self.text[:50]

    class Meta:
        verbose_name = "سؤال"
        verbose_name_plural = "الأسئلة"

# 5. جدول اشتراكات الطلاب
class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'category')
        verbose_name = "اشتراك طالب"
        verbose_name_plural = "اشتراكات الطلاب"

# 6. جدول نتائج الاختبارات
class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_results')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(verbose_name="الدرجة")
    total = models.IntegerField(verbose_name="الدرجة النهائية")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "نتيجة اختبار"
        verbose_name_plural = "نتائج الاختبارات"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, verbose_name="رقم الواتساب")

    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name = "ملف شخصي"
        verbose_name_plural = "الملفات الشخصية"
import uuid

class ActivationCode(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name="كود التفعيل")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="القسم المراد تفعيله")
    is_used = models.BooleanField(default=False, verbose_name="هل استُخدم؟")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            # توليد كود عشوائي تلقائياً إذا تركت الخانة فارغة
            self.code = str(uuid.uuid4()).split('-')[0].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {self.category.name}"

    class Meta:
        verbose_name = "كود تفعيل"
        verbose_name_plural = "أكواد التفعيل"
