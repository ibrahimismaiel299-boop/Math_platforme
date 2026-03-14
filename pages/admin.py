from django.contrib import admin
from .models import Category, Lesson, Quiz, Question

# لعرض الأسئلة داخل صفحة الاختبار مباشرة (سهولة في الإضافة)
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 3  # عدد الخانات الفارغة التي تظهر لك لإضافة أسئلة جديدة

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson')
    inlines = [QuestionInline]

# تسجيل بقية الموديلات
admin.site.register(Category)
admin.site.register(Lesson)

from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number') # يعرض اسم الطالب ورقمه في جدول واحد
    search_fields = ('user__username', 'phone_number') # يمكنك البحث بالاسم أو الرقم

from .models import ActivationCode

admin.site.register(ActivationCode)

from django.contrib import admin

admin.site.site_header = "لوحة إدارة الإبداع في الرياضيات"
admin.site.site_title = "مستر رمضان إبراهيم"
admin.site.index_title = "مرحباً بك يا مستر رمضان في منصتك"

