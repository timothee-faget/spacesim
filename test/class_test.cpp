#include "Player.hpp"
#include <iostream>

int main(){
    Player tim, clara;

    tim.attack(clara);
    clara.drinkPotion(10);
    clara.attack(tim);
    tim.changeDamage(50);
    tim.attack(clara);

    tim.printName();
    clara.printName();

    return 0;
}