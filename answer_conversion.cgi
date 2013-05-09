#!/usr/bin/perl
#!"C:\xampp\perl\bin\perl.exe"

########################################
# GLOBALS
########################################
use CGI;                                                                                                                                          
use website_functions;
use calculations;

my %GET_data     = website_functions::getData(); # GET form data
my $amount       = website_functions::validateNumber($GET_data{'amount'});
my $units        = $GET_data{'units'};
my $measure_type = ($units eq 'Grams' || $units eq 'Kilograms' || $units eq 'Pounds' || $units eq 'Ounces') ? 'MASS' : 'VOLUME';


########################################
# MAIN
########################################
invalid_entry_check($amount);

my (%volume_hash,%mass_hash,$OUTPUT);

if ($measure_type eq "VOLUME") {
    %volume_hash = build_volume_hash();
    $OUTPUT = build_volume_page();
}
elsif ($measure_type eq "MASS") {
    %mass_hash = build_mass_hash();
    $OUTPUT = build_mass_page();
}
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
            Amount: <b>$amount</b><br />
       </p>";
        website_functions::createPage($OUTPUT);
        exit(0);
}

sub build_volume_page {
    my $liters = $amount * $volume_hash{"liter (l)"}{$units};
    my $kg_mass = $liters;
    my $g_mass = $liters * 1000;
    my $lbs_mass = $liters * 2.205;
    my $oz_mass = $liters * 35.27;

    $OUTPUT .= "<h2>Common</h2>\n";
    $OUTPUT .= volume_data_convert("liter (l)","milliliter (ml)","gallon (US gal)","quart (US qt)","fluid ounce (US oz)");
    $OUTPUT .= "<h2>MASS/WEIGHT (Water Only)</h2> 
                    Kilograms (kg): $kg_mass<br />\n
                    Grams (g): $g_mass<br />\n
                    Pounds (US lbs): $lbs_mass<br />\n
                    Ounces (US oz): $oz_mass<br />\n ";
    $OUTPUT .= "<h2>Metric</h2>";
    $OUTPUT .= volume_data_convert("cubic meter (m3)","cubic decimeter (dm3)","cubic centimeter (cc)","cubic millimeter (mm3)","hectoliter (hl)","decaliter", "liter (l)", "deciliter (dl)", "centiliter (cl)", "milliliter (ml)", "microliter (µl)");
    $OUTPUT .= "<h2>U.S. Dry Measure</h2>";
    $OUTPUT .= volume_data_convert("barrel (DRY)", "bushel (DRY bu)", "peck (DRY pk)", "gallon (DRY gal)", "quart (DRY qt)", "pint (DRY pt)", "gill (DRY)");
    $OUTPUT .= "<h2>British and U.S. derivatives of length units</h2>";
    $OUTPUT .= volume_data_convert("cubic yard (yd3)", "cubic foot (ft3)", "cubic inch (in3)");
    $OUTPUT .= "<h2>Cooking (International)</h2>";
    $OUTPUT .= volume_data_convert("cup (UK)", "tablespoon (UK)", "teaspoon (UK)");
    $OUTPUT .= "<h2>Chinese Imperial</h2>";
    $OUTPUT .= "<h4>These units are used to measure grains.</h4>";
    $OUTPUT .= volume_data_convert("dan", "dou", "sheng", "ge", "shao", "cuo");
    $OUTPUT .= "<h2>Old Russian Liquid Measure</h2>";
    $OUTPUT .= volume_data_convert("vedro", "shtoff", "chetvert (quart)", "vine bottle", "vodka bottle", "charka", "shkalik");
    $OUTPUT .= "<h2>Old Russian Dry Measure</h2>";
    $OUTPUT .= volume_data_convert("cetverik (mera)", "vedro", "garnetz");
    $OUTPUT .= "<h2>Ancient Roman Dry Measure</h2>";
    $OUTPUT .= volume_data_convert("cubic ped (quadrantal)", "modium", "semodium", "sextarium", "quartarium");
    $OUTPUT .= "<h2>Biblical Liquid Measure (Old Testament)</h2>";
    $OUTPUT .= "<h4>Exact conversion for Biblical units is rarely certain.</h4>";
    $OUTPUT .= volume_data_convert("homer (cor) (Liquid)", "bath", "hin", "kab (cab) (Liquid)", "log");
    $OUTPUT .= "<h2>U.S. Liquid Measure</h2>";
    $OUTPUT .= volume_data_convert("acre foot", "barrel (petroleum)", "gallon (US gal)", "quart (US qt)", "pint (US pt)", "gill", "fluid ounce (US oz)", "fluid dram", "minim");
    $OUTPUT .= "<h2>British Imperial Liquid And Dry</h2>";
    $OUTPUT .= volume_data_convert("perch", "barrel", "bushel (bu)", "peck (pk)", "gallon (UK gal)", "quart (UK qt)", "pint (UK pt)", "fluid ounce (UK oz)");
    $OUTPUT .= "<h2>Cooking (U.S.)</h2>";
    $OUTPUT .= volume_data_convert("cup (US)", "tablespoon (US)", "teaspoon (US)");
    $OUTPUT .= "<h2>Japanese</h2>";
    $OUTPUT .= volume_data_convert("sai", "shaku", "go", "sho", "to", "koku");
    $OUTPUT .= "<h2>Thai</h2>";
    $OUTPUT .= volume_data_convert("kwien", "ban", "sat", "tanan");
    $OUTPUT .= "<h2>Old French</h2>";
    $OUTPUT .= "<h4>There were many local variations; the following are Quebec and Paris definitions</h4>";
    $OUTPUT .= volume_data_convert("minot", "litron");
    $OUTPUT .= "<h2>Ancient Roman Liquid Measure</h2>";
    $OUTPUT .= volume_data_convert("kulee (dolee)", "amphora", "urn", "kognee", "sextarium", "gemin", "quart (Roman)", "acetabul", "ciate");
    $OUTPUT .= "<h2>Biblical Dry Measure (Old Testament)</h2>";
    $OUTPUT .= "<h4>Exact conversion for Biblical units is rarely certain.</h4>";
    $OUTPUT .= volume_data_convert("cor (homer) (dry)", "lethek", "ephah", "seah", "omer", "cab (dry)");

    return $OUTPUT;
}


