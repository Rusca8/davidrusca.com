console.log("loading csrf token for AJAX calls...")

if(!$('meta[name="csrf-token"]')){
    console.log("Meta tag for csrf-token not found. Forgot to add it? :)")
}

/* derived from Django's DOCs example */
function csrfSafeMethod(method){
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings){
        if(!csrfSafeMethod(settings.type) && !settings.crossDomain) {
            xhr.setRequestHeader(
                "X-CSRFToken", $('meta[name="csrf-token"]').attr('content')
            );
        }
    }
});
