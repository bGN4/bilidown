from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from ...models import BiliComment
from common.encoders import JSONEncoder
from common.utils import isStringLike
import json
import os

class Command(BaseCommand):
    help = 'Manage BiliComment Table'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('args', metavar='table', nargs='*', type=str, help='')
        # Named (optional) arguments
        parser.add_argument('--mark-expired', action='store_true', default=False, help='mark expired status')
        parser.add_argument('--output', type=str, help='just list expired rows')

    def handle(self, *tables, **options):
        now = timezone._time.strftime('%Y-%m-%d %H:%M:%S')
        if options.get('mark_expired'):
            self.stdout.write('%-50s'%('Mark expired rows ...'), ending='')
            num = BiliComment.objects.filter(status="on",expire__lt=now).update(status="expire")
            self.stdout.write('%-50s'%('\rMark %s rows as expired.'%num))
        output = options.get('output', '')
        comments = BiliComment.objects.filter(status="on",ntime__lt=now).values('id','cid','aid','pid','ltime')
        total = comments.count()
        if not isStringLike(output):
            pass
        elif os.path.isdir(output):
            for (i,comment) in enumerate(comments,1):
                path = os.path.join(output, 'av{aid}#{pid}.txt'.format(**comment))
                if os.path.isfile(path):
                    self.stdout.write( 'Skip {}/{} to {}'.format(i,total,path) )
                else:
                    self.stdout.write( 'Dump {}/{} to {}'.format(i,total,path) )
                    with open(path, 'w') as fp:
                        fp.write( json.dumps(comment, ensure_ascii=False, cls=JSONEncoder, indent=1, separators=(',', ': ')) )
        else:
            text = json.dumps(list(comments), ensure_ascii=False, cls=JSONEncoder, indent=1, separators=(',', ': '))
            if output in ('-', ''):
                self.stdout.write( text )
            else:
                self.stdout.write( 'Dump {} comments to {}'.format(total,output) )
                with open(output, 'w') as fp:
                    fp.write( text )

