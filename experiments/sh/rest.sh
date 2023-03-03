cd ..
#algo_list=()
#n1=1
#n2=1
#c1=21
#n3=1

n1=0
n2=100
#n2=100
#c1=101
#n3=100


for ((seed=$n1;seed< $n2;seed++))
do
python run.py --M 4 --C 100 --W 10 --population_size 5 --generations 5 --exp game --algo "GE+PGE" --seed $seed
python run.py --M 4 --C 100 --W 10 --population_size 5 --generations 5 --exp game --algo "GE+GE" --seed $seed
done

