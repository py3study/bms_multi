from django.shortcuts import render, HttpResponse,redirect
# 导入5个表模型
from book.models import Book, Publish, Author, AuthorDetail,User
import json
import datetime
from book.form import UserForm
# Create your views here.

def zhuce(request):
    if request.method == "POST":
        # 将post数据传给UserForm
        form = UserForm(request.POST)
        # print(request.POST)
        # if form.is_valid():  # 验证数据
        #     print("###success###")
        #     print(form.cleaned_data)  # 所有干净的字段以及对应的值
        #     # ErrorDict : {"校验错误的字段":["错误信息",]}
        #     print(form.errors)
        #     print(type(form.errors))  # 打印
        #
        #     name = request.POST.get("name")
        #     pwd = request.POST.get("pwd")
        #     last_time = datetime.datetime.now()
        #     ret = User.objects.create(name=name,pwd=pwd,last_time=last_time)
        #     if ret:
        #         return HttpResponse("添加成功")
        #     else:
        #         return HttpResponse("添加失败")
        # else:
        #     print("###fail###")
        #     # print(form.cleaned_data)
        #     print(form.errors)
        #     # # 获取email错误信息,返回一个错误列表,可以切片
        #     # print(form.errors.get("email"))
        #     # # 获取第一个错误信息
        #     # print(form.errors.get("email")[0])
        #     g_error = form.errors.get("__all__")  # 接收全局钩子错误信息
        #     if g_error:  # 判断有错误信息的情况下
        #         g_error = g_error[0]  # 取第一个错误信息
        #
        #     # 将form和g_error变量传给adduser.html
        #     return render(request, "zhuce.html", {"form": form, "g_error": g_error})

    else:  # 默认是get请求(地址栏输入访问时)
        form = UserForm()  # 没有表单数据的form
    return render(request, "zhuce.html",{"form": form})

def zhuce_ajax(request):
    if request.method == "POST": # 判断POST请求
        print(request.POST)
        form = UserForm(request.POST)  #
        result = {"state": False,"name":"","pwd":"","r_pwd":""}
        if form.is_valid():
            name = request.POST.get("name")
            pwd = request.POST.get("pwd")
            last_time = datetime.datetime.now()
            ret = User.objects.create(name=name, pwd=pwd, last_time=last_time)
            if ret:
                result["state"] = True
            return HttpResponse(json.dumps(result,ensure_ascii=False))
        else:
            print(form.errors)
            if form.errors:  # 判断有错误信息的情况下
                if form.errors.get("name"):
                    result["name"] = form.errors.get("name")[0]
                if form.errors.get("pwd"):
                    result["pwd"] = form.errors.get("pwd")[0]
                if form.errors.get("r_pwd"):
                    result["r_pwd"] = form.errors.get("r_pwd")[0]

                g_error = form.errors.get("__all__")  # 接收全局钩子错误信息
                if g_error:  # 判断有错误信息的情况下
                    g_error = g_error[0]  # 取第一个错误信息
                    result["r_pwd"] = g_error

                return HttpResponse(json.dumps(result,ensure_ascii=False))


#装饰器，用来判断用户是否登录
def required_login(func):
    def inner(*args,**kwargs):
        request = args[0]  # 响应请求
        if request.session.get("is_login"): #判断登录状态,如果为True
            return func(*args,**kwargs)  # 执行视图函数
        else:
            if request.is_ajax():  # 此时未登录，判断ajax请求
                #返回一个json信息，并指定url
                return HttpResponse(json.dumps({"state":False,'url':'/login/'}))

            return render(request,"no_login.html")
            #return redirect("/login/")  # 302重定向

    return inner

def index(request):
    book_list = Book.objects.all()  # 查询表的所有记录
    print(book_list)
    return render(request, "index.html", {"book_list": book_list})
    # return render(request,"index.html")

def login(request):
    if request.method == "POST":
        name = request.POST.get("user")
        pwd = request.POST.get("pwd")
        user_list = User.objects.filter(name=name,pwd=pwd)
        response = {"state":False}
        if user_list:
            user_obj = user_list.first()
            # ret = redirect("/books/")
            request.session['is_login'] = True
            request.session['user'] = name
            request.session['last_time'] = str(user_obj.last_time)
            user_obj.last_time = datetime.datetime.now()
            user_obj.save()

            response["state"] = True

        return HttpResponse(json.dumps(response))
            
    return render(request,"login.html")

