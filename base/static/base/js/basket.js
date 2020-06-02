$(function(){
    $(".ajax-form-submit").submit(function(event){
        event.preventDefault();
        var form = $(this);
        var url = form.attr('action');

        $.post(url, form.serialize(), function(response){
            $("#basket-counter").fadeTo(500, 0.1, function() {
                $(this).text(response.count);
                $(this).fadeTo(500, 1.0);
            });
        }, 'json');
    });
});