import json
from django.contrib.auth.decorators import login_required
import requests
from django.core.paginator import Paginator
from django.db.models import Max, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .forms import PlanForm, CommentForm
from .models import Plan, Group, Category
from accountapp.models import UserLocation
from django.utils import timezone

######################## view ############################

# 메인 화면 (약속 리스트)
# url: /plan/
# 노출 조건: 참여한 약속만 노출되며, 현재 시점 기준으로 다가올 약속과 지나간 약속 크게 두가지로 분류해서 노출
# 정렬 조건: 다가올 약속은 빠른 날짜순, 지나간 약속은 늦은 날짜 순 정렬
# 검색 조건: 카테고리 필터 제공
class PlanList(ListView):
    model = Plan
    context_object_name = "plans"
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()

        search_query = self.request.GET.get('search-plan', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |  # title 필드에서 대소문자 구분 없이 일치하는 것을 찾거나,
                Q(memo__icontains=search_query)  # description 필드에서 대소문자 구분 없이 일치하는 것을 찾습니다.
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now_date = timezone.now().date()
        context['search'] = self.request.GET.get('search-plan', '')

        # 로그인 상태인 유저의 참여중 plan_id 리스트
        plan_ids = Group.objects.filter(user=self.request.user).values_list(
            "plan_id", flat=True
        )

        future_plans_list = list(
                self.object_list.filter(time__date__gte=now_date, id__in=plan_ids).order_by(
                    "time"
                )
            )
        past_plans_list = list(
                self.object_list.filter(time__date__lt=now_date, id__in=plan_ids).order_by(
                    "-time"
                )
            )

        # 카테고리 filtering
        context["categories"] = Category.objects.all()
        category_id = self.request.GET.get("category")

        if category_id:
            future_plans_list = [
                plan
                for plan in future_plans_list
                if plan.category.id == int(category_id)
            ]
            past_plans_list = [
                plan for plan in past_plans_list if plan.category.id == int(category_id)
            ]

        # 페이지네이션
        future_plans_paginator = Paginator(future_plans_list, self.paginate_by)
        past_plans_paginator = Paginator(past_plans_list, self.paginate_by)

        future_page_number = self.request.GET.get("future_page")
        past_page_number = self.request.GET.get("past_page")

        context["future_plans"] = future_plans_paginator.get_page(future_page_number)
        context["past_plans"] = past_plans_paginator.get_page(past_page_number)

        # 다가올 약속 d-day
        for plan in context["future_plans"]:
            plan.time_diff = now_date - plan.time.date()

        return context


# 상세 화면 (약속 상세)
# url: /plan/<uuid:pk>/
# 노출 항목: 약속 명, 약속 장소, 초대 코드, 방장, 참여자, 댓글
class PlanDetail(DetailView):
    model = Plan
    context_object_name = "plan"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 참여자 리스트
        plan_id = self.kwargs["pk"]
        context["group"] = Group.objects.filter(plan=plan_id)
        context["is_member"] = Group.objects.filter(
            plan=plan_id, user=self.request.user
        ).exists()

        # 댓글
        context["comment_form"] = CommentForm()
        return context


# 약속 생성
# url: /plan/create/
# 작성 항목: 카테고리, 제목, 주소 (주소지 입력 시, 위도 경도로 변환하여 db저장) , 시간, 메모, 비밀방 생성
@login_required()
def plan_create(request):
    if request.method == "POST":
        form = PlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.owner = request.user

            ## kakao map -> 주소지에서 위도 경도 추출해서 저장하기 ##
            url = "https://dapi.kakao.com/v2/local/search/address.json?query={address}".format(
                address=plan.address
            )
            headers = {"Authorization": "KakaoAK " + "33e22754a9930e9cb1e0ab6f691bd8d0"}
            response = json.loads(str(requests.get(url, headers=headers).text))
            geodata = (
                response.json()
                if isinstance(response, requests.models.Response)
                else response
            )
            # print(geodata)
            if geodata:
                plan.latitude = geodata["documents"][0]["y"]
                plan.longitude = geodata["documents"][0]["x"]

            plan.save()

            # 약속 생성자 group에 추가
            group_create(request, plan.id)
            return redirect("plan")

    else:
        form = PlanForm()
        return render(request, "plan/plan_form.html", {"form": form})


# 약속 수정
# url: /plan/<uuid:pk>/edit/
@login_required
def plan_edit(request, pk):
    plan = get_object_or_404(Plan, pk=pk)

    if request.user != plan.owner:
        return redirect("plan")

    if request.method == "POST":
        form = PlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            return redirect("plan")
    else:
        form = PlanForm(instance=plan)

    return render(request, "plan/plan_form.html", {"form": form})


# 약속 삭제
# url: /plan/<uuid:pk>/delete
@login_required
def plan_delete(request, pk):
    plan = get_object_or_404(Plan, pk=pk)
    if plan.owner == request.user:
        plan.delete()
    else:
        return redirect("plan")

    return redirect("plan")


# 그룹 생성
# url: /plan/<uuid:pk>/group/
# 생성 조건: Plan 생성 시 생성한 유저 추가, 약속 상세 페이지 내 참여하기 클릭
@login_required
def group_create(request, pk):
    plan = get_object_or_404(Plan, pk=pk)

    if not Group.objects.filter(plan=plan, user=request.user).exists():
        Group.objects.create(plan=plan, user=request.user)

    return redirect("plan")


# 그룹 삭제
# url: /plan/<uuid:pk>/group/delete
@login_required
def group_delete(request, pk):
    plan = get_object_or_404(Plan, pk=pk)

    if Group.objects.filter(plan=plan, user=request.user).exists():
        group = get_object_or_404(Group, plan=plan, user=request.user)
        group.delete()

    return redirect("plan")


# 참여자 위치
# url: /plan/<uuid:pk>/map
@login_required
def plan_map(request, pk):
    plan = get_object_or_404(Plan, pk=pk)
    group = Group.objects.filter(plan=plan)

    # group에 속한 user들의 id 리스트 생성
    user_ids = group.values_list("user", flat=True)

    # User Location table에서 유저별 최근 위치 정보 가져오기
    latest_user_locations = (
        UserLocation.objects.filter(user__in=user_ids)
        .values("user")
        .annotate(latest_created_at=Max("created_at"))
        .values_list("latest_created_at", flat=True)
    )

    # 그 결과를 이용하여 해당하는 UserLocation 객체들을 가져옵니다.
    user_locations = UserLocation.objects.filter(created_at__in=latest_user_locations)
    user_locations_json = json.dumps(
        [
            {
                "id": location.id,
                "latitude": location.latitude,
                "longitude": location.longitude,
                "user_id": location.user.id,
                "username": location.user.username,
            }
            for location in user_locations
        ]
    )

    ## 경로 계산
    url = "https://apis.openapi.sk.com/transit/routes/sub"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "appKey": "e8wHh2tya84M88aReEpXCa5XTQf3xgo01aZG39k5",
    }
    user_result = []
    for item in user_locations:
        user_info = {}
        if item.longitude == plan.longitude and item.latitude == plan.latitude:
            user_info["user"] = item.user.username
            user_info["distance"] = 0
            user_info["time"] = 0
            user_result.append(user_info)

        else:
            payload = {
                "startX": item.longitude,
                "startY": item.latitude,
                "endX": plan.longitude,
                "endY": plan.latitude,
                "format": "json",
                "count": 1,
                "searchDttm": "202310101200",
            }
            response = requests.post(url, json=payload, headers=headers)
            data = response.json()

            user_info["user"] = item.user.username
            user_info["distance"] = (
                data["metaData"]["plan"]["itineraries"][0]["totalDistance"] / 1000
            )
            user_info["time"] = (
                data["metaData"]["plan"]["itineraries"][0]["totalTime"] / 60
            )

            user_result.append(user_info)

    return render(
        request,
        "plan/plan_map.html",
        {
            "user_locations_json": user_locations_json,
            "plan_lat": plan.latitude,
            "plan_lng": plan.longitude,
            "result": user_result,
        },
    )


# 댓글 작성
# url : /plan/<uuid:pk>/comment/create
@login_required
def comment_create(request, pk):
    plan = get_object_or_404(Plan, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.plan = plan
            comment.save()
            return redirect("plan_detail", pk)
    else:
        form = CommentForm()
    return render(request, "plan/comment_form.html", {"form": form})
