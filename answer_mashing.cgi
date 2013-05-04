#!/usr/bin/perl
#!"C:\xampp\perl\bin\perl.exe"

########################################
# GLOBALS
########################################
use CGI;                                                                                                                                          
use website_functions;
use calculations;


my %GET_data     = website_functions::getData(); # GET form data
my $grain_temp   = website_functions::validateNumber($GET_data{'grain_temp'});
my $grain_weight = website_functions::validateNumber($GET_data{'grain_weight'});
my $grain_ratio  = website_functions::validateNumber($GET_data{'grain_ratio'});
my $boil_length  = website_functions::validateNumber($GET_data{'boil_length'});
my $evap_rate    = website_functions::validateNumber($GET_data{'evap_rate'});
my $batch_size   = website_functions::validateNumber($GET_data{'batch_size'});

my ($grain_tempF,$grain_tempC,$grain_weightLbs,$grain_weightKg,$total_waterQrts);
my %mash_schedule = build_mash_schedule();


########################################
# MAIN
########################################
invalid_entry_check($grain_temp,$grain_weight,$grain_ratio,$boil_length,$evap_rate,$batch_sizeGal,$batch_sizeL);

if ( $GET_data{'brewVolType'} =~ /^Gal/ ) {
    $batch_sizeGal = $batch_size;
    $batch_sizeL =  calculations::convertMeasurement('Gal->L',$batch_sizeGal);
}
else {
    $batch_sizeL = $batch_size;
    $batch_sizeGal =  calculations::convertMeasurement('L->Gal',$batch_sizeL);
}


if ( $GET_data{'mashTempType'} =~ /^F/i ) {
    $grain_tempF = $grain_temp;
    $grain_tempC = calculations::convertMeasurement('F->C',$grain_tempF);
}
else {
    $grain_tempC = $grain_temp;
    $grain_tempF = calculations::convertMeasurement('C->F',$grain_tempC);
}

if ( $GET_data{'mashWeightType'} =~ /^lbs/i ) {
    $grain_weightLbs = $grain_weight;
    $grain_weightKg = calculations::convertMeasurement('lb->kg',$grain_weightLbs);
}
else {
    $grain_weightKg = $grain_weight;
    $grain_weightLbs = calculations::convertMeasurement('kg->lb',$grain_weightKg);
}

    my $absorbtion_lossGal = calculations::absorbtion_loss($grain_weightLbs); # Loss is in gallons
    my $absorbtion_lossL = calculations::convertMeasurement('Gal->L',$absorbtion_lossGal);

    my($initial_temp,$water_added_qrts) = calculations::initial_strike_water($doughin_mash_tempF,$grain_tempF,$grain_weightLbs,$grain_ratio);

