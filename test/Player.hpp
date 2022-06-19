#ifndef DEF_PLAYER
#define DEF_PLAYER

#include <string>

class Player
{
    public: 

    Player();
    void receiveDamage(int nbDamage); // ok
    void attack(Player &target);
    void drinkPotion(int nbPotion);
    void changeDamage(int damage);
    bool isAlive() const; // ok
    void printName() const;

    private:

    std::string m_name;
    int m_vie;
    int m_mana;
    int m_damage;
};

#endif