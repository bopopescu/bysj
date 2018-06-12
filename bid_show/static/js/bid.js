$("#inputtable").bind('input propertychange ', function(){
        var searchText=$(this).val();
        //如果当前搜索内容为空，无须进行查询
        var temphtml = "";
        $.ajax({
            cache:false,
            type:"get",
            dataType:"json",
            url:"/bid/suggest.html?q="+searchText,
            // data:"search="+searchText,
            async:true,
            dataType: 'json',
            success: function(data){
                 for(var i=0;i < data.length;i++){
                     temphtml += '<option>'+data[i]+'</option>'
                 }
                 $("#datalist").html("")
                 $("#datalist").append(temphtml)
                if(data.length == 0){
                     $("#datalist").hide()
                }else {
                    $("#datalist").show()
                }
            }
        });
    });
$("#trendfold").click(function () {
 var key_word = $('#inputtable').val();
 var temphtml = "";
$.ajax({
    cache:false,
    type:"get",
    url:"/bid/drawpicture?q="+key_word,
    // data:"search="+searchText,
    async:true,
    success: function(data){
        // alert(data);
        temphtml = "<img class='plt-img' src='/static/pic/a.jpg'></img>";
        $(".show-img").html("");
        $(".show-img").append(temphtml);
        $(".show-img").show();
    }
 })
});
$("#trendzhu").click(function () {
 var key_word = $('#inputtable').val();
 var temphtml = "";
 $.ajax({
    cache:false,
    type:"get",
    url:"/bid/drawpicture?q="+key_word,
    // data:"search="+searchText,
    async:true,
    success: function(data){
        // alert(data);
        temphtml = "<img class='plt-img' src='/static/pic/b.jpg'></img>";
        $(".show-img2").html("");
        $(".show-img2").append(temphtml);
        $(".show-img2").show();
    }
 })
});
