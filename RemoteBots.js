function ejecutarBotCompra(data) {
var urlW10 = 'https://jqjl556k-5000.brs.devtunnels.ms/'; // Reemplaza con la URL de tu endpoint POST
var urlMac="https://gffc6wc9-5000.brs.devtunnels.ms/"
var url=urlMac+"ejecutarBot"

  var payload = JSON.stringify(data);
  var options = {
    "method" : "POST",
    "contentType" : "application/json",
    "payload" : payload
  };
  // Realiza la petición POST
  var respuesta = UrlFetchApp.fetch(url, options);

  // Comprueba si la respuesta fue exitosa (código de respuesta 200)
  if (respuesta.getResponseCode() === 200) {
    var contenido = respuesta.getContentText();
    updateGiftCarBalance(respuesta)
    var compraExitosa=true;
    Logger.log(contenido); // Registra la respuesta en el registro de ejecución
  } else {
    Logger.log('La solicitud no fue exitosa. Código de respuesta: ' + respuesta.getResponseCode());
    var compraExitosa=false
  }
  return compraExitosa
}

function validarConexion() {
var urlMac="https://gffc6wc9-5000.brs.devtunnels.ms/"
var urlW10="https://jqjl556k-5000.brs.devtunnels.ms/"
var url = urlMac+'mi_api'; // Reemplaza con la URL de tu endpoint POST

  // Realiza la petición POST
    var data={nombre:"daniel",
              fecha:"2024"}
   var payload = JSON.stringify(data);
  var options = {
  "method" : "POST",
  "contentType" : "application/json",
  "payload" : payload
};
try{
  var respuesta = UrlFetchApp.fetch(url,options);
  if (respuesta.getResponseCode() === 200) {
      Logger.log("respuesta exitosa")
      var conexion=true
      var contenido = respuesta.getContentText();
      Logger.log(contenido); // Registra la respuesta en el registro de ejecución
    } else {
      Logger.log('La solicitud no fue exitosa. Código de respuesta: ' + respuesta.getResponseCode());
    }
  }
catch (e)
{
  Logger.log("respuesta sin conexion")
var conexion=false
}
  return conexion
}

function botReproducirAudio() {
var urlMac="https://gffc6wc9-5000.brs.devtunnels.ms/"
var urlW10="https://jqjl556k-5000.brs.devtunnels.ms/"
var url = urlMac+'reproducirAudio'; // Reemplaza con la URL de tu endpoint POST

  // Realiza la petición POST
    var data={nombre:"daniel",
              fecha:"2024"}
   var payload = JSON.stringify(data);
  var options = {
  "method" : "POST",
  "contentType" : "application/json",
  "payload" : payload
};
try{
  var respuesta = UrlFetchApp.fetch(url,options);
  if (respuesta.getResponseCode() === 200) {
      Logger.log("respuesta exitosa")
      var conexion=true
      var contenido = respuesta.getContentText();
      Logger.log(contenido); // Registra la respuesta en el registro de ejecución
    } else {
      Logger.log('La solicitud no fue exitosa. Código de respuesta: ' + respuesta.getResponseCode());
    }
  }
catch (e)
{
  Logger.log("respuesta sin conexion")
var conexion=false
}
  return conexion
}