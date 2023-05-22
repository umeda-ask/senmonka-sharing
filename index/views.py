from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.views.generic import TemplateView #テンプレートタグ
from .forms import AccountForm, AddAccountForm #ユーザーアカウントフォーム
from .forms import SodanForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# ログイン・ログアウト処理に利用
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db import connection, transaction
from django.core.mail import send_mail
import datetime
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import sqlite3
import datetime
import urllib.parse
import cgi
from django.core.mail import send_mail
import datetime

from . import views_const

def index(request):
    return render(request, 'index/login.html')

#ログイン
def login_(request):
    # POST
    if request.method == 'POST':
        # フォーム入力のユーザーID・パスワード取得
        ID = request.POST.get('username')
        Pass = request.POST.get('password')

        print(ID, Pass)
        # Djangoの認証機能
        user = authenticate(request, username=ID, password=Pass)
        print(user)

        # ユーザー認証
        if user:
            #ユーザーアクティベート判定
            if user.is_active:
                # ログイン
                login(request,user)
                # ホームページ遷移
                return HttpResponseRedirect(reverse('home'))
            else:
                # アカウント利用不可
                return HttpResponse("アカウントが有効ではありません")
        # ユーザー認証失敗
        else:
#            return HttpResponse("ログインIDまたはパスワードが間違っています")
            return HttpResponseRedirect(reverse('login') + '?='+ 'loginfault')

    # GET
    else:
        return render(request, 'index/login.html')


#ログアウト
@login_required
def Logout(request):
    logout(request)
    # ログイン画面遷移
    return HttpResponseRedirect(reverse('Login'))


#ホーム
@login_required
def home(request):

    user_name = request.user

    #SQL接続
    conn = sqlite3.connect(views_const.dbpath)
    c = conn.cursor()

    #会社名取得
    user_name = request.user
    c.execute("select company_name from auth_user where username = '%s'" % user_name)
    company_name = str(c.fetchone())[2:][:-3]

    params = {
        'company_name' : company_name,
    }

    #決算月取得
    c.execute("select closing_month from auth_user where username = '%s'" % user_name)
    closing_month = c.fetchone()

    #TODOデータ取得
    c.execute("select month,year,title,id from t_law_revision where year = '2023' order by month")
    todo_data = c.fetchall()
    print(todo_data)

    today_data = datetime.date.today()
    params = {
        'company_name' : company_name,
        'todo_data' : todo_data,
        'today_data_year' : today_data.year,
        'today_data_month' : today_data.month

    }
    return render(request, "index/home.html",params)

class  accountRegistration(TemplateView):

    def __init__(self):
        self.params = {
        "AccountCreate":False,
        "account_form": AccountForm(),
        "add_account_form":AddAccountForm(),
        }

    # Get処理
    def get(self,request):
        self.params["account_form"] = AccountForm()
        self.params["add_account_form"] = AddAccountForm()
        self.params["AccountCreate"] = False
        return render(request,"index/register.html",context=self.params)

    # Post処理
    def post(self,request):
        self.params["account_form"] = AccountForm(data=request.POST)
        self.params["add_account_form"] = AddAccountForm(data=request.POST)

        # フォーム入力の有効検証
        if self.params["account_form"].is_valid() and self.params["add_account_form"].is_valid():
            # アカウント情報をDB保存
            account = self.params["account_form"].save()
            # パスワードをハッシュ化
            account.set_password(account.password)
            # ハッシュ化パスワード更新
            account.save()

            # 下記追加情報
            # 下記操作のため、コミットなし
            add_account = self.params["add_account_form"].save(commit=False)
            # AccountForm & AddAccountForm 1vs1 紐付け
            add_account.user = account

            # 画像アップロード有無検証
            if 'account_image' in request.FILES:
                add_account.account_image = request.FILES['account_image']

            # モデル保存
            add_account.save()

            # アカウント作成情報更新
            self.params["AccountCreate"] = True

        else:
            # フォームが有効でない場合
            print(self.params["account_form"].errors)

        return render(request,"index/register.html",context=self.params)

#todoリスト
def todolist_(request):

    #SQL接続
    conn = sqlite3.connect(views_const.dbpath)
    c = conn.cursor()

    #決算月取得
    user_name = request.user
    c.execute("select closing_month from auth_user where username = '%s'" % user_name)
    closing_month = str(c.fetchone())[1:][:-2]

    #会社名取得
    user_name = request.user
    c.execute("select company_name from auth_user where username = '%s'" % user_name)
    company_name = str(c.fetchone())[2:][:-3]

    params = {
        'company_name' : company_name,
    }

    #月取得
    month = request.GET.get("month")
    today_data = datetime.date.today()
    year = today_data.year

    #TODOデータ取得
    c.execute("select month,date,t_todo.title,t_todo.id from t_schedule INNER JOIN t_todo ON t_schedule.todo_id = t_todo.id where closing_month  = '%s' and month = '%s' order by t_schedule.date" % (closing_month, month))
    todo_data = c.fetchall()

    today_data = datetime.date.today()

    params = {
        'company_name' : company_name,
        'closing_month' : closing_month,
        'todo_data' : todo_data,
        'year' : year,
        'month' : month,
    }
    return render(request, "index/todolist.html", params)


