# Unisex Bathroom  Problem

This project solves the unisex problem and prevents starvation to any sex of men and women.

1- Man can enter the bathroom if (there are free spaces AND no other woman is waiting AND no other woman is using the bathroom)
2- Woman can enter the bathroom if (there are free spaces AND no other man is waiting AND no other man is using the bathroom)
3- When Man exits the bathroom, we will look if there is any woman waits, so if there are at least one, we will switch the priority here to make this woman enter and if there are not any waiting woman we will enter another man and so on.
4- When Woman exits the bathroom, we will look if there is any men waits, so if there are at least one, we will switch the priority here to make this man enter and if there are not any waiting men, we will enter another man and so on.
5- The important thing here is to prevent starvation, by not allowing any men to enter the bathroom if there are women waiting and viceversa.

### Prerequisites

you have to install python 2.7 on your machine

### Installing

This is the way how you will run scripts

```
python main.py
```

OR

```
chmod +x main.py
./main.py
```

## Built With

* python 2.7

## Authors

* **Ali Abdelrahman** - *Initial work*