sub build_mass_page {
    $OUTPUT .= "<h2>Common</h2>\n";
    $OUTPUT .= mass_data_convert("kilogram (kg)","gram (g)","pound (lb)","ounce (oz)");
    $OUTPUT .= "<h2>Metric</h2>\n";
    $OUTPUT .= mass_data_convert( 'kilotonne', 'tonne', 'kilonewton (on Earth surface) (kN)', "centner", "kilogram (kg)", "newton (on Earth surface) (N)", "carat (ct)", "gram (g)", "centigram", "milligram (mg)", "microgram (mcg)", );
    $OUTPUT .= "<h2>Troy</h2>\n";                            
    $OUTPUT .= mass_data_convert("pound (troy)", "ounce (ozt)", "pennyweight (dwt)", "carat (troy)", "grain (troy)", "mite", "doite");
    $OUTPUT .= "<h2>Japanese</h2>\n";
    $OUTPUT .= mass_data_convert("koku","kan","kin","hyakume","monnme","bu");
    $OUTPUT .= "<h2>Thai</h2>\n";
    $OUTPUT .= mass_data_convert("hap (pikul)", "chang (kati)", "tamlueng", "baht (tical)", "mayon/mayong", "salueng", "fueang", "sik", "sio/pie", "at", "solot", "bia");
    $OUTPUT .= "<h2>Old Russian</h2>\n";
    $OUTPUT .= mass_data_convert("berkovets", "pood", "pound (Old Russian)", "lot", "zolotnik", "dolya");
    $OUTPUT .= "<h2>Old German</h2>\n";
    $OUTPUT .= mass_data_convert("doppelzentner", "zentner", "pfund");
    $OUTPUT .= "<h2>Ancient Greek</h2>\n";
    $OUTPUT .= mass_data_convert("talent", "mine", "tetradram", "dram", "diobol", "obol", "halk");
    $OUTPUT .= "<h2>Baha'i Faith Units</h2>\n";
    $OUTPUT .= mass_data_convert("mithqal", "nakhud");
    $OUTPUT .= "<h2>Avoirdupois (U.S. / British)</h2>\n";
    $OUTPUT .= mass_data_convert("long ton (UK)", "short ton (US)", "long hundredweight (UK)", "short hundredweight (US)", "stone", "pound (lb)", "ounce (oz)", "dram (dr)", "grain (gr)");
    $OUTPUT .= "<h2>Apothecaries</h2>\n";
    $OUTPUT .= mass_data_convert("pound (Apothecaries)", "ounce (Apothecaries)", "dram (Apothecaries)", "scruple (Apothecaries)", "grain (Apothecaries)");
    $OUTPUT .= "<h2>Chinese Imperial</h2>\n";
    $OUTPUT .= mass_data_convert("dan", "jin", "liang", "tael", "qian", "fen", "li", "hao", "si", "hu");
    $OUTPUT .= "<h2>Hong Kong</h2>\n";
    $OUTPUT .= mass_data_convert("picul (tam)", "catty (kan)", "tael (leung)", "mace (tsin)", "candareen (fan)", "tael troy", "mace troy", "candareen troy");
    $OUTPUT .= "<h2>Old French</h2>\n";
    $OUTPUT .= "<h4>There were many local variations; the following are Quebec and Paris definitions</h4>\n";
    $OUTPUT .= mass_data_convert("quintal", "livre");
    $OUTPUT .= "<h2>Ancient Roman</h2>\n";
    $OUTPUT .= mass_data_convert("centumpondus", "meen", "pondus (libra)", "ounce (Roman)", "semiounce", "duella", "sicilicus", "milliaresium", "solid", "denarium", "scruple");
    $OUTPUT .= "<h2>Biblical</h2>\n";
    $OUTPUT .= "<h4>Exact conversion for Biblical units is rarely certain.</h4>\n";
    $OUTPUT .= mass_data_convert("talent", "mina", "shekel", "pim", "beka", "gerah");

    return $OUTPUT;
}

sub mass_data_convert {
    my $mass_data;
        for $type (@_) {
        my $conversion = $amount * $mass_hash{$type}{$units};
        $mass_data .= "$type => $conversion<br />\n";
    }
    return $mass_data;
}

sub volume_data_convert {
    my $volume_data;
        for $type (@_) {
        my $conversion = $amount * $volume_hash{$type}{$units};
        $volume_data .= "$type => $conversion<br />\n";
    }
    return $volume_data;
}


