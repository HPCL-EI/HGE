cd ..
#algo_list=()
#n1=1
#n2=1
#c1=21
#n3=1

n1=100
n2=100
c1=101
n3=100


for algo in "GE+PGE" "GE+GE" "R+R" "R+PR" "R+GE" "R+PGE" "GE+R" "GE+PR"
do
  for ((seed=0;seed< $n1;seed++))
  do
  python run.py --M 2 --C 10 --W 10 --population_size 5 --generations 5 --exp game --algo $algo --seed $seed
  done
done

C=10
for ((seed=0;seed< $n2;seed++))
do
python run.py --M 2 --C $C --W 10 --population_size 20 --generations 20 --exp game --algo "GE+PGE" --seed $seed
done

for ((seed=0;seed< $n2;seed++))
do
python run.py --M 2 --C $C --W 10 --population_size 10 --generations 10 --exp game --algo "GE+PGE" --seed $seed
done

for ((seed=0;seed< $n2;seed++))
do
python run.py --M 2 --C $C --W 10 --population_size 5 --generations 5 --exp game --algo "GE+PGE" --seed $seed
done

for ((seed=0;seed< $n2;seed++))
do
python run.py --M 2 --C $C --W 10 --population_size 5 --generations 5 --exp game --algo "GE+PR" --seed $seed
done

for ((seed=0;seed< $n2;seed++))
do
python run.py --M 2 --C $C --W 10 --population_size 5 --generations 5 --exp game --algo "GE+R" --seed $seed
done

for ((seed=0;seed< $n2;seed++))
do
python run.py --M 2 --C $C --W 10 --population_size 5 --generations 5 --exp game --algo "GE+GE" --seed $seed
done

for ((seed=0;seed< $n2;seed++))
do
python run.py --M 2 --C $C --W 10 --population_size 10 --generations 10 --exp game --algo "GE+GE" --seed $seed
done

for ((seed=0;seed< $n2;seed++))
do
python run.py --M 2 --C $C --W 10 --population_size 20 --generations 20 --exp game --algo "GE+GE" --seed $seed
done


for ((seed=0;seed< $n3;seed++))
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
#python run.py --exp game --algo R+PGE --result_folder boxes_results --seed $seed
#done
#
#for ((seed=0;seed< $run;seed++))
#do
#python run.py --exp game  --algo GE+PGE --result_folder boxes_results --seed $seed
#done
#
#for ((seed=0;seed< $run;seed++))
#do
#python run.py --exp game --algo GE+P --result_folder boxes_results --seed $seed
#done
#
#for ((seed=0;seed< $run;seed++))
#do
#python run.py --exp game  --algo R+R --result_folder boxes_results --seed $seed
#done
#
#for ((seed=0;seed< $run;seed++))
#do
#python run.py --exp game --algo R+GE --result_folder boxes_results --seed $seed
#done
#
#for ((seed=0;seed< $run;seed++))
#do
#python run.py --exp game --algo GE+R --result_folder boxes_results --seed $seed
#done
#
#for ((seed=0;seed< $run;seed++))
#do
#python run.py --exp game  --algo GE+GE --result_folder boxes_results --seed $seed
#done