my $OUTPUT = "
    <link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\">
    <div class=\"answerText\">
        <span class=\"answerHeader\">Mashing</span><br />"; 

    my $i=1;
    my $mash_hash_size = scalar keys %mash_schedule;
    for my $temp (sort {$a<=>$b} keys %mash_schedule) {
        my $type;

        if ($mash_schedule{$temp} eq 'F') {
            $mash_tempF = $temp;
            $mash_tempC = calculations::convertMeasurement('F->C',$mash_tempF);
        }
        else {
            $mash_tempC = $temp;
            $mash_tempF = calculations::convertMeasurement('C->F',$mash_tempC);
        }

        if ($i == 1) {
            ($initial_temp,$water_addedQrts) = calculations::initial_strike_water($mash_tempF,$grain_tempF,$grain_weightLbs,$grain_ratio);
            $water_tempF = $initial_temp;
            $water_tempC = calculations::convertMeasurement('F->C',$water_tempF);
            $type = '- Dough In';
        }
        else {
       	    $water_addedQrts = calculations::mash_infusion($initial_temp,$temp,$grain_weightLbs,$total_waterQrts,$infusion_temp); 
            $water_tempF = 212;
            $water_tempC = 100;
            $type = '- Mash Out' if $i == $mash_hash_size;
        }
        $total_waterQrts += $water_addedQrts;
        $water_addedL =calculations::convertMeasurement('qrts->L',$water_addedQrts);
        $water_addedGal =calculations::convertMeasurement('qrts->Gal',$water_addedQrts);
        $total_waterL = calculations::convertMeasurement('qrts->L',$total_waterQrts);
        $total_waterGal = calculations::convertMeasurement('qrts->Gal',$total_waterQrts);

        $OUTPUT .= "<b>STEP $i $type</b><br />DESIRED_MASH_TEMP: $mash_tempF&deg;F ($mash_tempC&deg;C)<br />WATER_TEMP: $water_tempF&deg;F ($water_tempC&deg;C)<br />WATER_ADDED: $water_addedQrts qrts ($water_addedL L, $water_addedGal Gal)<br />TOTAL_WATER: $total_waterQrts Qrts ($total_waterL L, $total_waterGal Gal)<br /><br />\n";


        $initial_temp = $mash_tempF;
        $i++;
    }

    my $sparge_waterGal = $batch_sizeGal - $total_waterGal - $absorbtion_lossGal;
    my $pre_wort_boilGal = calculations::boil_loss($batch_sizeGal,$boil_length,$evap_rate);
    my $total_water_neededGal = $pre_wort_boilGal + $absorbtion_lossGal;
    my $lauter_waterGal = $total_water_neededGal - $total_waterGal;
    my $lauter_waterL = calculations::convertMeasurement('Gal->L',$lauter_waterGal);
    $OUTPUT .= "
    <span class=\"answerHeader\">Lautering</span><br />
    <b>STEP $i - Lautering</b><br />
      LAUTER_WATER_ADDED: $lauter_waterGal Gal ($lauter_waterL L)<br />
      LAUTER_WATER_TEMP: 170&deg;F (76.667&deg;C)
      <br /><br />
      <div class=\"comment\">
      GRAIN_ABSORBTION_LOSS: $absorbtion_lossGal gal ($absorbtion_lossL L)<br />
      BATCH_SIZE_DESIRED: $batch_sizeGal Gal ($batch_sizeL L)<br />
      BOIL_EVAPORATION_RATE: $evap_rate an hour<br /> 
      TOTAL_PRE_BOIL_WATER_NEEDED: $pre_wort_boilGal Gal <br />
      </div>
      </div> <!-- AnswerText Ending -->
    ";

    website_functions::createPage($OUTPUT);


########################################
# SUBROUTINES
########################################
sub invalid_entry_check {
    my $invalid = 0;

    foreach (@_) { $invalid = 1 if $_ =~ /INVALID/; } 
    return unless $invalid;

    my $OUTPUT = "<link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\">
       <h3>INVALID ENTRY</h3>
       <p class=\"answerText\">
            Grain Temp: <b>$grain_temp</b><br />
            Grain Weight: <b>$grain_weight</b><br />
            Grain Ratio: <b>$grain_ratio</b><br />
            Boil Length: <b>$boil_length</b><br />
            Evaporation Rate: <b>$evap_rate</b><br />
            Batch Size: <b>$batch_size</b><br />
       </p>";
        website_functions::createPage($OUTPUT);
        exit(0);
}

sub build_mash_schedule {
    $GET_data{'AcidRest'}    = calculations::convertMeasurement('C->F',$1) .'F' if ($GET_data{'AcidRest'} =~ /(\d+)C$/);
    $GET_data{'ProteinRest'} = calculations::convertMeasurement('C->F',$1) .'F' if ($GET_data{'ProteinRest'} =~ /(\d+)C$/);
    $GET_data{'BetaRest'}    = calculations::convertMeasurement('C->F',$1) .'F' if ($GET_data{'BetaRest'} =~ /(\d+)C$/);
    $GET_data{'SacRest'}     = calculations::convertMeasurement('C->F',$1) .'F' if ($GET_data{'SacRest'} =~ /(\d+)C$/);
    $GET_data{'MashOut'}     = calculations::convertMeasurement('C->F',$1) .'F' if ($GET_data{'MashOut'} =~ /(\d+)C$/);

    $mash_schedule{$1} = $2 if $GET_data{'AcidRest'} =~ /([\d\.]+)([F])/;
    $mash_schedule{$1} = $2 if $GET_data{'ProteinRest'} =~ /([\d\.]+)([F])/;
    $mash_schedule{$1} = $2 if $GET_data{'BetaRest'} =~ /([\d\.]+)([F])/;
    $mash_schedule{$1} = $2 if $GET_data{'SacRest'} =~ /([\d\.]+)([F])/;
    $mash_schedule{$1} = $2 if $GET_data{'MashOut'} =~ /([\d\.]+)([F])/;

    return %mash_schedule;
}
