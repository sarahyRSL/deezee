from .functions import *
from markupsafe import escape
from .auth import login_required
from flask import Blueprint, redirect, request, render_template, g

bp = Blueprint('routes', __name__)

@bp.route("/")
def home_page():
    return render_template("index.html")

@bp.route("/db-tables/<userID>", methods=["GET"])
@login_required
def db_tables(userID):
    context = {}
    context["error"] = None
    db = g.db
    # ensure user exists
    try:
        db.execute('SELECT * FROM users WHERE id = %s', (userID,))
        g.user = db.fetchone()
        if getattr(g, 'user', None) is None:
            context["error"] = "You do not have access to this page."
            return redirect("/unauthorized")
    except Exception as e:
        print('User Error:', e)
        return redirect("/unauthorized")
    # get data
    try:
        db.execute('SELECT * FROM employee')
        employees = db.fetchall()
        db.execute('SELECT * FROM vendors')
        vendors= db.fetchall()
        db.execute('SELECT * FROM locations')
        locations = db.fetchall()
        db.execute('SELECT * FROM vendor_locations')
        vendor_locations = db.fetchall()
        # do some math so each vendor has a 'ships_to' object based on the vendor_locations
        for location in vendor_locations:
            # find in vendors with this location
            list_of_vendors_with_location = [vendor for vendor in vendors if vendor['id'] == location['vendor_id']]
            for vendor in list_of_vendors_with_location:
                # find location.location_id in locations
                address = locations[location['location_id']-1]
                # add to vendor ship to list
                if 'ship_to' in vendor:
                    vendor['ship_to'].append(address['label'])
                else: 
                    vendor.update({'ship_to':[address['label']]})
        context['employees'] = employees
        context['vendors'] = vendors
        context['locations'] = locations
    except Exception as e:
        print('DB Error:', e)
        return redirect("/login")
    return render_template("dbTables.html", context=context)

@bp.route("/unauthorized", methods=["GET"])
def unauth():
    return render_template("unauthorized.html")

@bp.route("/employee-registration", methods=["GET", "POST"])
def employee_form():
    context = {}
    context["error"] = None
    db = g.db
    if request.method == "POST":
        # Process form data here
        name = escape(request.form["name"])
        email = escape(request.form["email"])
        phone = escape(request.form["phone"])
        # error check here
        if "@" not in email or ".com" not in email:
            context["error"] = "You must enter a valid email address. Please try again"
            context["name"] = name
            context["phone"] = phone
            return render_template("employeeRegistration.html", context=context)
        if not validate_phone_number(phone):
            context["error"] = "You must enter a valid phone number. Please try again"
            context["name"] = name
            context["email"] = email
            return render_template("employeeRegistration.html", context=context)
        try:
            # put info in db and send off email
            db.execute('INSERT INTO employee (name, email, phone) VALUES (%s, %s, %s)', (name, email, phone))
            employee = {'name':name, 'email':email, 'phone':phone}
            email = send_email('employee', employee)
            if email == 'error':
                context['error'] = "There was an issue sending your data to our team. \
                    Please send your information to deezee@rocksolidlogistics.com to ensure your information is saved properly. \
                    We're sorry for the inconvenience." 
            return redirect("/")
        except Exception as e:
            print('Employee Registration Error:', e)
            context["name"] = name
            context["email"] = email
            context['phone'] = phone
            context["error"] = "Could not connect to the database. Please try again."
    return render_template("employeeRegistration.html", context=context)

@bp.route("/vendor-registration", methods=["GET", "POST"])
def vendor_form():
    context = {}
    context["error"] = None
    db = g.db
    if request.method == "POST":
        # Process form data here
        name = escape(request.form["name"])
        company = escape(request.form["company"])
        email = escape(request.form["email"])
        phone = escape(request.form["phone"])
        address = escape(request.form["address"])
        address2 = escape(request.form["address2"])
        city = escape(request.form["city"])
        state = escape(request.form["state"])
        zip = escape(request.form["zip"])
        country = escape(request.form["country"])
        # error check here
        if "@" not in email or ".com" not in email:
            context["error"] = "You must enter a valid email address. Please try again"
            context["name"] = name
            context["phone"] = phone
            context["company"] = company
            context["address"] = address
            context["address2"] = address2
            context["city"] = city
            context["state"] = state
            context["zip"] = zip
            context["country"] = country
            return render_template("vendorRegistration.html", context=context)
        if not validate_phone_number(phone):
            context["error"] = "You must enter a valid phone number. Please try again"
            context["name"] = name
            context["email"] = email
            context["company"] = company
            context["address"] = address
            context["address2"] = address2
            context["city"] = city
            context["state"] = state
            context["zip"] = zip
            context["country"] = country
            return render_template("vendorRegistration.html", context=context)
        try:
            # put info in db
            db.execute(
                'INSERT INTO vendors (name, company, email, phone, address, address2, city, zip, country) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (name, company, email, phone, address, address2, city, zip, country)
            )
            vendor = db.execute(
                'SELECT * FROM vendors WHERE name=%s AND company=%s AND email=%s AND phone=%s AND address=%s AND address2=%s AND city=%s AND zip=%s AND country=%s',
                (name, company, email, phone, address, address2, city, zip, country)
            )
            vendor = db.fetchone()
            return redirect("/vendor-registration-two/"+str(vendor['id']))
        except Exception as e:
            print(e)
            context["error"] = "There was an issue processing your data. Please try again."
            context['phone'] = phone
            context["name"] = name
            context["email"] = email
            context["company"] = company
            context["address"] = address
            context["address2"] = address2
            context["city"] = city
            context["state"] = state
            context["zip"] = zip
            context["country"] = country
            return render_template("vendorRegistration.html", context=context)
    return render_template("vendorRegistration.html", context=context)

@bp.route("/vendor-registration-two/<vendor_id>", methods=["GET", "POST"])
def vendor_form_two(vendor_id):
    context = {}
    context["error"] = None
    context['vendor_id'] = vendor_id
    db = g.db
    # pull locations from db
    try:
        db.execute('SELECT * FROM locations')
        context['locations'] = db.fetchall()
    except Exception as e:
        print(e)
        context["error"] = "Could connect to the database. Please try again."
        return redirect("/vendorRegistrationTwo/"+str(vendor_id))
    if request.method == "POST":
        # Process form data here
        locations = []
        for value in request.form.values():
            locations.append(value)
        # error check here
        if len(locations) < 1:
            context["error"] = "Please select at least one location"
            print('no locations')
            return redirect("/vendorRegistrationTwo/"+str(vendor_id))
        try:
            db.execute('SELECT * FROM vendors WHERE id = %s', (vendor_id,))
            vendor = db.fetchone()
            for location in locations:
                db.execute('INSERT INTO vendor_locations (vendor_id, location_id) VALUES (%s, %s)', (vendor_id, location))
            addresses = []
            for location in locations:
                db.execute('SELECT * FROM locations WHERE id = %s', (location,))
                addresses.append(db.fetchone()['label'])
            vendor.update({'addresses':addresses})
            email = send_email('vendor', vendor)
            if email == 'error':
                context['error'] = "There was an issue sending your data to our team. \
                    Please send your information to deezee@rocksolidlogistics.com to ensure your information is saved properly. \
                    We're sorry for the inconvenience." 
            return redirect("/")
        except Exception as e:
            print('Location Error:',e)
            context["error"] = "There was a problem processing your data. Please try again."
    return render_template("vendorRegistrationTwo.html", context=context)
