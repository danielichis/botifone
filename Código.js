function iterarPeticionGet() {
  var configData=leer_config()
  var url = 'https://www.apple.com/shop/fulfillment-messages?pl=true&mts.0=regular&mts.1=compact&cppart=UNLOCKED/US&parts.0=MTQU3LL&location=33166'; // Reemplaza con la URL de la API que deseas consultar
  var compraExitosa=false
  if (configData.Estado=="CONECTADO"){
    for (var i=0;i<configData.iterations;i++){
      for (var zc of configData.zipcodes){
      for (var pc of configData.products){
        var url="https://www.apple.com/shop/fulfillment-messages?pl=true&mts.0=regular&mts.1=compact&cppart=UNLOCKED/US&parts.0="+pc.code+"/A&location="+zc
        compraExitosa=realizarPeticion(url,configData,pc,zc)
        compraExitosa=false
        if (compraExitosa==true){
          console.log("se hizo la compra")
          break
        }
        Utilities.sleep(1000)
    }
    if (compraExitosa==true){
          break
        }
    }
    if (compraExitosa==true){
          break
        }
  }
  }
}

function realizarPeticion(url,configData,pc,zc){
   try {
    var compraExitosa=false
    var response = UrlFetchApp.fetch(url);
    
    if (response.getResponseCode() == 200) {
      var headers = response.getHeaders();
      var contenido=response.getContentText()
      //var c3=response.getBlob()
      //var c4=response.getAs("aplication/json")
      //Logger.log('Respuesta exitosa: ' + contenido);
      Logger.log('Respuesta exitosa: ' + response.getResponseCode()+pc.code);
      var markets=buscarDisponibilidad(JSON.parse(contenido),configData,pc,zc)
      if (markets.length>0){
        var respuesta="DISPONIBLE"
        configData.productAvaible=pc
        configData.zipcodeAvaible=zc
        registrarTiendasDisponible(markets,configData.zipcodeAvaible,fechaHora())
        //var compraExitosa=ejecutarBotCompra(configData)
        botReproducirAudio()
        console.log("ejecutando bot de compra")
        var compraExitosa=true
      }else{
        var respuesta="NO DISPONIBLE"
      }
      var tiempoActual=fechaHora()
      escribirEnUltimaFila(pc,zc,tiempoActual,respuesta)
    } else {
      Logger.log('Error al realizar la solicitud. Código de respuesta: '+configData.productAvaible.code + response.getResponseCode());
    }
  } catch (error) {
    Logger.log('Error en la solicitud: ' +configData.productAvaible.code +" "+ error.toString());
  }
  return compraExitosa
}

function buscarDisponibilidad(content,configData,pc,zc){
  var product_code=pc.code+"/A"
  var marketsAvaible=[]
  var disponibilidad=false
  var marketsTochoice=configData.bestMarkets
  var message= content.body.content.pickupMessage
  if ("stores" in message){
    var tiendas=message.stores
    for (tienda of tiendas){
      if (product_code in tienda.partsAvailability){
        if (tienda.partsAvailability[product_code].pickupSearchQuote=="Available Today" || tienda.partsAvailability[product_code].pickupSearchQuote=="Available Tomorrow")
        {
          var tiendaName=tienda.storeName
           if (marketsTochoice.includes(tiendaName)){
            marketsAvaible.push(tienda)
            var disponibilidad=true
              }
        }
      }
    }
  }
  else{
    var disponibilidad=false
  }
  return marketsAvaible
}
function main(){
  var conexion=true
  //var conexion=validarConexion()
    if (conexion==true){
      updateStatus("CONECTADO")
      iterarPeticionGet()
    }else{
        updateStatus("SIN CONEXION")
    }
    
}
function test_get_apple()
{
  var urlSample="https://www.apple.com/shop/fulfillment-messages?fae=true&pl=true&mts.0=regular&cppart=UNLOCKED/US&parts.0=MFXU4LL/A&location=Miami%20Beach,%20FL"
  var urlSample2="https://www.apple.com/shop/fulfillment-messages?pl=true&mts.0=regular&mts.1=compact&cppart=UNLOCKED/US&parts.0=MTQU3LL&location=33166"
  var response = UrlFetchApp.fetch(urlSample2);
   var contenido=response.getContentText()
   console.log(contenido)

}

