$(document).ready(function () {

    var error = 0;

    $("#id_first_name").change(function () {
       
       var name = $(this).val();
       var message1 = "El nombre debe contener sólo caracteres válidos sin espacio";
       var regexName =  /^[a-zA-ZáéíóúàèìòùÀÈÌÒÙÁÉÍÓÚñÑüÜ]*$/;
       var regexNum =  /^[0-9]+$/;
       if ( !(name.match(regexName))){
           error_name.innerHTML = message1;

       }
       else if (name.length == 0) {
           error_name.innerHTML = message1;
       }
    });

    $("#id_last_name").change(function () {
       
       var lastname = $(this).val();
       var message1 = "El Apellido debe contener sólo caracteres válidos sin espacio";
       var regexLastname =  /^[a-zA-ZáéíóúàèìòùÀÈÌÒÙÁÉÍÓÚñÑüÜ]*$/;
       if ( !(lastname.match(regexLastname))){
           error_lastname.innerHTML = message1;
       }

    });

    $("#id_email").change(function () {
       var email = $(this).val();
       var message1 = "Introduzca un correo electrónico válido";
       var regexEmail =  /^[a-zA-Z0-9\._-]+@[a-zA-Z0-9-]{2,}[.][a-zA-Z]{2,4}$/;
       var form = $(this).closest("form");

       if ( !(email.match(regexEmail))){
           error_email.innerHTML = message1;
           error = 1;
       }
       else {
           $.ajax({
               url: form.attr("data-validate-email-url"),
               data: {
                   email: email
               },
               type: 'POST',
               dataType: 'json',
               success: function (data) {
                   if (data.email_exists) {
                       error_email.innerHTML = data.error;
                   }
               }
           });
           $.ajax({
               url: form.attr("data-forgot-email-url"),
               data: {
                   email: email
               },
               type: 'POST',
               dataType: 'json',
               success: function (data) {
                   emailExist = data.email_exists;
                   if ((emailExist) == false) {
                       error_email.innerHTML = data.error;
                   }
               }
           })
       }

    });

    $("#id_username").change(function(){
        var username = $(this).val();
        var form = $(this).closest("form");
        $.ajax({
            url: form.attr("data-validate-username-url"),
            data: {username:username
                   },
            type:'POST',
            dataType: 'json',
            success: function(data){
                if (data.username_exists) {
                    error_username.innerHTML = data.error;
                }
            },
        });
    });

    $("#id_password").change(function () {
       
       var password = $(this).val();
       var message1 = "La contraseña debe tener una longitud entre seis y doce caracteres, alfanumérica, con mínimo una letra " +
                      "mayúscula y contener alguno de estos caracteres especiales: $@!%.#_*?&";
       var regexPassword = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[$@!%.#_*?&]).{6,12}$/;

       if (!(password.match(regexPassword))) {
            error_password.innerHTML = message1;
       }

    });

    $("#id_password2").change(function () {
       
       var password2 = $(this).val();
       var password = $("#id_password").val();
       var message1 = "Las contraseñas no coinciden, por favor verifique";
       if (password2 && (password2 !== password)){
           error_password2.innerHTML = message1;
       }

    });
});