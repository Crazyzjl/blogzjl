#__author:  Administrator
#date:   2019/3/1

import geoip2.database

def ip_to_addr(ip):
    """
    Ip 转换成现实中的地理位置
    :param ip:
    :return:
    """
    reader = geoip2.database.Reader('Blog/GeoLite2-City.mmdb')
    response = reader.city(ip)
    #有些IP的身份和城市未知，所以设置默认为空
    province = ''
    city = ''
    try:
        country = response.country.names["zh-CN"]
        province = response.subdivisions.most_specific.names["zh-CN"]
        city = response.city.names["zh-CN"]
    except:
        pass
    if country != '中国':
        return country
    if province and city:
        if province == city or city in province:
            return province
        return '%s%s' %(province,city)
    elif province and not city:
        return province
    else:
        return country


