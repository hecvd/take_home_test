from celebration_app.guest_list import Guests


def main():
    office_location = (53.339428, -6.257664)
    guests = Guests(office_location)
    guest_list = guests.get_guest_list("assets/customers.txt", 100)
    print "{:10}{}".format("User Id", "Name")
    for guest in guest_list:
        print "{g[0]:<10}{g[1]}".format(g=guest)
    print "\nCount: {}".format(len(guest_list))


if __name__ == "__main__":
    main()
