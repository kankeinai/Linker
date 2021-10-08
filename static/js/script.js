$(document).ready(function(){
    $('.header_burger').click(function(event){
        $('.header_burger, .header_menu').toggleClass('active');
        $('body').toggleClass('lock');
    });
    $('.more').click(function(event){
        var attr = "#"+String($(this).attr('id'))
        $(attr+'.event-detail').toggleClass('active');
        $('body').toggleClass('lock active');
    });   
    $('.closer').click(function(event){
        var attr = "#"+String($(this).attr('id'))
        $(attr+'.event-detail').toggleClass('active');
        $('body').toggleClass('lock active');
    });
});



