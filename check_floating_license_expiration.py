#!/usr/bin/env python
# Author: Eric Jay Stevens
# Version 0.1
# Last updated 2014 November
#==============================================================#
#                                                              #
# !!!IMPORTANT!!!                                              #
#                                                              #
# set the  $path_to_lmutil variable and set the location       #
# for your lmutil executable, which you must obtain from       #
# www.macrovision.com for your OS.                             #
#                                                              #
#==============================================================#

import argparse
import subprocess
import os
import sys
from datetime import date
from time import strptime

serviceState = {'ok': 0, 'warning' : 1, 'critical' : 2, 'unknown' :  3}

### handle arguments
parser = argparse.ArgumentParser(description="Test a Seat license feature for expiration")
parser.add_argument("-p","--port", help="The port the license deamon is running on.", default="27000")
parser.add_argument("-s","--server", help="The ip address or name of the license server.")
parser.add_argument("-f","--feature", help="The Name of the feature you are checking for expiration")
parser.add_argument("-t","--threshold", help="The Number of days before a warning state should", default="45")
parser.add_argument("-m","--license_manager", help="name of license manger the vendor is using", default="flexNet") 
parser.add_argument("-v","--verbose", help="Increaser verbosity")
args = parser.parse_args()

def main():
    if (not validateArgs(args)):
    	return False
        
    status = getLicenseStatusOutput(args.license_manager,args.server,args.port)
    expFeature = getExpFeature(status,args.feature)

    if expFeature.daysUntilExpiration < 1:
        print "critical:", expFeature.name, "expired on", expFeature.expDate 
    	sys.exit(serviceState['critical'])
    elif expFeature.daysUntilExpiration < int(args.threshold):
        print "warning:", expFeature.name, "expires on", expFeature.expDate 
    	sys.exit(serviceState['warning'])
    else:
        print "ok:", expFeature.name, "expires in", expFeature.daysUntilExpiration, "days." 
    	sys.exit(serviceState['ok'])


def getExpFeature(status,feature):

    lmOutput = status.split("\n")
    featureStatuses = []
    features = []
    expectedFormat = False

    isPartOfTable = False 
    for line in lmOutput:
        if line.startswith("___"):
        	isPartOfTable = True
        	expectedFormat = True
        if (isPartOfTable and not line.startswith("___")):
    	     featureStatuses.append(line)

    for featureLine in featureStatuses:
        if args.verbose:
            print featureLine
        ls = featureLine.split()
        if ls:
            myFeature = Feature(ls[0],ls[1],ls[2],ls[3],ls[4])
            myFeature.daysUntilExpiration()
            features.append(myFeature)

    if not expectedFormat:
        print "unknown: output from license manager in unexpected format"
    	sys.exit(serviceState['unknown'])


    #sort features by which one is expiring soonest
    features.sort(key=lambda x: x.daysUntilExpiration)

    # if feature name was specified return that feature
    # else return the feature the expires soonest 
    if feature:
        for f in features:
            if f.name == feature:
            	return f
        print(feature + " not found")
        sys.exit(serviceState['unknown'])
    else:
        if features[0]:
    	    return features[0]
        else:
            print(feature + " not found")
            sys.exit(serviceState['unknown'])

class Feature:
    def __init__(self, name, version, numberOfLicenses, expDate, vendor):
        self.name = name
        self.version = version
        self.numberOfLicenses = numberOfLicenses
        self.expDate = expDate
        self.vendor = vendor
        self.daysUntilExpiration
    
    def daysUntilExpiration(self):
        s = self.expDate.split("-")
        year = int(s[2])

        #converts Month names (like Jan) to an ordinal number
        month = int(strptime(s[1],"%b").tm_mon)
        day = int(s[0])

        if (year > 2035 or year < 100):
        	year = 2035
        expires = date(year, month, day)
        delta = expires - date.today()
        self.daysUntilExpiration = delta.days
        return delta.days

def getLicenseStatusOutput(licManager,server,port):

    if (licManager == "flexNet"):
    	lmutilPath = "/usr/local/nagios/libexec/lmutil"
    	
        licStatus = os.popen(lmutilPath + " lmstat -a -c " + port + "@" + server + " -i").read()
        return licStatus
                    

def validateArgs(args):

    try:
        float(args.port)
    except ValueError:
    	print "port non numeric"
    	return False

    return True

