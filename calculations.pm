#!"C:\xampp\perl\bin\perl.exe"
#!/usr/bin/perl -w
package calculations;
require Exporter;
our @ISA = qw(Exporter AutoLoader);
our @EXPORT = qw();
our $VERSION = '2013.03.29.1550';
use strict;

###################################################################
# SUBROUTINE: Boil Loss
#
# NOTES: Figures out the water needed in the pre boil to compensate 
# for loss in cooling and evaportation. Reverse engineered from the 
# following formulas.
#
# FORMULA: Pbw = Bs / (.96-Er*t*.016)
#
# Er = Pbw * 0.10 (keg kettle is closer to .08)
# El = (Er / 60) x t
# Cl = (Pbw - El) x 0.04
# Bs = Pbw - El - Cl
# Pbw = Bs / (.96-Er*t*.016)
#
# Bs = Batch Size (gal)
# Pbw = Pre-boil wort
# Er = Evaporation Rate
# El = Evaporation Loss
# Cl = Cooling loss
# t = Length of boil (mins)
###################################################################
sub boil_loss {
	my ($batch_size,$evap_rate,$boil_length) = @_;
	$evap_rate = .1 unless $evap_rate; # Default is 10% an hour if none is passed
	$boil_length = 90 unless $boil_length; # Default is 90 minutes if none is passed
	my $pre_wort_boil = $batch_size / (.96-$evap_rate*$boil_length*.016);
	return $pre_wort_boil;
}


###################################################################
# SUBROUTINE: Absorbtion Loss
#
# NOTES: Calculates the water lost absorbing into the grain (20% 
# is a common standard, adjust if needed)
#
# FORMULA: Absorption loss in gallons = (lbs of grain) x 0.20)
###################################################################
sub absorbtion_loss {
	my $total_lbs_grain = shift;
	my $a_loss = $total_lbs_grain * .20;
	return $a_loss;
}


###################################################################
# SUBROUTINE: Initial Strike Water
# NOTES: Calculates the intial water needed for all grain batches
# FORMULA: Tw = (.2/R)(T2 - T1) + T2
#
# R = The ratio of water to grain in quarts per pound.
# T1 = The initial temperature (F) of the mash.
# T2 = The target temperature (F) of the mash.
# Tw = The actual temperature (F) of the infusion water in Quarts
###################################################################
sub initial_strike_water {
	my ($mash_temp,$temp_of_grain,$total_lbs_grain,$water_to_grain_ratio) = @_;
	my $water_added_qrts = $water_to_grain_ratio * $total_lbs_grain; # Strike water volume
	my $initial_temp = (.2/$water_to_grain_ratio) * ($mash_temp - $temp_of_grain) + $mash_temp; # Strike water temp
	return ($initial_temp,$water_added_qrts);
}


###################################################################
# SUBROUTINE: Mash Infusion
# NOTES: Calculates the amount of boiling water that is needed to add to infusion to raise temp to desired temp
# FORMULA: Wa = (T2 - T1)(.2G + Wm)/(Tw - T2)
#
# T1 = The initial temperature (F) of the mash.
# T2 = The target temperature (F) of the mash.
# G = The amount of grain in the mash (in pounds).
# Wm = The total amount of water in the mash (in quarts).
# Tw = The actual temperature (F) of the infusion water.
# Wa = The amount of boiling water added (in quarts).
###################################################################
sub mash_infusion {
	my ($initial_temp,$target_temp,$grain_lbs,$mash_volume_qrts,$infusion_temp) = @_;
	$infusion_temp = 212 unless $infusion_temp; # If your water boils at a temperature other than 212F you will need to modify this.
	my $water_added_qrts = ( ($target_temp - $initial_temp) * (.2*$grain_lbs + $mash_volume_qrts) )/($infusion_temp - $target_temp);
	return ($water_added_qrts);
}


