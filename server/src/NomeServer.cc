#include <iostream>

int main(int argc, char** argv) {
    if (argc != 1) {
        std::cerr << "Usage: " << argv[0] << " <port>" << std::endl;
        return 1;
    }
    std::cout << "Server started" << std::endl;
    return 0;
}