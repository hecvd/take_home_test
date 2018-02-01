import os
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from celebration_app.guests import FindGuests

guest_list_page = Blueprint(
    "guest_list_page", __name__, template_folder="templates")


@guest_list_page.route("/")
def show_guest_list():
    """Renders the list of guests within a 100km radius.

    :return: A rendered HTML ready to be handled by flask.
    """
    try:
        source_file = os.path.abspath(
            os.path.join(__file__,  "../../assets/customers.txt"))
        office_location = (53.339428, -6.257664)
        guests = FindGuests(office_location)
        guest_list = guests.get_guest_list(source_file)
        return render_template("show_guest_list.html", guest_list=guest_list)
    except TemplateNotFound:
        abort(404)
