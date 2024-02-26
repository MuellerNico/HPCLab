#include <boost/asio/ip/host_name.hpp>

int main() {
	const auto host_name = boost::asio::ip::host_name();
	std::cout << host_name;
}
