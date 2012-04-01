# To change this template, choose Tools | Templates
# and open the template in the editor.


from django.contrib import admin
from mj_ranking.ranking.models import *


admin.site.register(Users)
admin.site.register(Leagues)
admin.site.register(Round,RoundAdmin)
admin.site.register(Group,GroupAdmin)
admin.site.register(Match,MatchAdmin)
admin.site.register(Detail,DetailAdmin)

