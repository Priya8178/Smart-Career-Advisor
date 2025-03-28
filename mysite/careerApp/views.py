from multiprocessing import Value
from django import db
from django.forms import IntegerField
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import *

# Create your views here.
@login_required
def quizStartApti(request):
    quizArea = request.GET.get("type")
    if quizArea == 'careerNStream':
        quizArea = 'Both Stream and Career'
    if not request.user.first_name == 'studentAccount':
        return HttpResponse(notAuthErrMsg)
    try:
        student = StudentProfile.objects.get(authAdmin=request.user)
    except: 
        student = None
    quizT = get_object_or_404(AptiQuizType, quizType='Numerical Aptitude')
    quizObj = quiz.objects.get(Type=quizT)
    quizT2 = get_object_or_404(AptiQuizType, quizType='Verbal Aptitude')
    quizObj2 = quiz.objects.get(Type=quizT2)
    quizT3 = get_object_or_404(AptiQuizType, quizType='Logical Aptitude')
    quizObj3 = quiz.objects.get(Type=quizT3)
    Qe1 = []
    Qe2 = []
    Qe3 = []
    if quizTaker.objects.filter(quizApplicant = request.user,quizTaken = quizObj,attemptedFor=quizArea):
        cd = quizTaker.objects.filter(quizApplicant = request.user,quizTaken = quizObj,attemptedFor=quizArea).first()        
        ansLength1 = userAnswer.objects.filter(whoAnswered = cd)
        for i in ansLength1:
            Qe1.append(i.forQuestion.id)
    if quizTaker.objects.filter(quizApplicant = request.user,quizTaken = quizObj2,attemptedFor=quizArea):
        cd2 = quizTaker.objects.filter(quizApplicant = request.user,quizTaken = quizObj2,attemptedFor=quizArea).first()
        ansLength2 = userAnswer.objects.filter(whoAnswered = cd2)
        for i in ansLength2:
            Qe2.append(i.forQuestion.id)
    if quizTaker.objects.filter(quizApplicant = request.user,quizTaken = quizObj3,attemptedFor=quizArea):
        cd3 = quizTaker.objects.filter(quizApplicant = request.user,quizTaken = quizObj3,attemptedFor=quizArea).first()
        ansLength3 = userAnswer.objects.filter(whoAnswered = cd3)
        for i in ansLength3:
            Qe3.append(i.forQuestion.id)
    questionList1 = question.objects.filter(forQuiz = quizObj).exclude(id__in=Qe1).order_by('?')
    questionList2 = question.objects.filter(forQuiz = quizObj2).exclude(id__in=Qe2).order_by('?')
    questionList3 = question.objects.filter(forQuiz = quizObj3).exclude(id__in=Qe3).order_by('?')
    questionList = questionList1 | questionList2 | questionList3
    questionListCount = questionList.count() + 60
    qcount = len(Qe1) + len(Qe2) + len(Qe3)
    ansLength1 = 0
    ansLength2 = 0
    ansLength3 = 0
    if quizTaker.objects.filter(quizApplicant=request.user,quizTaken=quizObj3,attemptedFor=quizArea,completedQuiz=True):
        return redirect(reverse('quizApp:quizStartInt')+'?type='+quizArea)
    answerList = []
    for item in questionList:
        ob = answer.objects.filter(ques = item).order_by('?')
        for i in ob:
            answerList.append(i)
    db.connection.close()
    return render(request,'quiz/UI/quizStartApti.html',{'questionList':questionList, 'questionList1':questionListCount,'answerList':answerList, 'quizArea':quizArea, 'student':student, 'qcount':qcount})

@login_required
def saveAnswer(request):
    Thread(target=sanswer, args=(request,)).start()
    return JsonResponse({"status": True})

