//Google apps script functions to intecact with Google sheets data

function removeWatch(email, prodID, combID, inStore, online) {
  
  //archive any active watchers once an instock email has been sent
  
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var responseSheet = ss.getSheets()[0];
  var parseSheet = ss.getSheetByName('Parse');
  var archiveSheet = ss.getSheetByName('Archive');

  //get the number of data rows on the parse sheet
  var r = getFirstEmptyRowByColumnArray('Parse') - 2;

  //create variable with parsed data
  var data = parseSheet.getRange(1, 1, r+1, parseSheet.getMaxColumns()).getValues();
  
  var emailInd = data[0].indexOf('Lowercase Email')
  var prodInd = data[0].indexOf('ProductID')
  var combInd = data[0].indexOf('CombinationID')
  var instoreInd = data[0].indexOf('Instore')
  var onlineInd = data[0].indexOf('Online')
  data.shift() //remove column headers

  //loop over each data row
  for (var i = r-1; i >= 0; i = i - 1) {
    
    //if the email, prodID and combID arguments match a data row write it to archive and delete from response sheet
    if (data[i][emailInd] == email.toLowerCase() && data[i][prodInd] == prodID && data[i][combInd] == combID && data[i][instoreInd] == inStore && data[i][onlineInd] == online) {
      arch_r = getFirstEmptyRowByColumnArray('Archive')
      //responseSheet.getRange(i+2,1).getDataRegion(SpreadsheetApp.Dimension.COLUMNS).copyTo(archiveSheet.getRange(arch_r, 1))
      
      //add date removed
      currentDate = Utilities.formatDate(new Date(), ss.getSpreadsheetTimeZone(), "dd/MM/yyyy HH:mm:ss")
      archiveSheet.getRange(arch_r, 1,1,3).setValues(responseSheet.getRange(i+2,1,1,3).getValues())
      archiveSheet.getRange(arch_r, 4).setValue(responseSheet.getRange(i+2,5).getValue())
      archiveSheet.getRange(arch_r, 5).setValue(currentDate)
      responseSheet.deleteRow(i+2)
    }
  };
  
};

function getActiveWatchers() {

  //return a list of active watchers to check stock
   
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Unique');
  var r = getFirstEmptyRowByColumnArray('Unique');
  var data = sheet.getRange(1, 1, r-1, 5).getValues(); 
  
  
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
