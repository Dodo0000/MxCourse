# coding:utf-8
from django.shortcuts import render
from django.views.generic import View
from .models import CourseOrg,CityDict
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


class OrgView(View):
    """
    课程机构列表
    """
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        all_citys = CityDict.objects.all()
        org_nums = all_orgs.count()

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_orgs, 1, request=request)
        orgs = p.page(page)

        return render(request, "org-list.html",
                      {"all_orgs": orgs,
                       "all_citys": all_citys,
                       "org_nums": org_nums})