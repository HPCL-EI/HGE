cd ..
run=100
#list=`cat $(dirname $0)/game_settings.txt`
#echo $list

for ((seed=0;seed< $run;seed++))
do
  cat sh/game_settings.txt | while read line
  do
    for algo in 'GE+GE' 'GE+PGE'
    do
      arr=(${line})
      python run.py --exp game --algo $algo --M ${arr[0]} --C ${arr[1]} --W ${arr[2]} --seed $seed
    done
  done
done



#for ((seed=0;seed< $run;seed++))
#do
#python run_game.py --algo R+P --seed $seed
#done
