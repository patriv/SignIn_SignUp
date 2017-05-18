$(document).ready(function () {

       $("#id_first_name").change(function () {
           alert("funcion");
           var name = $(this).val();
           var message1 = "El nombre debe contener sólo caracteres válidos sin espacio";
           var regex =  /^[a-zA-ZáéíóúàèìòùÀÈÌÒÙÁÉÍÓÚñÑüÜ]*$/;
           var regexNum =  /^[0-9]+$/;
           alert(name);
           if ( !(name.match(regex))){
               error.innerHTML = message1;
           }
           else if (name.length == 0) {
               alert("El nombre no puede estar vacío ");
               $("#error").innerText = message1;
           }
       });

       $("#id_last_name").change(function () {
           alert("funcion");
           var lastname = $(this).val();
           var message1 = "El Apellido debe contener sólo caracteres válidos sin espacio";
           var regex =  /^[a-zA-ZáéíóúàèìòùÀÈÌÒÙÁÉÍÓÚñÑüÜ]*$/;
           var regexNum =  /^[0-9]+$/;
           alert(lastname);
           if ( !(lastname.match(regex))){
               error.innerHTML = message1;
           }
           else if (lastname.length == 0) {
               alert("El Apellido no puede estar vacío donde no debe etra");
               $("#error").innerText = message1;
           }
       })
    });

