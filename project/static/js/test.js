$(document).ready(function () {
    $(document).ready(function () {
        $('.container-fluid').on('click', '.add_subparam', function () {
            var html = document.getElementById('subparam_1').innerHTML;
            document.getElementById('result').innerHTML = html;
        });
    });
    $(".container-fluid").on('click', '#submit', function () {
        var subparams = $("#" + $(params[i]).attr("id") + " .subparam");
        var data_subparams = [];
        for (j = 0; j < subparams.length; j++) {
            var tmp = {
                "name": $(subparams[j]).find("#sub_text").val(),
                "type_subparam": $(subparams[j]).find("#type_subparam").val(),
            };
            data_subparams.push(tmp);
        }
        var result = {"subparams": data_subparams, csrfmiddlewaretoken: '{{ csrf_token }}'};
        $.ajax({
            type: "post",
            url: "intervention/add/",
            data: result,
            success: function (response) {
                alert("Success");
                window.location = "http://127.0.0.1:8000/fls/comp/{{ comp.id }}";
            }
        });
    });
});