def sanswer(request):
    quizArea = request.POST.get("type")
    isSubmit = request.POST.get("isSubmit")
    quizT = get_object_or_404(AptiQuizType, quizType='Numerical Aptitude')
    quizObj = quiz.objects.get(Type=quizT)
    quizT2 = get_object_or_404(AptiQuizType, quizType='Verbal Aptitude')
    quizObj2 = quiz.objects.get(Type=quizT2)
    quizT3 = get_object_or_404(AptiQuizType, quizType='Logical Aptitude')
    quizObj3 = quiz.objects.get(Type=quizT3)
    if quizTaker.objects.filter(quizApplicant = request.user,quizTaken = quizObj,attemptedFor=quizArea):
        cd = quizTaker.objects.filter(quizApplicant = request.user,quizTaken = quizObj,attemptedFor=quizArea).first()    
    else:
        if quizTaker.objects.filter(quizApplicant = request.user,quizTaken = None,attemptedFor=quizArea):
            cd = quizTaker.objects.filter(quizApplicant = request.user,quizTaken = None,attemptedFor=quizArea).first()
            cd.quizTaken = quizObj
            cd.save()
        else:
            cd = quizTaker(quizApplicant = request.user,quizTaken = quizObj,attemptedFor=quizArea)
            cd.save()
    if quizTaker.objects.filter(quizApplicant = request.user,quizTaken = quizObj2,attemptedFor=quizArea):
            cd2 = quizTaker.objects.filter(quizApplicant = request.user,quizTaken = quizObj2,attemptedFor=quizArea).first()
    else:
        if quizTaker.objects.filter(quizApplicant = request.user,quizTaken = None,attemptedFor=quizArea):
            cd2 = quizTaker.objects.filter(quizApplicant = request.user,quizTaken = None,attemptedFor=quizArea).first()
            cd2.quizTaken = quizObj2
            cd2.save()
        else:
            cd2 = quizTaker(quizApplicant = request.user,quizTaken = quizObj2,attemptedFor=quizArea)
            cd2.save()
    if quizTaker.objects.filter(quizApplicant = request.user,quizTaken = quizObj3,attemptedFor=quizArea):
            cd3 = quizTaker.objects.filter(quizApplicant = request.user,quizTaken = quizObj3,attemptedFor=quizArea).first()
    else:
        if quizTaker.objects.filter(quizApplicant = request.user,quizTaken = None,attemptedFor=quizArea):
            cd3 = quizTaker.objects.filter(quizApplicant = request.user,quizTaken = None,attemptedFor=quizArea).first()
            cd3.quizTaken = quizObj3
            cd3.save()
        else:
            cd3 = quizTaker(quizApplicant = request.user,quizTaken = quizObj3,attemptedFor=quizArea)
            cd3.save()
    answers = request.POST.get('answers', [])
    for i in json.loads(answers):
        queObj = question.objects.get(id=int(i['que']))
        if i['answer'] == None:
            pass
        else:
            ansObj = answer.objects.get(id=int(i['answer']))
            if queObj.forQuiz == quizObj:
                if not userAnswer.objects.filter(forQuestion = queObj,whoAnswered = cd).exists():
                    ua = userAnswer(forQuestion = queObj,respondedWith = ansObj,whoAnswered = cd)
                    ua.save()
                    if ua.respondedWith:
                        if ua.respondedWith.isCorrect:
                            if cd.score:
                                cd.score += 1
                                cd.save()
                            else:
                                cd.score = 1
                                cd.save()
            if queObj.forQuiz == quizObj2:
                if not userAnswer.objects.filter(forQuestion = queObj,whoAnswered = cd2).exists():
                    ua = userAnswer(forQuestion = queObj,respondedWith = ansObj,whoAnswered = cd2)
                    ua.save()
                    if ua.respondedWith:
                        if ua.respondedWith.isCorrect:
                            if cd2.score:
                                cd2.score += 1
                                cd2.save()
                            else:
                                cd2.score = 1
                                cd2.save()
            if queObj.forQuiz == quizObj3:
                if not userAnswer.objects.filter(forQuestion = queObj,whoAnswered = cd3).exists():
                    ua = userAnswer(forQuestion = queObj,respondedWith = ansObj,whoAnswered = cd3)
                    ua.save()
                    if ua.respondedWith:
                        if ua.respondedWith.isCorrect:
                            if cd3.score:
                                cd3.score += 1
                                cd3.save()
                            else:
                                cd3.score = 1
                                cd3.save()
    if isSubmit == "true":
        cd.completedQuiz = True
        cd.save()
        cd2.completedQuiz = True
        cd2.save()
        cd3.completedQuiz = True
        cd3.save()
    db.connection.close()

