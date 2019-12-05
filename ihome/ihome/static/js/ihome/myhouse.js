$(document).ready(function () {
    $.get("/api/v1.0/users/auth", function (resp) {
        if ("4101" == resp.errno) {
            location.href = "/login.html";
        } else if ("0" == resp.errno) {
            if (!(resp.data.real_name && resp.data.id_card)) {
                $(".auth-warn").show();
                return;
            }
            $.get("/api/v1.0/user/houses", function (resp) {
                if ("0" == resp.errno) {
                    $("#houses-list").html(template("houses-list-tmpl", {houses: resp.data.houses}));
                } else {
                    $("#houses-list").html(template("houses-list-tmpl", {houses: []}));
                }
            });
        }
    });
})