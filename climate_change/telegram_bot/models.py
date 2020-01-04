from django.db import models
from django.contrib.auth import get_user_model
import hashlib
import os

def unique_md5_generator(models,para_name,length):
    key = hashlib.md5(os.urandom(length)).hexdigest()
    while models.objects.filter(**{para_name:key}).exists():
        key = hashlib.md5(os.urandom(length)).hexdigest()
    return key

def md5_func():
    return hashlib.md5(os.urandom(10)).hexdigest()

User = get_user_model()
# Create your models here.

class Knowledge(models.Model):
    title = models.CharField(max_length=30,null=False,blank=False)
    description = models.TextField(blank=False,null=False)
    score = models.IntegerField(default=0,blank=False,null=False)
    modify_user = models.ForeignKey(User, on_delete=models.CASCADE)
    knowledge_code = models.CharField(max_length=32,default=md5_func,blank=False,null=False,unique=True)
    add_time = models.DateTimeField(auto_now_add=True)

    def so_so_to_like(self,chat_id):
        self.score += 1
        self.save(update_fields=['score'])
        
    def so_so_to_unlike(self,chat_id):
        self.score -= 1
        self.save(update_fields=['score'])

    def so_so(self):
        pass

    def like_to_unlike(self,chat_id):
        self.score -= 2
        self.save(update_fields=['score'])

    def unlike_to_like(self,chat_id):
        self.score += 2
        self.save(update_fields=['score'])

    def has_seen(self, chat_id):
        chat,_ = TelegramChat.objects.get_or_create(chat_id=chat_id)
        chat.knowledge_pack.add(self)
        chat.save()

    def save(self,*args,**kwargs):
        code = self.knowledge_code
        while Knowledge.objects.filter(knowledge_code=self.knowledge_code).exists():
            code = md5_func()
        self.knowledge_code = code
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.title)

class KnowledgeStatus(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    like_or_unlike = models.CharField(max_length=10,blank=True,null=True,default="so_so")
    knowledge = models.ForeignKey(Knowledge,on_delete=models.CASCADE)

class Policy(models.Model):
    title = models.CharField(max_length=30,null=False,blank=False)
    description = models.TextField(blank=False,null=False)
    url = models.CharField(max_length=300,blank=True,null=True)
    score = models.IntegerField(default=0,blank=False,null=False)
    modify_user = models.ForeignKey(User, on_delete=models.CASCADE)
    policy_code = models.CharField(max_length=32,default=md5_func,blank=False,null=False,unique=True)
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)

class PolicyStatus(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    like_or_unlike = models.CharField(max_length=10,blank=True,null=True,default="so_so")
    policy = models.ForeignKey(Policy,on_delete=models.CASCADE)

class TelegramChat(models.Model):
    chat_id = models.CharField(max_length=50,null=False,blank=False,unique=True)
    knowledge_pack = models.ManyToManyField(KnowledgeStatus,null=True,blank=True)
    policy_pack = models.ManyToManyField(PolicyStatus,null=True,blank=True)

    def __str__(self):
        return str(self.chat_id)