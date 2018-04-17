from flask import Flask, send_from_directory, request, Response, render_template
from product import Product

app = Flask('mini-amazon', static_url_path='')
prod = Product()


@app.route('/', methods=['GET'])
def index():
    return send_from_directory('static', 'index.html')


@app.route('/api/products', methods=['POST', 'GET', 'DELETE'])
def products():
    if request.method == 'GET':
        matches = prod.search_by_name(request.args['name'])
        return Response(str(matches), mimetype='application/json', status=200)

    elif request.method == 'POST':
        if request.form['op_type'] == 'Insert':
            p = dict()
            p['name'] = request.form['name']
            p['description'] = request.form['description']
            p['price'] = request.form['price']

            prod.save(p)

            return Response(str({'status': 'success'}), mimetype='application/json', status=200)

        elif request.form['op_type'] == 'Delete_One':
            _id = request.form['_id']
            prod.delete_by_id(_id)
            return Response(str({'status': 'success'}), mimetype='application/json', status=200)

        elif request.form['op_type'] == 'Delete_All':
            prod.delete_all()
            return Response(str({'status': 'success'}), mimetype='application/json', status=200)

        elif request.form['op_type'] == 'Update':
            _id = request.form['id']
            updated_product = dict()

            if request.form['name'] != '':
                updated_product['name'] = request.form['name']
            if request.form['desc'] != '':
                updated_product['name'] = request.form['desc']
            if request.form['price'] != '':
                updated_product['name'] = request.form['price']

            prod.update_by_id(_id, updated_product)
            return Response(str({'status': 'success'}), mimetype='application/json', status=200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
