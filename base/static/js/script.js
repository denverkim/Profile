document
  .getElementById("fileInput")
  .addEventListener("change", handleFileSelect);

function handleFileSelect(event) {
  var file = event.target.files[0];
  if (!file) {
    return;
  }

  var reader = new FileReader();
  reader.onload = function (e) {
    var data = new Uint8Array(e.target.result);
    var workbook = XLSX.read(data, { type: "array" });

    // Assume we are working with the first sheet
    var sheetName = workbook.SheetNames[0];
    var worksheet = workbook.Sheets[sheetName];

    // Convert sheet to JSON
    var jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });

    // Extract x and y values (assuming they are in the first and second columns)
    var xArray = [];
    var yArray = [];

    for (var i = 1; i < jsonData.length; i++) {
      // Skipping header row
      xArray.push(jsonData[i][0]); // First column
      yArray.push(jsonData[i][1]); // Second column
    }

    const data = [
      {
        x: xArray,
        y: yArray,
        type: "bar",
        orientation: "v",
        marker: { color: "rgba(0,0,255,0.6)" },
      },
    ];

    const layout = { title: "World Wide Wine Production" };

    Plotly.newPlot("myPlot", data, layout);
  };

  reader.readAsArrayBuffer(file);
}
