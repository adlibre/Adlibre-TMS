/*
    Authentication generation scripts for Django admin and Xero Client
 */
$( document ).ajaxError(function( event, request, settings ) {
      alert("Error requesting page " + request.response);
});

function get_pin(event) {
    event.preventDefault();
    var url = $('#xero_get_pin').attr('post'),
        key = $('#id_consumer_key').val(),
        secret = $('#id_consumer_secret').val();


    $.post(
        url,
        data = {
            'key': key,
            'secret': secret
        },
        function( data ) {
            console.log( data );
            window.open(data);
        }
    );
    console.log(url);
    console.log(key);
    console.log(secret);

}