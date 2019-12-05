function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function () {
        setTimeout(function () {
            $('.popup_con').fadeOut('fast', function () {
            });
        }, 1000)
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


$(document).ready(function () {
    $("#form-avatar").submit(function (e) {
        e.preventDefault();
        $(this).ajaxSubmit({
            url: "/api/v1.0/users/avatar",
            type: "post",
            dataType: "json",
            headers: {
                "X-CSRFToken": getCookie("csrf_token")
            },
            success: function (resp) {
                if (resp.errno == "0") {
                    var avatarUrl = resp.data.avatar_url;
                    $("#user-avatar").attr("src", avatarUrl);
                } else {
                    alert(resp.errmsg);
                }
            }
        })
    })

    $.get("/api/v1.0/user", function (resp) {
        if ("4101" == resp.errno) {
            location.href = "/login.html";
        } else if ("0" == resp.errno) {
            $("#user-name").val(resp.data.name);
            if (resp.data.avatar) {
                $("#user-avatar").attr("src", resp.data.avatar);
            }
        }
    }, "json");

    $("#form-name").submit(function (e) {
        e.preventDefault();
        var name = $("#user-name").val();

        if (!name) {
            alert("请填写用户名！");
            return;
        }
        $.ajax({
            url: "/api/v1.0/users/name",
            type: "PUT",
            data: JSON.stringify({name: name}),
            contentType: "application/json",
            dataType: "json",
            headers: {
                "X-CSRFTOKEN": getCookie("csrf_token")
            },
            success: function (data) {
                if ("0" == data.errno) {
                    $(".error-msg").hide();
                    showSuccessMsg();
                } else if ("4001" == data.errno) {
                    $(".error-msg").show();
                } else if ("4101" == data.errno) {
                    location.href = "/login.html";
                }
            }
        });
    })


})
