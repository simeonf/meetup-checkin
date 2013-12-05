$(function(){
  var hide = function(){
      if($("#show_absent").prop('checked')){
          $(".present_1").fadeOut();
      }
  };
  // default to showing only the absent
  $("#show_absent").prop('checked', true);
  // hide all the present records, we don't need to see them
  hide();
  $("#show_absent").change(hide);
  $("#show_all").change(function(){
      $(".present_1").show();
  });
  $filter = $("#filter");
  $filter.bind('keyup', function(){
      var val = $filter.val();
      var all = $("#show_all").prop('checked');
      if(val.length > 0){
          $("a.title").hide().each(function(){
              var selector = ".lowername:contains('" + val.replace(/'|"/g, '').toLowerCase() + "')";
              // Show the user if they're not yet marked present or if we're showing everybody
              if($(this).find(selector).length > 0 && ($(this).hasClass("present_0") || all) ){
                  $(this).show();
                  }
          });
      }else{
          $("a.title").show();
          hide();
      }
  });
  // attach event to each member radio button
  $("a.title :radio").change(function(){
     var data = $(this).val().split('_');
     var value = data[0]; // value: 1 or 0 for yes or no
     var id = data[1]; // id - the db key
     $("#rsvp_" + id).toggleClass("present_1 present_0");
     hide();
     $.jGrowl("Updated " + $("#name_" + id).text());
     $.post("/ajax", {'id': id, 'present': value}, function(){
             $("#stats").load('/ajax/stats');
         });
  });
  // globally handle ajax failure
  $(document).ajaxError(function(){
      $.jGrowl("There was an error communicating with the server. Reload the page.");
      });
    
});

