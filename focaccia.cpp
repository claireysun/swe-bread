/**
 * focaccia.cpp
 *
 * Ava Schmidt
 * Avajian@umich.edu
 *
 * EECS 183: Project 1
 * Fall 2021
 * 
 * Project UID: fde244392017fe65ebcc34f01c226b11f113bb3dc6dae8af4cb6ea11bf76f7c8
 */

#include <iostream>
#include <cmath>
#include <string>
using namespace std;

/**
 * Returns the singular or plural form of a word, based on number
 *
 * Requires: singular is the singular form of the word.
 *           plural is the plural form of the word.
 *           number determines how many things there are; must be >= 0.
 * Modifies: Nothing.
 * Effects:  Returns return the singular form of the word if number == 1.
 *           Otherwise, returns the plural form.
 * Examples:
 *           // prints "bag"
 *           cout << pluralize("bag", "bags", 1);
 *
 *           // prints "pounds"
 *           string temp = pluralize("pound", "pounds", 3);
 *           cout << temp;
 */
string pluralize(string singular, string plural, int number);

int main() {
    
    int people;
    cout << "How many people do you need to serve? ";
    cin >> people;
    cout << endl << endl;
    
    //calculate total loaves needed
    
    const double PEOPLE_PER_LOAF = 4.0;
    int numLoaves = ceil(people/ PEOPLE_PER_LOAF);
    
    cout << "You need to make: " << numLoaves << pluralize(" loaf", " loaves", numLoaves) << " of focaccia" << endl << endl;
   
    cout << "Shopping List for Focaccia Bread" << endl;
    cout << "--------------------------------" << endl;
    
    const double FLOUR_CUPS_PER_LOAF = 5;
    const double FLOUR_CUPS_PER_BAG = 20;
    const double PACKAGES_YEAST_PER_LOAF = 1.75;
    const double PACKAGES_YEAST = 2.25;
    const double CANISTERS_SALT_PER_LOAF = 1.875;
    const double CANISTERS_SALT = 6;
    const double TABLESPOONS_OLIVE_OIL_PER_LOAF = 2;
    const double BOTTLES_OLIVE_OIL = (500/14.8);
   
    //calculate measurement of ingredients
    double bagsFlour = ceil(numLoaves * (FLOUR_CUPS_PER_LOAF/FLOUR_CUPS_PER_BAG));
    double packagesYeast = ceil(numLoaves * (PACKAGES_YEAST_PER_LOAF/ PACKAGES_YEAST));
    double canistersSalt = ceil(numLoaves * (CANISTERS_SALT_PER_LOAF/ CANISTERS_SALT));
    double bottleOliveOil = ceil(numLoaves * (TABLESPOONS_OLIVE_OIL_PER_LOAF/BOTTLES_OLIVE_OIL));
    
    cout << bagsFlour << pluralize(" bag", " bags", bagsFlour) << " of flour" << endl;
    cout << packagesYeast << pluralize(" package", " packages", packagesYeast) << " of yeast" << endl;
    cout << canistersSalt << pluralize(" canister", " canisters", canistersSalt) << " of salt" << endl;
    cout << bottleOliveOil << pluralize(" bottle", " bottles", bottleOliveOil) << " of olive oil" << endl << endl;
    
    double priceFlour = 2.69 * bagsFlour;
    double priceYeast = 0.40 * packagesYeast;
    double priceSalt = 0.49 * canistersSalt;
    double priceOliveOil = 6.39 * bottleOliveOil;
    
    //calculate the total price of ingredients
    
    double numPrice = (priceFlour + priceYeast + priceSalt + priceOliveOil);
    
    cout << "Total expected cost of ingredients: " << "$" << numPrice << endl << endl;
    cout << "Have a great party!" << endl;

    return 0;
}

// ----------------------------------------------
// *** DO NOT CHANGE ANYTHING BELOW THIS LINE ***

string pluralize(string singular, string plural, int number) {
    if (number == 1) {
        return singular;
    }
    return plural;
}
