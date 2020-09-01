function validar(){

    var correo = document.getElementById('correo').value;
    var contraseña = document.getElementById('contraseña').value;

    expresion = /\w+@\w+\.+[a-z]/;

    if(correo==='' || contraseña===''){
        alert("Todos los campos son requeridos!");
         return false;
    }
    else if(correo.length>20){
        alert("El correo tiene muchos caracteres");
        return false;
    }
    else if(!expresion.test(correo)){
        alert("Correo Invalido!");
        return false;
    }

    if(correo==='jccscarto@gmail.com' && contraseña==='qwerty123'){
        alert("Datos validos!")
        window.open('./html/gerente/home_gte.html')
    }

    if(correo==='coord@gmail.com' && contraseña==='qwerty123'){
        alert("Datos validos!")
        window.open('./html/coordinador/home.html')
    }

    if(correo==='operario@gmail.com' && contraseña==='qwerty123'){
        alert("Datos validos!")
        window.open('./html/operario/home_oper.html')
    }

    else if(contraseña.length>=6){
        alert("Contraseña muy larga");
        return false;
    }
    else if(contraseña.length<=3){
        alert("Contraseña muy corta");
        return false;
    }
    else if(contraseña!== 'qwerty123'){
        alert("Contraseña Incorrecta!");
        return false;
    }
}