const UUT_INFO_KEYS = ['id', 'uut', 'start_date_time', 'general_notes', 'temperature', 'uut_serial_number'];
const RESULT_BASE_KEYS = ['freq', 'vbatt_voltage', 'vbatt_current', 'vbatt_power',
    'vcc_voltage', 'vcc_current', 'vcc_power',
    'pae', 'pout', 'pin', 'gain',
    'dc_power', 'ch_power',
    'utra_lowadj', 'utra_highadj',
    'utra_lowalt', 'utra_highalt',
    'rms_mean', 'rms_max', 'freq_error_mean',
    'target_power', 'vcc', 'vbatt',
    'waveform',
    'mipi',
    'notes'];
const LTE_RESULT_KEYS = ['uut_test_id',
    'freq', 'vbatt_voltage', 'vbatt_current', 'vbatt_power',
    'vcc_voltage', 'vcc_current', 'vcc_power',
    'pae', 'pout', 'pin', 'gain',
    'dc_power', 'ch_power',
    'eutra_low', 'eutra_high',
    'utra_lowadj', 'utra_highadj',
    'utra_lowalt', 'utra_highalt',
    'rms_mean', 'rms_max', 'freq_error_mean',
    'target_power', 'vcc', 'vbatt',
    'waveform',
    'mipi',
    'notes'];
const WCDMA_RESULT_KEYS = ['uut_test_id',
    'freq', 'vbatt_voltage', 'vbatt_current', 'vbatt_power',
    'vcc_voltage', 'vcc_current', 'vcc_power',
    'pae', 'pout', 'pin', 'gain',
    'dc_power', 'ch_power',
    'utra_lowadj', 'utra_highadj',
    'utra_lowalt', 'utra_highalt',
    'rms_mean', 'rms_max', 'freq_error_mean', 'chip_rate_error',
    'target_power', 'vcc', 'vbatt',
    'waveform',
    'mipi',
    'notes'];
const TDSCDMA_RESULT_KEYS = ['uut_test_id',
    'freq', 'vbatt_voltage', 'vbatt_current', 'vbatt_power',
    'vcc_voltage', 'vcc_current', 'vcc_power',
    'pae', 'pout', 'pin', 'gain',
    'dc_power', 'ch_power',
    'utra_lowadj', 'utra_highadj',
    'utra_lowalt', 'utra_highalt',
    'rms_mean', 'rms_max', 'freq_error_mean', 'chip_rate_error',
    'target_power', 'vcc', 'vbatt',
    'waveform',
    'mipi',
    'notes'];
const CDMA2K_RESULT_KEYS = ['uut_test_id',
    'freq', 'vbatt_voltage', 'vbatt_current', 'vbatt_power',
    'vcc_voltage', 'vcc_current', 'vcc_power',
    'pae', 'pout', 'pin', 'gain',
    'dc_power', 'ch_power',
    'utra_lowadj', 'utra_highadj',
    'utra_lowalt', 'utra_highalt',
    'rms_mean', 'rms_max', 'freq_error_mean', 'chip_rate_error',
    'target_power', 'vcc', 'vbatt',
    'waveform',
    'mipi',
    'notes'];


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
            generateUUTTable(data);
        }
    });
});


$("#query_id_btn").click(function (event) {
    // event.preventDefault();
    var uut_test_id = document.getElementById("query_id").value
    console.log("post to ajax (test result)");
    $.get("/getTestResult", { 'uut_test_id': uut_test_id }, function (data) {
        console.log('successfully get result from server');
        generateTestResultTable(data);
    });
});


$("#query_checked_records_btn").click(function (event) {
    var records_id_arr = getRecordIDs();
    for (var value of records_id_arr) {        
        $.get("/getTestResult", { 'uut_test_id': value }, function (data) {
            console.log('successfully get result from server');
            generateTestResultTable(data);
        });
    }
});


$("#export_checked_records_btn").click(function(event) {
    var records_id_arr = getRecordIDs();
    $.get('/exportCSV', {uut_test_id: records_id_arr});
});


function getRecordIDs() {
    var table = document.getElementById("table2");
    var chkbox_records_arr = [];
    var inputs = table.getElementsByTagName("input");
    for (var i=0; i<inputs.length;i++) {
        if ((inputs[i].type==='checkbox') && (inputs[i].checked==true))
            chkbox_records_arr.push(inputs[i].value);
    }
    console.log(chkbox_records_arr);
    return chkbox_records_arr
}


function generateUUTTable(data) {
    var tb2 = document.getElementById('table2');
    var data_length = Object.keys(data).length;
    var tbbody = document.createElement("tbody");

    var header = document.createElement("tr");
    var cell = document.createElement("th");
    header.appendChild(cell);   // empty position for checkbox
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
        var cell = document.createElement("td");
        var chkbox = document.createElement("input")
        chkbox.setAttribute("type", "checkbox");
        chkbox.setAttribute("value", obj['id']);
        cell.appendChild(chkbox);
        row.appendChild(cell);
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


function generateTestResultTable(data) {
    var tb3 = document.getElementById('table3');
    var data_length = Object.keys(data).length;
    console.log('data_length :' + data_length);
    var tbbody = document.createElement("tbody");

    var header = document.createElement("tr");
    for (let item of LTE_RESULT_KEYS) {
        let cell = document.createElement("th");
        let cell_text = document.createTextNode(item);
        cell.appendChild(cell_text);
        header.appendChild(cell);
    }
    tbbody.appendChild(header);

    // Itinerate data array object
    for (let obj of data) {
        var row = document.createElement("tr");
        for (let item of LTE_RESULT_KEYS) {
            var cell = document.createElement("td");
            if (isFloat(obj[item]))
                x = obj[item].toPrecision(6);
            else
                x = obj[item];
            var cell_text = document.createTextNode(x);
            cell.appendChild(cell_text);
            row.appendChild(cell);
        }
        tbbody.appendChild(row);
    }
    tb3.appendChild(tbbody);
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

function isInt(n){
    return Number(n) === n && n % 1 === 0;
}

function isFloat(n){
    return Number(n) === n && n % 1 !== 0;
}