$(document).ready(function () {

    $("#id_first_name").click(function() {
    $("#error_name").empty();
    $("#id_first_name").val("");
    });
    $("#id_last_name").click(function() {
    $("#error_lastname").empty();
    $("#id_last_name").val("");
    });
    $("#id_email").click(function() {
    $("#error_email").empty();
    $("#id_email").val("");
    });
    $("#id_username").click(function() {
    $("#error_username").empty();
    $("#id_username").val("");
    });
    $("#id_password").click(function() {
    $("#error_password").empty();
    $("#id_password").val("");
    });
    $("#id_password2").click(function() {
    $("#error_password2").empty();
    $("#id_password2").val("");
    });
});
