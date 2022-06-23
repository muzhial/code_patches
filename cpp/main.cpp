#include <iostream>
#include <string>
#include <vector>
#include <algorithm>


int main() {
    std::vector<int> c{0, 1, 2, 3, 4, 5, 6};
    c.erase(std::remove_if(c.begin(),
                           c.end(),
                           [] (int id) { return id == 2; }),
            c.end());

    for (auto &e : c) {
        std::cout << e << std::endl;
    }
}