###################################################################
# SUBROUTINE: Hydrometer Temp Correction
# NOTES: Corrects for the temperature difference of hydrometer readings
#
# FORMULA: C = ((1.313454 - (0.132674*F) + (0.00205779 * F^2) - (0.000002627634 * F^2)))
# F = Temperature Deg F
# C = Correction
#
# SECOND FORMULA: CG = C + (SG * 0.001)
# SG = Specific Gravity before temperature correction.
# CG = Specific Gravity corrected for temperature
###################################################################
sub hydrometer_temp_correction {
	my ($temp,$orig_gravity) = @_;
	my $correction = ((1.313454 - (0.132674*$temp) + (0.00205779 * $temp^2) - (0.000002627634 * $temp^2)));
	my $corrected_gravity = $correction + ($orig_gravity * 0.001);
	return $corrected_gravity;
}


###################################################################
# SUBROUTINE: Priming Sugar
# NOTES: Calculates the priming sugar (in grams) required for bottling
# FORMULA: S = 15.195 x V ( D - 3.0378 + .050062 * T - .00026555 * T * T )
#
# T = Temperature at bottling in degrees F
# V = Volume in gallons
# D = Desired CO2 Volume
# S = Sugar in grams
###################################################################
sub priming_sugar {
	my ($desired_CO2,$volume,$temp) = @_;
	my $sugar = 15.195 * $volume * ( $desired_CO2 - 3.0378 + .050062 * $temp - .00026555 * $temp * $temp );
	$sugar = sprintf "%.3f", $sugar; # Limiting to 3 decimals
    $sugar =~ s/\.?0*$//; # Clearing the zeros off the end
	return $sugar;
}


###################################################################
# SUBROUTINE: Force Carbonation
# FORMULA: P = -16.6999 – 0.0101059 * T + 0.00116512 * T^2 + 0.173354 * T * V + 4.24267 * V – 0.0684226 * V^2
#
# P = Pressure needed (psi)
# T = Temperature of keg in °F
# V = Volumes of CO2 desired

###################################################################
sub force_carbonation {
	my ($desired_CO2,$volume,$temp) = @_;
    # my $pressure = -16.6999 - 0.0101059 * $temp + 0.00116512 * $temp^2 + 0.173354 * $temp * $desired_CO2 + 4.24267 * $desired_CO2 - 0.0684226 * $desired_CO2^2;
	my $pressure = -16.6999 - (0.0101059 * $temp) + (0.00116512 * $temp * $temp) + (0.173354 * $temp * $desired_CO2) + (4.24267 * $desired_CO2) - (0.0684226 * $desired_CO2 * $desired_CO2);
	$pressure = sprintf "%.3f", $pressure; # Limiting to 3 decimals
	$pressure =~ s/\.?0*$//; # Clearing the zeros off the end
	return $pressure;
}

###################################################################
# Beer Line Length Formula:
# L = (P -(H x .5) – 1 ) / R
# Where:
# L = length of beer line in feet
# P = pressure set of regulator
# H = total height from center of keg to faucet in feet
# R = resistance of the line from the following table
# 1 = residual pressure remaining at faucet (this can be increased to 2 if you need to increase pressure to increase dispense rate)
###################################################################
# sub beerLine { }


###################################################################
# SUBROUTINE: abv
# NOTES: Calculates the alcohol by volume
# FORMULA: ABV = ((1.05 * (OG – FG)) / FG) / 0.79 * 100
# Alcohol percentage by volume (ABV) = ABW * (FG / 0.794)
###################################################################
sub abv {
	my ($OG, $FG) = @_;
 	my $ABV = ((1.05 * ($OG - $FG)) / $FG) / 0.79 * 100;
	$ABV = sprintf "%.3f", $ABV; # Limiting to 3 decimals
    $ABV =~ s/\.?0*$//; # Clearing the zeros off the end
	return $ABV;
}


###################################################################
# SUBROUTINE: Apparent Attenuation Percentage:
# FORMULA: AA%=(OG-FG)/OG*100
#
# SG is original extract
# FG is terminal Gravity as read from the hydrometer
###################################################################
sub apparent_attenuation {
	my ($OG,$FG) = @_;
	my $attenuation = ($OG-$FG)/$OG*100;
	return $attenuation;
}


