# coding: utf-8
import json
from datetime import datetime
from flask import g, jsonify, current_app, request, session

from . import api
from ihome.utils.commons import login_required
from ihome.utils.response_code import RET
from ihome.utils.image_storage import storage
from ihome.models import User, Area,House,Facility,HouseImage,Order
from ihome import db, constants,redis_store


@api.route("/areas", methods=["GET"])
def get_area_info():
    '''获取城区信息'''
    # 尝试从redis中读取数据
    try:
        resp_json = redis_store.get("area_info")
    except Exception as e:
        current_app.logger.error(e)
    else:
        if resp_json is not None:
            resp_json = resp_json.decode()
            # print(resp_json,type(resp_json),"*"*100)
            # redis 有缓存数据，直接返回
            return resp_json, 200, {"Content-Type": "application/json"}
    # 查询数据库获取城区信息
    try:
        area_li = Area.query.all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库异常")
    area_dict_li = []
    for area in area_li:
        area_dict_li.append(area.to_dict())
    # 将数据转换为json字符串
    resp_dict=dict(errno=RET.OK,errmsg="ok",data = area_dict_li)
    resp_json = json.dumps(resp_dict)
    # print(resp_json,"-"*100)
    # 将数据作为缓存保存到redis中
    try:
        # 要设置有效期(因为避免数据库更改了，redis不改？)
        redis_store.setex("area_info",constants.AREA_INFO_REDIS_CACHE_EXPIRES,resp_json)
    except Exception as e:
        current_app.logger.error()
    return resp_json,200,{"Content-Type":"application/json"}


@api.route("/houses/info", methods=["POST"])
@login_required
def save_house_info():
    """保存房屋的基本信息
    前端发送过来的json数据
    {
        "title":"",
        "price":"",
        "area_id":"1",
        "address":"",
        "room_count":"",
        "acreage":"",
        "unit":"",
        "capacity":"",
        "beds":"",
        "deposit":"",
        "min_days":"",
        "max_days":"",
        "facility":["7","8"]
    }
    """
    # 获取数据
    user_id = g.user_id
    house_data = request.get_json()

    title = house_data.get("title")  # 房屋名称标题
    price = house_data.get("price")  # 房屋单价
    area_id = house_data.get("area_id")  # 房屋所属城区的编号
    address = house_data.get("address")  # 房屋地址
    room_count = house_data.get("room_count")  # 房屋包含的房间数目
    acreage = house_data.get("acreage")  # 房屋面积
    unit = house_data.get("unit")  # 房屋布局（几室几厅)
    capacity = house_data.get("capacity")  # 房屋容纳人数
    beds = house_data.get("beds")  # 房屋卧床数目
    deposit = house_data.get("deposit")  # 押金
    min_days = house_data.get("min_days")  # 最小入住天数
    max_days = house_data.get("max_days")  # 最大入住天数

    # 校验参数
    if not all([title, price, area_id, address, room_count, acreage, unit, capacity, beds, deposit, min_days, max_days]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    # 判断金额是否正确
    try:
        price = int(float(price) * 100)
        deposit = int(float(deposit) * 100)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 判断城区id是否存在
    try:
        area = Area.query.get(area_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库异常")

    if area is None:
        return jsonify(errno=RET.NODATA, errmsg="城区信息有误")
    # 信息还可继续校验
    # 保存房屋信息
    house = House(
        user_id=user_id,
        area_id=area_id,
        title=title,
        price=price,
        address=address,
        room_count=room_count,
        acreage=acreage,
        unit=unit,
        capacity=capacity,
        beds=beds,
        deposit=deposit,
        min_days=min_days,
        max_days=max_days
    )

    # 处理房屋的设施信息
    facility_ids = house_data.get("facility")

    # 如果用户勾选了设施信息，再保存数据库
    if facility_ids:
        # ["7","8"]
        try:
            # select  * from ih_facility_info where id in []
            facilities = Facility.query.filter(Facility.id.in_(facility_ids)).all()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg="数据库异常")

        if facilities:
            # 表示有合法的设施数据
            # 保存设施数据
            house.facilities = facilities

    try:
        db.session.add(house)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="保存数据失败")

    # 保存数据成功（house_id，关联上传图片信息）
    return jsonify(errno=RET.OK, errmsg="OK", data={"house_id": house.id})


@api.route("/houses/image",methods=["POST"])
@login_required
def save_house_image():
    '''保存房屋图片
    参数：图片，id
    '''
    image_file = request.files.get("house_image")
    house_id = request.form.get("house_id")
    if not all([image_file,house_id]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")
    # 判断house_id正确性
    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库异常")

    if house is None:  # if not house:
        return jsonify(errno=RET.NODATA, errmsg="房屋不存在")
    image_data = image_file.read()
    try:
        file_name = storage(image_data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg="保存图片失败")
    house_image = HouseImage(house_id=house_id,url=file_name)
    db.session.add(house_image)

    # 处理房屋的主图片(将第一张图片设置为主图片，当然是可以设计为选择的)
    if not house.index_image_url:
        house.index_image_url = file_name
        db.session.add(house)

    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="保存图片数据异常")

    image_url = constants.QINIU_URL_DOMAIN + file_name

    return jsonify(errno=RET.OK, errmsg="OK", data={"image_url": image_url})


