for d in */;
        do cd $d;
        for orb in */;
        do cd $orb
                cp ../*.loc ./
                cp ../*.xyz ./
                pwd;
                cd ..
        done
        cd ..
done