@login_required
def quizStartInt(request):
    quizArea = request.GET.get("type")
    if quizArea == 'careerNStream':
        quizArea = 'Both Stream and Career'
    if not request.user.first_name == 'studentAccount':
        return HttpResponse(notAuthErrMsg)
    try:
        student = StudentProfile.objects.get(authAdmin=request.user)
    except: 
        student = None
    flag = True
    quizObj = get_object_or_404(interestQuiz, quizType='Realistic') or None
    quizObj2 = get_object_or_404(interestQuiz, quizType='Investigative') or None
    quizObj3 = get_object_or_404(interestQuiz, quizType='Artistic') or None
    quizObj4 = get_object_or_404(interestQuiz, quizType='Social') or None
    quizObj5 = get_object_or_404(interestQuiz, quizType='Enterprising') or None
    quizObj6 = get_object_or_404(interestQuiz, quizType='Conventional') or None
    Qe1 = []
    Qe2 = []
    Qe3 = []
    Qe4 = []
    Qe5 = []
    Qe6 = []
    if quizTakerInterest.objects.filter(quizApplicant = request.user,quizTaken = quizObj,attemptedFor=quizArea):
        cd = quizTakerInterest.objects.filter(quizApplicant = request.user,quizTaken = quizObj,attemptedFor=quizArea).first()        
        ansLength1 = userInterestResponse.objects.filter(whoAnswered = cd)
        for i in ansLength1:
            Qe1.append(i.questionAnswered.id)
    if quizTakerInterest.objects.filter(quizApplicant = request.user,quizTaken = quizObj2,attemptedFor=quizArea):
        cd2 = quizTakerInterest.objects.filter(quizApplicant = request.user,quizTaken = quizObj2,attemptedFor=quizArea).first()
        ansLength2 = userInterestResponse.objects.filter(whoAnswered = cd2)
        for i in ansLength2:
            Qe2.append(i.questionAnswered.id)
    if quizTakerInterest.objects.filter(quizApplicant = request.user,quizTaken = quizObj3,attemptedFor=quizArea):
        cd3 = quizTakerInterest.objects.filter(quizApplicant = request.user,quizTaken = quizObj3,attemptedFor=quizArea).first()
        ansLength3 = userInterestResponse.objects.filter(whoAnswered = cd3)
        for i in ansLength3:
            Qe3.append(i.questionAnswered.id)
    if quizTakerInterest.objects.filter(quizApplicant = request.user,quizTaken = quizObj4,attemptedFor=quizArea):
        cd4 = quizTakerInterest.objects.filter(quizApplicant = request.user,quizTaken = quizObj4,attemptedFor=quizArea).first()
        ansLength4 = userInterestResponse.objects.filter(whoAnswered = cd4)
        for i in ansLength4:
            Qe4.append(i.questionAnswered.id)
    if quizTakerInterest.objects.filter(quizApplicant = request.user,quizTaken = quizObj5,attemptedFor=quizArea):
        cd5 = quizTakerInterest.objects.filter(quizApplicant = request.user,quizTaken = quizObj5,attemptedFor=quizArea).first()
        ansLength5 = userInterestResponse.objects.filter(whoAnswered = cd5)
        for i in ansLength5:
            Qe5.append(i.questionAnswered.id)
    if quizTakerInterest.objects.filter(quizApplicant = request.user,quizTaken = quizObj6,attemptedFor=quizArea):
        cd6 = quizTakerInterest.objects.filter(quizApplicant = request.user,quizTaken = quizObj6,attemptedFor=quizArea).first()
        ansLength6 = userInterestResponse.objects.filter(whoAnswered = cd6)
        for i in ansLength6:
            Qe6.append(i.questionAnswered.id)
    questionList1 = interestQues.objects.filter(linkedQuiz = quizObj).exclude(id__in=Qe1).order_by('?')
    questionList2 = interestQues.objects.filter(linkedQuiz = quizObj2).exclude(id__in=Qe2).order_by('?')
    questionList3 = interestQues.objects.filter(linkedQuiz = quizObj3).exclude(id__in=Qe3).order_by('?')
    questionList4 = interestQues.objects.filter(linkedQuiz = quizObj4).exclude(id__in=Qe4).order_by('?')
    questionList5 = interestQues.objects.filter(linkedQuiz = quizObj5).exclude(id__in=Qe5).order_by('?')
    questionList6 = interestQues.objects.filter(linkedQuiz = quizObj6).exclude(id__in=Qe6).order_by('?')
    # questionList = questionList1 | questionList2 | questionList3 | questionList4 | questionList5 | questionList6
    questionList = questionList1.union(questionList2,questionList3,questionList4,questionList5,questionList6)
    flagCom = request.user.authAdminSP.uniqueCode
    if not questionList or quizTakerInterest.objects.filter(quizApplicant=request.user,quizTaken=quizObj6,attemptedFor=quizArea,completedQuiz=True).exists():
        student.psychometricAssessmentCompleted = True
        student.save()
        assessmentNotification(student)
        if quizArea == 'Stream':
            return redirect(reverse('quizApp:reportStream')+'?flag='+str(flagCom)+'')
        elif quizArea == 'Career':
            return redirect(reverse('quizApp:report')+'?flag='+str(flagCom)+'')
        elif quizArea == 'Both Stream and Career':
            return redirect('quizApp:indexCareerAndStream')
    questionListCount = questionList.count() + 75
    qcount = len(Qe1) + len(Qe2) + len(Qe3) + len(Qe4) + len(Qe5) + len(Qe6)
    db.connection.close()
    return render(request,'quiz/UI/quizStartInt.html',{'questionList':questionList, 'questionList1':questionListCount, 'quizArea':quizArea, 'student':student, 'qcount':qcount})

