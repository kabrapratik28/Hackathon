    <div class="footer-w3layouts">
				<div class="container">
				<div class="agile-copy">
					<p>© 2017 Gym Workout. All rights reserved | Design by <a href="http://w3layouts.com/">W3layouts</a></p>
				</div>
					<div class="clearfix"></div>
				</div>
			</div>
<!-- //footer -->
</div>
	
	
	<script type="text/javascript" src="js/jquery-2.1.4.min.js"></script>

	<script src="js/responsiveslides.min.js"></script>
							<script>
								// You can also use "$(window).load(function() {"
								$(function () {
								  // Slideshow 3
								  $("#slider3").responsiveSlides({
									auto: true,
									pager:false,
									nav:true,
									speed: 500,
									namespace: "callbacks",
									before: function () {
									  $('.events').append("<li>before event fired.</li>");
									},
									after: function () {
									  $('.events').append("<li>after event fired.</li>");
									}
								  });
							
								});
							 </script>
<!-- Owl-Carousel-JavaScript -->
	<script src="js/owl.carousel.js"></script>
	<script>
		$(document).ready(function() {
			$("#owl-demo").owlCarousel ({
				items : 3,
				lazyLoad : true,
				autoPlay : true,
				pagination : true,
			});
		});
	</script>
	<!-- //Owl-Carousel-JavaScript -->  
	<!-- //galley-effect-JavaScript -->
	<script src="js/jquery.tools.min.js"></script>
				<script src="js/jquery.mobile.custom.min.js"></script>

	<script src="js/jquery.cm-overlay.js"></script>
				<script>
					$(document).ready(function(){
						$('.cm-overlay').cmOverlay();
					});
				</script>
	<!-- //galley-effect-JavaScript -->

	<script type="text/javascript" src="js/jquery.easing.min.js"></script>
	<script src="js/jquery.singlefull.js"></script>
    <script type="text/javascript">
    $(document).ready(function() {
        $("#single").singlefull({
            speed: 1000,
            loopScroll:true,
            loopTop:false,
            loopBottom:true
        });
        // Just a javascript alignment to the content
        function alignContent() {
            var windowHeight = $(window).height();

            $('.content-resizer').each(function() {
                contentHeight = $(this).height();
                $(this).css('top', (windowHeight / 2) - (contentHeight / 2));
            });

            $('.alt-img').html($("#img-example").attr('src'));
        }

        // Execute the function
        alignContent();

        // Bind the function to the window.onresize
        $(window).bind("resize", function() {
            alignContent();
        });


    });
    </script>
	<script type="text/javascript" src="js/bootstrap-3.1.1.min.js"></script>
</body>
</html>

