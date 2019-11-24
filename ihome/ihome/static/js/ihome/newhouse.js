function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // 像后端获取城区信息
    $.get("api/v1.0/areas",function (resp) {
        var areas = resp.data;
        if (resp.errno=="0"){
            // for (i = 0; i<areas.length; i++){
            //     var area=areas[i];
            //     $("#area-id").append('<option value="'+area.aid+'">'+area.aname+'</option>\n');
            // }
        //    js模板使用("areas-tmpl":选择该元素；{areas:areas}:模板中要使用的数据)
            var html = template("areas-tmpl",{areas:areas});
            $("#area-id").html(html)
        }else {
            alert(resp.errmsg)
        }
    },"json");

    $("#form-house-info").submit(function (e) {
        e.preventDefault();
        // 处理表单数据
        var data = {};
        // serializeArray()获取表单中name和value及其对应的值，返回的是数组
        // x是数组中每一个元素，这里是“字典”也就是js中的对象
        // map()返回的是“字典”
        $("#form-house-info").serializeArray().map(function(x) {
            // 如果没有return，默认将 data[x.name]=x.value; 返回
            return data[x.name]=x.value;
        });

        // 收集设置id信息
        var facility = [];
        //index:遍历的元素对应的索引,该索引对应的那个页面元素，不是对象，所以需要使用$选中
        $(":checked[name=facility]").each(function (index,x) {
            facility[index] = $(x).val();
        });
        // 给对象添加这个属性
        data.facility = facility;

        $.ajax({
            url: "/api/v1.0/houses/info",
            type: "post",
            contentType: "application/json",
            data: JSON.stringify(data),
            dataType: "json",
            headers: {
                "X-CSRFToken": getCookie("csrf_token")
            },
            success: function (resp) {
                if (resp.errno == "4101") {
                    // 用户未登录
                    location.href = "/login.html";
                } else if (resp.errno == "0") {
                    // 隐藏基本信息表单
                    $("#form-house-info").hide();
                    // 显示图片表单
                    $("#form-house-image").show();
                    // 设置图片表单中的house_id
                    $("#house-id").val(resp.data.house_id);
                } else {
                    alert(resp.errmsg);
                }
            }
        })
    });
    $("#form-house-image").submit(function (e) {
        e.preventDefault();
        $(this).ajaxSubmit({
            url: "/api/v1.0/houses/image",
            type: "post",
            dataType: "json",
            headers: {
                "X-CSRFToken": getCookie("csrf_token"),
            },
            success: function (resp) {
                if (resp.errno == "4101") {
                    location.href = "/login.html";
                } else if (resp.errno == "0") {

                    $(".house-image-cons").append('<img src="' + resp.data.image_url +'">');
                } else {
                    alert(resp.errmsg);
                }
            }
        })
    })
});