sub build_mass_hash {
    my %mass = (
# "Metric"
        "kilotonne" => { 'Grams' => 0.000000001,'Kilograms' => 0.000001,'Pounds'=>0.0000004536,'Ounces'=>0.00000002835},
        "tonne" => { 'Grams' => 0.000001,'Kilograms' => 0.001,'Pounds'=>0.0004536,'Ounces'=>0.00002835},
        "kilonewton (on Earth surface) (kN)" => { 'Grams' => 0.000009807,'Kilograms' => 0.009807,'Pounds'=>0.004448,'Ounces'=>0.000278},
        "centner" => { 'Grams' => 0.00001,'Kilograms' => 0.01,'Pounds'=>0.004536,'Ounces'=>0.0002835},
        "kilogram (kg)" => { 'Grams' => 0.001,'Kilograms' => 1,'Pounds'=>0.4536,'Ounces'=>0.02835},
        "newton (on Earth surface) (N)" => { 'Grams' => 0.009807,'Kilograms' => 9.807,'Pounds'=>4.448,'Ounces'=>0.278},
        "carat (ct)" => { 'Grams' => 5,'Kilograms' => 5000,'Pounds'=>2268,'Ounces'=>141.7},
        "gram (g)" => { 'Grams' => 1,'Kilograms' => 1000,'Pounds'=>453.6,'Ounces'=>28.35},
        "centigram" => { 'Grams' => 100,'Kilograms' => 100000,'Pounds'=>45360,'Ounces'=>2835},
        "milligram (mg)" => { 'Grams' => 1000,'Kilograms' => 1000000,'Pounds'=>453600,'Ounces'=>28350},
        "microgram (mcg)" => { 'Grams' => 1000000,'Kilograms' => 1000000000,'Pounds'=>453600000,'Ounces'=>28350000},
# "Troy"
        "pound (troy)" => { 'Grams' => 0.002679,'Kilograms' => 2.679,'Pounds'=>1.215,'Ounces'=>0.07595},
        "ounce (ozt)" => { 'Grams' => 0.03215,'Kilograms' => 32.15,'Pounds'=>14.58,'Ounces'=>0.9115},
        "pennyweight (dwt)" => { 'Grams' => 0.643,'Kilograms' => 643,'Pounds'=>291.7,'Ounces'=>18.23},
        "carat (troy)" => { 'Grams' => 4.878,'Kilograms' => 4878,'Pounds'=>2213,'Ounces'=>138.3},
        "grain (troy)" => { 'Grams' => 15.43,'Kilograms' => 15430,'Pounds'=>7000,'Ounces'=>437.5},
        "mite" => { 'Grams' => 308.6,'Kilograms' => 308600,'Pounds'=>140000,'Ounces'=>8750},
        "doite" => { 'Grams' => 7408,'Kilograms' => 7408000,'Pounds'=>3360000,'Ounces'=>210000},
# "Japanese"
        "koku" => { 'Grams' => 0.000005544,'Kilograms' => 0.005544,'Pounds'=>0.002515,'Ounces'=>0.0001572},
        "kan" => { 'Grams' => 0.0002667,'Kilograms' => 0.2667,'Pounds'=>0.121,'Ounces'=>0.00756},
        "kin" => { 'Grams' => 0.001667,'Kilograms' => 1.667,'Pounds'=>0.756,'Ounces'=>0.04725},
        "hyakume" => { 'Grams' => 0.002667,'Kilograms' => 2.667,'Pounds'=>1.21,'Ounces'=>0.0756},
        "monnme" => { 'Grams' => 0.2667,'Kilograms' => 266.7,'Pounds'=>121,'Ounces'=>7.56},
        "bu" => { 'Grams' => 2.667,'Kilograms' => 2667,'Pounds'=>1210,'Ounces'=>75.6},
# "Thai"
        "hap (pikul)" => { 'Grams' => 0.00001667,'Kilograms' => 0.01667,'Pounds'=>0.00756,'Ounces'=>0.0004725},
        "chang (kati)" => { 'Grams' => 0.0008333,'Kilograms' => 0.8333,'Pounds'=>0.378,'Ounces'=>0.02362},
        "tamlueng" => { 'Grams' => 0.01667,'Kilograms' => 16.67,'Pounds'=>7.56,'Ounces'=>0.4725},
        "baht (tical)" => { 'Grams' => 0.0656,'Kilograms' => 65.6,'Pounds'=>29.76,'Ounces'=>1.86},
        "mayon/mayong" => { 'Grams' => 0.1312,'Kilograms' => 131.2,'Pounds'=>59.51,'Ounces'=>3.719},
        "salueng" => { 'Grams' => 0.2624,'Kilograms' => 262.4,'Pounds'=>119,'Ounces'=>7.439},
        "fueang" => { 'Grams' => 0.5248,'Kilograms' => 524.8,'Pounds'=>238,'Ounces'=>14.88},
        "sik" => { 'Grams' => 1.05,'Kilograms' => 1050,'Pounds'=>476.1,'Ounces'=>29.76},
        "sio/pie" => { 'Grams' => 2.099,'Kilograms' => 2099,'Pounds'=>952.2,'Ounces'=>59.51},
        "at" => { 'Grams' => 4.198,'Kilograms' => 4198,'Pounds'=>1904,'Ounces'=>119},
        "solot" => { 'Grams' => 8.397,'Kilograms' => 8397,'Pounds'=>3809,'Ounces'=>238},
        "bia" => { 'Grams' => 419.8,'Kilograms' => 419800,'Pounds'=>190400,'Ounces'=>11900},
# "Old Russian"
        "berkovets" => { 'Grams' => 0.000006105,'Kilograms' => 0.006105,'Pounds'=>0.002769,'Ounces'=>0.0001731},
        "pood" => { 'Grams' => 0.00006105,'Kilograms' => 0.06105,'Pounds'=>0.02769,'Ounces'=>0.001731},
        "pound (Old Russian)" => { 'Grams' => 0.002442,'Kilograms' => 2.442,'Pounds'=>1.108,'Ounces'=>0.06923},
        "lot" => { 'Grams' => 0.07814,'Kilograms' => 78.14,'Pounds'=>35.44,'Ounces'=>2.215},
        "zolotnik" => { 'Grams' => 0.2344,'Kilograms' => 234.4,'Pounds'=>106.3,'Ounces'=>6.646},
        "dolya" => { 'Grams' => 22.5,'Kilograms' => 22500,'Pounds'=>10210,'Ounces'=>638},
# "Old German"
        "doppelzentner" => { 'Grams' => 0.00001,'Kilograms' => 0.01,'Pounds'=>0.004536,'Ounces'=>0.0002835},
        "zentner" => { 'Grams' => 0.00002,'Kilograms' => 0.02,'Pounds'=>0.009072,'Ounces'=>0.000567},
        "pfund" => { 'Grams' => 0.002,'Kilograms' => 2,'Pounds'=>0.9072,'Ounces'=>0.0567},
# "Ancient Greek"
        "talent" => { 'Grams' => 0.00003922,'Kilograms' => 0.03922,'Pounds'=>0.01779,'Ounces'=>0.001112},
        "mine" => { 'Grams' => 0.002353,'Kilograms' => 2.353,'Pounds'=>1.067,'Ounces'=>0.0667},
        "tetradram" => { 'Grams' => 0.05882,'Kilograms' => 58.82,'Pounds'=>26.68,'Ounces'=>1.668},
        "dram" => { 'Grams' => 0.2353,'Kilograms' => 235.3,'Pounds'=>106.7,'Ounces'=>6.67},
        "diobol" => { 'Grams' => 0.7059,'Kilograms' => 705.9,'Pounds'=>320.2,'Ounces'=>20.01},
        "obol" => { 'Grams' => 1.412,'Kilograms' => 1412,'Pounds'=>640.4,'Ounces'=>40.02},
        "halk" => { 'Grams' => 11.29,'Kilograms' => 11290,'Pounds'=>5123,'Ounces'=>320.2},
# "Baha'i Faith Units"
        "mithqal" => { 'Grams' => 0.2746,'Kilograms' => 274.6,'Pounds'=>124.6,'Ounces'=>7.785},
        "nakhud" => { 'Grams' => 5.217,'Kilograms' => 5217,'Pounds'=>2367,'Ounces'=>147.9},
# "Avoirdupois (U.S. / British)"
        "long ton (UK)" => { 'Grams' => 0.0000009842,'Kilograms' => 0.0009842,'Pounds'=>0.0004464,'Ounces'=>0.0000279},
        "short ton (US)" => { 'Grams' => 0.000001102,'Kilograms' => 0.001102,'Pounds'=>0.0005,'Ounces'=>0.00003125},
        "long hundredweight (UK)" => { 'Grams' => 0.00001968,'Kilograms' => 0.01968,'Pounds'=>0.008929,'Ounces'=>0.000558},
        "short hundredweight (US)" => { 'Grams' => 0.00002205,'Kilograms' => 0.02205,'Pounds'=>0.01,'Ounces'=>0.000625},
        "stone" => { 'Grams' => 0.0001575,'Kilograms' => 0.1575,'Pounds'=>0.07143,'Ounces'=>0.004464},
        "pound (lb)" => { 'Grams' => 0.002205,'Kilograms' => 2.205,'Pounds'=>1,'Ounces'=>0.0625},
        "ounce (oz)" => { 'Grams' => 0.03527,'Kilograms' => 35.27,'Pounds'=>16,'Ounces'=>1},
        "dram (dr)" => { 'Grams' => 0.5644,'Kilograms' => 564.4,'Pounds'=>256,'Ounces'=>16},
        "grain (gr)" => { 'Grams' => 15.43,'Kilograms' => 15430,'Pounds'=>7000,'Ounces'=>437.5},
# "Apothecaries"
        "pound (Apothecaries)" => { 'Grams' => 0.002679,'Kilograms' => 2.679,'Pounds'=>1.215,'Ounces'=>0.07595},
        "ounce (Apothecaries)" => { 'Grams' => 0.03215,'Kilograms' => 32.15,'Pounds'=>14.58,'Ounces'=>0.9115},
        "dram (Apothecaries)" => { 'Grams' => 0.2572,'Kilograms' => 257.2,'Pounds'=>116.7,'Ounces'=>7.292},
        "scruple (Apothecaries)" => { 'Grams' => 0.7716,'Kilograms' => 771.6,'Pounds'=>350,'Ounces'=>21.88},
        "grain (Apothecaries)" => { 'Grams' => 15.43,'Kilograms' => 15430,'Pounds'=>7000,'Ounces'=>437.5},
# "Chinese Imperial"
        "dan" => { 'Grams' => 0.00002,'Kilograms' => 0.02,'Pounds'=>0.009072,'Ounces'=>0.000567},
        "jin" => { 'Grams' => 0.002,'Kilograms' => 2,'Pounds'=>0.9072,'Ounces'=>0.0567},
        "liang" => { 'Grams' => 0.02,'Kilograms' => 20,'Pounds'=>9.072,'Ounces'=>0.567},
        "tael" => { 'Grams' => 0.02672,'Kilograms' => 26.72,'Pounds'=>12.12,'Ounces'=>0.7574},
        "qian" => { 'Grams' => 0.2,'Kilograms' => 200,'Pounds'=>90.72,'Ounces'=>5.67},
        "fen" => { 'Grams' => 2,'Kilograms' => 2000,'Pounds'=>907.2,'Ounces'=>56.7},
        "li" => { 'Grams' => 20,'Kilograms' => 20000,'Pounds'=>9072,'Ounces'=>567},
        "hao" => { 'Grams' => 200,'Kilograms' => 200000,'Pounds'=>90720,'Ounces'=>5670},
        "si" => { 'Grams' => 2000,'Kilograms' => 2000000,'Pounds'=>907200,'Ounces'=>56700},
        "hu" => { 'Grams' => 20000,'Kilograms' => 20000000,'Pounds'=>9072000,'Ounces'=>567000},
# "Hong Kong"
        "picul (tam)" => { 'Grams' => 0.00001653,'Kilograms' => 0.01653,'Pounds'=>0.0075,'Ounces'=>0.0004688},
        "catty (kan)" => { 'Grams' => 0.001653,'Kilograms' => 1.653,'Pounds'=>0.75,'Ounces'=>0.04688},
        "tael (leung)" => { 'Grams' => 0.02646,'Kilograms' => 26.46,'Pounds'=>12,'Ounces'=>0.75},
        "mace (tsin)" => { 'Grams' => 0.2646,'Kilograms' => 264.6,'Pounds'=>120,'Ounces'=>7.5},
        "candareen (fan)" => { 'Grams' => 2.646,'Kilograms' => 2646,'Pounds'=>1200,'Ounces'=>75},
        "tael troy" => { 'Grams' => 0.02672,'Kilograms' => 26.72,'Pounds'=>12.12,'Ounces'=>0.7574},
        "mace troy" => { 'Grams' => 0.2672,'Kilograms' => 267.2,'Pounds'=>121.2,'Ounces'=>7.574},
        "candareen troy" => { 'Grams' => 2.672,'Kilograms' => 2672,'Pounds'=>1212,'Ounces'=>75.74},
# "Old French"
# "There were many local variations; the following are Quebec and Paris definitions"
        "quintal" => { 'Grams' => 0.00002043,'Kilograms' => 0.02043,'Pounds'=>0.009266,'Ounces'=>0.0005792},
        "livre" => { 'Grams' => 0.002043,'Kilograms' => 2.043,'Pounds'=>0.9266,'Ounces'=>0.05792},
# "Ancient Roman"
        "centumpondus" => { 'Grams' => 0.00003067,'Kilograms' => 0.03067,'Pounds'=>0.01391,'Ounces'=>0.0008696},
        "meen" => { 'Grams' => 0.00184,'Kilograms' => 1.84,'Pounds'=>0.8348,'Ounces'=>0.05217},
        "pondus (libra)" => { 'Grams' => 0.003067,'Kilograms' => 3.067,'Pounds'=>1.391,'Ounces'=>0.08696},
        "ounce (Roman)" => { 'Grams' => 0.03681,'Kilograms' => 36.81,'Pounds'=>16.7,'Ounces'=>1.043},
        "semiounce" => { 'Grams' => 0.07362,'Kilograms' => 73.62,'Pounds'=>33.39,'Ounces'=>2.087},
        "duella" => { 'Grams' => 0.1104,'Kilograms' => 110.4,'Pounds'=>50.09,'Ounces'=>3.13},
        "sicilicus" => { 'Grams' => 0.1472,'Kilograms' => 147.2,'Pounds'=>66.78,'Ounces'=>4.174},
        "milliaresium" => { 'Grams' => 0.184,'Kilograms' => 184,'Pounds'=>83.48,'Ounces'=>5.217},
        "solid" => { 'Grams' => 0.2208,'Kilograms' => 220.8,'Pounds'=>100.2,'Ounces'=>6.261},
        "denarium" => { 'Grams' => 0.2945,'Kilograms' => 294.5,'Pounds'=>133.6,'Ounces'=>8.348},
        "scruple" => { 'Grams' => 0.8834,'Kilograms' => 883.4,'Pounds'=>400.7,'Ounces'=>25.04},
# "Biblical"
# "Exact conversion for Biblical units is rarely certain."
        "talent" => { 'Grams' => 0.00002939,'Kilograms' => 0.02939,'Pounds'=>0.01333,'Ounces'=>0.0008333},
        "mina" => { 'Grams' => 0.001764,'Kilograms' => 1.764,'Pounds'=>0.8,'Ounces'=>0.05},
        "shekel" => { 'Grams' => 0.08818,'Kilograms' => 88.18,'Pounds'=>40,'Ounces'=>2.5},
        "pim" => { 'Grams' => 0.1323,'Kilograms' => 132.3,'Pounds'=>60,'Ounces'=>3.75},
        "beka" => { 'Grams' => 0.1764,'Kilograms' => 176.4,'Pounds'=>80,'Ounces'=>5},
        "gerah" => { 'Grams' => 1.764,'Kilograms' => 1764,'Pounds'=>800,'Ounces'=>50},
        );
return %mass;
}




