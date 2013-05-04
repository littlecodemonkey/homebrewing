#!/usr/bin/perl
#!"C:\xampp\perl\bin\perl.exe"

########################################
# GLOBALS
########################################
use CGI;                                                                                                                                          
use website_functions;
use calculations;


my %GET_data = website_functions::getData(); # GET form data
my $Final = website_functions::validateNumber($GET_data{FG});
my $Original = website_functions::validateNumber($GET_data{OG});
my $OriginalTemp = website_functions::validateNumber($GET_data{OGtemp});
my $FinalTemp = website_functions::validateNumber($GET_data{FGtemp});
my ($OG_plato,$FG_plato,$OG_SG,$FG_SG,$OG_tempF,$FG_tempF);


########################################
# MAIN
########################################
invalid_entry($Original,$Final) if ( $Final =~ /INVALID/ || $Original =~ /INVALID/ );

if ( $GET_data{'gravTempType'} =~ /^F/i ) {
    $OG_tempF = $OriginalTemp;
    $FG_tempF = $FinalTemp;
    $OG_tempC = calculations::convertMeasurement('F->C',$OriginalTemp);
    $FG_tempC = calculations::convertMeasurement('F->C',$FinalTemp);
}
else {
    $OG_tempC = $OriginalTemp;
    $FG_tempC = $FinalTemp;
    $OG_tempF = calculations::convertMeasurement('C->F',$OriginalTemp);
    $FG_tempF = calculations::convertMeasurement('C->F',$FinalTemp);
}

if ( $GET_data{'gravType'} =~ /^Plato/i ) {
    $OG_SG = calculations::convertMeasurement('Plato->SG',$Original);
    $OG_SG = calculations::hydrometer_temp_correction($OG_tempF,$OG_SG);
    $OG_plato = calculations::convertMeasurement('SG->Plato',$OG_SG);

    $FG_SG = calculations::convertMeasurement('Plato->SG',$Final);
    $FG_SG = calculations::hydrometer_temp_correction($FG_tempF,$FG_SG);
    $FG_plato = calculations::convertMeasurement('SG->Plato',$FG_SG);
}
else {
    $OG_SG = $Original;
    $OG_SG = calculations::hydrometer_temp_correction($OG_tempF,$OG_SG);
    $OG_plato = calculations::convertMeasurement('SG->Plato',$OG_SG);

    $FG_SG = $Final;
    $FG_SG = calculations::hydrometer_temp_correction($FG_tempF,$FG_SG);
    $FG_plato = calculations::convertMeasurement('SG->Plato',$FG_SG);
}


my $ABV = calculations::abv($OG_SG,$FG_SG);
my $ABW = calculations::abw($OG_SG,$FG_SG);
my $apparent_attenuation = calculations::apparent_attenuation($OG_plato,$FG_plato);
my $calories = calculations::calories($OG_SG,$FG_SG);
my $real_extract = calculations::real_extract($OG_plato,$FG_plato);
my $real_attenuation = calculations::real_attenuation($OG_plato,$real_extract);

my $OUTPUT = "
    <link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\">
    <div class=\"answerText\">
        Entered Original: $Original $GET_data{'gravType'}<br />
        Entered Final: $Final $GET_data{'gravType'}<br />
        OG temp: ${OG_tempF}F (${OG_tempC}C)<br />
        FG temp: ${FG_tempF}F (${FG_tempC}C)<br />
        <br />
        Actual OG (corrected for temperature): <b>$OG_SG SG</b> ($OG_plato plato)<br />
        Actual FG (corrected for temperature): <b>$FG_SG SG</b> ($FG_plato plato)<br />
        <span class=\"answerHeader\"></span><br />
        ABV: <b>$ABV</b>% alcohol by volume<br />
        ABW: <b>$ABW</b>% alcohol by weight<br />
        Apparant attenuation: <b>${apparent_attenuation}%</b><br />
        Real attenuation: <b>${real_attenuation}%</b><br />
        Real extract: <b>$real_extract</b><br />
        Calories: <b>$calories</b> per 12 oz bottle<br />
    </div>"; 
    website_functions::createPage($OUTPUT);


########################################
# SUBROUTINES
########################################
sub invalid_entry {
    my ($OG,$FG) = @_;

    my $OUTPUT = "
        <link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\">
        <h3>INVALID ENTRY</h3>
        <p class=\"answerText\">
        Original Gravity: <b>$OG</b> $GET_data{OGgravType}<br />
        Final Gravity: <b>$FG</b> $GET_data{FGgravType}<br />
        </p>";
        website_functions::createPage($OUTPUT);
        exit(0);
}