###################################################################
# SUBROUTINE: Calories
# NOTES: Calories in a (12 US oz) bottle
# FORMULA: Calories = 3621 * FG * (((0.8114 * FG) + (0.1886 * OG) - 1) + (0.53 * ((OG - FG) / (1.775 - OG))))
#
# OG = Original gravity
# FG = Final gravity
###################################################################
sub calories {
	my ($OG,$FG) = @_;
	my $calories = 3621 * $FG * (((0.8114 * $FG) + (0.1886 * $OG) - 1) + (0.53 * (($OG - $FG) / (1.775 - $OG))));
	$calories = sprintf "%.3f", $calories; # Limiting to 3 decimals
    $calories =~ s/\.?0*$//; # Clearing the zeros off the end
	return $calories;
}


###################################################################
# SUBROUTINE: Real Extract
# NOTES: The "Real Extract" (RE, in °P) is a measure of the sugars which are fermented and accounts for the density lowering effects of alcohol.
# RE = (0.8114 * FE) + (0.1886 * OE)
#
# RE = Real extract
# OE = Original Plato
# FE = Final Plato
###################################################################
sub real_extract {
	my ($OE,$FE) = @_;
	my $RE = (0.8114 * $FE) + (0.1886 * $OE);
	return $RE;
}


###################################################################
# SUBROUTINE: Real attenuation
# NOTES: Attenuation is a measure of the degree to which sugar in wort has been fermented into alcohol in beer.
# Real attenuation (RA) = ((OE - RE) / OE) * 100
#
# RE = Real extract
# OE = Original Plato
###################################################################
sub real_attenuation {
	my ($OE,$RE) = @_;
	my $RA = (($OE - $RE) / $OE) * 100;
	return $RA;
}


###################################################################
# SUBROUTINE: ABW
# NOTES: alcohol percentage by weight
# FORMULA: ABW = (76.08 * (OG - FG)) / (1.775 - OG);
#
# ABW = Alcohol percentage by weight
# OG = Original gravity
# FG = Final gravity
###################################################################
sub abw {
	my ($OG,$FG) = @_;
 	my $ABW = (76.08 * ($OG - $FG)) / (1.775 - $OG);
	$ABW = sprintf "%.3f", $ABW; # Limiting to 3 decimals
    $ABW =~ s/\.?0*$//; # Clearing the zeros off the end
	return $ABW;
}



sub convertMeasurement {
    use feature "switch";
    my ($type,$measurement) = @_;
    my $output;

    given($type) {
        when (/L->Gal/)    { $output = $measurement * 0.2642; }
        when (/Gal->L/)    { $output = $measurement * 3.7854; }
        when (/oz->g/)     { $output = $measurement * 28.3495; }
        when (/g->oz/)     { $output = $measurement * 0.0353; }
        when (/lb->kg/)    { $output = $measurement * 0.4536; }
        when (/kg->lb/)    { $output = $measurement * 2.2046; }
        when (/qrts->Gal/) { $output = $measurement * 0.25; }
        when (/qrts->oz/)  { $output = $measurement * 32; }
        when (/C->F/)      { $output = ($measurement * 1.8) + 32; }
        when (/F->C/)      { $output = ($measurement - 32) / 1.8; }
        when (/SG->Plato/) { $output = (1000 * ($measurement - 1)) / 4; } # (not as accurate a version as I would like)
        when (/Plato->SG/) { $output = (($measurement) / (258.6 - ($measurement/258.2 * 227.1))) +1; }
        default { my $doNothing = 1; }
    } 
	$output = sprintf "%.3f", $output; # Limiting to 3 decimals
    $output =~ s/\.?0*$//; # Clearing the zeros off the end
    return $output;
}

# Autoload methods go after =cut, and are processed by the autosplit program.
1;
__END__