sub build_volume_hash {
    my %volume = (
# "MASS/WEIGHT (Water Only)"
            "Kilograms (MASS)" => { 'Liters' => "Liters * 1",'Milliliters' => "Liters * 1",'Gallons'=>"Liters * 1",'Quarts'=>"Liters * 1",'Fluid Ounces'=>"Liters * 1"},
            "Grams (MASS)" => { 'Liters' => "Liters* 1000",'Milliliters' => "Liters* 1000",'Gallons'=>"Liters* 1000",'Quarts'=>"Liters* 1000",'Fluid Ounces'=>"Liters* 1000"},
            "Pounds (MASS)" => { 'Liters' => "Liters * 2.205",'Milliliters' => "Liters * 2.205",'Gallons'=>"Liters * 2.205",'Quarts'=>"Liters * 2.205",'Fluid Ounces'=>"Liters * 2.205"},
            "Ounces (MASS)" => { 'Liters' => "Liters * 35.27",'Milliliters' => "Liters * 35.27",'Gallons'=>"Liters * 35.27",'Quarts'=>"Liters * 35.27",'Fluid Ounces'=>"Liters * 35.27"},
# "Metric"
            "cubic meter (m3)" => { 'Liters' => 0.001,'Milliliters' => 0.000001,'Gallons'=>0.003785,'Quarts'=>0.0009464,'Fluid Ounces'=>0.00002957},
            "cubic decimeter (dm3)" => { 'Liters' => 1,'Milliliters' => 0.001,'Gallons'=>3.785,'Quarts'=>0.9464,'Fluid Ounces'=>0.02957},
            "cubic centimeter (cc)" => { 'Liters' => 1000,'Milliliters' => 1,'Gallons'=>3785,'Quarts'=>946.4,'Fluid Ounces'=>29.57},
            "cubic millimeter (mm3)" => { 'Liters' => 1000000,'Milliliters' => 1000,'Gallons'=>3785000,'Quarts'=>946400,'Fluid Ounces'=>29570},
            "hectoliter (hl)" => { 'Liters' => 0.01,'Milliliters' => 0.00001,'Gallons'=>0.03785,'Quarts'=>0.009464,'Fluid Ounces'=>0.0002957},
            "decaliter" => { 'Liters' => 0.1,'Milliliters' => 0.0001,'Gallons'=>0.3785,'Quarts'=>0.09464,'Fluid Ounces'=>0.002957},
            "liter (l)" => { 'Liters' => 1,'Milliliters' => 0.001,'Gallons'=>3.785,'Quarts'=>0.9464,'Fluid Ounces'=>0.02957},
            "deciliter (dl)" => { 'Liters' => 10,'Milliliters' => 0.01,'Gallons'=>37.85,'Quarts'=>9.464,'Fluid Ounces'=>0.2957},
            "centiliter (cl)" => { 'Liters' => 100,'Milliliters' => 0.1,'Gallons'=>378.5,'Quarts'=>94.64,'Fluid Ounces'=>2.957},
            "milliliter (ml)" => { 'Liters' => 1000,'Milliliters' => 1,'Gallons'=>3785,'Quarts'=>946.4,'Fluid Ounces'=>29.57},
            "microliter (µl)" => { 'Liters' => 1000000,'Milliliters' => 1000,'Gallons'=>3785000,'Quarts'=>946400,'Fluid Ounces'=>29570},
# "U.S. Dry Measure"
            "barrel (DRY)" => { 'Liters' => 0.008648,'Milliliters' => 0.000008648,'Gallons'=>0.03274,'Quarts'=>0.008185,'Fluid Ounces'=>0.0002558},
            "bushel (DRY bu)" => { 'Liters' => 0.02838,'Milliliters' => 0.00002838,'Gallons'=>0.1074,'Quarts'=>0.02686,'Fluid Ounces'=>0.0008392},
            "peck (DRY pk)" => { 'Liters' => 0.1135,'Milliliters' => 0.0001135,'Gallons'=>0.4297,'Quarts'=>0.1074,'Fluid Ounces'=>0.003357},
            "gallon (DRY gal)" => { 'Liters' => 0.227,'Milliliters' => 0.000227,'Gallons'=>0.8594,'Quarts'=>0.2148,'Fluid Ounces'=>0.006714},
            "quart (DRY qt)" => { 'Liters' => 0.9081,'Milliliters' => 0.0009081,'Gallons'=>3.437,'Quarts'=>0.8594,'Fluid Ounces'=>0.02686},
            "pint (DRY pt)" => { 'Liters' => 1.816,'Milliliters' => 0.001816,'Gallons'=>6.875,'Quarts'=>1.719,'Fluid Ounces'=>0.05371},
            "gill (DRY)" => { 'Liters' => 7.265,'Milliliters' => 0.007265,'Gallons'=>27.5,'Quarts'=>6.875,'Fluid Ounces'=>0.2148},
# "British and U.S. derivatives of length units"
            "cubic yard (yd3)" => { 'Liters' => 0.001308,'Milliliters' => 0.000001308,'Gallons'=>0.004951,'Quarts'=>0.001238,'Fluid Ounces'=>0.00003868},
            "cubic foot (ft3)" => { 'Liters' => 0.03531,'Milliliters' => 0.00003531,'Gallons'=>0.1337,'Quarts'=>0.03342,'Fluid Ounces'=>0.001044},
            "cubic inch (in3)" => { 'Liters' => 61.02,'Milliliters' => 0.06102,'Gallons'=>231,'Quarts'=>57.75,'Fluid Ounces'=>1.805},
# "Cooking (International)"
            "cup (UK)" => { 'Liters' => 4.167,'Milliliters' => 0.004167,'Gallons'=>15.77,'Quarts'=>3.943,'Fluid Ounces'=>0.1232},
            "tablespoon (UK)" => { 'Liters' => 66.67,'Milliliters' => 0.06667,'Gallons'=>252.4,'Quarts'=>63.09,'Fluid Ounces'=>1.972},
            "teaspoon (UK)" => { 'Liters' => 200,'Milliliters' => 0.2,'Gallons'=>757.1,'Quarts'=>189.3,'Fluid Ounces'=>5.915},
# "Chinese Imperial"
# "These units are used to measure grains."
            "dan" => { 'Liters' => 0.01,'Milliliters' => 0.00001,'Gallons'=>0.03785,'Quarts'=>0.009464,'Fluid Ounces'=>0.0002957},
            "dou" => { 'Liters' => 0.1,'Milliliters' => 0.0001,'Gallons'=>0.3785,'Quarts'=>0.09464,'Fluid Ounces'=>0.002957},
            "sheng" => { 'Liters' => 1,'Milliliters' => 0.001,'Gallons'=>3.785,'Quarts'=>0.9464,'Fluid Ounces'=>0.02957},
            "ge" => { 'Liters' => 10,'Milliliters' => 0.01,'Gallons'=>37.85,'Quarts'=>9.464,'Fluid Ounces'=>0.2957},
            "shao" => { 'Liters' => 100,'Milliliters' => 0.1,'Gallons'=>378.5,'Quarts'=>94.64,'Fluid Ounces'=>2.957},
            "cuo" => { 'Liters' => 1000,'Milliliters' => 1,'Gallons'=>3785,'Quarts'=>946.4,'Fluid Ounces'=>29.57},
# "Old Russian Liquid Measure"
            "vedro" => { 'Liters' => 0.0813,'Milliliters' => 0.0000813,'Gallons'=>0.3078,'Quarts'=>0.07694,'Fluid Ounces'=>0.002404},
            "shtoff" => { 'Liters' => 0.813,'Milliliters' => 0.000813,'Gallons'=>3.078,'Quarts'=>0.7694,'Fluid Ounces'=>0.02404},
            "chetvert (quart)" => { 'Liters' => 0.3252,'Milliliters' => 0.0003252,'Gallons'=>1.231,'Quarts'=>0.3078,'Fluid Ounces'=>0.009617},
            "vine bottle" => { 'Liters' => 1.301,'Milliliters' => 0.001301,'Gallons'=>4.924,'Quarts'=>1.231,'Fluid Ounces'=>0.03847},
            "vodka bottle" => { 'Liters' => 1.626,'Milliliters' => 0.001626,'Gallons'=>6.155,'Quarts'=>1.539,'Fluid Ounces'=>0.04809},
            "charka" => { 'Liters' => 8.13,'Milliliters' => 0.00813,'Gallons'=>30.78,'Quarts'=>7.694,'Fluid Ounces'=>0.2404},
            "shkalik" => { 'Liters' => 16.26,'Milliliters' => 0.01626,'Gallons'=>61.55,'Quarts'=>15.39,'Fluid Ounces'=>0.4809},
# "Old Russian Dry Measure"
            "cetverik (mera)" => { 'Liters' => 0.03811,'Milliliters' => 0.00003811,'Gallons'=>0.1443,'Quarts'=>0.03607,'Fluid Ounces'=>0.001127},
            "vedro" => { 'Liters' => 0.0813,'Milliliters' => 0.0000813,'Gallons'=>0.3078,'Quarts'=>0.07694,'Fluid Ounces'=>0.002404},
            "garnetz" => { 'Liters' => 0.3049,'Milliliters' => 0.0003049,'Gallons'=>1.154,'Quarts'=>0.2885,'Fluid Ounces'=>0.009017},
# "Ancient Roman Dry Measure"
            "cubic ped (quadrantal)" => { 'Liters' => 0.0383,'Milliliters' => 0.0000383,'Gallons'=>0.145,'Quarts'=>0.03624,'Fluid Ounces'=>0.001133},
            "modium" => { 'Liters' => 0.1149,'Milliliters' => 0.0001149,'Gallons'=>0.4349,'Quarts'=>0.1087,'Fluid Ounces'=>0.003398},
            "semodium" => { 'Liters' => 0.2298,'Milliliters' => 0.0002298,'Gallons'=>0.8698,'Quarts'=>0.2175,'Fluid Ounces'=>0.006795},
            "sextarium" => { 'Liters' => 1.838,'Milliliters' => 0.001838,'Gallons'=>6.958,'Quarts'=>1.74,'Fluid Ounces'=>0.05436},
            "quartarium" => { 'Liters' => 7.353,'Milliliters' => 0.007353,'Gallons'=>27.83,'Quarts'=>6.958,'Fluid Ounces'=>0.2175},
# "Biblical Liquid Measure (Old Testament)"
# "Exact conversion for Biblical units is rarely certain."
            "homer (cor) (Liquid)" => { 'Liters' => 0.00473,'Milliliters' => 0.00000473,'Gallons'=>0.0179,'Quarts'=>0.004476,'Fluid Ounces'=>0.0001399},
            "bath" => { 'Liters' => 0.0473,'Milliliters' => 0.0000473,'Gallons'=>0.179,'Quarts'=>0.04476,'Fluid Ounces'=>0.001399},
            "hin" => { 'Liters' => 0.2838,'Milliliters' => 0.0002838,'Gallons'=>1.074,'Quarts'=>0.2686,'Fluid Ounces'=>0.008392},
            "kab (cab) (Liquid)" => { 'Liters' => 0.8513,'Milliliters' => 0.0008513,'Gallons'=>3.223,'Quarts'=>0.8057,'Fluid Ounces'=>0.02518},
            "log" => { 'Liters' => 3.405,'Milliliters' => 0.003405,'Gallons'=>12.89,'Quarts'=>3.223,'Fluid Ounces'=>0.1007},
# "U.S. Liquid Measure"
            "acre foot" => { 'Liters' => 0.0000008107,'Milliliters' => 0.0000000008107,'Gallons'=>0.000003069,'Quarts'=>0.0000007672,'Fluid Ounces'=>0.00000002398},
            "barrel (petroleum)" => { 'Liters' => 0.00629,'Milliliters' => 0.00000629,'Gallons'=>0.02381,'Quarts'=>0.005952,'Fluid Ounces'=>0.000186},
            "gallon (US gal)" => { 'Liters' => 0.2642,'Milliliters' => 0.0002642,'Gallons'=>1,'Quarts'=>0.25,'Fluid Ounces'=>0.007813},
            "quart (US qt)" => { 'Liters' => 1.057,'Milliliters' => 0.001057,'Gallons'=>4,'Quarts'=>1,'Fluid Ounces'=>0.03125},
            "pint (US pt)" => { 'Liters' => 2.113,'Milliliters' => 0.002113,'Gallons'=>8,'Quarts'=>2,'Fluid Ounces'=>0.0625},
            "gill" => { 'Liters' => 8.454,'Milliliters' => 0.008454,'Gallons'=>32,'Quarts'=>8,'Fluid Ounces'=>0.25},
            "fluid ounce (US oz)" => { 'Liters' => 33.81,'Milliliters' => 0.03381,'Gallons'=>128,'Quarts'=>32,'Fluid Ounces'=>1},
            "fluid dram" => { 'Liters' => 270.5,'Milliliters' => 0.2705,'Gallons'=>1024,'Quarts'=>256,'Fluid Ounces'=>8},
            "minim" => { 'Liters' => 16230,'Milliliters' => 16.23,'Gallons'=>61440,'Quarts'=>15360,'Fluid Ounces'=>480},
# "British Imperial Liquid And Dry"
            "perch" => { 'Liters' => 0.001427,'Milliliters' => 0.000001427,'Gallons'=>0.005401,'Quarts'=>0.00135,'Fluid Ounces'=>0.0000422},
            "barrel" => { 'Liters' => 0.006111,'Milliliters' => 0.000006111,'Gallons'=>0.02313,'Quarts'=>0.005783,'Fluid Ounces'=>0.0001807},
            "bushel (bu)" => { 'Liters' => 0.0275,'Milliliters' => 0.0000275,'Gallons'=>0.1041,'Quarts'=>0.02602,'Fluid Ounces'=>0.0008132},
            "peck (pk)" => { 'Liters' => 0.11,'Milliliters' => 0.00011,'Gallons'=>0.4163,'Quarts'=>0.1041,'Fluid Ounces'=>0.003253},
            "gallon (UK gal)" => { 'Liters' => 0.22,'Milliliters' => 0.00022,'Gallons'=>0.8327,'Quarts'=>0.2082,'Fluid Ounces'=>0.006505},
            "quart (UK qt)" => { 'Liters' => 0.8799,'Milliliters' => 0.0008799,'Gallons'=>3.331,'Quarts'=>0.8327,'Fluid Ounces'=>0.02602},
            "pint (UK pt)" => { 'Liters' => 1.76,'Milliliters' => 0.00176,'Gallons'=>6.661,'Quarts'=>1.665,'Fluid Ounces'=>0.05204},
            "fluid ounce (UK oz)" => { 'Liters' => 35.2,'Milliliters' => 0.0352,'Gallons'=>133.2,'Quarts'=>33.31,'Fluid Ounces'=>1.041},
# "Cooking (U.S.)"
            "cup (US)" => { 'Liters' => 4.227,'Milliliters' => 0.004227,'Gallons'=>16,'Quarts'=>4,'Fluid Ounces'=>0.125},
            "tablespoon (US)" => { 'Liters' => 67.63,'Milliliters' => 0.06763,'Gallons'=>256,'Quarts'=>64,'Fluid Ounces'=>2},
            "teaspoon (US)" => { 'Liters' => 202.9,'Milliliters' => 0.2029,'Gallons'=>768,'Quarts'=>192,'Fluid Ounces'=>6},
# "Japanese"
            "sai" => { 'Liters' => 554.4,'Milliliters' => 0.5544,'Gallons'=>2098,'Quarts'=>524.6,'Fluid Ounces'=>16.39},
            "shaku" => { 'Liters' => 55.44,'Milliliters' => 0.05544,'Gallons'=>209.8,'Quarts'=>52.46,'Fluid Ounces'=>1.639},
            "go" => { 'Liters' => 5.544,'Milliliters' => 0.005544,'Gallons'=>20.98,'Quarts'=>5.246,'Fluid Ounces'=>0.1639},
            "sho" => { 'Liters' => 0.5544,'Milliliters' => 0.0005544,'Gallons'=>2.098,'Quarts'=>0.5246,'Fluid Ounces'=>0.01639},
            "to" => { 'Liters' => 0.05544,'Milliliters' => 0.00005544,'Gallons'=>0.2098,'Quarts'=>0.05246,'Fluid Ounces'=>0.001639},
            "koku" => { 'Liters' => 0.005544,'Milliliters' => 0.000005544,'Gallons'=>0.02098,'Quarts'=>0.005246,'Fluid Ounces'=>0.0001639},
# "Thai"
            "kwien" => { 'Liters' => 0.0005,'Milliliters' => 0.0000005,'Gallons'=>0.001893,'Quarts'=>0.0004732,'Fluid Ounces'=>0.00001479},
            "ban" => { 'Liters' => 0.001,'Milliliters' => 0.000001,'Gallons'=>0.003785,'Quarts'=>0.0009464,'Fluid Ounces'=>0.00002957},
            "sat" => { 'Liters' => 0.05,'Milliliters' => 0.00005,'Gallons'=>0.1893,'Quarts'=>0.04732,'Fluid Ounces'=>0.001479},
            "tanan" => { 'Liters' => 1,'Milliliters' => 0.001,'Gallons'=>3.785,'Quarts'=>0.9464,'Fluid Ounces'=>0.02957},
# "Old French"
# "There were many local variations; the following are Quebec and Paris definitions"
            "minot" => { 'Liters' => 0.02941,'Milliliters' => 0.00002941,'Gallons'=>0.1113,'Quarts'=>0.02783,'Fluid Ounces'=>0.0008698},
            "litron" => { 'Liters' => 1.203,'Milliliters' => 0.001203,'Gallons'=>4.555,'Quarts'=>1.139,'Fluid Ounces'=>0.03559},
# "Ancient Roman Liquid Measure"
            "kulee (dolee)" => { 'Liters' => 0.001915,'Milliliters' => 0.000001915,'Gallons'=>0.007248,'Quarts'=>0.001812,'Fluid Ounces'=>0.00005663},
            "amphora" => { 'Liters' => 0.0383,'Milliliters' => 0.0000383,'Gallons'=>0.145,'Quarts'=>0.03624,'Fluid Ounces'=>0.001133},
            "urn" => { 'Liters' => 0.07659,'Milliliters' => 0.00007659,'Gallons'=>0.2899,'Quarts'=>0.07248,'Fluid Ounces'=>0.002265},
            "kognee" => { 'Liters' => 0.3064,'Milliliters' => 0.0003064,'Gallons'=>1.16,'Quarts'=>0.2899,'Fluid Ounces'=>0.009061},
            "sextarium" => { 'Liters' => 1.838,'Milliliters' => 0.001838,'Gallons'=>6.958,'Quarts'=>1.74,'Fluid Ounces'=>0.05436},
            "gemin" => { 'Liters' => 3.676,'Milliliters' => 0.003676,'Gallons'=>13.92,'Quarts'=>3.479,'Fluid Ounces'=>0.1087},
            "quart (Roman)" => { 'Liters' => 7.353,'Milliliters' => 0.007353,'Gallons'=>27.83,'Quarts'=>6.958,'Fluid Ounces'=>0.2175},
            "acetabul" => { 'Liters' => 14.71,'Milliliters' => 0.01471,'Gallons'=>55.67,'Quarts'=>13.92,'Fluid Ounces'=>0.4349},
            "ciate" => { 'Liters' => 22.06,'Milliliters' => 0.02206,'Gallons'=>83.5,'Quarts'=>20.88,'Fluid Ounces'=>0.6524},
# "Biblical Dry Measure (Old Testament)"
# "Exact conversion for Biblical units is rarely certain."
            "cor (homer) (dry)" => { 'Liters' => 0.00473,'Milliliters' => 0.00000473,'Gallons'=>0.0179,'Quarts'=>0.004476,'Fluid Ounces'=>0.0001399},
            "lethek" => { 'Liters' => 0.009459,'Milliliters' => 0.000009459,'Gallons'=>0.03581,'Quarts'=>0.008952,'Fluid Ounces'=>0.0002797},
            "ephah" => { 'Liters' => 0.0473,'Milliliters' => 0.0000473,'Gallons'=>0.179,'Quarts'=>0.04476,'Fluid Ounces'=>0.001399},
            "seah" => { 'Liters' => 0.1419,'Milliliters' => 0.0001419,'Gallons'=>0.5371,'Quarts'=>0.1343,'Fluid Ounces'=>0.004196},
            "omer" => { 'Liters' => 0.473,'Milliliters' => 0.000473,'Gallons'=>1.79,'Quarts'=>0.4476,'Fluid Ounces'=>0.01399},
            "cab (dry)" => { 'Liters' => 0.8513,'Milliliters' => 0.0008513,'Gallons'=>3.223,'Quarts'=>0.8057,'Fluid Ounces'=>0.02518},
    );
    
    return %volume;
}