#検索ホーム
def search_(request):

    #SQL接続
    conn = sqlite3.connect(views_const.dbpath)
    c = conn.cursor()

    #会社名取得
    user_name = request.user
    c.execute("select company_name from auth_user where username = '%s'" % user_name)
    company_name = str(c.fetchone())[2:][:-3]

    category_data = views_const.part_category_number_1

    #category取得
    category = request.GET.get("category")

    part_category_flg = 0

    if category:
        part_category_flg = 1
        
    if category == "1001":
      category_data = views_const.part_category_number_1
    elif category == "1002":
      category_data = views_const.part_category_number_2
    elif category == "1003":
      category_data = views_const.part_category_number_3
    else:
      category_data = views_const.part_category_number_4

    params = {
        'company_name' : company_name,
        'category_data' : category_data,
        'part_category_flg' : part_category_flg,
    }

    return render(request, "index/search.html", params)

#検索キーワード
def search_keyword_(request):

    #SQL接続
    conn = sqlite3.connect(views_const.dbpath)
    c = conn.cursor()

    #会社名取得
    user_name = request.user
    c.execute("select company_name from auth_user where username = '%s'" % user_name)
    company_name = str(c.fetchone())[2:][:-3]

    params = {
        'company_name' : company_name,
    }

    #keyword取得
    keyword = request.GET.get("keyword")
    category = str(request.GET.get("category"))

    if keyword:
      #事例データ取得
      sql1 = "select title,soudan_case,id from t_case where title like '%"
      sql2 = "%' or soudan_case like '%"
      sql3 = "%'"
      sql = sql1+keyword+sql2+keyword+sql3
    else:
      sql1 = "select title,soudan_case,id from t_case where category_id = '"
      sql2 = "'"
      sql = sql1+category+sql2
      
    c.execute(sql)
    soudan_case = c.fetchall()

    p = Paginator(soudan_case, 5)
    page = request.GET.get('page')
    print('toretenai?')
    print(page)

    try:
        pages = p.page(page)
        print('正常処理')
        print(page)
        print(pages)
    except PageNotAnInteger:
        print('PageNotInteger')
        pages = p.page(1)
    except EmptyPage:
        print('EmptyPage')
        pages = p.page(1)

    params = {
        'keyword' : keyword,
        'category' : category,
        'pages' : pages,
        'company_name' : company_name,
    }

    return render(request, "index/search_keyword.html", params)

#事例詳細
def case_detail_(request):

    #SQL接続
    conn = sqlite3.connect(views_const.dbpath)
    c = conn.cursor()

    #会社名取得
    user_name = request.user
    c.execute("select company_name from auth_user where username = '%s'" % user_name)
    company_name = str(c.fetchone())[2:][:-3]

    #ID取得
    caseid = request.GET.get("caseid")

    #事例データ取得
    sql1 = "select title,soudan_case,id from t_case where id = '"
    sql2 = "'"
    sql = sql1+caseid+sql2
    c.execute(sql)
    soudan_case = c.fetchall()

    case_data = str(soudan_case[0])
    case_data = case_data[:-1]
    case_data = case_data[1:]
    case_data =  case_data.split(',')
    title = case_data[0][1:]
    title = title[:-1]
    case = case_data[1][2:]
    case = case[:-1]
    id = case_data[2][2:]
    id = id[:-1]

    case = case.replace('<br>','\n')
    print(case)

    params = {
        'title' : title,
        'case' : case,
        'company_name' : company_name,
    }

    return render(request, "index/case_detail.html", params)

#問い合わせ
def contact_(request):

    #SQL接続
    conn = sqlite3.connect(views_const.dbpath)
    c = conn.cursor()

 #会社名取得
    user_name = request.user
    c.execute("select company_name from auth_user where username = '%s'" % user_name)
    company_name = str(c.fetchone())[2:][:-3]

    params = {
        'company_name' : company_name,
    }

    return render(request, "index/contact.html", params)

#問い合わせ確認
def contactre_(request):

    #SQL接続
    conn = sqlite3.connect(views_const.dbpath)
    c = conn.cursor()

     #会社名取得
    user_name = request.user
    c.execute("select company_name from auth_user where username = '%s'" % user_name)
    company_name = str(c.fetchone())[2:][:-3]

    params = {
        'companyname' : request.POST['companyname'],
        'customername' : request.POST['customername'],
        'phone' : request.POST['phone'],
        'mail' : request.POST['mail'],
        'genre' : request.POST['genre'],
        'consultation' : request.POST['consultation'],
        'company_name' : company_name,
        }
    return render(request, "index/contact_conf.html", params)

