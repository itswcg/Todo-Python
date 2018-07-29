$(function () {
    $("main").on("mouseenter", "ul.list-group > li", function (event) {
        var li = $(this);
        $(li).children('.remove-Todo').show();
    });


    $("main").on("mouseleave", 'ul.list-group > li', function (event) {
        var li = $(this);
        $(li).children('.remove-Todo').hide();
    });

    $("main").on("mouseenter", "ul.list-group > li", function (event) {
        var li = $(this);
        $(li).children('.edit-Todo').show();
    });


    $("main").on("mouseleave", 'ul.list-group > li', function (event) {
        var li = $(this);
        $(li).children('.edit-Todo').hide();
    });

    $('ul.list-group').on('click', '.remove-Todo', function () {
        var li = $(this).closest('li');
        var todo = $(li).attr('todo-id');
        $.ajax({
            url: '/del/',
            data: {
                'todo-id': todo
            },
            type: 'get',
            cache: false,
            success: function (data) {
                $(li).fadeOut(200, function () {
                    $(li).remove();
                });

            }
        });
    });

});
