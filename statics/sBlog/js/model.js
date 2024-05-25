$('.modal-content').resizable({
    //alsoResize: ".modal-dialog",
    minHeight: 300,
    minWidth: 300
  });
  $('.modal-dialog').draggable();

  $('#myModal').on('show.bs.modal', function() {
    $(this).find('.modal-body').css({
      'max-height': '100%'
    });
  });