# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.db import transaction
from django.db import models
from django.contrib.auth.models import User
from common.utils import safe_cast

# Create your models here.


class BiliCommentManager(models.Manager):
    use_in_migrations = True

    def get_or_create_by_avid(self, aid, pid=1):
        now = timezone.now()
        expire = now + timezone.timedelta(seconds=12*60*60)
        comment = self.model(cid=0, aid=aid, pid=pid, status='on', count=0, expire=expire, ltime='1970-1-1', ntime=now)
        with transaction.atomic():
            comments = self.filter(aid=aid, pid=pid)[:1]
            if comments:
                comment = comments[0]
                comment.status = 'on'
                comment.expire = expire
                comment.ntime = now
                comment.save()
            else:
                comment.save()
        return comment

class BiliComment(models.Model):
    cid      = models.CharField(max_length=64)
    aid      = models.CharField(max_length=64)
    pid      = models.CharField(max_length=64)
    status   = models.CharField(max_length=64)
    count    = models.IntegerField(default=0)
    expire   = models.DateTimeField()
    ltime    = models.DateTimeField()
    ntime    = models.DateTimeField()
    atime    = models.DateTimeField(auto_now_add=True)
    objects  = BiliCommentManager()

    class Meta:
        verbose_name = _('BiliComment')
        verbose_name_plural = _('BiliComments')
        db_table = 'bili_comment'

    def __unicode__(self):
        return u'%s@av%s#%s'%(self.cid,self.aid,self.pid)


class BiliRecordManager(models.Manager):
    use_in_migrations = True

class BiliRecord(models.Model):
    url      = models.CharField(max_length=500)
    status   = models.CharField(max_length=64)
    comment  = models.ForeignKey(BiliComment)
    user     = models.ForeignKey(User)
    atime    = models.DateTimeField(auto_now_add=True)
    deleted  = models.IntegerField(default=0)
    objects  = BiliRecordManager()

    class Meta:
        verbose_name = _('BiliRecord')
        verbose_name_plural = _('BiliRecords')
        db_table = 'bili_records'

    def __unicode__(self):
        return u'%s'%self.pk

