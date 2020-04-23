from flask import Flask, request, redirect
import sqlite3

app = Flask(__name__)


@app.route("/")
def homepage():
    return app.send_static_file("index.html")


@app.route("/SELECT")
def SELECT():
    with sqlite3.connect('CarCrash.db') as conn:
        cursor = conn.cursor()

        page = int(request.args.get('page', 1))
        offset = page * 50

        rows = list(cursor.execute(
            "select ID, City, State, Description from CarCrashData limit :offset, 50", locals()).fetchall())

        table_html = ""
        for row in rows:
            table_html += f"<tr><td><a href=/UPDATE?id={row[0]}>{row[0]}</td><td>" + '</td><td>'.join(
                row[1:]) + '</td></tr>'

        return f"""
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
        <h1 style="text-align:center;">This Table Selects Every Record From The Database</h1>
        <br>
        <br>
        <table class="w3-table-all">
        <tr><th>ID</th><th>City</th><th>State</th><th>Description</tr> 
        {table_html}
        </table>
        <a href="?page={page+1}">Next Page</a>
        """


@app.route("/CREATE_ACCIDENT", methods=['GET', 'POST'])
def POST():
    with sqlite3.connect('CarCrash.db') as conn:
        cursor = conn.cursor()

        query = cursor.execute(
            "INSERT INTO CarCrashData(ID,City,State,Description)  VALUES(:id, :city, :statecode, :description)",  {"id": request.form.get("id"),
                                                                                                                   "city": request.form.get("city"),
                                                                                                                   "statecode": request.form.get("statecode"),
                                                                                                                   "description": request.form.get("description")

                                                                                                                   })

        conn.commit()

        return f"""
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
        <h1 style="text-align:center;">POST A NEW RECORD TO THE DATABASE</h1>
        <br>
        <br>
        <form method = "post">
        <label for="id">ID:</label><br>
        <input type="text" id="id" name="id" value="">
        <br>
        <br>

        <label for="city">City:</label><br>
        <input pattern = "^[a-zA-Z0-9 ]*$" type="text" id="city" name="city" value=""><br><br>

        <label for="statecode">State Code:</label><br>
        <input maxlength="2" type="text" id="statecode" name="statecode" value=""><br><br>

        <label for="description">Description:</label><br>
        <input type="text" id="description" name="description" value=""><br><br>



        <input type="submit" value="Submit">
</form> 
        """


@app.route("/UPDATE", methods=['GET'])
def UPDATE_GET():
    with sqlite3.connect('CarCrash.db') as conn:
        cursor = conn.cursor()
        id = {"id": request.args.get("id")}
        cursor.execute("select ID, City, State, Description from CarCrashData Where ID = :id", {
                       "id": request.args.get("id")})
        row = cursor.fetchone()

        return f"""
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
        <h1 style="text-align:center;">UPDATE AN OLD ACCIDENT</h1>
        <br>
        <br>
        <form method = "post">
        <label for="id">Pre-Existing ID:</label><br>
        <input disabled type="text" id="id" name="id" value="{request.args.get("id")}">
        <br>
        <br>

        <label for="city">City:</label><br>
        <input pattern = "^[a-zA-Z0-9 ]*$" type="text" id="city" name ="city" value="{row[1]}"><br><br>

        <label for="statecode">State Code:</label><br>
        <input maxlength = "2" type="text" id="statecode" name="statecode" value="{row[2]}"><br><br>

        <label for="description">Description:</label><br>
        <input type="text" id="description" name="description" value="{row[3]}"><br><br>

        <input type="submit" value="Submit">
</form> 
        """


@app.route("/UPDATE", methods=['POST'])
def UPDATE_POST():
    with sqlite3.connect('CarCrash.db') as conn:
        cursor = conn.cursor()

        query = cursor.execute(
            "UPDATE CarCrashData SET City = :city, State = :statecode, Description = :description WHERE ID = :id",  {"id": request.form.get("id"),
                                                                                                                     "city": request.form.get("city"),
                                                                                                                     "statecode": request.form.get("statecode"),
                                                                                                                     "description": request.form.get("description")

                                                                                                                     })
        conn.commit()
    return redirect(f'/UPDATE?id={request.form.get("id")}')


@app.route("/DELETE", methods=['GET', 'POST'])
def DELETE():
    with sqlite3.connect('CarCrash.db') as conn:
        cursor = conn.cursor()

        query = cursor.execute("DELETE FROM CarCrashData WHERE ID = :id",  {
                               "id": request.form.get("id")})
        conn.commit()

    return f"""
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
        <h1 style="text-align:center;">DELETE AN ACCIDENT</h1>
        <br>
        <br>
        <form method = "post">
        <label for="id">Pre-Existing ID:</label><br>
        <input type="text" id="id" name="id" value="">
        <br>
        <br>
        <input type="submit" value="Submit">
        </form> 
        """


@app.route("/SEARCH_CITY")
def SEARCH_BY_CITY():
    with sqlite3.connect('CarCrash.db') as conn:

        cursor = conn.cursor()

        page = int(request.args.get('page', 0))

        offset = page * 50

        city = str(request.args.get('city', ""))

        rows = list(cursor.execute(
            "select ID, City, State, Description from CarCrashData Where City = :city limit :offset, 50", locals()).fetchall())

        rows = [
            '<tr><td>' + '</td><td>'.join(cols) + '</td></tr>' + '</td><td>' for cols in rows]

        return f"""
        

        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
        <h1 style="text-align:center;">Search For City in Which Accidents Occured</h1>
        

        <form class="w3-container w3-card-4 w3-light-grey">
        <p><label>Enter The City Name Here: </label>
        <input class="w3-input w3-border" placeholder="City Name" type="text" name="city">
        </form>
        

        <br>
        <br>
        <table class="w3-table-all">
        <tr><th>ID</th><th>City</th><th>State</th><th>Description</tr>
        {''.join(rows)}
        </table>
        <a href="?page={page+1}&city={city}">Next page</a>
        """


if __name__ == "__main__":
    app.run()