@login_required
def saveAnswer1(request):
    Thread(target=sanswer1, args=(request,)).start()
    return JsonResponse({"status": True})

def sanswer1(request):
    quizArea = request.POST.get("type")
    isSubmit = request.POST.get("isSubmit")
    quizObj = get_object_or_404(interestQuiz, quizType='Realistic') or None
    quizObj2 = get_object_or_404(interestQuiz, quizType='Investigative') or None
    quizObj3 = get_object_or_404(interestQuiz, quizType='Artistic') or None
    quizObj4 = get_object_or_404(interestQuiz, quizType='Social') or None
    quizObj5 = get_object_or_404(interestQuiz, quizType='Enterprising') or None
    quizObj6 = get_object_or_404(interestQuiz, quizType='Conventional') or None
    if quizTakerInterest.objects.filter(quizApplicant = request.user,quizTaken = quizObj,attemptedFor=quizArea):
        cd = quizTakerInterest.objects.filter(quizApplicant = request.user,quizTaken = quizObj,attemptedFor=quizArea).first()    
    else:
        if quizTakerInterest.objects.filter(quizApplicant = request.user,quizTaken = None,attemptedFor=quizArea):
            cd = quizTakerInterest.objects.filter(quizApplicant = request.user,quizTaken = None,attemptedFor=quizArea).first()
            cd.quizTaken = quizObj
            cd.save()
        else:
            cd = quizTakerInterest(quizApplicant = request.user,quizTaken = quizObj,attemptedFor=quizArea)
            cd.save()
    if quizTakerInterest.objects.filter(quizApplicant = request.user,quizTaken = quizObj2,attemptedFor=quizArea):
        cd2 = quizTakerInterest.objects.filter(quizApplicant = request.user,quizTaken = quizObj2,attemptedFor=quizArea).first()
    else:
        if quizTakerInterest.objects.filter(quizApplicant = request.user,quizTaken = None,attemptedFor=quizArea):
            cd2 = quizTakerInterest.objects.filter(quizApplicant = request.user,quizTaken = None,attemptedFor=quizArea).first()
            cd2.quizTaken = quizObj2
            cd2.save()
        else:
            cd2 = quizTakerInterest(quizApplicant = request.user,quizTaken = quizObj2,attemptedFor=quizArea)
            cd2.save()
    if quizTakerInterest.objects.filter(quizApplicant = request.user,quizTaken = quizObj3,attemptedFor=quizArea):
        cd3 = quizTakerInterest.objects.filter(quizApplicant = request.user,quizTaken = quizObj3,attemptedFor=quizArea).first()
    else:
        if quizTakerInterest.objects.filter(quizApplicant = request.user,quizTaken = None,attemptedFor=quizArea):
            cd3 = quizTakerInterest.objects.filter(quizApplicant = request.user,quizTaken = None,attemptedFor=quizArea).first()
            cd3.quizTaken = quizObj3
            cd3.save()
        else:
            cd3 = quizTakerInterest(quizApplicant = request.user,quizTaken = quizObj3,attemptedFor=quizArea)
            cd3.save()
    if quizTakerInterest.objects.filter(quizApplicant = request.user,quizTaken = quizObj4,attemptedFor=quizArea):
        cd4 = quizTakerInterest.objects.filter(quizApplicant = request.user,quizTaken = quizObj4,attemptedFor=quizArea).first()
    else:
        if quizTakerInterest.objects.filter(quizApplicant = request.user,quizTaken = None,attemptedFor=quizArea):
            cd4 = quizTakerInterest.objects.filter(quizApplicant = request.user,quizTaken = None,attemptedFor=quizArea).first()
            cd4.quizTaken = quizObj4
            cd4.save()
        else:
            cd4 = quizTakerInterest(quizApplicant = request.user,quizTaken = quizObj4,attemptedFor=quizArea)
            cd4.save()
    if quizTakerInterest.objects.filter(quizApplicant = request.user,quizTaken = quizObj5,attemptedFor=quizArea):
        cd5 = quizTakerInterest.objects.filter(quizApplicant = request.user,quizTaken = quizObj5,attemptedFor=quizArea).first()
    else:
        if quizTakerInterest.objects.filter(quizApplicant = request.user,quizTaken = None,attemptedFor=quizArea):
            cd5 = quizTakerInterest.objects.filter(quizApplicant = request.user,quizTaken = None,attemptedFor=quizArea).first()
            cd5.quizTaken = quizObj5
            cd5.save()
        else:
            cd5 = quizTakerInterest(quizApplicant = request.user,quizTaken = quizObj5,attemptedFor=quizArea)
            cd5.save()
    if quizTakerInterest.objects.filter(quizApplicant = request.user,quizTaken = quizObj6,attemptedFor=quizArea):
        cd6 = quizTakerInterest.objects.filter(quizApplicant = request.user,quizTaken = quizObj6,attemptedFor=quizArea).first()
    else:
        if quizTakerInterest.objects.filter(quizApplicant = request.user,quizTaken = None,attemptedFor=quizArea):
            cd6 = quizTakerInterest.objects.filter(quizApplicant = request.user,quizTaken = None,attemptedFor=quizArea).first()
            cd6.quizTaken = quizObj6
            cd6.save()
        else:
            cd6 = quizTakerInterest(quizApplicant = request.user,quizTaken = quizObj6,attemptedFor=quizArea)
            cd6.save()
    answers = request.POST.get('answers', [])
    for i in json.loads(answers):
        queObj = interestQues.objects.get(id=int(i['que']))
        if i['answer'] == None:
            pass
        else:
            ansObj = interestChoice.objects.get(id=int(i['answer']))
            if queObj.linkedQuiz == quizObj:
                if not userInterestResponse.objects.filter(questionAnswered = queObj,whoAnswered = cd).exists():
                    ua = userInterestResponse(questionAnswered = queObj,response = ansObj,whoAnswered = cd)
                    ua.save()
                    if ansObj:
                        cd.score += ansObj.weightage
                        cd.save()
            if queObj.linkedQuiz == quizObj2:
                if not userInterestResponse.objects.filter(questionAnswered = queObj,whoAnswered = cd2).exists():
                    ua = userInterestResponse(questionAnswered = queObj,response = ansObj,whoAnswered = cd2)
                    ua.save()
                    if ansObj:
                        cd2.score += ansObj.weightage
                        cd2.save()
            if queObj.linkedQuiz == quizObj3:
                if not userInterestResponse.objects.filter(questionAnswered = queObj,whoAnswered = cd3).exists():
                    ua = userInterestResponse(questionAnswered = queObj,response = ansObj,whoAnswered = cd3)
                    ua.save()
                    if ansObj:
                        cd3.score += ansObj.weightage
                        cd3.save()
            if queObj.linkedQuiz == quizObj4:
                if not userInterestResponse.objects.filter(questionAnswered = queObj,whoAnswered = cd4).exists():
                    ua = userInterestResponse(questionAnswered = queObj,response = ansObj,whoAnswered = cd4)
                    ua.save()
                    if ansObj:
                        cd4.score += ansObj.weightage
                        cd4.save()
            if queObj.linkedQuiz == quizObj5:
                if not userInterestResponse.objects.filter(questionAnswered = queObj,whoAnswered = cd5).exists():
                    ua = userInterestResponse(questionAnswered = queObj,response = ansObj,whoAnswered = cd5)
                    ua.save()
                    if ansObj:
                        cd5.score += ansObj.weightage
                        cd5.save()
            if queObj.linkedQuiz == quizObj6:
                if not userInterestResponse.objects.filter(questionAnswered = queObj,whoAnswered = cd6).exists():
                    ua = userInterestResponse(questionAnswered = queObj,response = ansObj,whoAnswered = cd6)
                    ua.save()
                    if ansObj:
                        cd6.score += ansObj.weightage
                        cd6.save()
    if isSubmit == "true":
        cd.completedQuiz = True
        cd.save()
        cd2.completedQuiz = True
        cd2.save()
        cd3.completedQuiz = True
        cd3.save()
        cd4.completedQuiz = True
        cd4.save()
        cd5.completedQuiz = True
        cd5.save()
        cd6.completedQuiz = True
        cd6.save()
    db.connection.close()

