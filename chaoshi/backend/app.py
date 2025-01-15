from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
from io import BytesIO
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# MongoDB连接
client = MongoClient('mongodb://127.0.0.1:27017/')
db = client['chaoshi']

# 三个不同的集合用于存储不同角色的用户
user_collection = db['user']
admin_collection = db['admin']
manager_collection = db['manager']
picture_collection = db['picture']
favorite_collection = db['favorite']  # 新增一个集合用于存储收藏的图片
shopping_collection = db['shopping']  # 新增一个集合用于存储购物车的商品
purchase_collection = db['purchase']  # 新增一个集合用于存储购买记录
comment_collection = db['comment']  # 新增一个集合用于存储评论


def get_collection_by_role(role):
    """根据角色获取对应的集合"""
    if role == 'admin':
        return admin_collection
    elif role == 'manager':
        return manager_collection
    else:
        return user_collection

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.form
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')
        phone = data.get('phone')

        # 获取对应角色的集合
        collection = get_collection_by_role(role)
        
        # 检查用户名是否已存在
        if collection.find_one({'username': username}):
            return jsonify({'message': '用户名已存在'}), 400

        # 创建新用户
        user_data = {
            'username': username,
            'password': password,
            'role': role,
            'phone': phone
        }
        
        collection.insert_one(user_data)
        return jsonify({'message': '注册成功', 'username': username, 'role': role}), 201
        
    except Exception as e:
        print('注册错误:', str(e))
        return jsonify({'message': '注册失败'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.form
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')

        # 获取对应角色的集合
        collection = get_collection_by_role(role)
        
        # 查找用户
        user = collection.find_one({'username': username})
        
        if not user:
            return jsonify({'message': '用户不存在，请先注册'}), 404
            
        if user['password'] != password:
            return jsonify({'message': '密码错误'}), 401
            
        if user['role'] != role:
            return jsonify({'message': '角色不匹配'}), 401
            
        return jsonify({
            'message': '登录成功',
            'username': username,
            'role': role
        })
        
    except Exception as e:
        print('登录错误:', str(e))
        return jsonify({'message': '登录失败'}), 500

@app.route('/api/images', methods=['GET'])
def get_images():
    try:
        # 获取所有图片
        images = picture_collection.find()
        image_list = []
        labels = set()
        for image in images:
            label = image.get('label', '未分类')
            labels.add(label)
            image_list.append({
                'id': str(image['_id']),
                'name': image.get('name', 'Unnamed Image'),  # 获取图片的 name 字段，默认为 'Unnamed Image'
                'num': image.get('num', 0),  # 获取图片的 num 字段，默认为 0
                'price': image.get('price', 0),  # 获取图片的 price 字段，默认为 0
                'produce': image.get('produce', 'Unknown'),  # 获取图片的 producer 字段，默认为 'Unknown'
                'favorite': image.get('favorite', 0),  # 获取图片的 favorite 字段，默认为 0
                'cart': image.get('cart', 0),  # 获取图片的 cart 字段，默认为 0
                'label': label  # 获取图片的 label 字段
            })
        return jsonify({'images': image_list, 'labels': list(labels)})

    except Exception as e:
        print('获取图片错误:', str(e))
        return jsonify({'message': '获取图片失败'}), 500

    except Exception as e:
        print('获取图片错误:', str(e))
        return jsonify({'message': '获取图片失败'}), 500

@app.route('/api/image/<image_id>', methods=['GET'])
def get_image(image_id):
    try:
        # 根据ID获取图片
        image = picture_collection.find_one({'_id': ObjectId(image_id)})
        if not image:
            return jsonify({'message': '没有找到图片'}), 404

        # 读取图片数据
        image_data = image['data']
        return send_file(BytesIO(image_data), mimetype='image/jpeg/png/gif')

    except Exception as e:
        print('获取图片错误:', str(e))
        return jsonify({'message': '获取图片失败'}), 500

@app.route('/api/favorite', methods=['POST'])
def add_favorite():
    data = request.get_json()
    username = data['username']
    image_id = data['id']
    try:
        # 获取图片信息
        image = picture_collection.find_one({'_id': ObjectId(image_id)})
        if not image:
            return jsonify({'message': '图片不存在'}), 404
        
        favorite_data = {
            'username': username,
            'image_id': image_id,
            'name': image.get('name', 'Unnamed Image'),
            'produce': image.get('produce', 'Unknown'),
            'price': image.get('price', 0),
            'src': f"http://localhost:11000/api/image/{image_id}"
        }
        favorite_collection.insert_one(favorite_data)
        picture_collection.update_one({'_id': ObjectId(image_id)}, {'$inc': {'favorite': 1}})
        return jsonify({'message': '收藏成功'}), 201
    except Exception as e:
        print('收藏错误:', str(e))
        return jsonify({'message': '收藏失败'}), 500

@app.route('/api/favorite/<image_id>', methods=['DELETE'])
def remove_favorite(image_id):
    username = request.args.get('username')
    try:
        result = favorite_collection.delete_one({'username': username, 'image_id': image_id})
        if result.deleted_count == 0:
            return jsonify({'message': '没有找到收藏的图片'}), 404
        picture_collection.update_one({'_id': ObjectId(image_id)}, {'$inc': {'favorite': -1}})
        return jsonify({'message': '取消收藏成功'}), 200
    except Exception as e:
        print('取消收藏错误:', str(e))
        return jsonify({'message': '取消收藏失败'}), 500

@app.route('/api/favorites/<username>', methods=['GET'])
def get_favorites(username):
    try:
        # 获取用户收藏的所有图片
        favorites = favorite_collection.find({'username': username})
        favorite_list = []
        for favorite in favorites:
            favorite_list.append({
                'image_id': favorite['image_id'],
                'name': favorite.get('name', 'Unnamed Image'),
                'price': favorite.get('price', 0),
                'produce': favorite.get('produce', 'Unknown')
            })
        return jsonify(favorite_list)

    except Exception as e:
        print('获取收藏错误:', str(e))
        return jsonify({'message': '获取收藏失败'}), 500

@app.route('/api/favorites/<username>/<image_id>', methods=['DELETE'])
def remove_favorite1(username, image_id):
    try:
        result = favorite_collection.delete_one({'username': username, 'image_id': image_id})
        if result.deleted_count == 0:
            return jsonify({'message': '没有找到收藏的图片'}), 404
        picture_collection.update_one({'_id': ObjectId(image_id)}, {'$inc': {'favorite': -1}})
        return jsonify({'message': '取消收藏成功'}), 200
    except Exception as e:
        print('取消收藏错误:', str(e))
        return jsonify({'message': '取消收藏失败'}), 500

@app.route('/api/shopping', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    username = data['username']
    image_id = data['id']
    try:
        # 获取图片信息
        image = picture_collection.find_one({'_id': ObjectId(image_id)})
        if not image:
            return jsonify({'message': '图片不存在'}), 404
        
        cart_data = {
            'username': username,
            'image_id': image_id,
            'name': image.get('name', 'Unnamed Image'),
            'produce': image.get('produce', 'Unknown'),
            'price': image.get('price', 0),
            'src': f"http://localhost:11000/api/image/{image_id}"
        }
        shopping_collection.insert_one(cart_data)
        picture_collection.update_one({'_id': ObjectId(image_id)}, {'$inc': {'cart': 1}})
        return jsonify({'message': '加入购物车成功'}), 201
    except Exception as e:
        print('加入购物车错误:', str(e))
        return jsonify({'message': '加入购物车失败'}), 500

@app.route('/api/shopping/<image_id>', methods=['DELETE'])
def remove_from_cart(image_id):
    username = request.args.get('username')
    try:
        result = shopping_collection.delete_one({'username': username, 'image_id': image_id})
        if result.deleted_count == 0:
            return jsonify({'message': '没有找到购物车中的图片'}), 404
        picture_collection.update_one({'_id': ObjectId(image_id)}, {'$inc': {'cart': -1}})
        return jsonify({'message': '取消加入购物车成功'}), 200
    except Exception as e:
        print('取消加入购物车错误:', str(e))
        return jsonify({'message': '取消加入购物车失败'}), 500


@app.route('/api/shopping/<username>', methods=['GET'])
def get_cart(username):
    try:
        # 获取用户购物车中的所有商品
        cart_items = shopping_collection.find({'username': username})
        cart_list = []
        for item in cart_items:
            cart_list.append({
                'image_id': item['image_id'],
                'name': item.get('name', 'Unnamed Image'),
                'price': item.get('price', 0),
                'produce': item.get('produce', 'Unknown')
            })
        return jsonify(cart_list)

    except Exception as e:
        print('获取购物车错误:', str(e))
        return jsonify({'message': '获取购物车失败'}), 500



@app.route('/api/picture/<image_id>', methods=['GET'])
def get_picture(image_id):
    try:
        picture = picture_collection.find_one({'_id': ObjectId(image_id)})
        if not picture:
            return jsonify({'message': '没有找到图片'}), 404
        return jsonify({
            'id': str(picture['_id']),
            'name': picture.get('name', 'Unnamed Image'),
            'num': picture.get('num', 0),
            'price': picture.get('price', 0),
            'produce': picture.get('produce', 'Unknown')
        })
    except Exception as e:
        print('获取图片错误:', str(e))
        return jsonify({'message': '获取图片失败'}), 500

@app.route('/api/pay', methods=['POST'])
def pay():
    try:
        data = request.json
        selected_items = data.get('selected_items', [])
        for item in selected_items:
            # 从购物车中删除商品
            shopping_collection.delete_one({'image_id': item['image_id'], 'username': item['username']})
            # 更新图片集合中的商品数量
            picture_collection.update_one(
                {'_id': ObjectId(item['image_id'])},
                {'$inc': {'num': -item['quantity'], 'cart': -1, 'purchased': item['quantity']}}  # 更新购买数量
                
            )
            # 更新购物车人数
            cart_count = shopping_collection.count_documents({'image_id': item['image_id']})
            if (cart_count == 0):
                shopping_collection.delete_many({'image_id': item['image_id']})
            # 添加购买记录
            purchase_data = {
                'username': item['username'],
                'image_id': item['image_id'],
                'name': item['name'],
                'quantity': item['quantity'],
                'total_price': item['price'] * item['quantity'],
                'purchase_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # 添加付款时间
                'src': f"http://localhost:11000/api/image/{item['image_id']}",
                'produce': item.get('produce', 'Unknown')  # 添加商品介绍字段
            }
            purchase_collection.insert_one(purchase_data)
        return jsonify({'message': '付款成功'}), 200

    except Exception as e:
        print('付款错误:', str(e))
        return jsonify({'message': '付款失败'}), 500

@app.route('/api/purchase-history/<username>', methods=['GET'])
def get_purchase_history(username):
    try:
        # 获取用户的购买记录
        purchases = purchase_collection.find({'username': username})
        purchase_list = []
        for purchase in purchases:
            purchase_list.append({
                'name': purchase['name'],
                'quantity': purchase['quantity'],
                'total_price': purchase['total_price'],
                'purchase_time': purchase['purchase_time'],  # 返回付款时间
                'src': purchase['src'],
                'comment': purchase.get('comment', None)  # 返回评论字段
            })
        return jsonify(purchase_list)

    except Exception as e:
        print('获取购买记录错误:', str(e))
        return jsonify({'message': '获取购买记录失败'}), 500

@app.route('/api/purchase/item', methods=['GET'])
def get_purchase_item():
    try:
        name = request.args.get('name')
        purchase_time = request.args.get('purchase_time')
        if not name or not purchase_time:
            return jsonify({'message': '商品名称和购买时间不能为空'}), 400

        item = purchase_collection.find_one({'name': name, 'purchase_time': purchase_time})
        if not item:
            return jsonify({'message': '没有找到商品'}), 404

        item_info = {
            'name': item['name'],
            'quantity': item['quantity'],
            'total_price': item['total_price'],
            'purchase_time': item['purchase_time'],
            'src': item['src'],
            'produce': item.get('produce', 'Unknown'),  # 返回商品介绍字段
            'comment': item.get('comment', None)
        }
        return jsonify(item_info)

    except Exception as e:
        print('获取商品信息错误:', str(e))
        return jsonify({'message': '获取商品信息失败'}), 500



@app.route('/api/shopping/item', methods=['GET'])
def get_item_by_name():
    try:
        name = request.args.get('name')
        if not name:
            return jsonify({'message': '商品名称不能为空'}), 400

        item = shopping_collection.find_one({'name': name})
        if not item:
            return jsonify({'message': '没有找到商品'}), 404

        item_info = {
            'image_id': item['image_id'],
            'name': item['name'],
            'price': item['price'],
            'produce': item['produce'],
            'src': f"http://localhost:11000/api/image/{item['image_id']}"
        }
        return jsonify(item_info)

    except Exception as e:
        print('获取商品信息错误:', str(e))
        return jsonify({'message': '获取商品信息失败'}), 500
    
@app.route('/api/purchase/comment', methods=['POST'])
def add_comment():
    try:
        data = request.json
        name = data.get('name')
        purchase_time = data.get('purchase_time')
        comment = data.get('comment')

        # 更新购买记录中的评论
        result = purchase_collection.update_one(
            {'name': name, 'purchase_time': purchase_time},
            {'$set': {'comment': comment}}
        )

        if result.matched_count == 0:
            return jsonify({'message': '没有找到购买记录'}), 404

        # 获取购买记录
        purchase = purchase_collection.find_one({'name': name, 'purchase_time': purchase_time})
        if not purchase:
            return jsonify({'message': '没有找到购买记录'}), 404

        # 获取商品ID
        image_id = purchase['image_id']



        # 构建新的评论数据
        new_comment = {
            'username': purchase['username'],
            'comment': comment
        }

        # 更新或插入评论数据
        comment_collection.update_one(
            {
                'image_id': image_id,
                'name':purchase['name'],
                'src': purchase['src'],
            },
            {'$push': {'comments': new_comment}},
            upsert=True
        )

        return jsonify({'message': '评论提交成功', 'comment': comment}), 200

    except Exception as e:
        print('提交评论错误:', str(e))
        return jsonify({'message': '提交评论失败'}), 500
    
@app.route('/api/my-comments/<username>', methods=['GET'])
def get_my_comments(username):
    try:
        items = purchase_collection.find({'username': username, 'comment': {'$exists': True}})
        item_list = []
        for item in items:
            item_info = {
                'name': item['name'],
                'quantity': item['quantity'],
                'total_price': item['total_price'],
                'purchase_time': item['purchase_time'],
                'src': item['src'],
                'comment': item['comment']
            }
            item_list.append(item_info)
        return jsonify(item_list)
    except Exception as e:
        print('获取用户评论信息错误:', str(e))
        return jsonify({'message': '获取用户评论信息失败'}), 500

@app.route('/api/add-product', methods=['POST'])
def add_product():
    try:
        name = request.form.get('name')
        price = request.form.get('price')
        num = request.form.get('num')
        produce = request.form.get('produce')
        label = request.form.get('label')
        image = request.files.get('image')

        if not all([name, price, num, produce, label, image]):
            return jsonify({'message': '所有字段都是必填的'}), 400

        # 将 price 和 num 转换为整数类型
        try:
            price = float(price)
            num = int(num)
        except ValueError:
            return jsonify({'message': '价格和数量必须是数字'}), 400

        image_data = image.read()

        product_data = {
            'name': name,
            'price': price,
            'num': num,
            'produce': produce,
            'label': label,
            'data': image_data,
            'favorite': 0,
            'cart': 0
        }

        picture_collection.insert_one(product_data)
        return jsonify({'message': '商品添加成功'}), 201

    except Exception as e:
        print('添加商品错误:', str(e))
        return jsonify({'message': '添加商品失败'}), 500

@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        products = picture_collection.find()
        product_list = []
        for product in products:
            product_list.append({
                'name': product.get('name', 'Unnamed Product'),
                'price': product.get('price', 0),
                'num': product.get('num', 0),
                'produce': product.get('produce', 'Unknown'),
                'label': product.get('label', '未分类'),
                'src': f"http://localhost:11000/api/image/{product['_id']}",  # 添加图片链接
                'favorite': product.get('favorite', 0),
                'cart': product.get('cart', 0),
                'purchased': product.get('purchased', 0)

            })
        return jsonify(product_list)
    except Exception as e:
        print('获取库存信息错误:', str(e))
        return jsonify({'message': '获取库存信息失败'}), 500

@app.route('/api/product/<name>', methods=['DELETE'])
def delete_product(name):
    try:
        # 查找商品
        product = picture_collection.find_one({'name': name})
        if not product:
            return jsonify({'message': '商品未找到'}), 404

        # 获取商品的 ID
        product_id = str(product['_id'])

        # 删除产品集合中的商品
        picture_collection.delete_one({'name': name})
        # 删除收藏集合中的商品
        favorite_collection.delete_many({'image_id': product_id})
        # 删除购物车集合中的商品
        shopping_collection.delete_many({'image_id': product_id})

        return jsonify({'message': '商品已下架'}), 200
    except Exception as e:
        print('下架商品失败:', str(e))
        return jsonify({'message': '下架商品失败'}), 500


@app.route('/api/product/<name>', methods=['GET'])
def get_product(name):
    try:
        product = picture_collection.find_one({'name': name})
        if not product:
            return jsonify({'message': '没有找到商品'}), 404
        return jsonify({
            'name': product.get('name', 'Unnamed Product'),
            'price': product.get('price', 0),
            'num': product.get('num', 0),
            'produce': product.get('produce', 'Unknown'),
            'label': product.get('label', '未分类'),
            'src': f"http://localhost:11000/api/image/{product['_id']}"  # 返回图片链接
        })
    except Exception as e:
        print('获取商品错误:', str(e))
        return jsonify({'message': '获取商品失败'}), 500

@app.route('/api/product/<name>', methods=['PUT'])
def update_product(name):
    try:
        data = request.form
        update_data = {
            'name': data.get('name'),
            'produce': data.get('produce'),
            'label': data.get('label')
        }
        
        # 将 price 和 num 转换为整数类型
        try:
            update_data['price'] = float(data.get('price'))
            update_data['num'] = int(data.get('num'))
        except ValueError:
            return jsonify({'message': '价格和数量必须是数字'}), 400
        
        # 检查是否有新的图片上传
        if 'image' in request.files:
            image = request.files['image']
            update_data['data'] = image.read()
        
        # 更新 picture_collection 集合中的商品信息
        result = picture_collection.update_one(
            {'name': name},
            {'$set': update_data}
        )
        
        if result.matched_count == 0:
            return jsonify({'message': '商品未找到'}), 404
        
        # 更新其他相关集合中的商品信息
        collections_to_update = [favorite_collection, shopping_collection, purchase_collection, comment_collection]
        for collection in collections_to_update:
            collection.update_many(
                {'name': name},
                {'$set': update_data}
            )
        
        return jsonify({'message': '修改成功'}), 200
    except Exception as e:
        print('修改商品错误:', str(e))
        return jsonify({'message': '修改失败'}), 500
    
@app.route('/api/sold-out-products', methods=['GET'])
def get_sold_out_products():
    try:
        sold_out_products = picture_collection.find({'$or': [{'num': 0}, {'num': '0'}]})
        product_list = []
        for product in sold_out_products:
            product_list.append({
                'id': str(product['_id']),
                'name': product.get('name', 'Unnamed Product'),
                'num': product.get('num', 0),
                'price': product.get('price', 0),
                'produce': product.get('produce', 'Unknown'),
                'src': f"http://localhost:11000/api/image/{product['_id']}",
                'label': product.get('label', '未分类'),
                'cart': product.get('cart', 0),
                'favorite': product.get('favorite', 0),
                'purchased': product.get('purchased', 0)
            })
        return jsonify(product_list)
    except Exception as e:
        print('获取售罄商品错误:', str(e))
        return jsonify({'message': '获取售罄商品失败'}), 500
    
@app.route('/api/comments', methods=['GET'])
def get_comments():
    try:
        comments = comment_collection.find()
        comment_list = []
        for comment in comments:
            comment_data = {
                'name': comment['name'],
                'src': comment['src']
            }
            for i, c in enumerate(comment['comments'], start=1):
                comment_data[f'username{i}'] = c['username']
                comment_data[f'comment{i}'] = c['comment']
            comment_list.append(comment_data)
        return jsonify(comment_list)
    except Exception as e:
        print('获取评论信息错误:', str(e))
        return jsonify({'message': '获取评论信息失败'}), 500

@app.route('/api/comments/length', methods=['GET'])
def get_comments_length():
    try:
        length = comment_collection.count_documents({})
        return jsonify({'length': length})
    except Exception as e:
        print('获取评论数量错误:', str(e))
        return jsonify({'message': '获取评论数量失败'}), 500

@app.route('/api/comments/<name>', methods=['GET'])
def get_comments_by_name(name):
    try:
        comments = comment_collection.find_one({'name': name})
        if not comments:
            return jsonify({'message': '没有找到评论'}), 404

        comment_list = []
        for comment in comments['comments']:
            comment_list.append({
                'username': comment['username'],
                'comment': comment['comment']
            })
        return jsonify(comment_list)
    except Exception as e:
        print('获取评论信息错误:', str(e))
        return jsonify({'message': '获取评论信息失败'}), 500
    
@app.route('/api/add-admin', methods=['POST'])
def add_admin():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        phone = data.get('phone')

        # 检查用户名是否已存在
        if admin_collection.find_one({'username': username}):
            return jsonify({'message': '用户名已存在'}), 400

        # 创建新管理员
        admin_data = {
            'username': username,
            'password': password,
            'phone': phone,
            'role': 'admin'

        }
        
        admin_collection.insert_one(admin_data)
        return jsonify({'message': '管理员添加成功'}), 201
    except Exception as e:
        print('添加管理员错误:', str(e))
        return jsonify({'message': '添加管理员失败'}), 500

@app.route('/api/labels-products', methods=['GET'])
def get_labels_and_products():
    try:
        # 获取标签数据
        pipeline = [
            {"$group": {"_id": "$label", "count": {"$sum": 1}}},
            {"$project": {"_id": 0, "name": "$_id", "count": 1}}
        ]
        labels = list(picture_collection.aggregate(pipeline))

        # 获取商品数据
        products = list(picture_collection.find({}, {'_id': 0, 'name': 1, 'label': 1, 'num': 1, 'purchased': 1}))

        # 按标签分类商品
        label_product_map = {}
        for product in products:
            label = product['label']
            if label not in label_product_map:
                label_product_map[label] = []
            label_product_map[label].append(product)

        return jsonify({'labels': labels, 'label_product_map': label_product_map})
    except Exception as e:
        print('获取标签和商品数据错误:', str(e))
        return jsonify({'message': '获取标签和商品数据失败'}), 500

@app.route('/api/product-total-price', methods=['GET'])
def get_product_total_price():
    try:
        pipeline = [
            {
                "$group": {
                    "_id": "$name",
                    "total_price": {"$sum": "$total_price"}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "name": "$_id",
                    "total_price": 1
                }
            }
        ]
        result = list(purchase_collection.aggregate(pipeline))
        return jsonify(result)
    except Exception as e:
        print('获取商品销售额错误:', str(e))
        return jsonify({'message': '获取商品销售额失败'}), 500
    

@app.route('/api/product-dynamic-data', methods=['GET'])
def get_product_dynamic_data():
    try:
        name = request.args.get('name')
        if not name:
            return jsonify({'message': '缺少商品名称参数'}), 400

        # 获取指定商品的购买记录
        purchases = purchase_collection.find({'name': name}).sort('purchase_time', 1)
        purchase_data = []
        for purchase in purchases:
            purchase_data.append({
                'purchase_time': purchase['purchase_time'],
                'total_price': purchase['total_price'],
                'quantity': purchase['quantity']
            })

        return jsonify(purchase_data)
    except Exception as e:
        print('获取动态数据错误:', str(e))
        return jsonify({'message': '获取动态数据失败'}), 500

@app.route('/api/product-names', methods=['GET'])
def get_product_names():
    try:
        # 获取所有商品名称
        product_names = purchase_collection.distinct('name')
        return jsonify(product_names)
    except Exception as e:
        print('获取商品名称错误:', str(e))
        return jsonify({'message': '获取商品名称失败'}), 500
    
@app.route('/api/admins', methods=['GET'])
def get_admins():
    try:
        admins = admin_collection.find()
        admin_list = []
        for admin in admins:
            admin_list.append({
                'username': admin.get('username', 'N/A'),
                'phone': admin.get('phone', 'N/A'),
                'role': admin.get('role', 'N/A'),
                'password': admin.get('password', 'N/A')
            })
        return jsonify(admin_list)
    except Exception as e:
        print('获取管理员信息错误:', str(e))
        return jsonify({'message': '获取管理员信息失败'}), 500
    
@app.route('/api/admin/<username>', methods=['GET'])
def get_admin(username):
    try:
        admin = admin_collection.find_one({'username': username})
        if not admin:
            return jsonify({'message': '管理员未找到'}), 404
        return jsonify({
            'username': admin.get('username'),
            'password': admin.get('password'),
            'phone': admin.get('phone')
        })
    except Exception as e:
        print('获取管理员信息错误:', str(e))
        return jsonify({'message': '获取管理员信息失败'}), 500

@app.route('/api/admin/<username>', methods=['PUT'])
def update_admin(username):
    try:
        data = request.get_json()
        result = admin_collection.update_one({'username': username}, {'$set': data})
        if result.matched_count == 0:
            return jsonify({'message': '管理员未找到'}), 404
        return jsonify({'message': '管理员信息更新成功'})
    except Exception as e:
        print('更新管理员信息错误:', str(e))
        return jsonify({'message': '更新管理员信息失败'}), 500

@app.route('/api/admin/<username>', methods=['DELETE'])
def delete_admin(username):
    try:
        result = admin_collection.delete_one({'username': username})
        if result.deleted_count == 0:
            return jsonify({'message': '管理员未找到'}), 404
        return jsonify({'message': '管理员删除成功'})
    except Exception as e:
        print('删除管理员错误:', str(e))
        return jsonify({'message': '删除管理员失败'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=11000, host='0.0.0.0')