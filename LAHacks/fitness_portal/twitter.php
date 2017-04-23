<!DOCTYPE html>
<html lang="en">
<head>
<?php include('header.php');?>
</head>
<body>
    <div id="single">
<!--home-->
        <div data-target="home" class="contact-w3layouts" id="home">
		<!-- header -->
<?php include('navbar.php');?>
				<div class="container"></div>
				<div class="container">
				<h3 class="title-w3-agile"><span style="color:white;">TWITTER ANALYTICS</span></h3>
			<!-- banner-slider -->
			<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
<script type="text/javascript" src="sentiment.json" name="data"></script>
<script type="text/javascript">
window.onload = function () {
var mydata;
		  var xhttp = new XMLHttpRequest();
		  xhttp.onreadystatechange = function() {
			if (this.readyState == 4 && this.status == 200) {
			 console.log(this.responseText);
		   mydata=JSON.parse(this.responseText);
	var pos=(mydata.sentiment_details.positive/(mydata.sentiment_details.positive+mydata.sentiment_details.negative))*100;
	var neg=(mydata.sentiment_details.negative/(mydata.sentiment_details.positive+mydata.sentiment_details.negative))*100;
	
	var chart = new CanvasJS.Chart("chartContainer",
	{
		backgroundColor: "rgb(0,0,0,0.3)",

        animationEnabled: true,
		legend: {
			verticalAlign: "bottom",
			horizontalAlign: "center"
		},
		theme: "theme2",
		 legend : {
			fontColor: "white",
		},
		data: [
		{        
			type: "pie",
			indexLabelFontFamily: "Garamond",       
			indexLabelFontSize: 20,
			indexLabelFontWeight: "bold",
			startAngle:0,
			indexLabelFontColor: "MistyRose",       
			indexLabelLineColor: "darkgrey", 
			indexLabelPlacement: "inside", 
			toolTipContent: "{name}: {y} %",
			showInLegend: true,
			indexLabel: "#percent%", 
			dataPoints: [
				{  y: pos, name: "Positivity in your Tweets", legendMarkerType: "triangle"},
				{  y: neg, name: "Negativity in your Tweets", legendMarkerType: "square"},
			]
		}
		]
	});
	chart.render();
	}
	};
	xhttp.open("GET", "sentiment.json", true);
		  xhttp.send();
		  console.log("Request Sent!");
}
</script>
<script type="text/javascript" src="http://canvasjs.com/assets/script/canvasjs.min.js"></script>
		<div id="chartContainer" style="height: 500px; width: 50%;margin:auto;"></div>	<div class="clearfix"></div>
		<!-- //banner-slider -->
			</div>
			
<?php include('below.php');?>