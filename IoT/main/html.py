
html_template_A = """ <!DOCTYPE html>
<html><head><title>IoT Weather Station</title>
<meta name='viewport' content='width=device-width, initial-scale=1'>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
<link rel="apple-touch-icon-precomposed" sizes="57x57" href="apple-touch-icon-57x57.png" />
<style>.center-div { margin: auto; width: 50%; border: 3px solid green; padding: 10px;}
.live-icon {display: inline-block;position: relative;top: calc(50% - 5px);background-color: red;
            width: 10px;height: 10px;margin-left: 20px;border: 1px solid rgba(black, 0.1);
            border-radius: 50%;z-index: 1;
  &:before {content: "";display: block;position: absolute;background-color: rgba(red, 0.6);
            width: 100%;height: 100%;border-radius: 50%;animation: live 2s ease-in-out infinite;z-index: -1;}}
@keyframes live {0% {transform: scale(1, 1);}100% {transform: scale(3.5, 3.5);background-color: rgba(red, 0);}}
body {background-color: lightskyblue;}
footer {text-align: center;padding: 1px;background-color: DarkSalmon;color: white;}
h2 {font-size: 30px;}
h3 {font-size: 20px;}
h2, h3 {width: 50%;height: 50px;margin: 0;padding: 0;display: inline;}</style>
<script src=\"https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js\"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script></head>
<body><h1 class="center-div">&#x26C5; Realtime Weather Station Panel </h1>
<a href="#" class="btn btn_live">Live Streaming Data<span class="live-icon"></span></a>
<h3 align="float" id="datetime"></h3> <!-- Live Timestamp -->"""


html_template_C = """
<!------------------- Timer Script ---------------------->
<script>window.onload = function() {
    setInterval(function(){
        var date = new Date();
        var displayDate = date.toLocaleDateString();
        var displayTime = date.toLocaleTimeString();
        document.getElementById('datetime').innerHTML = displayDate + " " + displayTime;
    }, 1000); // 1000 milliseconds = 1 second
}</script>
<footer><p> © 2025. All Rights Reserved. &#128578; A.G. </p></footer></body></html>
"""