@api.route("/user/houses", methods=["GET"])
@login_required
def get_user_houses():
    """获取房东发布的房源信息条目"""
    user_id = g.user_id

    try:
        # houses = House.query.filter_by(user_id=user_id)
        user = User.query.get(user_id)
        houses = user.houses
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取数据失败")

    # 将查询到的房屋信息转换为字典存放到列表中
    houses_list = []
    if houses:
        for house in houses:
            houses_list.append(house.to_basic_dict())
    return jsonify(errno=RET.OK, errmsg="OK", data={"houses": houses_list})


@api.route("/houses/index", methods=["GET"])
def get_house_index():
    """获取主页幻灯片展示的房屋基本信息"""
    # 从缓存中尝试获取数据
    try:
        ret = redis_store.get("home_page_data")
    except Exception as e:
        current_app.logger.error(e)
        # 使不用使用else（避免抛出ret未定义异常）
        ret = None

    if ret:
        ret = ret.decode()
        current_app.logger.info("hit house index info redis")
        # 因为redis中保存的是json字符串，所以直接进行字符串拼接返回
        return '{"errno":0, "errmsg":"OK", "data":%s}' % ret, 200, {"Content-Type": "application/json"}
    else:
        try:
            # 查询数据库，返回房屋订单数目最多的5条数据
            houses = House.query.order_by(House.order_count.desc()).limit(constants.HOME_PAGE_MAX_HOUSES)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg="查询数据失败")

        if not houses:
            return jsonify(errno=RET.NODATA, errmsg="查询无数据")

        houses_list = []
        for house in houses:
            # 如果房屋未设置主图片，则跳过
            if not house.index_image_url:
                continue
            houses_list.append(house.to_basic_dict())

        # 将数据转换为json，并保存到redis缓存
        json_houses = json.dumps(houses_list)  # "[{},{},{}]"
        try:
            redis_store.setex("home_page_data", constants.HOME_PAGE_DATA_REDIS_EXPIRES, json_houses)
        except Exception as e:
            current_app.logger.error(e)

        return '{"errno":0, "errmsg":"OK", "data":%s}' % json_houses, 200, {"Content-Type": "application/json"}


@api.route("/houses/<int:house_id>", methods=["GET"])
def get_house_detail(house_id):
    """获取房屋详情"""
    # 前端在房屋详情页面展示时，如果浏览页面的用户不是该房屋的房东，则展示预定按钮，否则不展示，
    # 所以需要后端返回登录用户的user_id
    # 尝试获取用户登录的信息，若登录，则返回给前端登录用户的user_id，否则返回user_id=-1
    user_id = session.get("user_id", "-1")

    # 校验参数
    if not house_id:
        return jsonify(errno=RET.PARAMERR, errmsg="参数确实")

    # 先从redis缓存中获取信息
    try:
        ret = redis_store.get("house_info_%s" % house_id)
    except Exception as e:
        current_app.logger.error(e)
        ret = None
    if ret:
        ret = ret.decode()
        current_app.logger.info("hit house info redis")
        return '{"errno":"0", "errmsg":"OK", "data":{"user_id":%s, "house":%s}}' % (user_id, ret), \
               200, {"Content-Type": "application/json"}

    # 查询数据库
    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据失败")

    if not house:
        return jsonify(errno=RET.NODATA, errmsg="房屋不存在")

    # 将房屋对象数据转换为字典
    try:
        house_data = house.to_full_dict()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg="数据出错")

    # 存入到redis中
    json_house = json.dumps(house_data)
    try:
        redis_store.setex("house_info_%s" % house_id, constants.HOUSE_DETAIL_REDIS_EXPIRE_SECOND, json_house)
    except Exception as e:
        current_app.logger.error(e)

    resp = '{"errno":"0", "errmsg":"OK", "data":{"user_id":%s, "house":%s}}' % (user_id, json_house), \
           200, {"Content-Type": "application/json"}
    return resp