def logout(request):
    ret = redirect("/login/")
    request.session.flush()
    return ret

def reg(request):
    if request.method == "POST":
        user = request.POST.get("user")
        pwd = request.POST.get("pwd1")
        the_user = User.objects.filter(name=user).exists()

        if the_user:
            hint = '<script>alert("用户名已存在！不能重复注册");window.location.href="/reg/"</script>'
            return HttpResponse(hint)  # js跳转到添加页面
        else:
            last_time = datetime.datetime.now()
            result = User.objects.create(name=user, pwd=pwd, last_time=last_time)
            hint = '<script>alert("注册成功");window.location.href="/login/"</script>'
            return HttpResponse(hint)  # js跳转到首页


    return render(request,"reg.html")



@required_login
def books(request):  # 首页
    ret = Book.objects.all().exists()  # 判断表是否有记录
    if ret:
        book_list = Book.objects.all()  # 查询表的所有记录
        return render(request, "books.html", {"book_list": book_list})

    else:
        hint = '<script>alert("没有书籍，请添加书籍");window.location.href="/books/add_book"</script>'
        return HttpResponse(hint)  # js跳转到添加页面

@required_login
def see_publish(request):  # 查看出版社
    ret = Publish.objects.all().exists()  # 判断表是否有记录
    if ret:
        publish_list = Publish.objects.all()  # 查询表的所有记录
        return render(request, "see_publish.html", {"publish_list": publish_list})

    else:
        hint = '<script>alert("没有出版社，请添加出版社");window.location.href="/books/add_publish"</script>'
        return HttpResponse(hint)  # js跳转到添加页面

@required_login
def see_author(request):  # 查看作者
    ret = Author.objects.all().exists()  # 判断表是否有记录
    if ret:
        author_list = Author.objects.all()  # 查询表的所有记录
        return render(request, "see_author.html", {"author_list": author_list})

    else:
        hint = '<script>alert("没有作者，请添加作者");window.location.href="/books/add_author"</script>'
        return HttpResponse(hint)  # js跳转到添加页面

@required_login
def book_exists(request):  # 添加书籍
    if request.method == "POST":
        # print(request.POST)
        title = request.POST.get("title")
        the_book = Book.objects.filter(title=title).exists()
        result = {"state":False,"msg":""}
        if the_book:
            result["msg"] = "书籍已存在！不能重复添加"
            return HttpResponse(json.dumps(result, ensure_ascii=False))
        else:
            result["state"] = True
            return HttpResponse(json.dumps(result, ensure_ascii=False))

@required_login
def add_book(request):  # 添加书籍
    if request.method == "POST":
        title = request.POST.get("title")
        price = request.POST.get("price")
        pub_date = request.POST.get("pub_date")
        publish_id = request.POST.get("publish_id")
        author_id = request.POST.get("author_id")  # 返回json

        print(title, price, pub_date, publish_id,author_id)
        author_arr = json.loads(author_id);
        print(author_arr,type(author_arr['author_id']))

        result = {"state": False, "msg": ""}

        the_book = Book.objects.filter(title=title).exists()
        if the_book:
            result["msg"] = "书籍已存在！不能重复添加"
            return HttpResponse(json.dumps(result, ensure_ascii=False))
        else:
            # 先插入书籍
            book = Book.objects.create(title=title, price=price, pub_date=pub_date, publish_id=publish_id)
            # 再插入作者
            book.authors.add(*author_arr['author_id'])

            # hint = '<script>alert("添加成功");window.location.href="/books/"</script>'
            # return HttpResponse(hint)  # js跳转到首页
            if book.id:
                result["state"] = True
            else:
                result["msg"] = "插入记录失败!"

        return HttpResponse(json.dumps(result, ensure_ascii=False))

    # 读取所有出版社，过滤出id和name
    publish_list = Publish.objects.all().values("id", "name")
    # 读取所有作者，过滤出id和name
    author_list = Author.objects.all().values("id", "name")

    return render(request, "add_book.html", {"publish_list": publish_list, "author_list": author_list})

