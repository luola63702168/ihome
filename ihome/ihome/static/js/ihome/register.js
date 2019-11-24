// js读取cookie的方法（\b匹配不占位置的空格（单词边界））
function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

// 保存图片验证码编号
var imageCodeId = "";

function generateUUID() {
    var d = new Date().getTime();
    if(window.performance && typeof window.performance.now === "function"){
        d += performance.now(); //use high-precision timer if available
    }
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x3|0x8)).toString(16);
    });
    return uuid;
}

function generateImageCode() {
    // 形成图片验证码的后端地址， 设置到页面中，让浏览请求验证码图片
    // 1. 生成图片验证码编号
    // 一般函数中如果不使用var的话就是全局变量，但是这个函数得调用才会生效（这里仅是修改全局变量的值）
    imageCodeId = generateUUID();
    // 设置图片url
    var url = "/api/v1.0/image_codes/"+imageCodeId;
    $(".image-code img").attr("src",url);
}

function sendSMSCode() {
    $(".phonecode-a").removeAttr("onclick");
    var mobile = $("#mobile").val();
    if (!mobile) {
        $("#mobile-err span").html("请填写正确的手机号！");
        $("#mobile-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    } 
    var imageCode = $("#imagecode").val();
    if (!imageCode) {
        $("#image-code-err span").html("请填写验证码！");
        $("#image-code-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    }
    var req_data={
        image_code:imageCode,//图片验证码的值
        image_code_id:imageCodeId, // 图片验证码的编号,（全局变量）
    };

    $.get("api/v1.0/sms_codes/"+mobile,req_data,function(resp){
        //resp是后端的响应值，后端返回的是json字符串，ajax将其转换为js对象，也就是resp
        if (resp.errno=="0"){
            // 发送成功
            var num=60;
            var timer=setInterval(function(){
                if (num>1) {
                    // 修改倒计时文本
                $(".phonecode-a").html(num+"秒");
                }else {
                $(".phonecode-a").html("获取验证码");
                $(".phonecode-a").attr("onclick", "sendSMSCode();");
                clearInterval(timer);
                }
                num -=1;
            //    这里的60是在定时器结束后作为参数给回调函数的，这里没有任何作用
            },1000,60)
        }else {
            alert(resp.errmsg)
            $(".phonecode-a").attr("onclick", "sendSMSCode();");
        }
    });
}

$(document).ready(function() {
    generateImageCode();
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#imagecode").focus(function(){
        $("#image-code-err").hide();
    });
    $("#phonecode").focus(function(){
        $("#phone-code-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
        $("#password2-err").hide();
    });
    $("#password2").focus(function(){
        $("#password2-err").hide();
    });
    // 为表单的提交补充自定义的函数行为（提交事件e）
    $(".form-register").submit(function(e){
        e.preventDefault();
        var mobile = $("#mobile").val();
        var phoneCode = $("#phonecode").val();
        var passwd = $("#password").val();
        var passwd2 = $("#password2").val();
        if (!mobile) {
            $("#mobile-err span").html("请填写正确的手机号！");
            $("#mobile-err").show();
            return;
        } 
        if (!phoneCode) {
            $("#phone-code-err span").html("请填写短信验证码！");
            $("#phone-code-err").show();
            return;
        }
        if (!passwd) {
            $("#password-err span").html("请填写密码!");
            $("#password-err").show();
            return;
        }
        if (passwd != passwd2) {
            $("#password2-err span").html("两次密码不一致!");
            $("#password2-err").show();
            return;
        }
        // 调用ajax向后端发送注册请求
        var req_data={
            mobile:mobile,
            sms_code:phoneCode,
            password:passwd,
            password2:passwd2
        };
        var req_json=JSON.stringify(req_data);
        $.ajax({
            url:"api/v1.0/users",
            type:"post",
            data:req_json,
            contentType:"application/json",
            dataType:"json",
            headers:{
                "X-CSRFToken":getCookie("csrf_token")
            },
            success:function(resp){
                if (resp.errno=="0"){
                    location.href="index.html";
                }else {
                    alert(resp.errmsg);
                }
            }
        })
    });
});