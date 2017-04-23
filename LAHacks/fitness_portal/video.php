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
			<h3 class="title-w3-agile"><span style="color:white;">VIDEO ANALYTICS</span></h3>
				<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
<script type="text/javascript" src="data.json" name="data"></script>
	<script type="text/javascript">
	window.onload = function () {
		
		//initial value of dataPoints 
		var dps = [
		{label: "Sadness", y:0},
		{label: "Happiness", y:0},
		{label: "Disgust", y:0},
		{label: "Anger", y: 0},
		{label: "Surprise", y: 0},
		{label: "Fear", y: 0},
		{label: "Contempt", y: 0},
		{label: "Neutral", y: 0}
		];	

		var nameArray=["Sadness","Happiness","Disgust","Anger","Surprise","Fear","Contempt","Neutral"];
		var chart = new CanvasJS.Chart("chartContainer",{			
			axisY: {				
				ticks: {
                                beginAtZero: true
						}
			},		
			legend :{
				verticalAlign: 'bottom',
				horizontalAlign: "center",
				fontColor: "white"
			},
			data: [
			{
				type: "column",	
				bevelEnabled: false,				
				indexLabel: "{y} %",
				dataPoints: dps					
			}
			]
		});

		
		var updateInterval = 1000;	
		
		
		var updateChart = function () {
		var mydata;
		  var xhttp = new XMLHttpRequest();
		  xhttp.onreadystatechange = function() {
			if (this.readyState == 4 && this.status == 200) {
			 console.log(this.responseText);
		   mydata=JSON.parse(this.responseText);
			 
			
			var yVal=[mydata.scores.sadness,mydata.scores.happiness,mydata.scores.disgust,mydata.scores.anger,mydata.scores.surprise,mydata.scores.fear,mydata.scores.contempt,mydata.scores.neutral];
			for (var i = 0; i < dps.length; i++) {
				
				// generating random variation deltaY
				// color of dataPoint dependent upon y value. 
				var semiVal=yVal[i];
				if(semiVal<0.001)
					semiVal=0;
				// updating the dataPoint
				dps[i] = {label: nameArray[i] , y:semiVal, color: "#FF2500"};

			};

			chart.render();
			
			
			}
		  };
		  xhttp.open("GET", "data.json", true);
		  xhttp.send();
		  console.log("Request Sent!");
			  
			  
			
		};
		
		updateChart();		

		// update chart after specified interval 
		console.log("Setting Interval");
		setInterval(function(){updateChart()}, updateInterval);
		console.log("Interval Set");


	}
	</script>
	<script type="text/javascript" src="http://canvasjs.com/assets/script/canvasjs.min.js"></script>
<div id="chartContainer" style="height: 500px; width: 100;">
	</div>
			</div>
        </div>
<!--//about-->
<!--section3-->


<!--//section5-->
<!--section6-->

<!--//membership-->
<!--contact-->

<!--//contact-->
<!-- //footer -->

<?php include('below.php');?>