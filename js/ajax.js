/**
 * Created by Paras on 1/17/2017.
 */
$(function () {
    $('#search').keyup(function () {
        $.ajax({
            type:"POST",
            url:"/movies/search/",
            data:{
                'search_text': $('#search').val(),
                'csrfmiddlewaretoken':$("input[name=csrfmiddlewaretoken]").val()
            },
            success:searchSuccess,
            dataType:'html'
            });
    });

});

function searchSuccess(data,textStatus,jqXHR) {
    $('#search_result').html(data)
}