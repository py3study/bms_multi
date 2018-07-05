from django.db import models

# Create your models here.
class Book(models.Model):
    title=models.CharField(max_length=32,unique=True)
    price=models.DecimalField(max_digits=8,decimal_places=2,null=True)
    pub_date=models.DateField()
    # 与Publish建立一对多的关系,外键字段建立在多的一方
    publish=models.ForeignKey(to="Publish",to_field="id",on_delete=models.CASCADE)
    # 与Author表建立多对多的关系,ManyToManyField可以建在两个模型中的任意一个，自动创建关系表book_authors
    authors=models.ManyToManyField(to="Author")

class Publish(models.Model):
    name=models.CharField(max_length=32)
    email=models.CharField(max_length=32)
    addr=models.CharField(max_length=32)


class Author(models.Model):
    name=models.CharField(max_length=32)
    age=models.IntegerField()
    # 与AuthorDetail建立一对一的关系
    # ad=models.ForeignKey(to="AuthorDetail",to_field="id",on_delete=models.CASCADE,unique=True)
    ad=models.OneToOneField(to="AuthorDetail",to_field="id",on_delete=models.CASCADE,)


class AuthorDetail(models.Model):
    gf=models.CharField(max_length=32)
    tel=models.CharField(max_length=32)


class User(models.Model):
    name = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
    last_time = models.DateTimeField()