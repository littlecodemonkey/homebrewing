#!/usr/bin/perl

########################################
# GLOBALS
########################################
use CGI;                                                                                                                                          
use website_functions;
use calculations;
use DateTime;

my %GET_data = website_functions::getData(); # GET form data
my $Final = website_functions::validateNumber($GET_data{FG});
my $Original = website_functions::validateNumber($GET_data{OG});
my ($OG_plato,$FG_plato,$OG,$FG);


########################################
# MAIN
########################################
invalid_entry($Original,$Final) if ( $Final =~ /INVALID/ || $Original =~ /INVALID/ );

if ( $GET_data{'OGgravType'} =~ /^Plato/i ) {
    $OG_plato = $Original;
    $OG_SG = calculations::convertMeasurement('Plato->SG',$Original);
}
else {
    $OG_SG = $Original;
    $OG_plato = calculations::convertMeasurement('SG->Plato',$Original);
}

if ( $GET_data{'FGgravType'} =~ /^Plato/i ) {
    $FG_plato = $Final;
    $FG_SG = calculations::convertMeasurement('Plato->SG',$Final);
}
else {
    $FG_SG = $Final;
    $FG_plato = calculations::convertMeasurement('SG->Plato',$Final);
}

my $ABV = calculations::abv($OG_SG,$FG_SG);
my $ABW = calculations::abw($OG_SG,$FG_SG);
my $apparent_attenuation = calculations::abv($OG_plato,$FG_plato);
my $calories = calculations::calories($OG_SG,$FG_SG);
my $real_extract = calculations::real_extract($OG_plato,$FG_plato);
my $real_attenuation = calculations::abv($OG_plato,$real_extract);

my $OUTPUT = "
    <link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\">
    <div class=\"answerText\">
        <span class=\"answerHeader\"></span><br />
        ABV: <b>$ABV</b>% alcohol by volume<br />
        ABW: <b>$ABW</b>% alcohol by weight<br />
        Apparant attenuation: <b>$apparent_attenuation</b><br />
        Real attenuation: <b>$real_attenuation</b><br />
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

