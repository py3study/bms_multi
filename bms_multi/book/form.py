from django import forms  # 必须导入模块
from django.forms import widgets
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from book.models import User  # 导入user表

class UserForm(forms.Form):  # 必须继承Form
    # 定义变量，专门给text类型的输入框添加class
    wid = widgets.TextInput(attrs={"class": "form-control"})
    # 定义字典，错误信息显示中文
    # 限制数据为字符串，最小长度4,最大长度12
    error_hints = {"required": "该字段不能为空", "invalid": "格式错误!"}
    name = forms.CharField(max_length=12, label="姓名", widget=wid, error_messages=error_hints)
    # 密码字段
    pwd = forms.CharField(label="密码", widget=widgets.PasswordInput(attrs={"class": "form-control"}),
                          error_messages=error_hints)

    r_pwd = forms.CharField(label="确认密码", widget=widgets.PasswordInput(attrs={"class": "form-control"}),
                            error_messages=error_hints)

    def clean_name(self):  # 校验name值
        val = self.cleaned_data.get("name")  # 获取输入的用户名
        if len(val) >= 4:  # 判断用户名长度
            if val.isdigit() is False:  # 判断用户名不是纯数字
                if not User.objects.filter(name=val).exists():  # 判断用户名是否存在
                    return val  # 返回正确的值
                else:
                    raise ValidationError("用户名已存在")
            else:
                raise ValidationError("用户名不能为纯数字")
        else:
            raise ValidationError("用户名长度不能小于4位")

    def clean_pwd(self):  # 校验pwd值
        val = self.cleaned_data.get("pwd")  # 获取输入的密码
        if len(val) >= 6:  # 判断密码长度
            if val.isdigit() is False:  # 判断密码不是纯数字
                return val  # 返回正确的值
            else:
                raise ValidationError("密码不能为纯数字")
        else:
            raise ValidationError("密码长度不能小于6位")


    def clean(self):  # 全局钩子
        pwd = self.cleaned_data.get("pwd")
        r_pwd = self.cleaned_data.get("r_pwd")
        if pwd and r_pwd and pwd != r_pwd:  # 判断2次密码不为空，并且2次密码不相等
            raise ValidationError("两次密码不一致")
        else:
            return self.cleaned_data  # 这句是固定写法，不能变动