main()
'''
my $path_to_lmutil = "/usr/local/nagios/libexec/lmutil";   # path to the lmutil executable on the system.  Make sure the web server user can run it!

$port = " " if (!$port); # no port for default

my $lmstat_output;
$lmstat_output = `$path_to_lmutil lmstat -a -c $port\@$hostname -i -f $feature`;  # Get output of lmstat from port $port on FLEXlm server $server

if ($verbose) {print $lmstat_output;}

my @lmstat_lines = split /\n/, $lmstat_output;
for $line (@lmstat_lines) {
    if ($line =~ /^$feature/){ 
        my @values = split(/\s+/,$line);
	if (defined $myFeature){
            if ($myFeature->{_version} < $values[1]) {
                     
                $myFeature = new LmFeature($values[0],$values[1],$values[3]);

            } 
        } else {

            $myFeature = new LmFeature($values[0],$values[1],$values[3]);
        }
    }
}





say $myFeature->{_expirationDate};
my @parsedTime = split('-',$myFeature->{_expirationDate});

my $year = @parsedTime[2];
my $month = @parsedTime[1];
my $day = @parsedTime[0];

my $expDate = DateTime->new(
    year       => @parsedTime[2],
    month      => @parsedTime[1],
    day        => @parsedTime[0],
    hour       => 0,
    minute     => 0,
    second     => 0,
    nanosecond => 0,
    time_zone  => "floating",
);

if ($expDate=>{year} == "0000") { 
    say "does not expire" ;
    exit (0) if ($owc_output =~ /^FLEXlm OK/);
} 
else {
    say $year ;
}

#print $lmstat_output;




exit (1) if ($owc_output =~ /^FLEXlm WA/);
exit (2) if ($owc_output =~ /^FLEXlm CR/);

#@ MAIN_LOGIC

exit (3);



# owc_stat will read in lmstat output and display its status as CRITICAL, WARNING, or OK
#
# CRITICAL = At least one vendor daemon on this server is down.
# WARNING = All vendor daemons are up, but at least one feature reached %warning in use (% warning = % in use).
# OK = All vendor daemons are up, all licensed features have at least one license available for checkout.
#
sub owc_stat {
        my $lmstat_output = shift;
        my $output;
        # Split the lines of $lmstat_output at the newlines.
        my @lmstat_lines = split /\n/, $lmstat_output;
        my $red_flag = 0;
        my $yellow_flag = 0;
        my $yellow_feats = [];
        my $features = 0;
        my $current_use = 0;
        my $tot_lic = 0;
        my $perc_in_use = 0;
        for (@lmstat_lines)
        {
                if ($features eq 0)
                {
                        $red_flag ++ if ((/[Cc]annot/)||(/[Uu]nable/)||(/refused/)||(/down/)||(/[Ww]in[sS]ock/));
                }
                else
                {
                        if (/Users of (.*): .* of ([0-9]+) .* issued; .* of ([0-9]+) .* use/)
                        {
                                 my $available_licenses = $2 - $3;
                                 $current_use = $3;
                                 $tot_lic = $2;
                                 $perc_in_use = ($current_use/$tot_lic)*100;
                                 if ($perc_in_use > $warning)
                                 {
                                        $yellow_flag ++;
                                        push @$yellow_feats, $1;
                                 }
                        }
                }
                #if ($curfile =~ /.+_[0-9]{4}\.([a-zA-Z]{3,4})\.Z$/)
                $features ++ if (/Feature usage info:/)||(/Users of features served by $vendor:/);
        }
        if ($red_flag > 0)
        {
                $output = "FLEXlm CRITICAL: License Server Down or Unreachable.\n";
        }
        elsif ($yellow_flag > 0)
        {
                $output = "FLEXlm WARNING: Reach Usage Warning for Features: ";
                for my $feat (@$yellow_feats)
                {
                        $output .= $feat . " ";
                }
                $output .=$tot_lic;
                $output .=" Current users = ";
                $output .=$current_use;
                $output .=" - ";
                $output .=int($perc_in_use);
                $output .="% in use| user=";
                $output .= $current_use;
                $output .="\n";
        }
        else
        {
                $output = "FLEXlm OK: Tot license = ";
                $output .=$tot_lic;
                $output .=" Current users = ";
                $output .=$current_use;
                $output .=" - ";
                $output .=int($perc_in_use);
                $output .="% in use| user=";
                $output .= $current_use;
      
                $output .="\n";        
        }
        return ($output);
}

package LmFeature;
sub new
{
    my $class = shift;
    my $self = {
        _name => shift,
        _version  => shift,
        _expirationDate  => shift,
    };
    bless $self, $class;
    return $self;
}

# ----------------------------------------------------------------------
'''
