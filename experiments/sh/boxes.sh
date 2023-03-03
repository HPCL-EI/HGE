cd ..
#algo_list=()
run=100

#for ((seed=0;seed< $run;seed++))
#do
#python run.py --M 2 --C 5 --W 5 --exp game --algo "GE+R" --seed $seed
#done


for algo in "GE+PGE" "GE+GE" "R+R" "R+PR" "R+GE" "R+PGE" "GE+R" "GE+PR"
do
  for ((seed=0;seed< $run;seed++))
  do
  python run.py --M 2 --C 10 --W 10 --exp game --algo $algo --seed $seed
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
