from django.contrib import admin

from .models import Bowler, Batsman, UserSelect, Team

admin.site.register(Bowler)
admin.site.register(Batsman)
admin.site.register(UserSelect)
admin.site.register(Team)
