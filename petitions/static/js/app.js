;(function ($) {
    
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
        var panel = $('.panel');
        panel.insertBefore('hr:first');
    }

}(jQuery));
