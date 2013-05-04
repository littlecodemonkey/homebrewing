#!/usr/bin/perl
#!"C:\xampp\perl\bin\perl.exe"

########################################
# GLOBALS
########################################
use CGI;                                                                                                                                          
use website_functions;
use calculations;
use DateTime;

my $OUTPUT;
my %GET_data     = website_functions::getData(); # GET form data
my $batch_size   = website_functions::validateNumber($GET_data{'batch_size'});
my $boil_length  = website_functions::validateNumber($GET_data{'boil_length'});
my $evap_rate    = website_functions::validateNumber($GET_data{'evap_rate'});
invalid_entry($volume,$temp,$desiredCO2) if ($batch_size =~ /INVALID/ || $boil_length =~ /INVALID/ || $evap_rate =~ /INVALID/);


# Calculating pre-wort boil water
if ( $GET_data{'brewVolType'} =~ /^Gal/ ) {
    $batch_sizeGal = $batch_size;
    $batch_sizeL =  calculations::convertMeasurement('Gal->L',$batch_sizeGal);
}
else {
    $batch_sizeL = $batch_size;
    $batch_sizeGal =  calculations::convertMeasurement('L->Gal',$batch_sizeL);
}
my $pre_wort_boilGal = calculations::boil_loss($batch_sizeGal,$boil_length,$evap_rate);
my $pre_wort_boilL =  calculations::convertMeasurement('Gal->L',$pre_wort_boilGal); 






$OUTPUT .= "
<html>
<head>

