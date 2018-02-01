from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from celebration_app.guest_list import Guests

guest_list_page = Blueprint(
    "guest_list_page", __name__, template_folder="templates")


@guest_list_page.route("/")
def show_guest_list():
    """Renders the list of guests within a 100km radius.

    :return: A rendered HTML ready to be handled by flask.
    """
    try:
        office_location = (53.339428, -6.257664)
        guests = Guests(office_location)
        guest_list = guests.get_guest_list("assets/customers.txt")
        return render_template("show_guests.html", guest_list=guest_list)
    except TemplateNotFound:
        abort(404)