#問い合わせ確認
def contact_conf_(request):

    #SQL接続
    conn = sqlite3.connect(views_const.dbpath)
    c = conn.cursor()

#会社名取得
    user_name = request.user
    c.execute("select company_name from auth_user where username = '%s'" % user_name)
    company_name = str(c.fetchone())[2:][:-3]

    params = {
        'companyname' : request.POST.get('companyname'),
        'customername' : request.POST.get('customername'),
        'phone' : request.POST.get('phone'),
        'mail' : request.POST.get('mail'),
        'genre' : request.POST.get('genre'),
        'consultation' : request.POST.get('consultation'),
        'company_name' : company_name,
    }

    return render(request, "index/contact_conf.html", params)


def contact_comp_(request):

    #SQL接続
    conn = sqlite3.connect(views_const.dbpath)
    c = conn.cursor()

    #日時の取得
    createdate = datetime.datetime.now()

     #会社名取得
    user_name = request.user
    c.execute("select company_name from auth_user where username = '%s'" % user_name)
    company_name = str(c.fetchone())[2:][:-3]

    params = {
        'companyname' : request.POST.get('companyname'),
        'customername' : request.POST.get('customername'),
        'phone' : request.POST.get('phone'),
        'mail' : request.POST.get('mail'),
        'genre' : request.POST.get('genre'),
        'consultation' : request.POST.get('consultation'),
        'company_name' : company_name,
    }
    print(request.POST.get('consultation'))
    print(request.POST.get('customername'))
    print(request.POST.get('genre'))
    print(request.POST.get('mail'))
    print(createdate.isoformat())

    #DBへのデータ登録

    c.execute("INSERT INTO contact (companyname, customername, phone, mail, genre, consultation, createdate) VALUES ('%s','%s','%s','%s','%s','%s','%s')" % (request.POST.get('companyname'), request.POST.get('customername'), request.POST.get('phone'), request.POST.get('mail'), request.POST.get('genre'), request.POST.get('consultation'), createdate));

    conn.commit()

    conn.close()
    context={"companyname": request.POST.get('companyname'), "customername" : request.POST.get('customername'), "phone" : request.POST.get('phone'), "mail" : request.POST.get('mail'), "genre" : request.POST.get('genre'), "consultation" : request.POST.get('consultation')}
    # HTMLファイルを読み込む
    html_content = render_to_string("contactcomp_mail.html",context)
    # HTMLタグを取り除く
    text_content = strip_tags(html_content)


    #メール送信
    send_mail(
      subject="お問い合わせありがとうございます。",
      message=text_content,
      from_email="from@example.com",
      recipient_list=["ri.terui.ask@gmail.com"],
      html_message=html_content,
      )

    print(request.POST.get('companyname'))
    print(request.POST.get('customername'))
    print(request.POST.get('genre'))
    print(request.POST.get('mail'))
    print(createdate.isoformat())

    return render(request, "index/contact_comp.html", params)

#月選択
def select_month_(request):

    #SQL接続
    conn = sqlite3.connect(views_const.dbpath)
    c = conn.cursor()

    #会社名取得
    user_name = request.user
    c.execute("select company_name from auth_user where username = '%s'" % user_name)
    company_name = str(c.fetchone())[2:][:-3]

    #月取得
    today_data = datetime.date.today()
    year = today_data.year

    params = {
        'company_name' : company_name,
        'year' : year,
    }
    return render(request, "index/select_month.html", params)

#ジャンル選択
def case_genre_(request):

    #SQL接続
    conn = sqlite3.connect(views_const.dbpath)
    c = conn.cursor()

    return render(request, "index/case_genre.html")

#todo詳細
def todo_detail_(request):

    #SQL接続
    conn = sqlite3.connect(views_const.dbpath)
    c = conn.cursor()

    #会社名取得
    user_name = request.user
    c.execute("select company_name from auth_user where username = '%s'" % user_name)
    company_name = str(c.fetchone())[2:][:-3]

    params = {
        'company_name' : company_name,
    }

    #ID取得
    id = request.GET.get("id")

    #todoデータ取得
    sql1 = "select title,law_revision,year,month from t_law_revision where id = '"
    sql2 = "'"
    sql = sql1+id+sql2
    c.execute(sql)
    todo_data = c.fetchall()

    todo_data = str(todo_data[0])
    todo_data = todo_data[:-1]
    todo_data = todo_data[1:]
    todo_data =  todo_data.split(',')
    title = todo_data[0][1:]
    title = title[:-1]
    revision_data = todo_data[1][2:]
    revision_data = revision_data[:-1]
    year = todo_data[2][1:]
    month = todo_data[3][1:]

    params = {
        'title' : title,
        'revision_data' : revision_data,
        'year' : year,
        'company_name' : company_name,
    }

    print(params)

    return render(request, "index/todo_detail.html", params)
