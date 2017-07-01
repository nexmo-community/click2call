
$(document).ready(function(){
  $('.notification .delete').click(function(){
    $('.notification').addClass('is-hidden')
  })

  $('#send').click(function() {
    $('.notification').addClass('is-hidden')
    $('input').removeClass('is-danger')

    var data = {
      'name': $('#name').val(),
      'number': $('#number').val()
    }

    if(data.name && data.number) {
      $('.control').addClass('is-disabled')

      $.post('/call', JSON.stringify(data), function(response){
        $('.control').removeClass('is-disabled')

        if(response.status === "started") {
          $('#notification-number').html(data.number)
          $('#notification-success').removeClass('is-hidden')
          $('#name').val("")
          $('#number').val("")
        } else {
          $('#notification-failure').removeClass('is-hidden')
        }
      }).fail(function() {
        $('#notification-failure').removeClass('is-hidden')
      })
    } else {
      // missing a 1 or more required values
      if(!$('#name').val()) {
        $('#name').addClass('is-danger')
      }
      if(!$('#number').val()) {
        $('#number').addClass('is-danger')
      }
    }
  })
})
