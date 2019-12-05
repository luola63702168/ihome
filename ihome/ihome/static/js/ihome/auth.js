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
    $.get("/api/v1.0/users/auth", function (resp) {
        if ("4101" == resp.errno) {
            location.href = "/login.html";
        } else if ("0" == resp.errno) {
            if (resp.data.real_name && resp.data.id_card) {
                $("#real-name").val(resp.data.real_name);
                $("#id-card").val(resp.data.id_card);
                $("#real-name").prop("disabled", true);
                $("#id-card").prop("disabled", true);
                $("#form-auth>input[type=submit]").hide();
            }
        } else {
            alert(resp.errmsg);
        }
    }, "json");

    $("#form-auth").submit(function (e) {
        e.preventDefault();
        var realName = $("#real-name").val();
        var idCard = $("#id-card").val();
        if (realName == "" || idCard == "") {
            $(".error-msg").show();
        }

        var data = {
            real_name: realName,
            id_card: idCard
        };
        var jsonData = JSON.stringify(data);

        $.ajax({
            url: "/api/v1.0/users/auth",
            type: "POST",
            data: jsonData,
            contentType: "application/json",
            dataType: "json",
            headers: {
                "X-CSRFTOKEN": getCookie("csrf_token")
            },
            success: function (resp) {
                if (0 == resp.errno) {
                    $(".error-msg").hide();
                    showSuccessMsg();
                    $("#real-name").prop("disabled", true);
                    $("#id-card").prop("disabled", true);
                    $("#form-auth>input[type=submit]").hide();
                } else {

                    $(".error-msg").show();
                    alert(resp.errmsg)
                }
            }

        });
    })

})