const UUT_INFO_KEYS = ['id', 'uut', 'start_date_time', 'notes', 'temperature', 'uut_serial_number'];



$("form").submit(function (event) {
    // alert( "Handler for .submit() called." );
    event.preventDefault();
    // $.post('/getJSONResult', $("form").serialize(), generateResultTable(this.data), 'json');
    console.log("post to ajax")
    $.ajax({
        url: "/getUUTRecord",
        type: 'POST',
        data: $("form").serialize(),
        timeout: 4000,
        dataType: 'json',
        statusCode: { 500: function () { alert('error occur'); } },
        success: function (data) {
            console.log('successfully get result from server')  // returned an array object
            console.log(data.length);
            generateResultTable(data);
        }
    });
});


function generateResultTable(data) {
    var tb2 = document.getElementById('table2');
    var data_length = Object.keys(data).length;
    var tbbody = document.createElement("tbody");

    var header = document.createElement("tr");
    for (let item of UUT_INFO_KEYS) {
        let cell = document.createElement("th");
        let cell_text = document.createTextNode(item);
        cell.appendChild(cell_text);
        header.appendChild(cell);
    }
    tbbody.appendChild(header);

    // Itinerate data array object
    for (let obj of data) {
        var row = document.createElement("tr");
        for (let item of UUT_INFO_KEYS) {
            var cell = document.createElement("td");
            var cell_text = document.createTextNode(obj[item]);
            cell.appendChild(cell_text);
            row.appendChild(cell); 
        }
        tbbody.appendChild(row);
    }
    tb2.appendChild(tbbody);
}


function generate_table() {
    var body = document.getElementById("table1");
    var tb1 = document.createElement("table");
    var tb1Body = document.createElement("tbody");
    for (var i = 0; i < 2; i++) {
        var row = document.createElement("tr");
        for (var j = 0; j < 2; j++) {
            var cell = document.createElement("td");
            var cellText = document.createTextNode("cell in row " + i + ", column " + j);
            cell.appendChild(cellText);
            row.appendChild(cell);
        }
        tb1Body.appendChild(row);
    }

    tb1.appendChild(tb1Body);
    body.appendChild(tb1)
    tb1.setAttribute("border", "2");
}