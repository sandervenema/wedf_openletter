;(function ($) {
    $("#accordion").accordion({
        collapsible: true,
        animate: false,
        active: false,
        heightStyle: "content",
        activate: function( event, ui ) {
            if(!$.isEmptyObject(ui.newHeader.offset())) {
                $('html:not(:animated), body:not(:animated)').scrollTop(ui.newHeader.offset().top - 10);
            }
        }
    });

    var accordion_options = { collapsible: true, animate: false };
    if ($(window).width() <= 640) {
        accordion_options['active'] = false;
    }
    $("#accordion_forms").accordion(accordion_options);
    $("#signatures_box").accordion({ collapsible: true, animate: false, active: false });
    
    // Language switcher logic
    $('ul.languages > li > a').on('click', function click_language(evt) {
        evt.preventDefault();
        var language_clicked = $(this).data('languageCode');
        $('form#language_form select').val(language_clicked);
        $('form#language_form').submit();
        return false;
    });

    // On mobile devices, move the sign box to just below the statement.
    if ($(window).width() <= 640) {
        var forms = $('.the-forms');
        forms.insertBefore('.the-letter');
    }

}(jQuery));
