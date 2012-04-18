/*
 * MAIN Expenses events handler
 */

/*///////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////// GLOBAL HELPERS ///////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////*/
var mydate_now = new Date();
var editing_now = false;

// TODO: comment changed to empty space " " instead of nothing...
// This will allow form serialization with empty comment. need to fix that in future.
function clear_expenses_form() {
	//clearing form data
    $('#id_currency').selectBox('value', "---------");
    $('#id_expense_date_day').selectBox('value', mydate_now.getDate());
    $('#id_expense_date_yearmonth').selectBox('value', (mydate_now.getFullYear()+'-'+(mydate_now.getMonth()+1)));//month count starts from 0
    $('#id_claim_date_day').selectBox('value', mydate_now.getDate());
    $('#id_claim_date_yearmonth').selectBox('value', (mydate_now.getFullYear()+'-'+(mydate_now.getMonth()+1)));//month count starts from 0
    $('#id_customer').selectBox('value', "---------");
    $('#id_expense_type').selectBox('value', "---------");
    $('#id_comment').selectBox('value', " ");
    $('#id_is_receipted').attr('checked', 'checked');
    $('#id_payment_method').selectBox('value', "---------");
    $('#id_is_taxable').attr('checked', 'checked');
    $('#id_expense_amount').selectBox('value', "0");
    $('#id_tax_amount').selectBox('value', "0");
    $('#id_local_amount').selectBox('value', "0");
    
    // clearing edit PK
    editing_now = false;
    $('#edit_pk').attr('edit_id', ' ');
	// clearing form errors (visually) if existed any
	$('div.ctrlHolder').removeClass('error');
	$('p.errorField').remove();
	// removing any visually selected rows
	$('tr').removeClass('editing_now_entry');
    return false;
};

//Populating form with data from JSON <div> created on page load for each entry
function expenses_form_populate(pk) {
		//assuming json data does not exist trying to parse it from 
		// html instead and construct our item array
		item_currency = $('#edit_currency-'+pk).html();
		item_temp1_date_day = $('#edit_expense_date_day-'+pk).html();
		item_expense_date_day = parseInt(item_temp1_date_day, 10);
		item_expense_date_month = $('#edit_expense_date_month-'+pk).html();
		item_expense_date_year = $('#edit_expense_date_year-'+pk).html();
			expense_month_cleaned = parseInt(item_expense_date_month, 10);
			item_expense_yearmonth = item_expense_date_year+'-'+ expense_month_cleaned;
		item_temp_date_day = $('#edit_claim_date_day-'+pk).html();
		item_claim_date_day = parseInt(item_temp_date_day, 10);
		item_claim_date_month = $('#edit_claim_date_month-'+pk).html();
		item_claim_date_year = $('#edit_claim_date_year-'+pk).html();
			claim_month_cleaned = parseInt(item_claim_date_month, 10);
			item_claim_yearmonth = item_claim_date_year+'-'+ claim_month_cleaned;
		item_customer = $('#edit_customer-'+pk).html();
		item_expense_type = $('#edit_expense_type-'+pk).html();
		item_comment = $('#edit_comment-'+pk).html();
		item_is_receipted = $('#edit_is_receipted-'+pk).html();
		item_payment_method = $('#edit_payment_method-'+pk).html();
		item_is_taxable = $('#edit_is_taxable-'+pk).html();
		item_expense_amount = $('#edit_expense_amount-'+pk).html();
		item_tax_amount = $('#edit_tax_amount-'+pk).html();
		item_local_amount = $('#edit_local_amount-'+pk).html();

	
		//Populating Form with elements according to provided timesheet div data
	    $('#id_currency').selectBox('value', item_currency);
	    $('#id_expense_date_day').selectBox('value', item_expense_date_day);
	    $('#id_expense_date_yearmonth').selectBox('value', item_expense_yearmonth);
	    $('#id_claim_date_day').selectBox('value', item_claim_date_day);
	    $('#id_claim_date_yearmonth').selectBox('value', item_claim_yearmonth);
	    $('#id_customer').selectBox('value', item_customer);
	    $('#id_expense_type').selectBox('value', item_expense_type);
	    $('#id_comment').selectBox('value', item_comment);
	    if (item_is_receipted == 'True') {
	    	$('#id_is_receipted').attr('checked', 'checked');
	    } else { 
	    	$('#id_is_receipted').removeAttr('checked');
	    };
	    $('#id_payment_method').selectBox('value', item_payment_method);
	    if (item_is_receipted == 'True') {
	    	$('#id_is_taxable').attr('checked', 'checked');
	    } else { 
	    	$('#id_is_taxable').removeAttr('checked');
	    };
	    $('#id_expense_amount').selectBox('value', item_expense_amount);
	    $('#id_tax_amount').selectBox('value', item_tax_amount);
	    $('#id_local_amount').selectBox('value', item_local_amount);
    return false;
};

