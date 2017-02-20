startdate=20070101
enddate=`date +%Y%m%d`

curr="$startdate"
while true; do
    echo "$curr"
    [ "$curr" \< "$enddate" ] || break
    curr=$( date +%Y%m%d --date "$curr +1 day" )
done
