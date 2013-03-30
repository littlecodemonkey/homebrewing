#!/usr/bin/perl -w
package calculations;
use strict;

our qw($VERSION @ISA @EXPORT @EXPORT_OK);
require Exporter;
our @ISA = qw(Exporter AutoLoader);
our @EXPORT = qw();
our $VERSION = '2013.03.29.1550';

###################################################################
# SUBROUTINE: validateNumbers
# NOTES: Validate number passed by users is actually a number
# (not as secure as I would like, but it is nice to clean some of the data)
###################################################################
sub validateNumbers {
    my $numbers_passed = shift;
    my %numbers = %{ $numbers_passed };  

    while (my ($key, $value) = each(%numbers)){
        my $invalid = 1; # Assuming the number is invalid
        $value =~ s/\s|\t|\n|\r|,//g; # Strip whitespace and commas
        $invalid = 0 if $value =~ /^[\d\.]+$/;
        ($invalid) ? $key{$value} = 'INVALID' : $key{$value} = $value;
    }
    return \%numbers;
}



# Autoload methods go after =cut, and are processed by the autosplit program.
1;
__END__
