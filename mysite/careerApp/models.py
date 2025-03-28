from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.utils import timezone

class StudentProfile(models.Model):
    marital_status_choices = [
        ('Married', 'Married'),
        ('Widowed', 'Widowed'),
        ('Separated', 'Separated'),
        ('Divorced', 'Divorced'),
        ('Single', 'Single'),
        ('Other', 'Other'),
    ]
    interests = models.ManyToManyField('Interest', blank=True)
    name = models.TextField(null=True, blank=True)
    maritalstatus = models.CharField(max_length=160, choices=marital_status_choices, null=True, blank=True)
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True)
    accessTime = models.DateField(null=True, blank=True)
    psychometricAssessmentCompleted = models.BooleanField(default=False, null=True, blank=True)
    profileCompleted = models.BooleanField(default=False, null=True, blank=True)
    percentageOfProfileCompleted = models.BigIntegerField(default=0, null=True, blank=True)
    profilePic = models.FileField(upload_to='student/profilePic/', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
    gender = models.CharField(max_length=50, choices=[('Male', 'Male'), ('Female', 'Female')], default="Male")
    dob = models.DateField(null=True, blank=True)
    category = models.CharField(max_length=25, choices=[('General', 'General'), ('OBC', 'OBC'), ('SC', 'SC'), ('ST', 'ST')], null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='authorSTUProfile', null=True, blank=True)
    availableCredits = models.PositiveIntegerField(null=True, blank=True, default=0)
    authAdmin = models.OneToOneField(User, on_delete=models.CASCADE, related_name="authAdminSP", null=True, blank=True)
    phoneNo = models.BigIntegerField(null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    currentClass = models.ForeignKey('StudentClass', related_name='currClassSP', on_delete=models.SET_NULL, null=True, blank=True)
    currentStream = models.ForeignKey('Stream', related_name='currStreamSP', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name or '--Name not provided--'

    class Meta:
        verbose_name_plural = 'Student Profiles'


class AptiReportContent(models.Model):
    CALIBER = (
        ('Very High', 'Very High'),
        ('High', 'High'),
        ('Moderate', 'Moderate'),
        ('Below Average', 'Below Average'),
        ('Low', 'Low')
    )
    typeOfApti = models.ForeignKey('AptiQuizType', on_delete=models.SET_NULL, related_name='typeOfAptiAReportC', null=True)
    levelOfApti = models.CharField(max_length=50, choices=CALIBER, null=True)
    content = models.TextField(null=True, blank=True)
    contentHindi = models.TextField(null=True, blank=True)
    contentTamil = models.TextField(null=True, blank=True)
    contentMarathi = models.TextField(null=True, blank=True)
    contentGujarati = models.TextField(null=True, blank=True)
    contentUrdu = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.typeOfApti}-{self.levelOfApti}'

    class Meta:
        verbose_name_plural = 'Quiz-Aptitude Quiz Report Content'


class InterestReportContent(models.Model):
    TYPE = (
        ('Realistic', 'Realistic'),
        ('Investigative', 'Investigative'),
        ('Artistic', 'Artistic'),
        ('Social', 'Social'),
        ('Enterprising', 'Enterprising'),
        ('Conventional', 'Conventional'),
    )
    INT = (
        ('Very High', 'Very High'),
        ('High', 'High'),
        ('Moderate', 'Moderate'),
        ('Below Average', 'Below Average'),
        ('Low', 'Low')
    )
    typeOfInterest = models.CharField(max_length=50, choices=TYPE, null=True)
    levelOfInterest = models.CharField(max_length=50, choices=INT, null=True)
    content = models.TextField(null=True, blank=True)
    contentHindi = models.TextField(null=True, blank=True)
    contentTamil = models.TextField(null=True, blank=True)
    contentMarathi = models.TextField(null=True, blank=True)
    contentGujarati = models.TextField(null=True, blank=True)
    contentUrdu = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.typeOfInterest}-{self.levelOfInterest}'

    class Meta:
        verbose_name_plural = 'Quiz-Interest Quiz Report Content'


class UserInterestResponse(models.Model):
    questionAnswered = models.ForeignKey('InterestQues', related_name='questionAnsweredUIR', on_delete=models.SET_NULL, null=True)
    response = models.ForeignKey('InterestChoice', related_name='responseUIR', on_delete=models.SET_NULL, null=True)
    whoAnswered = models.ForeignKey('QuizTakerInterest', related_name='whoAnsweredUIR', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.questionAnswered}-{self.response}-{self.whoAnswered}'

    class Meta:
        verbose_name_plural = 'Quiz-User Interest Response'


class QuizTakerInterest(models.Model):
    FOR = (
        ('Stream', 'Stream'),
        ('Career', 'Career'),
        ('Both Stream and Career', 'Both Stream and Career')
    )
    quizApplicant = models.ForeignKey(User, related_name='quizApplicantQTI', on_delete=models.SET_NULL, null=True)
    score = models.BigIntegerField(default=0)
    quizTaken = models.ForeignKey('InterestQuiz', related_name='quizTakenQTI', on_delete=models.SET_NULL, null=True, blank=True)
    completedQuiz = models.BooleanField(null=True, default=False)
    attemptedFor = models.CharField(max_length=200, choices=FOR, null=True, blank=True)

    def __str__(self):
        return f'{self.quizApplicant}-{self.quizTaken}'


class InterestLevel(models.Model):
    INT = (
        ('Very High', 'Very High'),
        ('High', 'High'),
        ('Moderate', 'Moderate'),
        ('Below Average', 'Below Average'),
        ('Low', 'Low')
    )
    FOR = (
        ('Stream', 'Stream'),
        ('Career', 'Career'),
        ('Both Stream and Career', 'Both Stream and Career')
    )
    nameOfApplicant = models.CharField(max_length=250, null=True)
    interestLevel = models.CharField(max_length=50, choices=INT, null=True)
    typeOfInterest = models.CharField(max_length=200, null=True)
    attemptedFor = models.CharField(max_length=200, choices=FOR, null=True, blank=True)

    def __str__(self):
        return f'{self.nameOfApplicant}-{self.interestLevel}-{self.typeOfInterest}'


class InterestQues(models.Model):
    label = models.CharField(max_length=500, verbose_name="English Question Label", null=True, blank=True)
    linkedQuiz = models.ForeignKey('InterestQuiz', related_name='linkedQuizIQ', on_delete=models.SET_NULL, null=True)
    choicesAvailable = models.ManyToManyField('InterestChoice', blank=True, related_name='choicesAvailableIQ')

    def __str__(self):
        return self.label + f'-{self.linkedQuiz}'


class InterestChoice(models.Model):
    label = models.CharField(max_length=250, verbose_name="English Choices Label", null=True, blank=True)
    weightage = models.IntegerField(null=True)

    def __str__(self):
        return self.label


class InterestQuiz(models.Model):
    TYPE = (
        ('Realistic', 'Realistic'),
        ('Investigative', 'Investigative'),
        ('Artistic', 'Artistic'),
        ('Social', 'Social'),
        ('Enterprising', 'Enterprising'),
        ('Conventional', 'Conventional'),
    )
    quizName = models.CharField(max_length=250, null=True, unique=True)
    quizType = models.CharField(max_length=50, choices=TYPE, null=True)
    rollOut = models.BooleanField(null=True, default=False)

    def __str__(self):
        return self.quizName + f'-{self.quizType}'

    class Meta:
        verbose_name_plural = 'Quiz-Interests Quiz'


class QuizTaker(models.Model):
    FOR = (
        ('Stream', 'Stream'),
        ('Career', 'Career'),
        ('Both Stream and Career', 'Both Stream and Career')
    )
    quizApplicant = models.ForeignKey(User, related_name='quizApplicantQT', on_delete=models.SET_NULL, null=True)
    score = models.IntegerField(null=True)
    quizTaken = models.ForeignKey('Quiz', related_name='quizTaken', on_delete=models.SET_NULL, null=True, blank=True)
    completedQuiz = models.BooleanField(null=True, default=False)
    attemptedFor = models.CharField(max_length=200, choices=FOR, null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.quizApplicant}-{self.quizTaken}'

    class Meta:
        verbose_name_plural = 'Quiz-Quiz Taker Aptitude'


class AptiReportScorewise(models.Model):
    TYPE = (
        ('Career', 'Career'),
        ('Stream', 'Stream'),
        ('Both Stream and Career', 'Both Stream and Career')
    )
    nameOfStudent = models.CharField(max_length=250, null=True)
    typeOfApti = models.ForeignKey('AptiQuizType', related_name='typeOfAptiARS', on_delete=models.SET_NULL, null=True)
    score = models.BigIntegerField(default=0, null=True)
    totalScore = models.BigIntegerField(default=0, null=True)
    attemptedFor = models.CharField(null=True, blank=True, choices=TYPE, max_length=200)

    def __str__(self):
        return self.nameOfStudent + '-' + f'{self.typeOfApti}'

    class Meta:
        verbose_name_plural = 'Quiz-Aptitude Scorewise Report'


class AptiReportCaliber(models.Model):
    CALIBER = (
        ('Very High', 'Very High'),
        ('High', 'High'),
        ('Moderate', 'Moderate'),
        ('Below Average', 'Below Average'),
        ('Low', 'Low')
    )
    TYPE = (
        ('Career', 'Career'),
        ('Stream', 'Stream'),
        ('Both Stream and Career', 'Both Stream and Career')
    )
    nameOfStudent = models.CharField(max_length=250, null=True)
    typeOfApti = models.ForeignKey('AptiQuizType', related_name='typeOfAptiARC', on_delete=models.SET_NULL, null=True)
    caliber = models.CharField(null=True, max_length=100, choices=CALIBER)
    attemptedFor = models.CharField(null=True, blank=True, choices=TYPE, max_length=200)


class Answer(models.Model):
    ques = models.ForeignKey('Question', related_name='quesA', on_delete=models.SET_NULL, null=True)
    label = models.TextField(verbose_name="English Answer Label", null=True, blank=True)
    isCorrect = models.BooleanField(null=True, default=False)
    answerImage = models.FileField(upload_to='quiz/answerImages', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])

    def __str__(self):
        return self.label + '-' + f'{self.isCorrect}'


class Question(models.Model):
    label = models.TextField(verbose_name="English Question Label", null=True, blank=True)
    forQuiz = models.ForeignKey('Quiz', related_name='forQuizQ', on_delete=models.SET_NULL, null=True)
    questionImage = models.FileField(upload_to='quiz/questionImages', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])

    def __str__(self):
        if self.forQuiz:
            if self.forQuiz.quizType:
                return self.forQuiz.quizType + " -- " + self.label
        return self.label
