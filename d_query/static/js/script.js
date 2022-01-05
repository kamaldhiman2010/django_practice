<script>
window.setTimeout(function() {
   $(".messages").fadeTo(400, 0).slideUp(400, function(){
     $(this).remove();
  });
}, 30);
</script>