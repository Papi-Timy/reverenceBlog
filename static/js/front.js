$(function () {
    lightbox.option({
      'resizeDuration': 200,
      'wrapAround': true
  });

  /* ===============================================================
         HUMBERGUR MENU ACTIVATE
      =============================================================== */
    $('.navbar-toggler').on('click dblclick', function () {
        $(this).toggleClass('active');
    });
    
    $('.set-bg').each(function () {
        var bg = $(this).data('setbg');
        $(this).css('background-image', 'url(' + bg + ')');
    });
});
