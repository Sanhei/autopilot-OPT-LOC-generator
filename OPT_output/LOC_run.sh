for folder in */; do
        (cd "$folder"
        for file in ./LOC*.sh; do 
                sbatch "$file"
        done)
done
