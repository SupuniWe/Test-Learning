from bottle import Bottle, run, get, post, request, response
import label_image as li
import zipfile
import os

'''
    Instructions
    1. Train the model and get the retrained_graph.pb and the label file to the scripts directory inside model folder
    2. Copy the image and put it into inference_image folder
    3. Call the get_labels function in the label_image script

    Note: Make sure you have installed tensorflow or run it in the anaconda
'''

html = '''
    <html>
        <head>
            <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" rel="stylesheet" crossorigin="anonymous">
        </head>
        <body class="card card-body">
            <form method="post" action="{0}" enctype="multipart/form-data">
                <input type="file" name="{1}" />
                <input class="btn btn-success" type="submit" value="{2}" />
            </form>
        </body>
    </html>
'''
# Hooks
app = Bottle()
@app.hook('after_request')
def enable_cors():
    """
    You need to add some headers to each request.
    Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

# pages

# @get('/')
@app.route('/', method=['OPTIONS', 'GET'])
def indexPage():
    return html.format("/upload", "image", "Predict")

# @get('/upload-model')
@app.route('/upload-model', method=['OPTIONS', 'GET'])
def uploadModelPage():
    return html.format("/upload-model", "model", "Upload Model")

# other routes

# @post('/upload')
@app.route('/upload', method=['OPTIONS', 'POST'])
def uploadImage():
    image = request.files.image
    filename = "inference_image/image.jpg"
    _openAndSaveFile(filename, image)

    return _getTopPredictions()

# @get('/predictions')
@app.route('/predictions', method=['OPTIONS', 'GET'])
def get_prediction():
    return _getTopPredictions()


# @post('/upload-model')
@app.route('/upload-model', method=['OPTIONS', 'POST'])
def uploadsModel():
    modelZip = request.files.model
    filename = "model/model.zip"
    _openAndSaveFile(filename, modelZip)

    zip_ref = zipfile.ZipFile(filename, 'r')
    zip_ref.extractall("model/")
    zip_ref.close()

# Utility functions

def _getTopPredictions():
    lable_index, labels_list, results_list = li.get_lables("image.jpg")
    selected_list = [{"class": labels_list[i], "probability": float(results_list[i]) } for i in lable_index]
    return {"predictions": selected_list}

def _openAndSaveFile(filename, uploadedFile):
    with open(filename,'wb') as open_file:
        open_file.write(uploadedFile.file.read())
    open_file.close()


#run(reloader=True,debug=True)
run(app, host='0.0.0.0', port=os.environ.get('PORT', '5000'))
