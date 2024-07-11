<script type="text/javascript">
$(function(){
  var Address;
  var add;
  var global_address;
  $(".profile").bind('click',this,function()
  {
    alert('test');
    Address1=$(this).attr("name");
    Address="index.php/"+Address1;
    add=window.location.origin;
    // global_address=add+"localhost/project2/index.php"+Address;
    global_address=add+"/project2/"+ Address;
    // global_address=add+"/project2/index.php/";
    alert(global_address);
    $.ajax({
      url : global_address,
      // url : global_address+"/Master_con",
      // alert(global_address);
      // url : "<?php echo base_url() ?>" + "index.php/Home/ProductList",
      type:"POST",
      cache:false,
      asycn:false,
      data: {value:Address},
      dataType: 'html',
      success: function(data,status)
      {
        $('#load').html("data");
        $('#load').html(data);
      },
      error:function(status,data)
      { 
        alert('fail');
      }
    });
  });
});
</script>