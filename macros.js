//Google apps script functions to intecact with Google sheets data

function removeWatch(email, prodID, combID) {
  
  //archive any active watchers once an instock email has been sent
  
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var responseSheet = ss.getSheets()[0];
  var parseSheet = ss.getSheetByName('Parse');
  var archiveSheet = ss.getSheetByName('Archive');

  //get the number of data rows on the parse sheet
  var r = getFirstEmptyRowByColumnArray('Parse') - 2;

  //create variable with parsed data
  var data = parseSheet.getRange(1, 1, r+1, 6).getValues();
  data.shift() //remove column headers

  //loop over each data row
  for (var i = r-1; i >= 0; i = i - 1) {
    
    //if the email, prodID and combID arguments match a data row write it to archive and delete from response sheet
    if (data[i][3] == email.toLowerCase() && data[i][4] == prodID && data[i][5] == combID){
      arch_r = getFirstEmptyRowByColumnArray('Archive')
      responseSheet.getRange(i+2,1).getDataRegion(SpreadsheetApp.Dimension.COLUMNS).copyTo(archiveSheet.getRange(arch_r, 1))
      
      //add date removed
      currentDate = Utilities.formatDate(new Date(), ss.getSpreadsheetTimeZone(), "dd/MM/yyyy HH:mm:ss")
      archiveSheet.getRange(arch_r, 4).setValue(currentDate)
      responseSheet.deleteRow(i+2)
    }
  };
  
};

function getActiveWatchers() {

  //return a list of active watchers to check stock
   
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Unique');
  var r = getFirstEmptyRowByColumnArray('Unique');
  var data = sheet.getRange(1, 1, r-1, 3).getValues(); 
  
  
  data.shift() //remove column headers
  return data
}

// From answer https://stackoverflow.com/a/9102463/1677912
function getFirstEmptyRowByColumnArray(sheetName) {
  var spr = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName);
  var column = spr.getRange('A:A');
  var values = column.getValues(); // get all data in one call
  var ct = 0;
  while ( values[ct] && values[ct][0] != "" ) {
    ct++;
  }
  return (ct+1);
}