@required_login
def add_publish(request):  # 添加出版社
    if request.method == "POST":
        # print(request.POST)
        name = request.POST.get("name")
        the_publish = Publish.objects.filter(name=name).exists()

        if the_publish:
            hint = '<script>alert("出版社已存在！不能重复添加");window.location.href="/books/add_publish/"</script>'
            return HttpResponse(hint)  # js跳转到添加页面
        else:
            email = request.POST.get("email")
            addr = request.POST.get("addr")
            print(name, email, addr)

            # 插入出版社
            publish = Publish.objects.create(name=name, email=email, addr=addr)

            if publish.id:  # 判断状态
                hint = '<script>alert("添加成功");window.location.href="/books/"</script>'
                return HttpResponse(hint)  # js跳转到首页
            else:
                hint = '<script>alert("添加失败");window.location.href="/books/"</script>'
                return HttpResponse(hint)  # js跳转到首页

    return render(request, "add_publish.html")

@required_login
def add_author(request):  # 添加作者
    if request.method == "POST":
        # print(request.POST)
        name = request.POST.get("name")
        age = request.POST.get("age")
        gf = request.POST.get("gf")
        tel = request.POST.get("tel")

        the_author = Author.objects.filter(name=name).exists()

        if the_author:
            hint = '<script>alert("作者已存在！不能重复添加");window.location.href="/books/add_author/"</script>'
            return HttpResponse(hint)  # js跳转到添加页面
        if not age.isdigit():
            hint = '<script>alert("年龄必须为数字！");window.location.href="/books/add_author/"</script>'
            return HttpResponse(hint)  # js跳转到添加页面
        if not tel.isdigit():
            hint = '<script>alert("手机号码必须为数字！");window.location.href="/books/add_author/"</script>'
            return HttpResponse(hint)  # js跳转到添加页面

        # 先添加作者详细信息
        author_gf = AuthorDetail.objects.create(gf=gf, tel=tel)
        # 再添加作者，因为它依赖AuthorDetail表
        author = Author.objects.create(name=name, age=age, ad=author_gf)

        if author.id:  # 判断状态
            hint = '<script>alert("添加成功");window.location.href="/books/"</script>'
            return HttpResponse(hint)  # js跳转到首页
        else:
            hint = '<script>alert("添加失败");window.location.href="/books/"</script>'
            return HttpResponse(hint)  # js跳转到首页

    return render(request, "add_author.html")

@required_login
def delete_book(request, id):  # 删除书籍
    #先删除关系表中的作者
    book_ad = Book.objects.filter(id=id).first()  # 获取这本书
    book_ad.authors.clear()  # 清理这本书的作者关系

    #再删除书籍
    ret = Book.objects.filter(id=id).delete()  # 返回元组
    print(ret)

    response = {"state":False}

    if ret[0]:  # 取值为1的情况下
        response['state'] = True
    else:  # 取值为0的情况下
        response['state'] = False
    return HttpResponse(json.dumps(response))

@required_login
def delete_publish(request, id):  # 删除出版社
    # 删除出版社
    ret = Publish.objects.filter(id=id).delete()  # 返回元组
    print(ret)

    if ret[0]:  # 取值为1的情况下
        hint = '<script>alert("删除成功");window.location.href="/books/manage_publish/"</script>'
        return HttpResponse(hint)
    else:  # 取值为0的情况下
        hint = '<script>alert("删除失败");window.location.href="/books/manage_publish/"</script>'
        return HttpResponse(hint)

@required_login
def delete_author(request, id):  # 删除作者
    # 获取作者信息
    author = Author.objects.filter(id=id).first()
    # # 反向查询出作者出版过的所有书籍
    # ret = author.book_set.all()
    #
    # for i in ret:  # 循环queryset对象
    #     i.authors.clear()  # 依次清理所有关系对象
    #
    # # 作者表先删除作者
    # ret = author.delete()  # 返回元组

    # 再删除作者详细信息
    # 删除这张表的记录，author和book_author表的相关记录，会自动删除
    ret = AuthorDetail.objects.filter(id=author.ad_id).delete()

    print(ret)

    if ret[0]:  # 取值为1的情况下
        hint = '<script>alert("删除成功");window.location.href="/books/manage_author/"</script>'
        return HttpResponse(hint)
    else:  # 取值为0的情况下
        hint = '<script>alert("删除失败");window.location.href="/books/manage_author/"</script>'
        return HttpResponse(hint)

@required_login
def manage_book(request):  # 管理页面
    ret = Book.objects.all().exists()
    if ret:
        book_list = Book.objects.all()
        # 加载管理页面
        return render(request, "manage_book.html", {"book_list": book_list})
    else:
        hint = '<script>alert("没有书籍，请添加书籍");window.location.href="/books/add_book/"</script>'
        return HttpResponse(hint)

