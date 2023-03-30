for folder in */; do
        (cd "$folder"
        for file in ./OPT*.sh; do 
                echo "$file"
                sbatch "$file"
        done)
done
