#!"C:\xampp\perl\bin\perl.exe"
#!/usr/bin/perl -w
package website_functions;
use strict;

#our qw($VERSION @ISA @EXPORT @EXPORT_OK);
require Exporter;
our @ISA = qw(Exporter AutoLoader);
our @EXPORT = qw();
our $VERSION = '2013.03.29.1550';


###################################################################
# SUBROUTINE: validateNumber
# COMMAND: my $clean_number = website_functions::validateNumber($number)
# NOTES: Validate number passed by users is actually a number
# (not as secure as I would like, but it is nice to clean some of the data)
# Numbers are passed in as type => value hash.
###################################################################
sub validateNumber {
    my $number_passed = shift;
    my $invalid = 1; # Assuming the number is invalid
    $number_passed =~ s/\s|\t|\n|\r|,//g; # Strip whitespace and commas
    $invalid = 0 if $number_passed =~ /^[\d\.]+$/; # Flag as valid if number is actually valid
    $number_passed = '<span class="invalidInput">INVALID</span>' if $invalid;
    return $number_passed;
}


#########################################################################
# Subroutine: getData
# Command:    $GET_hash = website_functions::getData()
# USE:       Gets the data from GET method and returns in hashed refrence
#########################################################################
sub getData {
	my ($buffer, @pairs, $pair, $name, $value, %FORM);

	# Read in text
	$ENV{'REQUEST_METHOD'} =~ tr/a-z/A-Z/;
	$buffer = $ENV{'QUERY_STRING'} if ($ENV{'REQUEST_METHOD'} eq "GET"); 

	# Split information into name/value pairs
	@pairs = split(/&/, $buffer);
	foreach $pair (@pairs) {
		($name, $value) = split(/=/, $pair);
		$value =~ tr/+/ /;
		$value =~ s/%(..)/pack("C", hex($1))/eg;
		$FORM{$name} = $value;
	}
	return %FORM;
}


#########################################################################
# Subroutine: createPage
# Command:    website_functions::createPage($OUTPUT)
# USE:       creates a webpage
#########################################################################
sub createPage {
    use CGI;
    my $OUTPUT = shift;
    my $q = new CGI;
    print $q->header( "text/html" );
    print $q->start_html( "Carbonation" );
    print $OUTPUT;
    print $q->end_html;
}



# Autoload methods go after =cut, and are processed by the autosplit program.
1;
__END__
