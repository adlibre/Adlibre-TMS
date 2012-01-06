/*
 * MAIN Timesheet buttons events handler
 */

/*///////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////// GLOBAL HELPERS ///////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////*/

// TODO: comment changed to empty space " " instead of nothing...
// This will allow form serialization with empty comment. need to fix that in future.
function clear_timesheet_form() {
    var mydate_now = new Date();
	//clearing form data
    $('#id_job').selectBox('value', "---------");
    $('#id_date_start_day').selectBox('value', mydate_now.getDate());
    $('#id_date_start_yearmonth').selectBox('value', (mydate_now.getFullYear()+'-'+(mydate_now.getMonth()+1)));//month count starts from 0
    $('#id_start_time_hour').selectBox('value', mydate_now.getHours());
    $('#id_start_time_minute').selectBox('value', mydate_now.getMinutes());
    $('#id_end_time_hour').selectBox('value', mydate_now.getHours());
    $('#id_end_time_minute').selectBox('value', mydate_now.getMinutes());
    $('#id_comment').selectBox('value', " ");
    // clearing edit PK
    // TODO: add clearing of edit settings
    editing_now = false;
    $('#edit_pk').attr('edit_id', ' ');
	// clearing form errors (visually) if existed any
	$('div.ctrlHolder').removeClass('error');
	$('p.errorField').remove();
	// removing any visually selected rows
	$('tr').removeClass('editing_now_entry');

    // adding data from last timesheet
    timesheet_latest_date = $('#timesheet_latest_date').attr('paramether');
    timesheet_latest_job = $('#timesheet_latest_job').attr('paramether');
    //alert(timesheet_latest_date);
    if (timesheet_latest_date) {
        init_date = new Date(timesheet_latest_date);
        $('#id_start_time_hour').selectBox('value', init_date.getHours());
        $('#id_start_time_minute').selectBox('value', init_date.getMinutes());
        $('#id_job').selectBox('value', timesheet_latest_job);
    };

    return false;
};

// special saving sequence of timesheet
// to preserve job set from last time
function clear_timesheet_form_preserve_job() {
	temp_value = $('#id_job').selectBox('value');
	clear_timesheet_form();
	$('#id_job').selectBox('value', temp_value);
    return false;
};

//Populating form with data from JSON <div> created on page load for each entry
function timesheet_form_populate(pk) {
	//assuming json data does not exist trying to parse it from 
	// html instead and construct our item array
	item_job_id = $('#edit_job_id-'+pk).html();
	item_start_date_day = $('#edit_start_date_day-'+pk).html();
	item_start_date_month = $('#edit_start_date_month-'+pk).html();
	item_start_date_year = $('#edit_start_date_year-'+pk).html();
	item_start_time_hours = $('#edit_start_time_hours-'+pk).html();
	item_start_time_minutes = $('#edit_start_time_minutes-'+pk).html();
	item_end_time_minutes = $('#edit_end_time_minutes-'+pk).html();
	item_end_time_hours = $('#edit_end_time_hours-'+pk).html();
	item_comment = $('#edit_comment-'+pk).html();
	
	// clearing data values for correct selectbox insertions
	month_cleaned = parseInt(item_start_date_month, 10);
	item_yearmonth = item_start_date_year+'-'+ month_cleaned;
	item_cleaned_start_date_day = parseInt(item_start_date_day, 10);
	item_cleaned_start_time_hours = parseInt(item_start_time_hours, 10);
	item_cleaned_start_time_minutes = parseInt(item_start_time_minutes, 10);
	item_cleaned_end_time_hours = parseInt(item_end_time_hours, 10);
	item_cleaned_end_time_minutes = parseInt(item_end_time_minutes, 10);
	
	//Populating Form with elements according to provided timesheet div data
	$('#id_job').selectBox('value', item_job_id);
	$('#id_date_start_day').selectBox('value', item_cleaned_start_date_day);
	$('#id_date_start_yearmonth').selectBox('value', item_yearmonth);
	$('#id_comment').selectBox('value', item_comment);
	// handling 00 hours/minutes situations
	if (item_cleaned_start_time_hours == 0) {
		value = $('#id_start_time_hour').selectBox('value', '00');
	} else {
		$('#id_start_time_hour').selectBox('value', item_cleaned_start_time_hours);
	};
	if (item_cleaned_start_time_minutes == 0) {
		$('#id_start_time_minute').selectBox('value', '00');
	} else {
		$('#id_start_time_minute').selectBox('value', item_cleaned_start_time_minutes);
	};
	if (item_cleaned_end_time_hours == 0) {
		$('#id_end_time_hour').selectBox('value', '00');
	} else {
		$('#id_end_time_hour').selectBox('value', item_cleaned_end_time_hours);
	};
	if (item_cleaned_end_time_minutes == 0) {
		$('#id_end_time_minute').selectBox('value', '00');
	} else {
		$('#id_end_time_minute').selectBox('value', item_cleaned_end_time_minutes);
	};
    return false;
};

