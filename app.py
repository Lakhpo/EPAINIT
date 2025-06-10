from flask import Flask, request, render_template_string, redirect, url_for, session
import os

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.secret_key = "super_secret_key"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


def main(
    inp_path,
    csv_path,
    min_pressure,
    max_velocity,
    min_velocity,
    population_size,
    num_generations,
):
    print("✅ Running main() with:")
    print(f"{inp_path=}")
    print(f"{csv_path=}")
    print(f"{min_pressure=}, {max_velocity=}, {min_velocity=}")
    print(f"{population_size=}, {num_generations=}")
    # Your GA logic here


HTML_FORM = """
<!DOCTYPE html>
<html>
<head><title>GA Setup</title></head>
<body>
  <h2>Step 1: Upload Files and Parameters</h2>
  <form method="post" enctype="multipart/form-data" action="{{ url_for('form') }}">
    INP File: <input type="file" name="inp_file"><br>
    CSV File: <input type="file" name="csv_file"><br>
    Min Pressure: <input type="text" name="min_pressure"><br>
    Max Velocity: <input type="text" name="max_velocity"><br>
    Min Velocity: <input type="text" name="min_velocity"><br>
    Population Size: <input type="text" name="population_size"><br>
    Generations: <input type="text" name="num_generations"><br>
    <input type="submit" value="Upload and Save Settings">
  </form>

  {% if session.saved %}
    <hr>
    <h3>✅ Inputs Saved. Now Validate them:</h3>
    <form method="post" action="{{ url_for('run_validation') }}">
        <input type="submit" value="Run Validation)">
    </form>
  {% endif %}
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        inp_file = request.files["inp_file"]
        csv_file = request.files["csv_file"]

        inp_path = os.path.join(app.config["UPLOAD_FOLDER"], inp_file.filename)
        csv_path = os.path.join(app.config["UPLOAD_FOLDER"], csv_file.filename)

        # inp_file.save(inp_path)
        # csv_file.save(csv_path)

        # Save values in session (or temp storage)
        session["inp_path"] = inp_path
        session["csv_path"] = csv_path
        session["min_pressure"] = request.form["min_pressure"]
        session["max_velocity"] = request.form["max_velocity"]
        session["min_velocity"] = request.form["min_velocity"]
        session["population_size"] = request.form["population_size"]
        session["num_generations"] = request.form["num_generations"]
        session["saved"] = True

        return redirect(url_for("form"))

    return render_template_string(HTML_FORM)


HTML_VALIDATION = """
<!DOCTYPE html>
<html>
<head><title>✅ data Validated Good Job Lakhpo. Check terminal/logs.</title></head>
<body>

<hr>
    <h3>✅ Inputs Saved. RUN GA:</h3>
    <form method="post" action="{{ back }}">
        <input type="submit" value="form)">
    </form>

"""


@app.route("/validate", methods=["POST"])
def run_validation():
    if session.get("saved"):
        print("Running Validation")
        print(session["min_pressure"])
        try:

            min_pressure = float(session["min_pressure"])
        except:
            return "⚠️ MIN PRESSURE"
        try:
            max_velocity = float(session["max_velocity"])
        except:
            return "⚠️ MAX VELOCITY"
        try:
            min_velocity = float(session["min_velocity"])
        except:
            return "⚠️ MIN VELOCITY"
        try:
            population_size = int(session["population_size"])
        except:
            return "⚠️ NUM POPULATION SIZE"
        try:
            num_generations = int(session["num_generations"])
        except:
            return "⚠️ NUM GENERATIONS"

        return HTML_VALIDATION


@app.route("/run_main", methods=["POST"])
def run_main():
    if session.get("saved"):
        print("IT RAN LOL")
        main(
            inp_path=session["inp_path"],
            csv_path=session["csv_path"],
            min_pressure=session["min_pressure"],
            max_velocity=session["max_velocity"],
            min_velocity=session["min_velocity"],
            population_size=session["population_size"],
            num_generations=session["num_generations"],
        )
        return "✅ main() ran successfully. Check terminal/logs."
    return "⚠️ No input data found. Please upload first."


if __name__ == "__main__":
    app.run(debug=True)
