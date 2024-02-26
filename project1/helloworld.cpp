//#include <boost/asio/ip/host_name.hpp>
#include <iostream>
#include <unistd.h>
#include <limits.h>

int main() {
	char hostname[HOST_NAME_MAX];
	char username[LOGIN_NAME_MAX];
	gethostname(hostname, HOST_NAME_MAX);
	getlogin_r(username, LOGIN_NAME_MAX);
	std::cout << "Hello, " << username << ", the host name of your machine is: " << hostname << std::endl;
}



