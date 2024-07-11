$('#searchKeyword').on('keyup keypress',function (e) {
    if(e.type == 'keypress'){
       if(e.keyCode == 13){
            return false;
        }
    }else{
    	var all=$('.show').width();
        var str = $(this).val();
    	var suggestList=$("#searchList");
        var strlen = str.length;
        if(strlen=="0")//if no keyword is there then hide the poup
            suggestList.hide();
        if(strlen<3){//minimum length should be 3 to search
            return false;
        }else{
    		suggestList.css({left:all})
            $.ajax({
                type: "get",
                url: "/search?keyword="+str,
                success: function (data) {
                    //console.log(data);
                    suggestList.html(data);
                    suggestList.show();
                }
            });
        }
    }
});
$(document).on("click", '.close', function() {
    $("#searchList").hide();
});
$(document).on("click", '.name-price', function() {
    // console.log('Here');
    $("#searchList").hide();
});
