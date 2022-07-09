function PutCliente(){

    var request = new XMLHttpRequest();
    usernombre = window.prompt('Usernombre:')
    password = window.prompt('Password:')

    var id_cliente = window.location.search.substring(1);
    
    let id_cliente1 = id_cliente;
    let nombre = document.getElementById("nombre");
    let email  = document.getElementById("email");

    let payload = {
        "id_cliente": id_cliente1,
        "nombre": nombre.value,
        "email" : email.value,
    }

    console.log("id_cliente: " + id_cliente);
    console.log("email: "  + email.value);
    console.log("nombre: " + nombre.value);
    console.log(payload);
    
    request.open('PUT', "https://8000-arturomarquezl-apirest-yv4tjpyrt41.ws-us53.gitpod.io/clientes/",true);
    request.setRequestHeader("Accept", "application/json");

    request.setRequestHeader("Authorization", "Basic " + btoa(usernombre + ":" + password))
    request.setRequestHeader("content-type", "application/json");

    
    request.onload = () => {
        
        const response  = request.responseText;
        const json      = JSON.parse(response);     
        const status    = request.status;

        if (request.status === 401 || request.status === 403) {
            alert(json.detail);
        }

        else if (request.status == 202){

            console.log("Response: " + response);
            console.log("JSON: " + json);
            console.log("Status: " + status);

            alert(json.message);
            window.location.replace("/templates/getclientes.html")
        }
    };
    request.send(JSON.stringify(payload));
}