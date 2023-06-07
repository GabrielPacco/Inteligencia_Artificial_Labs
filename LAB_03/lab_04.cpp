#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <ctime>

using namespace std;

const int POPULATION_SIZE = 100;
const int NUM_GENERATIONS = 1000;
const double MUTATION_RATE = 0.05;
const double CROSSOVER_RATE = 0.8;

struct City {
    char name;
    double x, y;
};

struct Individual {
    vector<char> chromosome;
    double fitness;
};

vector<City> cities = {
    {'G', 1, 1},
    {'A', 2, 3},
    {'B', 3, 2},
    {'R', 4, 4},
    {'I', 5, 5},
    {'E', 6, 6},
    {'L', 7, 7},
    {'P', 8, 8},
    {'C', 9, 9},
    {'O', 10,10}
};

double distance(City a, City b) {
    return sqrt(pow(a.x - b.x, 2) + pow(a.y - b.y, 2));
}

double pathLength(vector<char> path) {
    double length = 0;
    for (int i = 0; i < path.size() - 1; i++) {
        City a = cities[path[i] - 'A'];
        City b = cities[path[i + 1] - 'A'];
        length += distance(a, b);
    }
    return length;
}

Individual createIndividual() {
    Individual individual;
    individual.chromosome = vector<char>(cities.size());
    for (int i = 0; i < cities.size(); i++) {
        individual.chromosome[i] = cities[i].name;
    }
    random_shuffle(individual.chromosome.begin(), individual.chromosome.end());
    individual.fitness = pathLength(individual.chromosome);
    return individual;
}

vector<Individual> createPopulation() {
    vector<Individual> population(POPULATION_SIZE);
    for (int i = 0; i < POPULATION_SIZE; i++) {
        population[i] = createIndividual();
    }
    return population;
}

bool compareIndividuals(Individual a, Individual b) {
    return a.fitness < b.fitness;
}

void evaluatePopulation(vector<Individual>& population) {
    for (int i = 0; i < population.size(); i++) {
        population[i].fitness = pathLength(population[i].chromosome);
    }
}

Individual rouletteSelection(vector<Individual>& population) {
    double totalFitness = 0;
    for (int i = 0; i < population.size(); i++) {
        totalFitness += population[i].fitness;
    }
    
    double value = (double)rand() / RAND_MAX * totalFitness;
    
    for (int i = 0; i < population.size(); i++) {
        value -= population[i].fitness;
        if (value <= 0) return population[i];
    }
    
    return population[population.size() -1];
}

vector<Individual> OBX(Individual parent1, Individual parent2) {
    
   int size=parent1.chromosome.size();
   vector<char> p1,p2;
   vector<int> p1_index,p2_index;

   for(int i=0;i<size;i++){
       p1.push_back(parent1.chromosome[i]);
       p2.push_back(parent2.chromosome[i]);
       p1_index.push_back(0);
       p2_index.push_back(0);
   }

   int num_points=rand()%size;

   vector<int> points;

   for(int i=0;i<num_points;i++){
       int point=rand()%size;
       points.push_back(point);
       p1_index[point]=1;
       p2_index[point]=1;
   }

   sort(points.begin(),points.end());

   for(int i=0;i<num_points;i++){
       int point=points[i];
       p1[point]=parent2.chromosome[point];
       p2[point]=parent1.chromosome[point];
   }

   int index1=0,index2=0;

   for(int i=0;i<size;i++){
       if(p1_index[i]==0){
           while(p2_index[index1]==1){
               index1++;
           }
           p1[i]=parent2.chromosome[index1++];
       }
       if(p2_index[i]==0){
           while(p1_index[index2]==1){
               index2++;
           }
           p2[i]=parent1.chromosome[index2++];
       }
   }

   vector<Individual> children(2);
   children[0].chromosome=p1;
   children[1].chromosome=p2;

   return children;

}


void mutate(Individual& individual) {
    
     int size=individual.chromosome.size();
     int index=rand()%size;

     int swap_index=rand()%size;

     swap(individual.chromosome[index],individual.chromosome[swap_index]);

}

vector<Individual> evolvePopulation(vector<Individual>& population) {
    
     sort(population.begin(),population.end(),compareIndividuals);

     vector<Individual> new_population;

     new_population.push_back(population[0]);
     new_population.push_back(population[1]);

     while(new_population.size()<population.size()){

         Individual parent1=rouletteSelection(population);
         Individual parent2=rouletteSelection(population);

         vector<Individual> children=OBX(parent1,parent2);
         
         evaluatePopulation(children);

         new_population.push_back(children[0]);
         new_population.push_back(children[1]);

     }

     for(int i=2;i<population.size();i++){
         if((double)rand()/RAND_MAX<MUTATION_RATE){
             mutate(new_population[i]);
         }
     }

     evaluatePopulation(new_population);

     return new_population;

}

int main() {

    srand(time(NULL));

    ofstream file("output.txt");

    vector<Individual> population=createPopulation();

    evaluatePopulation(population);

    sort(population.begin(),population.end(),compareIndividuals);

    for(int i=0;i<population.size();i++){
    file<<i+1<<": ";
    for(int j=0;j<population[i].chromosome.size();j++){
        file<<population[i].chromosome[j]<<" ";
    }
    file<<"("<<population[i].fitness<<")"<<endl;
    }

    file<<endl;

    for(int generation=0;generation<NUM_GENERATIONS;generation++){

    file<<"Generation "<<generation+1<<":"<<endl;

    population=evolvePopulation(population);

    sort(population.begin(),population.end(),compareIndividuals);

    for(int i=0;i<population.size();i++){
        file<<i+1<<": ";
        for(int j=0;j<population[i].chromosome.size();j++){
            file<<population[i].chromosome[j]<<" ";
        }
        file<<"("<<population[i].fitness<<")"<<endl;
    }

    file<<endl;
    }
}
