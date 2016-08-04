# this is a script that will consolidate the whole process and automate it

source last_iteration_boundaries
echo ${last_iteration_lower_boundary}
echo ${last_iteration_upper_boundary}

echo "so present slice will be..."
present_iter_lower=`echo ${last_iteration_upper_boundary}`
present_iter_upper=$(( present_iter_lower + 30 ))

echo ${present_iter_lower}
echo ${present_iter_upper}

echo "get the data.out"
python organise_retrieved_data.py ${present_iter_lower} ${present_iter_upper} > data.out

echo "create the x and y:"

## or the following lines should do it. be vary careful
this changes the data

sed "s/], /],\n/g" data.out > data.out_bak
mv data.out_bak data.out
sed "s/]]/],\n/g" data.out > data.out_bak
mv data.out_bak data.out
sed "s/],//g" data.out > data.out_bak
mv data.out_bak data.out
sed "s/,//g" data.out > data.out_bak
mv data.out_bak data.out
sed "s/\[//g" data.out > data.out_bak
mv data.out_bak data.out

# this will take the 10% data lines in a file randomly
awk 'BEGIN {srand()} !/^$/ { if (rand() <= .1) print $0}' data.out > data_test.out

cat data.out | awk '{ print $(NF) }' > y_data.out

cat data_test.out | awk '{ print $(NF) }' > y_data_test.out

## remove the last digit(y part) from data.out and data_test.out

sed "s/\w*$//" data.out > data.out_bak
mv data.out_bak data.out

sed "s/\w*$//" data_test.out > data_test.out_bak
mv data_test.out_bak data_test.out

echo "now the model part:"
python run_saved_batsman_out_model.py

echo "change the model to existing one and cleaning"
mv batsman_out_model_new.json batsman_out_model.json
mv batsman_out_model_weights_new.hdf5 batsman_out_model_weights.hdf5

l_line=`cat last_iteration_boundaries | grep last_iteration_lower_boundary`
sed "s/${l_line}/last_iteration_lower_boundary=${present_iter_lower}/g" last_iteration_boundaries > last_iteration_boundaries_bak
mv last_iteration_boundaries_bak last_iteration_boundaries

u_line=`cat last_iteration_boundaries | grep last_iteration_upper_boundary`
sed "s/${u_line}/last_iteration_upper_boundary=${present_iter_upper}/g" last_iteration_boundaries > last_iteration_boundaries_bak
mv last_iteration_boundaries_bak last_iteration_boundaries
