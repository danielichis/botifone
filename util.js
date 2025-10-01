function leer_config() {
  var sheet_config = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('config');
  var sheet_master = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('maestro');

  var columna_zc = sheet_config.getRange('A:A');
  var valores_zipcodes = columna_zc.getValues();
  var rango = sheet_config.getRange('B:D');
  var valores_producto = rango.getValues();
  var rango_best_markets=sheet_config.getRange("E:E")
  var valores_markets=rango_best_markets.getValues();
  var rango_giftCards=sheet_config.getRange("J:J")
  var valores_giftCards=rango_giftCards.getValues()
  var rango_maestro = sheet_master.getRange('A:G');
  var valores_maestro = rango_maestro.getValues();

  var nameBuyer=sheet_config.getRange("I2").getValue()
  var lastNameBuyer=sheet_config.getRange("I3").getValue()
  var numberBuyer=sheet_config.getRange("I4").getValue()
  var emailBuyer=sheet_config.getRange("I5").getValue()
  var schedull=sheet_config.getRange("G2").getValue()
  var compraFinal=sheet_config.getRange("L2").getValue()
  var debug=sheet_config.getRange("M2").getValue()

  var mainButton=sheet_config.getRange("N2").getValue()

  var configData={
    zipcodes:[],
    products:[],
    bestMarkets:[],
    giftCards:[],
    buyerInfo:{"name":nameBuyer,"lastName":lastNameBuyer,"number":numberBuyer,"email":emailBuyer},
    "schedule":schedull,
    "debug":debug,
    "compraFinal":compraFinal,
    productAvaible:{},
    "zipcodeAvaible":"",
    "Estado":mainButton,
    "iterations":""
  }
  
  for (var i = 1; i < valores_zipcodes.length; i++) {
    var valor = valores_zipcodes[i][0];
    if (valor !== "") {
      //Logger.log('Valor en la fila ' + (i + 1) + ': ' + valor);
      configData.zipcodes.push(valor);
    }else{
      break
    }
  }
  for (var i = 1; i < valores_markets.length; i++) {
    var valor = valores_markets[i][0];
    if (valor !== "") {
      //Logger.log('Valor en la fila ' + (i + 1) + ': ' + valor);
      configData.bestMarkets.push(valor);
    }else{
      break
    }
  }

  for (var i = 1; i < valores_giftCards.length; i++) {
    var valor = valores_giftCards[i][0];
    if (valor !== "") {
      //Logger.log('Valor en laa ' + (i + 1) + ': ' + valor);
      configData.giftCards.push(valor);
    }else{
      break
    }
  }

   for (var i = 1; i < valores_producto.length; i++) {
      var product_code = valores_producto[i][1];
      var product_name = valores_producto[i][0];
      var product_price = valores_producto[i][2];
      if (product_code !== "") {
        var productMainInfo={
          "code":product_code,
          "name":product_name,
          "price":product_price}
        var aditionalInfo=searchFromMaestro(product_code,valores_maestro)
        var product_total = Object.assign({}, productMainInfo, aditionalInfo);
        configData.products.push(
          product_total
        )
      } else{
        break
      }
    
  }
  configData.iterations=Math.ceil(30/(configData.zipcodes.length*configData.products.length)-1)
  //console.log(configData)
  return configData
}

function searchFromMaestro(code,valores_maestro){
  for (var product of valores_maestro){
    if (product[1]==code){
      var data={
        "gamma":product[2],
        "color":product[3],
        "capacity":product[4],
        "version":product[5],
        "price":product[6]
      }
      break 
    }
   }
   return data
  }
function escribirEnUltimaFila(pc,zp,tiempoActual,respuesta) {
  var hoja = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('DATA'); // Reemplaza con el nombre de tu hoja
  var ultimaFila = hoja.getLastRow() + 1; // Obtiene el número de la última fila y suma 1 para obtener la siguiente fila vacía
  
  // Datos que deseas escribir en la última fila
  var datos = [pc.name,pc.price,zp,tiempoActual,respuesta];
  
  // Escribe los datos en la última fila
  hoja.getRange(ultimaFila, 1, 1, datos.length).setValues([datos]);
}
function registrarTiendasDisponible(tiendas,zipCode,tiempoActual) {
  var hoja = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('TIENDAS'); // Reemplaza con el nombre de tu hoja
   // Obtiene el número de la última fila y suma 1 para obtener la siguiente fila vacía
  for (tienda of tiendas){
    var ultimaFila = hoja.getLastRow() + 1;
    var datos = [tienda.storeName,tienda.city,zipCode,tiempoActual];
    hoja.getRange(ultimaFila, 1, 1, datos.length).setValues([datos]);
  }
}

function fechaHora() {
var zonaHoraria = "America/Lima"; // Zona horaria de Perú

  // Obtén la fecha y hora actual en la zona horaria de Perú
  var fechaHoraActual = Utilities.formatDate(new Date(), zonaHoraria, "yyyy-MM-dd HH:mm:ss");

 return fechaHoraActual
}

function updateStatus(status) {
  var allowedValues = ["CONECTADO", "SIN CONEXION"];
  
  // Verificar si el valor proporcionado está en la lista de valores permitidos
  if (allowedValues.indexOf(status) !== -1) {
    var hoja = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('config');
    hoja.getRange("N2").setValue(status);
    var updatedVal = hoja.getRange("N2").getValue();
    Logger.log(updatedVal);
  } else {
    Logger.log("El valor proporcionado no es válido. Debe ser 'APAGADO' o 'PRENDIDO'.");
  }
}
function updateGiftCarBalance(respuesta) {
    var hoja = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('config');
    var valoresGiftCards=hoja.getRange("J:K").getValues()

    for (var i=0;i<valoresGiftCards.length;i++){
      if (valoresGiftCards[i][0]==respuesta.giftCard){
        hoja.getRange("K"+(i+1).toString()).setValue(respuesta.remainingBalance);
        break
      }
    }
}
function mainUtils(){
  var response={
        "giftCard":"X5ZHZHNJ9JV2VJ6C",
        "purchaseStatus":true,
        "remainingBalance":309
    }
updateGiftCarBalance(response)
}

