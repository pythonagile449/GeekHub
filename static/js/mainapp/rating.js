"use strict"
//Получение переменной cookie по имени
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function like()
{
    var like = $(this);
    var type = like.data('type');
    var pk = like.data('id');
    var action = like.data('action');
    var dislike = like.next();
    $.ajax({
        url : "rating" + "/" + type + "/" + action + "/",
        type : 'POST',
        data : { 'obj' : pk },

        success : function (json) {
            like.find("[data-count='positive']").text(json.positive);
            dislike.find("[data-count='negative']").text(json.negative);
        }
    });
    return false;
}

function dislike()
{
    var dislike = $(this);
    var type = dislike.data('type');
    var pk = dislike.data('id');
    var action = dislike.data('action');
    var like = dislike.prev();

    $.ajax({
        url : "rating" + "/" + type + "/" + action + "/",
        type : 'POST',
        data : { 'obj' : pk },

        success : function (json) {
            dislike.find("[data-count='negative']").text(json.negative);
            like.find("[data-count='positive']").text(json.positive);
        }
    });

    return false;
}
// Подключение обработчиков
$(function() {
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });
    $('[data-action="like"]').click(like);
    $('[data-action="dislike"]').click(dislike);
});