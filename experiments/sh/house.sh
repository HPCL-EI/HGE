cd ..
#algo_list=()
#n1=1
n2=10
#c1=21
#n3=1

for ((seed=0;seed< $n2;seed++))
do
python run.py --exp house --algo "GE+GE" --seed $seed
done
