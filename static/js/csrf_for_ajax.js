console.log("%cCSRF :: Loading token for AJAX calls...%c", 'color: saddlebrown')

if(!$('meta[name="csrf-token"]')){
    console.log("Meta tag for csrf-token not found. Forgot to add it? :)")
}

/* derived from Django's DOCs example */
function csrfSafeMethod(method){
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

let csrf_token = $('meta[name="csrf-token"]').attr('content');  // initial token (will need refresh)
let csrf_token_timestamp = Date.now();
let csrf_refresh_promise = null;
console.log("%cCSRF :: Initial token loaded (timestamp: " + csrf_token_timestamp + ")%c", 'color: saddlebrown');

async function ensure_valid_csrf_token(){
    const max_age = 45 * (60*1000);  // 45'
    if(csrf_token && Date.now() - csrf_token_timestamp < max_age){
        return;
    }
    if(!csrf_refresh_promise){
        console.log("%cCSRF :: Token not loaded or expired. Fetching new token...%c", 'color: saddlebrown');
        csrf_refresh_promise = $.getJSON('/csrf-token')
        .fail(function(jqXHR, textStatus, errorThrown){
            console.log("%cCSRF :: Token renewal failed.%c", 'color: saddlebrown');
        })
        .done(function(data){
            csrf_token = data.csrf_token;
            csrf_token_timestamp = Date.now();
            console.log("%cCSRF :: Token renewed.%c", 'color: saddlebrown')
        })
        .always(() => {csrf_refresh_promise = null});  // gotta clear it or future runs won't start
    }else{
        console.log("%cCSRF :: Someone is renewing the expired token. Waiting with them...%c", 'color: saddlebrown')
    }

    await csrf_refresh_promise;
}

$.ajaxSetup({
    beforeSend: function(xhr, settings){
        if(!csrfSafeMethod(settings.type) && !settings.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        }
    }
});

/*
 * Class as "decorator proxy": swap $ to S in ajax .post calls to wrap them with
 * a function that tries to ensure it'll use a valid csrf-token for the ajax call.
 *
 * - Gràcies a l'Alejandro per resoldre el repte d'exposar els mètodes de l'xhr!
 */
class S {
    static post(params) {
        const deferred = $.Deferred();

        ensure_valid_csrf_token()
            .then(() => {
                $.post(params)
                    .done((...args) => {
                        deferred.resolve(...args);
                    })
                    .fail((...args) => {
                        deferred.reject(...args);
                    });
            })

        return deferred.promise();
    }

    static async ajax(params){
        if(!params.type == "get"){
            await ensure_valid_csrf_token();
        }
        console.log("%cAJAX :: Swap S.ajax() call for an explicit S." + params.type + "() (and remove type:'post') for using .done & .fail%c", 'color: steelblue');
        return $.ajax(params);
    }
}