@required_login
def manage_publish(request):  # 管理页面
    ret = Publish.objects.all().exists()
    if ret:
        publish_list = Publish.objects.all()
        # 加载管理页面
        return render(request, "manage_publish.html", {"publish_list": publish_list})
    else:
        hint = '<script>alert("没有出版社，请添加出版社");window.location.href="/books/add_publish/"</script>'
        return HttpResponse(hint)

@required_login
def manage_author(request):  # 管理页面
    ret = Publish.objects.all().exists()
    if ret:
        author_list = Author.objects.all()
        # 加载管理页面
        return render(request, "manage_author.html", {"author_list": author_list})
    else:
        hint = '<script>alert("没有出版社，请添加出版社");window.location.href="/books/add_publish/"</script>'
        return HttpResponse(hint)

@required_login
def modify_book(request, id):  # 修改
    if request.method == "POST":
        title = request.POST.get("title")
        price = request.POST.get("price")
        pub_date = request.POST.get("pub_date")
        publish_id = request.POST.get("publish_id")
        author_id = request.POST.getlist("author_id")  # 返回列表
        print(author_id)

        # 先修改书籍
        ret = Book.objects.filter(id=id).update(title=title, price=price, pub_date=pub_date, publish_id=publish_id)
        # 获取当前书籍
        book_ad = Book.objects.filter(id=id).first()
        book_ad.authors.set(author_id)  # 先清空再设置

        if ret:  # 判断返回值为1
            hint = '<script>alert("修改成功");window.location.href="/books/manage_book/"</script>'
            return HttpResponse(hint)  # js跳转
        else:  # 返回为0
            hint = '<script>alert("修改失败");window.location.href="/books/manage_book/"</script>'
            return HttpResponse(hint)  # js跳转

    book = Book.objects.get(id=id)  # 默认获取id值
    # print(book)

    # 读取所有出版社，过滤出id和name
    publish_list = Publish.objects.all().values("id", "name")
    # 读取所有作者，过滤出id和name
    author_list = Author.objects.all().values("id", "name")
    the_author = []  # 当前书籍的作者
    for i in book.authors.all():
        the_author.append(i.name)  # 最加到列表中
    print(the_author)

    return render(request, "modify_book.html",
                  {"book": book, "publish_list": publish_list, "author_list": author_list, "the_author": the_author})

@required_login
def modify_publish(request, id):  # 修改出版社
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        addr = request.POST.get("addr")

        print(name, email, addr)

        # 修改
        ret = Publish.objects.filter(id=id).update(name=name, email=email, addr=addr)

        if ret:  # 判断返回值为1
            hint = '<script>alert("修改成功");window.location.href="/books/manage_publish/"</script>'
            return HttpResponse(hint)  # js跳转
        else:  # 返回为0
            hint = '<script>alert("修改失败");window.location.href="/books/manage_publish/"</script>'
            return HttpResponse(hint)  # js跳转

    publish = Publish.objects.get(id=id)  # 默认获取id值
    # print(book)

    return render(request, "modify_publish.html", {"publish": publish})

@required_login
def modify_author(request, id):  # 修改
    if request.method == "POST":
        name = request.POST.get("name")
        age = request.POST.get("age")
        gf = request.POST.get("gf")
        tel = request.POST.get("tel")

        print(name, age, gf, tel)

        # 获取作者
        the_author = Author.objects.filter(id=id).first()
        print(the_author.ad_id)
        # 先修改作者详细信息,注意，这里的过滤条件必须是id=author.ad_id，因为它是关联的
        AuthorDetail.objects.filter(id=the_author.ad_id).update(gf=gf, tel=tel)

        # 再修改作者，因为它依赖AuthorDetail表
        ret = Author.objects.filter(id=id).update(name=name, age=age)

        if ret:  # 判断返回值为1
            hint = '<script>alert("修改成功");window.location.href="/books/manage_author/"</script>'
            return HttpResponse(hint)  # js跳转
        else:  # 返回为0
            hint = '<script>alert("修改失败");window.location.href="/books/manage_author/"</script>'
            return HttpResponse(hint)  # js跳转

    author = Author.objects.get(id=id)  # 默认获取id值
    # print(book)

    return render(request, "modify_author.html", {"author": author})
