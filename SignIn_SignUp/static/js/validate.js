$(document).ready(function () {

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
       else if (lastname.length == 0) {
           error_lastname.innerHTML = message1;
       }
    });

    $("#id_email").change(function () {
       var email = $(this).val();
       var message1 = "Introduzca un correo electrónico válido";
       var regexEmail =  /^[a-zA-Z0-9\._-]+@[a-zA-Z0-9-]{2,}[.][a-zA-Z]{2,4}$/;
       if ( !(email.match(regexEmail))){
           error_email.innerHTML = message1;
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
       var message1 = "La contraseña debe ser mayor de seis dígitos, alfanumérica, con mínimo una letra mayúscula y " +
                        "contener alguno de estos caracteres especiales: $@!%_*?&";
       var regexPassword =  /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%_*?&])([A-Za-z\d$@$!%*_?&]|[^ ]){6,10}$/;
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