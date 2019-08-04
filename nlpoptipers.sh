output_path=$1
dimension_pd=$2
dataset_name=$3
path_to_dataset=$4

optiperslp -p "$output_path" -d "$dimension_pd" -n "$dataset_name" "$path_to_dataset"
