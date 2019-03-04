#__author:  Administrator
#date:   2019/3/1

from Blog.ip_convert_addr import ip_to_addr
from django.utils import timezone
from .models import UserIp,VisitNumber,DayNumber


def visit_info(request, end_point):
    """
    修改网站访问量和访问IP的信息
    每一次访问，网站总访问次数加一
    :param request:
    :param end_point:
    :return:
    """

    count_nums = VisitNumber.objects.filter(id=1)
    if count_nums:
        count_nums = count_nums[0]
        count_nums.count += 1
    else:
        count_nums = VisitNumber()
        count_nums.count = 1
    count_nums.save()
    print("26",count_nums.count)
    #记录访问IP和每个IP的次数
    if 'HTTP_X_FORWARDED_FOR' in request.META: #获取ip
        client_ip = request.META['HTTP_X_FORWARDED_FOR']
        client_ip = client_ip.split(",")[0] #这里是真实的ip
    else:
        client_ip = request.META['REMOTE_ADDR'] #这是代理ip
    ip_exist = UserIp.objects.filter(ip=str(client_ip), end_point=end_point)
    if ip_exist:
        uobj = ip_exist[0]
        uobj.count += 1
    else:
        uobj = UserIp()
        uobj.ip = client_ip
        uobj.end_point = end_point
        try:
            uobj.ip_addr = ip_to_addr(client_ip)
        except:
            uobj.ip_addr = "unknown"
        uobj.count = 1
    uobj.save()
    print("47:uobj",uobj.ip_addr)

    #增加每日访问量次数
    date = timezone.now().date()
    today = DayNumber.objects.filter(day=date)
    if today:
        temp = today[0]
        temp.count += 1
    else:
        temp = DayNumber()
        temp.day = date
        temp.count = 1
    temp.save()
    print("60:temp", temp.count)