<script type=\"text/javascript\">
    var mins = $boil_length;
    var secs = mins * 60;
    var hopmins1 = $GET_data{'bittering1'};
    var hopsecs1 = hopmins1 * 60;
    var hopmins2 = $GET_data{'bittering2'};
    var hopsecs2 = hopmins2 * 60;
    var hopmins3 = $GET_data{'flavor1'};
    var hopsecs3 = hopmins3 * 60;
    var hopmins4 = $GET_data{'flavor2'};
    var hopsecs4 = hopmins4 * 60;
    var hopmins5 = $GET_data{'aroma1'};
    var hopsecs5 = hopmins5 * 60;
    var hopmins6 = $GET_data{'aroma2'};
    var hopsecs6 = hopmins6 * 60;
    var t, count;


    function countdown() {
        clearTimeout(t);
        setTimeout('Decrement()',1000);
    }

    function Decrement() {
        if (document.getElementById) {
            if (seconds < 59) {   // if less than a minute remaining
                document.getElementById(\"minutes\").value = secs;
                document.getElementById(\"hopseconds1\").value = hopsecs1;
                document.getElementById(\"hopseconds2\").value = hopsecs2;
                document.getElementById(\"hopseconds3\").value = hopsecs3;
                document.getElementById(\"hopseconds4\").value = hopsecs4;
                document.getElementById(\"hopseconds5\").value = hopsecs5;
                document.getElementById(\"hopseconds6\").value = hopsecs6;
            } 
            else {
                dMinutes = getminutes();
                dSeconds = getseconds();
                document.getElementById(\"minutes\").value = dMinutes[0];
                document.getElementById(\"seconds\").value = dSeconds[0];
                document.getElementById(\"hopminutes1\").value = dMinutes[1];
                document.getElementById(\"hopseconds1\").value = dSeconds[1];
                document.getElementById(\"hopminutes2\").value = dMinutes[2];
                document.getElementById(\"hopseconds2\").value = dSeconds[2];
                document.getElementById(\"hopminutes3\").value = dMinutes[3];
                document.getElementById(\"hopseconds3\").value = dSeconds[3];
                document.getElementById(\"hopminutes4\").value = dMinutes[4];
                document.getElementById(\"hopseconds4\").value = dSeconds[4];
                document.getElementById(\"hopminutes5\").value = dMinutes[5];
                document.getElementById(\"hopseconds5\").value = dSeconds[5];
                document.getElementById(\"hopminutes6\").value = dMinutes[6];
                document.getElementById(\"hopseconds6\").value = dSeconds[6];
            }
            if (secs >0) { secs--; }
            if (hopsecs1 > 0) { hopsecs1--; }
            if (hopsecs2 > 0) { hopsecs2--; }
            if (hopsecs3 > 0) { hopsecs3--; }
            if (hopsecs4 > 0) { hopsecs4--; }
            if (hopsecs5 > 0) { hopsecs5--; }
            if (hopsecs6 > 0) { hopsecs6--; }
            if (hopsecs6 == 1) { window.alert(\"sometext\"); }
            t = setTimeout('Decrement()',1000);
        }
    }

    function getminutes() {   // minutes is seconds divided by 60, rounded down
        mins = Math.floor(secs / 60);
        hopmins1 = Math.floor(hopsecs1 / 60);
        hopmins2 = Math.floor(hopsecs2 / 60);
        hopmins3 = Math.floor(hopsecs3 / 60);
        hopmins4 = Math.floor(hopsecs4 / 60);
        hopmins5 = Math.floor(hopsecs5 / 60);
        hopmins6 = Math.floor(hopsecs6 / 60);
        return [mins,hopmins1,hopmins2,hopmins3,hopmins4,hopmins5,hopmins6];
    }

    function getseconds() {    // take mins remaining (as seconds) away from total seconds remaining
        var value0 = secs-Math.round(mins *60);
        var value1 = hopsecs1-Math.round(hopmins1 *60);
        var value2 = hopsecs2-Math.round(hopmins2 *60);
        var value3 = hopsecs3-Math.round(hopmins3 *60);
        var value4 = hopsecs4-Math.round(hopmins4 *60);
        var value5 = hopsecs5-Math.round(hopmins5 *60);
        var value6 = hopsecs6-Math.round(hopmins6 *60);
        return [value0,value1,value2,value3,value4,value5,value6];
    }

    function cdpause() {     // pauses countdown
        clearTimeout(t);
    }

    function pauseResume() {
        if (document.getElementById(\"myButton1\").value == \"Pause\") {
            document.getElementById(\"myButton1\").value=\"Resume\";
            cdpause();
        }
        else {
            document.getElementById(\"myButton1\").value=\"Pause\";
            countdown();    
        }
    }

</script>

</head>

<body>
 
<div id=\"timer\">
<input type=\"button\" id=\"myButton1\" name=\"myButton1\" value=\"Pause\" onclick=\"pauseResume()\">
<br /><br />

<table>
<tr><th>Type</th><th>MINS</th><th>SECS</th></tr>
<tr>
    <td>Boil Length:</td>
    <td><input id=\"minutes\" type=\"text\" style=\"width: 26px; border: none; background-color:none; font-size: 16px; font-weight: bold;\"></td>
    <td><input id=\"seconds\" type=\"text\" style=\"width: 26px; border: none; background-color:none; font-size: 16px; font-weight: bold;\"></td>
</tr>";

$OUTPUT .= print_table('bittering1','hopminutes1','hopseconds1');
$OUTPUT .= print_table('bittering2','hopminutes2','hopseconds2');
$OUTPUT .= print_table('flavor1','hopminutes3','hopseconds3');
$OUTPUT .= print_table('flavor2','hopminutes4','hopseconds4');
$OUTPUT .= print_table('aroma1','hopminutes5','hopseconds5');
$OUTPUT .= print_table('aroma2','hopminutes6','hopseconds6');

 $OUTPUT .= "
</div>
<script>
countdown();
</script>

</body>
</html>
";
website_functions::createPage($OUTPUT);


########################################
# SUBROUTINES
########################################
sub invalid_entry {
    my ($volume,$temp,$desiredCO2) = @_;

    my $OUTPUT = "
        <link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\">
        <h3>INVALID ENTRY</h3>
        <p class=\"answerText\">
        Batch Size: <b>$batch_size</b><br />
        Boil length: <b>$boil_length</b><br />
        Evap Rate: <b>$evap_rate</b><br />
        </p>";
        website_functions::createPage($OUTPUT);
        exit(0);
}


sub print_table {
    my ($hashvalue,$minvalue,$secvalue) = @_;
    my $data;
    my $label = $1 if $hashvalue =~ /(.*)\d+/;

    if ($GET_data{$hashvalue}) {
        $data = "<tr>
                <td>$label:</td>
                <td><input id=\"$minvalue\" type=\"text\" style=\"width: 26px; border: none; background-color:none; font-size: 16px; font-weight: bold;\"></td>
                <td><input id=\"$secvalue\" type=\"text\" style=\"width: 26px; border: none; background-color:none; font-size: 16px; font-weight: bold;\"></td>
                </tr>";
    }
    else { $data = "<input id=\"$minvalue\" type=\"hidden\" value=\"0\" /> <input id=\"$secvalue\" type=\"hidden\" value=\"0\" />"; }
    return $data;
}