# /api/v1.0/houses?sd=2019-11-01&ed2019-11-31&aid10&sk=new&p=1
@api.route("/houses")
def get_house_list():
    '''获取房屋的列表信息（搜索页面）'''
    #  默认值的原因是避免none，redis存入不进去
    start_date = request.args.get("sd","")  # 用户想要的起始时间
    end_date = request.args.get("ed", "")  # 用户想要的结束时间
    area_id = request.args.get("aid", "")  # 区域编号
    sort_key = request.args.get("sk", "new")  # 排序关键字
    page = request.args.get("p")  # 页数

    # 时间处理
    try:
        if start_date:
            # 字符串到时间：datetime.strptime();时间到字符串：datetime.strftime()  %H%M%S:时分秒
            start_date = datetime.strptime(start_date,"%Y-%m-%d")
        if end_date:
            end_date = datetime.strptime(end_date,"%Y-%m-%d")

        if start_date and end_date:
            assert start_date <= end_date
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="日期参数有误")

    # 校验区域id(get只可以根据主键id获取对象(django中可以以定义的所有字段为判断标准))
    if area_id:
        try:
            area = Area.query.get(area_id)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.PARAMERR, errmsg="区域参数有误")

    # 不做排序关键字处理，如果传递非法的，按照默认的进行处理

    # 处理页数
    try:
        page = int(page)
    except Exception as e:
        current_app.logger.error(e)
        page = 1

    # 获取缓存数据
    redis_key = f"house_{start_date}_{end_date}_{area_id}_{sort_key}"
    try:
        resp_json = redis_store.hget(redis_key, page)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if resp_json:
            resp_json=resp_json.decode()
            return resp_json, 200, {"Content-Type": "application/json"}

    # 过滤条件的参数容器
    filter_params = []
    # 时间条件（冲突的订单）
    conflict_orders = None
    # 要在订单中筛选出来没有冲突的订单是不合理的，因为有的房子也许连一次订单都没有，所以就选择筛选出来所有有冲突的，然后取反进行解决。
    # 什么时候有冲突：订单起始时间小于用户需求结束时间，并且，订单结束时间大于用户起始时间，便是存在冲突,所以
    # select * from order where order.begin_date<=end_date and order.end_date >= start_date
    try:
        order_status_li = Order.order_status_li
        if start_date and end_date:
            # fixme 这里没有对拒单和取消订单的房屋信息做剔除(已解决)
            # 查询冲突的订单
            conflict_orders = Order.query.filter(Order.begin_date <= end_date, Order.end_date >= start_date,Order.status.notin_(order_status_li)).all()
            # print("*"*100)
        elif start_date:
            conflict_orders = Order.query.filter(Order.end_date >= start_date,Order.status.notin_(order_status_li)).all()
        elif end_date:
            conflict_orders = Order.query.filter(Order.begin_date <= end_date,Order.status.notin_(order_status_li)).all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库异常")

    if conflict_orders:
        # 获取冲突的房屋id
        conflict_house_ids = [order.house_id for order in conflict_orders]
        # if conflict_house_ids:
        filter_params.append(House.id.notin_(conflict_house_ids))
    # 区域条件
    if area_id:
        # list append的是一个表达式(可以理解塞进去的是一系列的条件，然后通过解包的方式解开了)
        filter_params.append(House.area_id == area_id)
        # a=House.area_id == area_id
        # print(a,type(a),"="*100)

    # 查询并排序(这里还没到数据库查询，这里只是组织条件，因为没有.all())
    if sort_key == "booking":  # 入住最多
        house_query = House.query.filter(*filter_params).order_by(House.order_count.desc())
    elif sort_key == "price-inc":  # 价格由低到高
        house_query = House.query.filter(*filter_params).order_by(House.price.asc())
    elif sort_key == "price-des":  # 价格由高到低
        house_query = House.query.filter(*filter_params).order_by(House.price.desc())
    else:  # 新旧
        house_query = House.query.filter(*filter_params).order_by(House.create_time.desc())
    # 这里才真正的进行了数据库的查询
    try:
        # 参数的意义：当前页数 每页数据量 自定义错误输出(当page不存在的时候，并不会abort404，而是返回一个对象，page_obj.items,返回了一个空列表)
        page_obj = house_query.paginate(page=page,per_page=constants.HOUSE_LIST_PAGE_CAPACITY,error_out=False)
        # print(page_obj,type(page_obj),"*"*100)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库异常")

    # 获取页面数据
    house_li = page_obj.items
    # print(house_li,type(house_li),"-"*100)
    # 存每个房子的数据
    houses = []
    for house in house_li:
        houses.append(house.to_basic_dict())

    # 获取总页数
    total_page = page_obj.pages
    resp_dict = dict(errno=RET.OK, errmsg="OK", data={"total_page": total_page, "houses": houses, "current_page": page})
    resp_json = json.dumps(resp_dict)
    if page <=total_page:
    # 设置缓存数据
        redis_key = f"house_{start_date}_{end_date}_{area_id}_{sort_key}"
        # 哈希
        try:
            # redis_store.hset(redis_key, page, resp_json)
            # redis_store.expire(redis_key, constants.HOUES_LIST_PAGE_REDIS_CACHE_EXPIRES)

            # 创建redis管道对象，可以一次执行多个语句(避免第一句执行了，第二句执行的时候出错，数据变成永久的了)
            pipeline = redis_store.pipeline()

            # 开启多个语句的记录
            pipeline.multi()

            pipeline.hset(redis_key, page, resp_json)
            pipeline.expire(redis_key, constants.HOUES_LIST_PAGE_REDIS_CACHE_EXPIRES)

            # 执行语句
            pipeline.execute()
        except Exception as e:
            current_app.logger.error(e)

    return resp_json, 200, {"Content-Type": "application/json"}