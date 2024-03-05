import os
from flask import Flask, flash, request, redirect, url_for, render_template_string, send_file
from werkzeug.utils import secure_filename
from flask import send_from_directory
from ultralytics import YOLO

UPLOAD_FOLDER = 'images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'} #todo shorten to just images

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            results = predict(filename=filename)
            # show image and results
            image_and_results = create_image_and_text(file_name=filename, results=results)
            #return results
            return image_and_results # test how it looks on webpage, but when a file is posted

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

def create_image_and_text(file_name, results):
    # Get the path to the file in the results folder
    results_folder = 'results'
    file_path = os.path.join(results_folder, file_name)

    # Define the one-line string

    # Define the HTML template
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Results</title>
    </head>
    <body>
        <h1>Image:</h1>
        <img src="{{ url_for('get_image', filename=file_name) }}" alt="Image">
        <h1>Detected Objects:</h1>
        <p>{{ one_line_string }}</p>
    </body>
    </html>
    """

    # Render the HTML template with the one-line string
    rendered_html = render_template_string(html_template, file_name=file_name, one_line_string=results)

    return rendered_html  

@app.route('/results/<path:filename>')
def get_image(filename):
    return send_file(os.path.join('results', filename))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/')
def hello():
    return 'Welcome to the application!'

def predict(filename):
    model = YOLO('best.pt')
    results = model.predict(source='images/' + filename) # test with multiple images
    results[0].save(filename='results/' + filename) # save only element
    return isolate_classes(results=results)

def isolate_classes(results):
    classes = []
    boxes = results[0].boxes  # Boxes object for bounding box outputs
    for box in boxes:
        class_id = results[0].names[box.cls[0].item()]
        classes.append(class_id)
        #result.show()  # display to screen 
    return str(classes)


if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=5000)