def create_html_page(dataframe : list=None):

    html_template_B = f"""
                    <!-- This is a Frame for 1 single sensor data -->
                    <p></p>
                    <h2> ------------ BME DataFrame --------------- </h2>
                    <p></p>
                    <div style="clear: both">
                        <h3 style="float: left">Temperature: </h3>
                        <h3 style="float: right" id=\"temp\">{str(dataframe[0])} °C</h3>
                    </div>
                    <div style="clear: both">
                        <h3 style="float: left">Humidity: </h3>
                        <h3 style="float: right" id=\"hum\">{str(dataframe[0])} %</h3>
                    </div>
                    <div style="clear: both">
                        <h3 style="float: left">Pressure: </h3>
                        <h3 style="float: right" id=\"pres\">{str(dataframe[0])} hPa</h3>
                    </div>
                    <div style="clear: both">
                        <h3 style="float: left">Gas: </h3>
                        <h3 style="float: right" id=\"gas\">{str(dataframe[0])} KOhms</h3>
                    </div>
                    <div style="clear: both">
                        <h3 style="float: left">Altitude @ Sea-level: </h3>
                        <h3 style="float: right" id=\"sea_alt\">{str(dataframe[0])} meters</h3>
                    </div><p>.</p><hr />
                    <!------------------- Frame Ends ---------------------->

                    <!-- This is a Frame for 1 single sensor data -->
                    <p></p>
                    <h2> ------------ GPS DataFrame --------------- </h2>
                    <p></p>
                    <div style="clear: both">
                        <h3 style="float: left">Latitude  : </h3>
                        <h3 style="float: right" id=\"lat\">{str(dataframe[0])}</h3>
                    </div>
                    <div style="clear: both">
                        <h3 style="float: left">Longitude  : </h3>
                        <h3 style="float: right" id=\"long\">{str(dataframe[0])}</h3>
                    </div>
                    <div style="clear: both">
                        <h3 style="float: left">Altitude: </h3>
                        <h3 style="float: right" id=\"alt\">{str(dataframe[0])} meters</h3>
                    </div>
                    <div style="clear: both">
                        <h3 style="float: left">Timestamp: </h3>
                        <h3 style="float: right" id=\"time\">{str(dataframe[0])} UTC</h3>
                    </div>
                    <div style="clear: both">
                        <h3 style="float: left">Date: </h3>
                        <h3 style="float: right" id=\"date\">{str(dataframe[0])}</h3>
                    </div><p>.</p><hr />
                    <!------------------- Frame Ends ---------------------->

                    <!-- This is a Frame for 1 single sensor data -->
                    <p></p>
                    <h2> ------------ AQI DataFrame --------------- </h2>
                    <p></p>
                    <div style="clear: both">
                        <h3 style="float: left">Voltage: </h3>
                        <h3 style="float: right" id=\"vlt\">{str(dataframe[0])} Volts</h3>
                    </div>
                    <div style="clear: both">
                        <h3 style="float: left">Dust Density: </h3>
                        <h3 style="float: right" id=\"dd\">{str(dataframe[0])} mg x m3</h3>
                    </div>
                    <div style="clear: both">
                        <h3 style="float: left">PPM: </h3>
                        <h3 style="float: right" id=\"ppm\">{str(dataframe[0])} ppm</h3>
                    </div><p>.</p><hr />
                    <!------------------- Frame Ends ---------------------->

                    <!-- This is a Frame for 1 single sensor data -->
                    <p></p>
                    <h2> ------------ TOF DataFrame --------------- </h2>
                    <p></p>
                    <div style="clear: both">
                        <h3 style="float: left">Lidar Distance: </h3>
                        <h3 style="float: right" id=\"tof\">{str(dataframe[0])} meters</h3>
                    </div><p>.</p><hr />
                    <!------------------- Frame Ends ---------------------->

                    <!-- This is a Frame for 1 single sensor data -->
                    <p></p>
                    <h2> ------------ UV DataFrame --------------- </h2>
                    <p></p>
                    <div style="clear: both">
                        <h3 style="float: left">UV-Index: </h3>
                        <h3 style="float: right" id=\"uv\">{str(dataframe[0])} mW/cm^2</h3>
                    </div><p>.</p><hr />
                    <!------------------- Frame Ends ---------------------->

                    <!-- This is a Frame for 1 single sensor data -->
                    <p></p>
                    <h2> ------------ MPU DataFrame --------------- </h2>
                    <p></p>
                    <div style="clear: both">
                        <h3 style="float: left">Acceleration X-axis: </h3>
                        <h3 style="float: right" id=\"acx\">{str(dataframe[0])}</h3>
                    </div>
                    <div style="clear: both">
                        <h3 style="float: left">Acceleration Y-axis </h3>
                        <h3 style="float: right" id=\"acy\">{str(dataframe[0])}</h3>
                    </div>
                    <div style="clear: both">
                        <h3 style="float: left">Acceleration Z-axis: </h3>
                        <h3 style="float: right" id=\"acz\">{str(dataframe[0])}</h3>
                    </div>
                    <div style="clear: both">
                        <h3 style="float: left">Gyroscope X-axis: </h3>
                        <h3 style="float: right" id=\"gyx\">{str(dataframe[0])}</h3>
                    </div>
                    <div style="clear: both">
                        <h3 style="float: left">Gyroscope X-axis: </h3>
                        <h3 style="float: right" id=\"gyy\">{str(dataframe[0])}</h3>
                    </div>
                    <div style="clear: both">
                        <h3 style="float: left">Gyroscope X-axis: </h3>
                        <h3 style="float: right" id=\"gyz\">{str(dataframe[0])}</h3>
                    </div><p>.</p><hr />
                    <!------------------- Frame Ends ---------------------->

                    <!-- This is a Frame for 1 single sensor data -->
                    <p></p>
                    <h2> ------------ General DataFrame --------------- </h2>
                    <p></p>
                    <div style="clear: both">
                        <h3 style="float: left">Battery Percentage  [%]: </h3>
                        <h3 style="float: right" id=\"batt\">{str(dataframe[0])} %</h3>
                    </div>
                    <div style="clear: both">
                        <h3 style="float: left">Load Current: </h3>
                        <h3 style="float: right" id=\"current\">{str(dataframe[0])} mAm3</h3>
                    </div>
                    <div style="clear: both">
                        <h3 style="float: left">IP Address  : </h3>
                        <h3 style="float: right" id=\"ip\">{str(dataframe[0])}</h3>
                    </div>
                    <div style="clear: both">
                        <h3 style="float: left">System Info: </h3>
                        <h3 style="float: right" id=\"status\">{str(dataframe[0])}</h3>
                    </div><p>.</p><hr />
                    <div style="clear: both">
                        <h3 style="float: left">Status: </h3>
                        <h3 style="float: right" id=\"status\">{str(dataframe[0])}</h3>
                    </div><p>.</p><hr />
                    <!------------------- Frame Ends ---------------------->
    """
    html_template = html_template_A + html_template_B + html_template_C
    return html_template