function set_timesheet_form_AJAX() {
    var options = { 
            beforeSubmit:  before_submit_timesheets,  // pre-submit callback 
            success:       after_submit_timesheets,   // post-submit callback 
            resetForm: true,               // reset the form after submit success 
            data: { data_id: '' }         //passing edit pk var to populate later
        }; 
        
        $('form#timesheets_form').ajaxForm(options); 
        return false;
};

function before_submit_timesheets(formData, jqForm, options) { 
	// inserting edit_pk parameter to every form post
	edit_pk = $('#edit_pk').attr('edit_id');

	// looking for data_id in form Query and passing it objects PK
	for(var i = 0; i < formData.length && formData[i].name != "data_id"; i++);
	if (i < formData.length) {
		formData[i].value=edit_pk;
	};
	
    return true; 
};

function after_submit_timesheets(responseText, statusText, xhr, $form)  { 
	// determine if view returns form with errors or posted timesheet entry
	// and commit after post operations
	// (Insert form with errors/entry to DOM and map events)
	if (responseText.indexOf("timesheets_form") > -1) {
		//form_exists in response inserting it to DOM and remapping form events interceptors 
		// clearing selectbox events, changing form and remaping events
		$('select').selectBox('destroy');
		$('form#timesheets_form').replaceWith(responseText);
		set_timesheet_form_AJAX();
		$('select').selectBox();
		
	} else if (responseText.indexOf("timesheet-") > -1) {
		//new entry exist in response
		//prepend it into table
		
		// determining if the response is edit or a new table entry
		if (responseText.indexOf("edited_item_returned") > -1) {
			// edited entry returned. Need2Update existing <tr> element
			// replacing existing TR element with this response
			pk = $('#edit_pk').attr('edit_id');
			existing_tr = $('tr[data-id="timesheet-'+pk+'"]');
			existing_tr.replaceWith(responseText);
		} else { 
			// new entry returned
			$('table tbody#tbody').prepend(responseText);
            // setting form init data according to Wiki specs
            //alert(responseText);
            var timesheet_init_date = $(responseText).find('.init_start_time_data').html();
            var timesheet_init_job_id = $(responseText).find('.init_job_data').html();
            $('#timesheet_latest_date').attr('paramether', timesheet_init_date);
            $('#timesheet_latest_job').attr('paramether', timesheet_init_job_id);
		};
		clear_timesheet_form();
	} 
};

/*///////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////// EDIT /////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////*/

function timesheet_editbtn_press(button, pk){
	clear_timesheet_form();
	timesheet_form_populate(pk);
	//globally switching to edit mode for submit events
	editing_now = true;
	// store current editing item pk in the DOM for submit actions
	//$('#control-panel').attr('edit_id', pk)
	$('#edit_pk').attr('edit_id', pk);
	
	$('tr[data-id="timesheet-'+pk+'"]').addClass('editing_now_entry');
	return false;
};

$(document).ready(function() {

	set_timesheet_form_AJAX();

	//setting "NEW" button events handler 
	$('#id_timesheet_form_clear').click(function() {
		clear_timesheet_form();
		editing_now = false;
		
        return false;
    });
});

/*///////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////// DELETE ////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////*/

function timesheet_delbtn_press(button, pk, url){
var delete_disabled = false;
	$.post(url, { data_id: pk }, function(response_data){
		$('tr[data-id="timesheet-'+response_data+'"]').hide("fast");
	});
	return false;
};

/*///////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////// INITIALISATION ///////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////*/


$(document).ready(function() {

    var mydate_now = new Date();
    var editing_now = false;

    //Clears all form time upon reload/page load
    clear_timesheet_form();

});
