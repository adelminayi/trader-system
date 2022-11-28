from django.contrib import admin

from userstrategies.models import UserStrategy, Symbol



class WidgetAdmin(admin.ModelAdmin):
    # def has_delete_permission(self, request, obj=None):
    #     return False

    # def has_change_permission(self, request, obj=None):
    #     print("method:",request.method)
    #     print("header:",request.headers)
    #     print("body:",request.body)
    #     return False

    pass

admin.site.register(UserStrategy, WidgetAdmin)
admin.site.register(Symbol)
