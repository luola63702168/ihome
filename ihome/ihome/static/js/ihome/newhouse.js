function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {
    $.get("api/v1.0/areas", function (resp) {
        var areas = resp.data;
        if (resp.errno == "0") {
            var html = template("areas-tmpl", {areas: areas});
            $("#area-id").html(html)
        } else {
            alert(resp.errmsg)
        }
    }, "json");

    $("#form-house-info").submit(function (e) {
        e.preventDefault();
        var data = {};
        $("#form-house-info").serializeArray().map(function (x) {
            return data[x.name] = x.value;
        });

        var facility = [];
        $(":checked[name=facility]").each(function (index, x) {
            facility[index] = $(x).val();
        });
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
                    location.href = "/login.html";
                } else if (resp.errno == "0") {
                    $("#form-house-info").hide();
                    $("#form-house-image").show();
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

                    $(".house-image-cons").append('<img src="' + resp.data.image_url + '">');
                } else {
                    alert(resp.errmsg);
                }
            }
        })
    })
});