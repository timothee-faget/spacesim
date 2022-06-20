#include <iostream>
#include <string>
#include <vector>
#include <cmath>

using namespace std;

double distance(vector<double> pos_1, vector<double> pos_2);

int main(){
    bool test_chain(false);
    bool test_dist(true);

    if (test_chain){
        string chain;
        cout << "What do you want to display?" << endl;
        getline(cin, chain);
        cout << "The sentence to display is:" << endl;
        cout << chain << endl;
    }
    
    if (test_dist){
        vector<double> pos_A(3, 1);
        vector<double> pos_B(1, 0);
        cout << "Distance between the points is:" << endl;
        cout << distance(pos_A, pos_B) << endl; 
    }

    return 0;  
}




double distance(vector<double> pos_1, vector<double> pos_2){
    double dx = (pos_1[0] - pos_2[0]);
    double dy = (pos_1[1] - pos_2[1]);
    double dz = (pos_1[2] - pos_2[2]);
    double distance = sqrt(dx*dx + dy*dy + dz*dz);

    return distance;
}