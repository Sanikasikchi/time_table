
// JavaScript Document
$(document).ready(function() {

$(function(){
	'use strict';
	
	// call to windows scroll
	// $('html,body')
	// 	.animate({ scrollTop: 1 }, 0)
	// 	.animate({ scrollTop: 0 }, 0);
	
	// fix anchor position
	var anchor = location.hash;
	if (anchor){
		history.pushState(null, null, ' ');
		setTimeout(function(){
			scrollToAnchor( $(anchor) );
		}, 50);
	}
	
	var mainOffset = 0;
	var $header = $('#header');
	var $menu = $('#menu ul');
	var $menuItems = $('li:not(.mobile) a[href*="#"]', $menu);
	//var $reviews = $('#testimonials li');
	
	$(window).scroll();
	
	$(window).scroll(function(){
		var scrollTop = $(window).scrollTop();
		//var viewportBottom = scrollTop + $(window).height();
		
		if (scrollTop > 0) {
			$header.addClass('sticky');
		}else {
			$header.removeClass('sticky');
		}
		
		// set active menu item
		$menuItems.each(function (ind) {
			var padReset=ind>0?76:66;
			var $obj = $(this);
			var href = $obj.attr('href');			
			var $ref = $( href.substring(href.indexOf('#')) );			
			if($('div').is($ref)){
				var refTop=$ref.offset().top-padReset;
				if (refTop <= scrollTop + mainOffset && (refTop) + $ref.height() > scrollTop + mainOffset) {
					$('#menu a').not($obj).removeClass('active');
					$obj.addClass('active');
				}else{
					$obj.removeClass('active');
				}
			}
		});
		
	
	});
			
  	
	$(window).resize(function(){
		if( $('#btnMenu').is(':visible') ){
			$menu.hide();
		}else{
			$menu.show();
		}
	});
	
	$('#btnMenu a').click(function(){
		$menu.slideToggle();
		return false;
	});
	
	$('li a', $menu).click(function(){
		var href = $(this).attr('href');
		var hash = href.indexOf('#');
		var $ref = hash !== -1 ? $( href.substring(hash) ) : '';

		if($('div').is($ref)){
			$(this).addClass('active');
			scrollToAnchor($ref);
		}else{
			return;
		}
		return false;
	});
	
	function scrollToAnchor($obj) {
		var otop = $obj.offset().top;
		if ($(window).scrollTop() !== otop) {
			$('html, body').animate({
				scrollTop: otop - mainOffset / 2
			}, 1000);
		}
		return false;
	}
	
		 $('#mainBox').click(function() {
		 if($('#btnMenu').is(':visible')){
     		$('#menu ul').slideUp();
		 }
	 });
	

	$('#menu ul li').click(function() {
	   if($('#btnMenu').is(':visible')){
     		$('#menu ul').slideUp(1000);
		 }
});
	
	$('#menu ul li a').click(function() {
	   if($('#btnMenu').is(':visible')){
     		$('#menu ul').slideUp(1000);
		 }
});
	
	
});
	
	
		$('.srchWrp a.srch').click(function(){
		$('.srchWrp span').addClass('show');
	});
	
	$('.srchWrp a.close').click(function(){
		$('.srchWrp span').removeClass('show');
	});
	
	$('.responsive').slick({
        dots: true,
        infinite: true,
        speed: 500,
        slidesToShow: 1,
        slidesToScroll: 1,
		autoplay: true,
	  	autoplaySpeed: 3000
    });
	
	});