function set_expenses_form_AJAX() {
    var options = { 
            beforeSubmit:  before_submit_expenses,  // pre-submit callback 
            success:       after_submit_expenses,   // post-submit callback 
            resetForm: true,               // reset the form after submit success 
            data: { data_id: '' },         //passing edit pk if exists
        }; 
        
        $('form#expenses_form').ajaxForm(options); 
        return false;
};

function before_submit_expenses(formData, jqForm, options) { 
	// inserting edit_pk parameter to every form post
	
	edit_pk = $('#edit_pk').attr('edit_id');
	
	// looking for data_id in form Query and passing it objects PK
	for(var i = 0; i < formData.length && formData[i].name != "data_id"; i++);
	if (i < formData.length) {
		formData[i].value=edit_pk;
	};

    return true; 
};

function after_submit_expenses(responseText, statusText, xhr, $form)  { 
	// determine if view returns form with errors or posted timesheet entry
	// and commit after post operations
	// (Insert form with errors/entry to DOM and map events)
	if (responseText.indexOf("expenses_form") > -1) {
		//form_exists in response inserting it to DOM and remapping form events interceptors 
		// clearing selectbox events, changing form and remaping events
		$('select').selectBox('destroy');
		$('form#expenses_form').replaceWith(responseText);
		set_expenses_form_AJAX();
		$('select').selectBox();
		
	} else if (responseText.indexOf("expense-") > -1) {
		//new entry exist in response
		//prepend it into table
		
		// determining if the response is edit or a new table entry
		if (responseText.indexOf("edited_item_returned") > -1) {
			// edited entry returned. Need2Update existing <tr> element
			// replacing existing TR element with this response
			pk = $('#edit_pk').attr('edit_id');
			existing_tr = $('tr[data-id="expense-'+pk+'"]');
			existing_tr.replaceWith(responseText);
		} else { 
			// new entry returned
			$('table tbody#tbody').prepend(responseText);
		};
		clear_expenses_form();
		
	} 
};

/*///////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////// EDIT /////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////*/
function expense_editbtn_press(button, pk){
	clear_expenses_form();
	expenses_form_populate(pk);
	//globally switching to edit mode for submit events
	editing_now = true;
	// store current editing item pk in the DOM for submit actions
	//$('#control-panel').attr('edit_id', pk)
	$('#edit_pk').attr('edit_id', pk);
	
	$('tr[data-id="expense-'+pk+'"]').addClass('editing_now_entry');
	return false;
};

/*///////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////// DELETE ////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////*/
function expense_delbtn_press(button, pk, url){
	$.post(url, { data_id: pk }, function(response_data){
		$('tr[data-id="expense-'+response_data+'"]').hide("fast");
	});
	return false;
};



//Main Events mapping on page load
$(document).ready(function() {

	set_expenses_form_AJAX();

	//setting "NEW" button events handler 
	$('#id_expenses_form_clear').click(function() {
		clear_expenses_form();
        return false;
    });
});
