#include "Player.hpp"
#include <iostream>
#include <string>

using namespace std;

Player::Player()
{
    m_vie = 100;
    m_damage = 20;
    m_mana = 100;
    m_name = "def";
}

void Player::receiveDamage(int nbDamage) // ok
{
    m_vie -= nbDamage;

    if (m_vie<0){
        m_vie = 0;
    }
}

void Player::attack(Player &target)
{
    target.receiveDamage(m_damage);
}

void Player::drinkPotion(int nbPotion)
{
    m_vie += nbPotion;

    if (m_vie>100){
        m_vie = 100;
    }
}

void Player::changeDamage(int nbDamage)
{
    m_damage = nbDamage;
}

bool Player::isAlive() const // ok
{
    return m_vie > 0;
}

void Player::printName() const
{
    cout << m_name << endl;
}