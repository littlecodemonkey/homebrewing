#!"C:\xampp\perl\bin\perl.exe"
#!/usr/bin/perl

########################################
# GLOBALS
########################################
use CGI;                                                                                                                                          
use website_functions;
use calculations;
use DateTime;

my %GET_data = website_functions::getData(); # GET form data
my $volume = website_functions::validateNumber($GET_data{volume});
my $temp = website_functions::validateNumber($GET_data{temp});
my $desiredCO2 = website_functions::validateNumber($GET_data{vol_co2});


########################################
# MAIN
########################################
invalid_entry($volume,$temp,$desiredCO2) if ($volume =~ /INVALID/ || $temp =~ /INVALID/ || $desiredCO2 =~ /INVALID/);
my $volume = $GET_data{'volType'} =~ /^L/i ? calculations::convertMeasurement('L->Gal',$volume) : $volume;
my $temp = $GET_data{'volTempType'} =~ /^C/i ? calculations::convertMeasurement('C->F',$temp) : $temp;
my $priming_sugar_g = calculations::priming_sugar($desiredCO2,$volume,$temp);
my $priming_sugar_oz = calculations::convertMeasurement('g->oz',$priming_sugar_g);
my $force_carbonation_psi = calculations::force_carbonation($desiredCO2,$volume,$temp);

my $OUTPUT = "
        <link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\">
        <div class=\"answerText\">
        
            <!-- Volume: $volume $GET_data{volType}<br />
            Temperature: $temp $GET_data{volTempType}<br />
            Volumes of CO2: $desiredCO2<br /> -->
            <span class=\"answerHeader\">Bottling</span><br />
            Priming sugar needed: <b>$priming_sugar_oz</b> ounces (<b>$priming_sugar_g</b> grams)<br />
            <br />
            <span class=\"answerHeader\">Kegging</span><br />
            Set pressure to: <b>$force_carbonation_psi</b> psi<br />
        </div>"; 

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
        Volume: <b>$volume</b><br />
        Temperature: <b>$temp</b><br />
        Volumes of CO2: <b>$desiredCO2</b><br />
        </p>";
        website_functions::createPage($OUTPUT);
        exit(0);
}
