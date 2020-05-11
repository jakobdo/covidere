$(function(){
    console.log("Basket.js - loaded!");
    $(".ajax-form-submit").submit(function(event){
        event.preventDefault();
        var form = $(this);
        var url = form.attr('action');

        $.post(url, form.serialize(), function(response){
            $("#basket-counter").text(response.count);
        }, 'json');
    });
});