@login_required
def reportCareer(request):
    code = request.GET.get('profileCode')
    if code:
        stuObj = get_object_or_404(StudentProfile, uniqueCode = code)
    else:
        stuObj = get_object_or_404(StudentProfile, authAdmin = request.user)
    if not stuObj.authAdmin.first_name == 'studentAccount':
        return HttpResponse("not authorized")
    flag = False
    quizObj = quiz.objects.filter(rollOut=True)
    quizList = []
    quizTakers = quizTaker.objects.filter(quizApplicant=stuObj.authAdmin,completedQuiz=True,attemptedFor='Career')
    temp = []
    for item in quizTakers:
        temp.append(item.quizTaken)
    for item in quizObj:
        if not item in temp:
            quizList.append(item)
    intQuiz = interestQuiz.objects.filter(rollOut = True)
    quizIntList = [] 
    quizTakerInt = quizTakerInterest.objects.filter(quizApplicant=stuObj.authAdmin,completedQuiz=True,attemptedFor='Career')
    temp2 = []
    for item in quizTakerInt:
        temp2.append(item.quizTaken)
    for item in intQuiz:
        if not item in temp2:
            quizIntList.append(item)
    if quizList or quizIntList:
        flag = True
    flag2 = False
    lang = None
    
        
    if not flag:
        stuObj.psychometricAssessmentCompleted = True
        stuObj.save()
        if 'subHindi' in request.POST:
            flag2 = True
            lang = "Hin"
        if 'subEnglish' in request.POST:
            flag2 = True
            lang = 'Eng'
        aptiReportobj = aptiReportCaliber.objects.filter(nameOfStudent=stuObj.authAdmin.username,attemptedFor='Career')
        aptiReportScore = aptiReportScorewise.objects.filter(nameOfStudent=stuObj.authAdmin.username,attemptedFor='Career')
        logical = 0
        verbal = 0
        numerical = 0
        for item in aptiReportScore:
            
            if item.typeOfApti.quizType == 'Numerical Aptitude':
                if item.score:
                    numerical += item.score
            if item.typeOfApti.quizType == 'Logical Aptitude':
                if item.score:
                    logical += item.score
            if item.typeOfApti.quizType == 'Verbal Aptitude':
                if item.score:
                    verbal += item.score

        interestReportObj = interestLevel.objects.filter(nameOfApplicant=stuObj.authAdmin.username,attemptedFor='Career')
        sortInt = quizTakerInterest.objects.filter(quizApplicant=stuObj.authAdmin,attemptedFor='Career').order_by('-score')
        sortApti = aptiReportScorewise.objects.filter(nameOfStudent=stuObj.authAdmin.username,attemptedFor='Career').order_by('-score')
        temp = []
        firstBest = None
        secondBest = None
        for item in sortInt:
            temp.append(item)
        firstBest = temp[0].quizTaken.quizType
        secondBest = temp[1].quizTaken.quizType
        code = ''
        if firstBest and firstBest == 'Realistic':
            code += 'R'
        elif firstBest and firstBest == 'Investigative':
            code += 'I'
        elif firstBest and firstBest == 'Artistic':
            code += 'A'
        elif firstBest and firstBest == 'Social':
            code += 'S'
        elif firstBest and firstBest == 'Enterprising':
            code += 'E'
        elif firstBest and firstBest == 'Conventional':
            code += 'C'

        if secondBest and secondBest == 'Realistic':
            code += 'R'
        elif secondBest and secondBest == 'Investigative':
            code += 'I'
        elif secondBest and secondBest == 'Artistic':
            code += 'A'
        elif secondBest and secondBest == 'Social':
            code += 'S'
        elif secondBest and secondBest == 'Enterprising':
            code += 'E'
        elif secondBest and secondBest == 'Conventional':
            code += 'C'

        codeRev = code[::-1]
        careers = career.objects.filter(status="published")
        aptitude_career = careers.filter(numerical__lte=numerical, logical__lte=logical, verbal__lte=verbal)
        interest_career = careers.filter(Q(riasecCode=codeRev) | Q(riasecCode=code))
        aptitude_career_conv = aptitude_career.filter(cluster__vocational=False)
        aptitude_career_voc = aptitude_career.filter(cluster__vocational=True)
        interest_career_conv = interest_career.filter(cluster__vocational=False)
        interest_career_voc = interest_career.filter(cluster__vocational=True)

        stream_exists = False
        if stuObj.currentClass:
            if stuObj.currentClass.name in ['XI', 'XII']:
                student_stream = stuObj.currentStream.name if stuObj.currentStream else None
                if student_stream:
                    stream_exists = True
                    stream_filter = Q(stream=stuObj.currentStream) | Q(stream__name="Any Stream")
                    # stream_filter = Q(stream=stuObj.currentStream)

                    if student_stream == "Humanities With Maths":
                        stream_filter |= Q(stream__name="Humanities Without Maths")
                    elif student_stream == "Commerce With Maths":
                        stream_filter |= Q(stream__name="Commerce Without Maths")
                    elif student_stream == "Humanities Without Maths":
                        stream_filter = Q(stream__name="Humanities Without Maths")
                    elif student_stream == "Commerce Without Maths":
                        stream_filter = Q(stream__name="Commerce Without Maths")
                    
                    ordering = Case(
                        When(stream=stuObj.currentStream, then=Value(1)),
                        When(stream__name="Any Stream", then=Value(2)),
                        default=Value(3),
                        output_field=IntegerField()
                    )

                    aptitude_career_conv = aptitude_career_conv.filter(stream_filter)
                    aptitude_career_voc = aptitude_career_voc.filter(stream_filter)
                    interest_career_conv = interest_career_conv.filter(stream_filter)
                    interest_career_voc = interest_career_voc.filter(stream_filter)
        
                    common_conv = aptitude_career_conv.distinct().intersection(interest_career_conv.distinct())
                    common_voc = aptitude_career_voc.distinct().intersection(interest_career_voc.distinct())

                    common_conv_ids = common_conv.values_list('id', flat=True)

                    aptitude_career_conv = aptitude_career_conv.annotate(
                        priority=ordering,
                        is_common=Case(
                            When(id__in=common_conv_ids, then=Value(1)),
                            default=Value(0),
                            output_field=IntegerField(),
                        )
                    ).order_by('-is_common', 'priority')

                    interest_career_conv = interest_career_conv.annotate(
                        priority=ordering,
                        is_common=Case(
                            When(id__in=common_conv_ids, then=Value(1)),
                            default=Value(0),
                            output_field=IntegerField(),
                        )
                    ).order_by('-is_common', 'priority')
        if not stream_exists:
            common_conv = aptitude_career_conv.distinct().intersection(interest_career_conv.distinct())
            common_voc = aptitude_career_voc.distinct().intersection(interest_career_voc.distinct())

            common_conv_ids = common_conv.values_list('id', flat=True)

            aptitude_career_conv = aptitude_career_conv.annotate(
                is_common=Case(
                    When(id__in=common_conv_ids, then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ).order_by('-is_common')

            interest_career_conv = interest_career_conv.annotate(
                is_common=Case(
                    When(id__in=common_conv_ids, then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ).order_by('-is_common')

        aptiCon = aptiReportContent.objects.all()
        intCon = interestReportContent.objects.all()
        db.connection.close()

        context = {
            'obj':aptiReportobj,
            'obj1':interestReportObj,
            'common_conv':common_conv,
            'aptitude_career_conv':aptitude_career_conv.distinct(),
            'interest_career_conv':interest_career_conv.distinct(),
            'vocatinal_career':aptitude_career_voc.distinct().union(interest_career_voc.distinct()),
            'stuObj':stuObj,
            'code':code,
            'sortApti':sortApti,
            'sortInt':sortInt,
            'aptiCon':aptiCon,
            'intCon':intCon,
            'flag2':flag2,
            'lang':lang,
            'report':report
        }
        if lang == "Hin":
            return render(request,'quiz/UI/CareerReportHindi.html',context)
        else:
            return render(request,'quiz/UI/report.html',context)
    db.connection.close()
    if lang == "Hin":
        return render(request,'quiz/UI/CareerReportHindi.html',{'flag':flag})
    else:
        return render(request,'quiz/UI/report.html',{'flag':flag})
