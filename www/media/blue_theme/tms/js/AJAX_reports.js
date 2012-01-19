/**
 * User: garmoncheg
 * Date: 1/19/12
 * Time: 4:05 PM
 * Main reports initializer
 */

function init_reports_form() {
    var reports_date_init = false;
    var mydate_now = new Date();
    reports_date_init = $('div#init_reports').attr('init');
    if (reports_date_init=="init") {
        $('#id_date_start_day').selectBox('value', mydate_now.getDate());
        $('#id_date_start_yearmonth').selectBox('value', (mydate_now.getFullYear()+'-'+(mydate_now.getMonth()+1)));//month count starts from 0
        $('#id_date_end_day').selectBox('value', mydate_now.getDate());
        $('#id_date_end_yearmonth').selectBox('value', (mydate_now.getFullYear()+'-'+(mydate_now.getMonth()+1)));//month count starts from 0
    };
    return false;
};


//Main Events mapping on page load
$(document).ready(function() {
    init_reports_form();
});