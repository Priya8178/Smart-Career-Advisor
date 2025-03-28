from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django_summernote.admin import SummernoteModelAdmin
from .models import (
    aptiReportContent, aptiReportCaliber, aptiReportScorewise, 
    quizTaker, quizTakerInterest, interestLevel, userAnswer, 
    interestReportContent, userInterestResponse, question, 
    quiz, answer, AptiQuizType, interestQuiz, interestChoice, 
    interestQues
)

@admin.register(aptiReportContent)
class aptiReportContentAdmin(ImportExportModelAdmin, SummernoteModelAdmin, admin.ModelAdmin):
    summernote_fields = ('content', 'contentHindi', 'contentTamil', 'contentMarathi', 'contentGujrati', 'contentUrdu', )


class aptiReportCaliberAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('nameOfStudent', 'typeOfApti', 'caliber', 'attemptedFor')
    search_fields = ('nameOfStudent',)
    list_filter = ('typeOfApti', 'caliber')


class aptiReportScorewiseAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('nameOfStudent', 'typeOfApti', 'score', 'totalScore', 'attemptedFor')
    search_fields = ('nameOfStudent',)
    list_filter = ('typeOfApti',)


class quizTakerAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('quizApplicant', 'score', 'quizTaken', 'completedQuiz', 'attemptedFor', 'publish')
    search_fields = ('quizApplicant__username',)
    autocomplete_fields = ('quizApplicant',)
    list_filter = ('completedQuiz',)


class quizTakerInterestAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('quizApplicant', 'score', 'quizTaken', 'completedQuiz', 'attemptedFor')
    search_fields = ('quizApplicant__username',)
    autocomplete_fields = ('quizApplicant',)
    list_filter = ('completedQuiz',)


class interestLevelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('nameOfApplicant', 'interestLevel', 'typeOfInterest', 'attemptedFor')
    search_fields = ('nameOfApplicant', 'interestLevel')
    list_filter = ('interestLevel',)


class userAnswerAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['forQuestion', 'respondedWith', 'whoAnswered']
    search_fields = ['whoAnswered__quizApplicant__username']


@admin.register(interestReportContent)
class interestReportContentAdmin(ImportExportModelAdmin, SummernoteModelAdmin, admin.ModelAdmin):
    summernote_fields = ('content', 'contentHindi', 'contentTamil', 'contentMarathi', 'contentGujrati', 'contentUrdu', )


class userInterestResponseAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['questionAnswered', 'response', 'whoAnswered']
    search_fields = ['whoAnswered__quizApplicant__username']


admin.site.register(quizTaker, quizTakerAdmin)
admin.site.register(question, questionAdmin)
admin.site.register(quiz, ImportExportModelAdmin)
admin.site.register(answer, ImportExportModelAdmin)
admin.site.register(userAnswer, userAnswerAdmin)
admin.site.register(AptiQuizType, ImportExportModelAdmin)
admin.site.register(aptiReportCaliber, aptiReportCaliberAdmin)
admin.site.register(aptiReportScorewise, aptiReportScorewiseAdmin)
admin.site.register(interestQuiz, ImportExportModelAdmin)
admin.site.register(interestChoice, ImportExportModelAdmin)
admin.site.register(interestQues, ImportExportModelAdmin)
admin.site.register(quizTakerInterest, quizTakerInterestAdmin)
admin.site.register(userInterestResponse, userInterestResponseAdmin)
admin.site.register(interestLevel, interestLevelAdmin)
