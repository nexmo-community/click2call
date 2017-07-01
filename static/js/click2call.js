
$(document).ready(function(){
  $('.notification .delete').click(function(){
    $('.notification').addClass('is-hidden')
  })

  $('#send').click(function() {
    $('.notification').addClass('is-hidden')

    var data = {
      'name': $('#name').val(),
      'number': $('#number').val()
    }

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
    })
  })
})
