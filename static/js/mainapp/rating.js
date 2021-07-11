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

function like() {
    var like = $(this);
    var type = like.data('type');
    var pk = like.data('id');
    var action = like.data('action');
    var dislike = like.next();
    $.ajax({
        url: "rating" + "/" + type + "/" + action + "/",
        type: 'POST',
        data: {'obj': pk},
        success: function (json) {
            console.log(json)
            $('.positive').html(json.positive)
            $('.negative').html(json.negative)
            $('.modal-content').html(json.access_denied)
        }
    });
    return false;
}

function dislike() {
    var dislike = $(this);
    var type = dislike.data('type');
    var pk = dislike.data('id');
    var action = dislike.data('action');
    var like = dislike.prev();

    $.ajax({
        url: "rating" + "/" + type + "/" + action + "/",
        type: 'POST',
        data: {'obj': pk},

        success: function (json) {
            console.log(json)
            $('.positive').html(json.positive)
            $('.negative').html(json.negative)
            $("#modal-articles .modal-content").html(json.access_denied);
        }
    });

    return false;
}


// Set handlers
$(function () {
    $.ajaxSetup({
        headers: {"X-CSRFToken": getCookie("csrftoken")}
    });
    $('.like-article').click(like);
    $('.dislike-article').click(dislike);
});


class CommentsRating {
    constructor() {
        this.likeButtons = document.querySelectorAll('.like-comment-btn');
        this.dislikeButtons = document.querySelectorAll('.dislike-comment-btn');
        this.setHandlers();
    }

    setHandlers() {
        this.likeButtons.forEach(button => {
            button.addEventListener('click', evt => {
                let requestParams = this.getAjaxParams(evt);
                this.sendCommentRatingAjax(requestParams, evt);
            })
        })

        this.dislikeButtons.forEach(button => {
            button.addEventListener('click', evt => {
                let requestParams = this.getAjaxParams(evt);
                this.sendCommentRatingAjax(requestParams, evt);
            })
        })
    }

    getAjaxParams(evt) {
        let targetSet = evt.target.parentNode; // get parentNode (<li>) to catch dataset params
        let requestParams = {
            type: targetSet.dataset.type,
            action: targetSet.dataset.action,
            formData: new FormData(document.querySelector('.comment-form')), // to set csrf token
        };
        requestParams.formData.append('obj_id', targetSet.dataset.id);

        return requestParams;
    }

    sendCommentRatingAjax(requestParams, evt) {
        $.ajax({
            url: `rating/${requestParams.type}/${requestParams.action}/`,
            type: 'POST',
            data: requestParams.formData,
            cache: false,
            processData: false,
            contentType: false,
            enctype: 'multipart/form-data',
            success: json => {
                console.log(json);
                evt.target.parentNode.parentNode.querySelector('.positiveComment').innerHTML = json.positive;
                evt.target.parentNode.parentNode.querySelector('.negativeComment').innerHTML = json.negative;
            },
            error: d => {
                console.log('err');
                console.log(d);
            }
        })
    }
}

export {CommentsRating};