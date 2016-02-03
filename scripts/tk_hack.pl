#!/usr/bin/env perl

use strict;
use utf8;

sub google_tk_hack($){
    my $a = $_[0]; utf8::decode($a);
    my @d;
    #print length $a,"\n";
    for ( my $e = 0, my $f = 0; $f < (length $a); $f++) { #dump function "hexdump" " -v -e'1/1 \"%03u\" \" \"'"
	    my $char = ord substr($a, $f, $f+1);
	    if( 128 > $char){
		$d[$e++] = $char;
	    }else{
		if( 2048 > $char ){
		    $d[$e++] = ($char >> 6) | 192;
		}else{
		    if( (55296 == ($char & 64512)) && (($f + 1) < (length $a)) && (56320 == (ord substr($a,$f+1,$f+2) & 64512))  ){
			$f++;
			$char = 65536 + (($char & 1023) << 10) + (ord substr($a,$f,$f+1) & 1023);
			$d[$e++] = ($char >> 18) | 240;
			$d[$e++] = ($char >> 12) & 63 | 128;
		    }else{
			$d[$e++] = ($char >> 12) | 224;
		    }
		    $d[$e++] = ($char >> 6) & 63 | 128;
		}
		$d[$e++] = ($char & 63) | 128;
	    }
    }

	my $tkk = int(time/3600); #window[TKK]   #15 dec 2015
	$a = $tkk;

    for (my $e = 0; $e < scalar @d ; $e++){
	$a += $d[$e];
	#$a = &RLVb($a);
	my $dr = scalar ($a<<(10+(64-32)))>>(64-32);
	$a = ($a + $dr) & 4294967295;
	$a = ($a - 4294967296) if ($a > 2147483647); #2**31-1 and 2*32 corrections
	$dr = $a < 0 ? (4294967296+($a)) >> 6 : $a >> 6; #>>>
	if ($a<0){
	    $a=(((4294967296 + $a) ^ $dr) - 4294967296 );
	}elsif($dr<0){
	    $a=(((4294967296+$dr) ^ $a)-4294967296 );
        }else{
	    $a = $a ^ $dr;
        }
    }

    #$a = &RLUb($a);
    my $db = scalar ($a<<(3+(64-32)))>>(64-32);
    $a = $a + $db & 4294967295;
    $db = $a < 0 ? (2**32+($a)) >> 11 : $a >> 11; #>>>
    $a = $a ^ $db;
    $db = scalar ($a<<(15+(64-32)))>>(64-32);
    $a = $a + $db & 4294967295;
    $a = $a > 2147483647 ? $a - 4294967296 : $a;

    if (0 > $a){
		$a = ($a & 2147483647) + 2147483648;
    }
    $a %= 1000000; #1E6

    #print $a ^ $tkk,"\n";
    return sprintf("%i.%i",$a,($a ^ $tkk));
}

my $request = join(" ", @ARGV);
$request =~ s/^\s+//g;
print google_tk_hack($request);
