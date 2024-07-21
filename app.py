from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import os
import certifi
import jwt
import traceback
# from datetime import datetime, timedelta, timezone
import datetime
import json
from werkzeug.utils import secure_filename
from pymongo import MongoClient

cert = certifi.where()
client = MongoClient('mongodb+srv://farahmzahra:Q331XH7JryD66b28@cluster0.si84fvq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0', tlsCAFile=cert,
                     socketTimeoutMS=30000, connectTimeoutMS=30000)
db = client.LaundryLab

app = Flask(__name__)
app.secret_key = 'thisissecret'
# CORS(app, resources={r"/*": {"origins": "*"}})
CORS(app, resources={r"/*": {"origins": "http://laundrylab.pocari.id"}})

@app.route('/')
def home():
    return 'This is House!'

@app.route('/test')
def test():
    return 'This is Test hosting ke 6 yeyyy!'

@app.route('/userRegister', methods=['POST'])
@cross_origin()
def userRegister():
    try:
        dataId = request.form.get('idUser')
        dataNama = request.form.get('nama')
        dataEmail = request.form.get('email')
        dataNotelp = request.form.get('notelp')
        dataPassword = request.form.get('password')
        duplicateValidateUser = db.pelanggan.find_one({'email':dataEmail})
        validator = ''

        if duplicateValidateUser:
            validator = 'true'
        else:
            doc = {
                'idUser': dataId,
                'nama': dataNama,
                'email': dataEmail,
                'notelp': dataNotelp,
                'password': dataPassword
            }
            db.pelanggan.insert_one(doc)

        return jsonify({
            'validator': validator,
            'success': True
        })
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/getAlamatDetails/<emailUser>/<alamat>', methods=['GET']) # API baru
@cross_origin()
def getAlamatDetails(emailUser, alamat):
    try:
        dataAlamat = db.alamatPelanggan.find({'emailUser': emailUser, 'alamat': alamat})
        user_list = []
        for users in dataAlamat:
            user_list.append({
                'idAlamat': users['idAlamat'],
                'emailUser': users['emailUser'],
                'alamat': users['alamat'],
                'kelurahan': users['kelurahan'],
                'kecamatan': users['kecamatan'],
                'kodePos': users['kodePos'],
                'longitudeUser': users['longitudeUser'],
                'latitudeUser': users['latitudeUser'],
                'detailAlamat': users['detailAlamat']
            })
        return jsonify({'success': True, 'users': user_list})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/getAlamat/<emailUser>', methods=['GET']) # API baru
@cross_origin()
def getAlamat(emailUser):
    try:
        dataAlamat = db.alamatPelanggan.find({'emailUser': emailUser})
        user_list = []
        for users in dataAlamat:
            user_list.append({
                'idAlamat': users['idAlamat'],
                'emailUser': users['emailUser'],
                'alamat': users['alamat'],
                'kelurahan': users['kelurahan'],
                'kecamatan': users['kecamatan'],
                'kodePos': users['kodePos'],
                'longitudeUser': users['longitudeUser'],
                'latitudeUser': users['latitudeUser'],
                'detailAlamat': users['detailAlamat']
            })
        return jsonify({'success': True, 'users': user_list})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/getLongLatUser/<emailUser>/<idAlamat>', methods=['GET']) # API baru
@cross_origin()
def getLongLatUser(emailUser, idAlamat):
    try:
        dataAlamat = db.alamatPelanggan.find({'emailUser': emailUser, 'idAlamat': idAlamat})
        user_list = []
        for users in dataAlamat:
            user_list.append({
                'idAlamat': users['idAlamat'],
                'emailUser': users['emailUser'],
                'alamat': users['alamat'],
                'longitudeUser': users['longitudeUser'],
                'latitudeUser': users['latitudeUser']
            })
        return jsonify({'success': True, 'users': user_list})
        print(user_list.alamat)
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/getLongLatPesananUser/<emailUser>/<alamat>', methods=['GET']) # API baru
@cross_origin()
def getLongLatPesananUser(emailUser, alamat):
    try:
        dataAlamat = db.alamatPelanggan.find({'emailUser': emailUser, 'alamat': alamat})
        user_list = []
        for users in dataAlamat:
            user_list.append({
                'idAlamat': users['idAlamat'],
                'emailUser': users['emailUser'],
                'alamat': users['alamat'],
                'kelurahan': users['kelurahan'],
                'kecamatan': users['kecamatan'],
                'kodePos': users['kodePos'],
                'longitudeUser': users['longitudeUser'],
                'latitudeUser': users['latitudeUser'],
                'detailAlamat': users['detailAlamat']
            })
        return jsonify({'success': True, 'users': user_list})
        print(user_list.alamat)
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/getAlamatId/<idAlamat>/<emailUser>', methods=['GET']) # API baru
@cross_origin()
def getAlamatId(idAlamat, emailUser):
    try:
        alamatUser = db.alamatPelanggan.find_one({'idAlamat': idAlamat, 'emailUser': emailUser})
        if alamatUser:
            return jsonify({
                'success': True,
                'alamatUser': {
                    'idAlamat': alamatUser['idAlamat'],
                    'emailUser': alamatUser['emailUser'],
                    'alamat': alamatUser['alamat'],
                    'kelurahan': alamatUser['kelurahan'],
                    'kecamatan': alamatUser['kecamatan'],
                    'kodePos': alamatUser['kodePos'],
                    'longitudeUser': alamatUser['longitudeUser'],
                    'latitudeUser': alamatUser['latitudeUser'],
                    'detailAlamat': alamatUser['detailAlamat']
                }
            })
        else:
            return jsonify({'success': False, 'error': 'Alamat not found'})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/addAlamatUser/<email>', methods=['POST']) # API baru
@cross_origin()
def addAlamatUser(email):
    try:
        idAlamat = request.form.get('idAlamat')
        emailUser = request.form.get('emailUser')
        alamat = request.form.get('alamat')
        kelurahan = request.form.get('kelurahan')
        kecamatan = request.form.get('kecamatan')
        kodePos = request.form.get('kodePos')
        dataLongitudeUser = request.form.get('longitudeUser')
        dataLatitudeUser = request.form.get('latitudeUser')
        detailAlamat = request.form.get('detailAlamat')

        dataAlamat = {
            'idAlamat': idAlamat,
            'emailUser': emailUser,
            'alamat': alamat,
            'kelurahan': kelurahan,
            'kecamatan': kecamatan,
            'kodePos': kodePos,
            'longitudeUser': float(dataLongitudeUser),
            'latitudeUser': float(dataLatitudeUser),
            'detailAlamat': detailAlamat
        }
        db.alamatPelanggan.insert_one(dataAlamat)
        return jsonify({'success': True, 'message': 'Payment method added successfully'})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/editAlamatUser/<idAlamat>/<emailUser>', methods=['PUT']) # API baru
@cross_origin()
def editAlamatUser(idAlamat, emailUser):
    try:
        emailUser = request.form.get('emailUser')
        alamat = request.form.get('alamat')
        kelurahan = request.form.get('kelurahan')
        kecamatan = request.form.get('kecamatan')
        kodePos = request.form.get('kodePos')
        dataLongitudeUser = request.form.get('longitudeUser')
        dataLatitudeUser = request.form.get('latitudeUser')
        detailAlamat = request.form.get('detailAlamat')

        current_record = db.alamatPelanggan.find_one({'idAlamat': idAlamat, 'emailUser': emailUser})
        
        if not current_record:
            return jsonify({'success': False, 'message': 'Alamat not found'})

        db.alamatPelanggan.update_one(
            {'idAlamat': idAlamat, 'emailUser': emailUser}, 
            {'$set': {
                'alamat': alamat, 
                'kelurahan': kelurahan, 
                'kecamatan': kecamatan, 
                'kodePos': kodePos, 
                'longitudeUser': float(dataLongitudeUser), 
                'latitudeUser': float(dataLatitudeUser), 
                'detailAlamat': detailAlamat
            }}
        )
        return jsonify({'success': True, 'message': 'Alamat updated successfully'})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/deleteAlamatUser/<idAlamat>/<emailUser>', methods=['DELETE']) # API baru
@cross_origin()
def deleteAlamatUser(idAlamat, emailUser):
    try:
        result = db.alamatPelanggan.delete_one({'idAlamat': idAlamat, 'emailUser': emailUser})

        if result.deleted_count > 0:
            return jsonify({'success': True, 'message': 'Alamat deleted successfully'})
        else:
            return jsonify({'success': False, 'error': 'Alamat not found'})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/adminRegister', methods=['POST'])
@cross_origin()
def adminRegister():
    try:
        dataId = request.form.get('idAdmin')
        dataEmail = request.form.get('email')
        dataNotelp = request.form.get('notelp')
        dataPassword = request.form.get('password')
        dataNamaLaundry = request.form.get('namaLaundry')
        dataBukaTutupLaundry = request.form.get('bukaTutupLaundry')
        duplicateValidateAdmin = db.laundry.find_one({'email':dataEmail})
        validator = ''

        if duplicateValidateAdmin:
            validator = 'true'
        else:
            doc = {
                'idAdmin': dataId,
                'email': dataEmail,
                'notelp': dataNotelp,
                'password': dataPassword,
                'namaLaundry': dataNamaLaundry,
                'bukaTutupLaundry': dataBukaTutupLaundry
            }

            db.laundry.insert_one(doc)

        return jsonify({
            'validator': validator,
            'success': True
        })
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/adminRegisterById/<id>', methods=['PUT'])
@cross_origin()
def adminRegisterById(id):
    try:
        dataAlamat = request.form.get('alamat')
        dataKelurahan = request.form.get('kelurahan')
        dataKecamatan = request.form.get('kecamatan')
        dataKodePos = request.form.get('kodePos')
        dataLongitudeLaundry = request.form.get('longitudeLaundry')
        dataLatitudeLaundry = request.form.get('latitudeLaundry')
        dataDetailAlamat = request.form.get('detailAlamat')
        
        if not dataLongitudeLaundry or not dataLatitudeLaundry:
            return jsonify({'success': False, 'message': 'Longitude and latitude must be provided'})

        admin = db.laundry.find_one({'idAdmin': id})
        
        if admin:
            db.laundry.update_one(
                {'idAdmin': id},
                {'$set': {
                    'alamat': dataAlamat,
                    'kelurahan': dataKelurahan,
                    'kecamatan': dataKecamatan,
                    'kodePos': dataKodePos,
                    'longitudeLaundry': float(dataLongitudeLaundry),
                    'latitudeLaundry': float(dataLatitudeLaundry),
                    'detailAlamat': dataDetailAlamat
                }}
            )
            return jsonify({'success': True, 'message': 'Address updated successfully'})
        else:
            return jsonify({'success': False, 'message': 'Admin not found'})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/adminRegisterByIdJam/<email>', methods=['PUT'])
@cross_origin()
def adminRegisterByIdJam(email):
    try:
        dataDays = request.form.get('days')
        days = json.loads(dataDays)
        
        admin = db.laundry.find_one({'email': email})
        
        if admin:
            db.laundry.update_one(
                {'email': email},
                {'$set': {
                    'days': days
                }}
            )
            return jsonify({'success': True, 'message': 'Jam Operasional updated successfully'})
        else:
            return jsonify({'success': True, 'message': 'Admin not found'})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/editAdminState/<email>', methods=['PUT'])
@cross_origin()
def editAdminState(email):
    try:
        dataState = request.form.get('bukaTutupLaundry')
        
        admin = db.laundry.find_one({'email': email})
        
        if admin:
            db.laundry.update_one(
                {'email': email},
                {'$set': {
                    'bukaTutupLaundry': dataState
                }}
            )
            return jsonify({'success': True, 'message': 'State Laundry updated successfully'})
        else:
            return jsonify({'success': True, 'message': 'State Laundry not found'})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/petugasRegister/<email>', methods=['POST'])
@cross_origin()
def petugasRegister(email):
    try:
        id_petugas = request.form.get('id_petugas')
        emailLaundry = request.form.get('emailLaundry')
        nama_petugas = request.form.get('nama_petugas')
        notelp_petugas = request.form.get('notelp_petugas')
        email_petugas = request.form.get('email_petugas')
        password_petugas = request.form.get('password_petugas')
        upload_path = request.form.get('upload_path')
        profil_petugas = None

        if 'profil_petugas' in request.files:
            file = request.files['profil_petugas']

            if file.filename != '':
                filename = secure_filename(file.filename)
                filepath = os.path.join(upload_path, filename)

                if not os.path.exists(upload_path):
                    os.makedirs(upload_path)

                file.save(filepath)
                profil_petugas = filename

        petugas = {
            'id_petugas': id_petugas,
            'emailLaundry': emailLaundry,
            'nama_petugas': nama_petugas,
            'notelp_petugas': notelp_petugas,
            'email_petugas': email_petugas,
            'password_petugas': password_petugas,
            'profil_petugas': profil_petugas
        }

        db.petugas.insert_one(petugas)
        return jsonify({'success': True})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/login', methods=['POST'])
@cross_origin()
def login():
    try:
        dataEmail = request.form.get('email')
        dataPassword = request.form.get('password')
        emailValidateUser = db.pelanggan.find_one({'email': dataEmail})
        emailValidateAdmin = db.laundry.find_one({'email': dataEmail})
        emailValidatePetugas = db.petugas.find_one({'email_petugas': dataEmail})
        validator = ''
        token = ''
        user_id = None

        if emailValidateUser:
            if emailValidateUser['password'] == dataPassword:
                validator = 'user'
                user_id = emailValidateUser['idUser']
                token = jwt.encode({'email': dataEmail, 'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)}, app.secret_key, algorithm="HS256")
            else:
                validator = 'incorrect'
        elif emailValidateAdmin:
            if emailValidateAdmin['password'] == dataPassword:
                validator = 'admin'
                user_id = emailValidateAdmin['idAdmin']
                token = jwt.encode({'email': dataEmail, 'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)}, app.secret_key, algorithm="HS256")
            else:
                validator = 'incorrect'
        elif emailValidatePetugas:
            if emailValidatePetugas['password_petugas'] == dataPassword:
                validator = 'petugas'
                user_id = emailValidatePetugas['id_petugas']
                token = jwt.encode({'email_petugas': dataEmail, 'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)}, app.secret_key, algorithm="HS256")
            else:
                validator = 'incorrect'
        else:
            validator = 'not_found'

        return jsonify({
            'success': True,
            'validator': validator,
            'token': token,
            'id': user_id
        })
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(traceback.format_exc())
        return jsonify({'success': False, 'error': error_message}), 500

# @app.route('/login', methods=['POST'])
# @cross_origin()
# def login():
#     try:
#         dataEmail = request.form.get('email')
#         dataPassword = request.form.get('password')

#         validator = ''
#         token = ''
#         user_id = None

#         emailValidateUser = db.pelanggan.find_one({'email': dataEmail})
#         if emailValidateUser and emailValidateUser['password'] == dataPassword:
#             validator = 'user'
#             user_id = emailValidateUser['idUser']
#             token = jwt.encode({'email': dataEmail, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, app.secret_key, algorithm="HS256")
            
#         if not validator:
#             validator = 'not_found'

#         return jsonify({
#             'success': True,
#             'validator': validator,
#             'token': token,
#             'id': user_id
#         })
#     except Exception as e:
#         error_message = f'Error: {str(e)}'
#         print(traceback.format_exc())
#         return jsonify({'success': False, 'error': error_message}), 500

    # dataEmail = request.form.get('email')
    # dataPassword = request.form.get('password')
    # emailValidateUser = db.pelanggan.find_one({'email': dataEmail})
    # emailValidateAdmin = db.laundry.find_one({'email': dataEmail})
    # emailValidatePetugas = db.petugas.find_one({'email': dataEmail})
    # validator = ''
    # token = ''

    # if emailValidateUser:
    #     if emailValidateUser['password'] == dataPassword:
    #         validator = 'user'
    #         user_id = emailValidateUser['idUser']
    #         # token = jwt.encode({'email': dataEmail, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, app.secret_key, algorithm="HS256")
    #         token = jwt.encode({'email': dataEmail, 'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)}, app.secret_key, algorithm="HS256")
    #     else:
    #         validator = 'incorrect'
    # elif emailValidateAdmin:
    #     if emailValidateAdmin['password'] == dataPassword:
    #         validator = 'admin'
    #         user_id = emailValidateAdmin['idAdmin']
    #         # token = jwt.encode({'email': dataEmail, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, app.secret_key, algorithm="HS256")
    #         token = jwt.encode({'email': dataEmail, 'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)}, app.secret_key, algorithm="HS256")
    #     else:
    #         validator = 'incorrect'
    # elif emailValidatePetugas:
    #     if emailValidatePetugas['password'] == dataPassword:
    #         validator = 'petugas'
    #         user_id = emailValidatePetugas['id_petugas']
    #         # token = jwt.encode({'email': dataEmail, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, app.secret_key, algorithm="HS256")
    #         token = jwt.encode({'email': dataEmail, 'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)}, app.secret_key, algorithm="HS256")
    #     else:
    #         validator = 'incorrect'
    # else:
    #     validator = 'not_found'

    # return jsonify({
    #     'validator': validator,
    #     'token': token,
    #     'id': user_id
    # })

@app.route('/getPetugas/<emailLaundry>', methods=['GET']) # findnya ditambahin
@cross_origin()
def getPetugas(emailLaundry):
    try:
        dataPetugas = db.petugas.find({'emailLaundry': emailLaundry})
        user_list = []
        for users in dataPetugas:
            user_list.append({
                'id_petugas': users['id_petugas'],
                'emailLaundry': users['emailLaundry'],
                'nama_petugas': users['nama_petugas'],
                'notelp_petugas': users['notelp_petugas'],
                'email_petugas': users['email_petugas'],
                'password_petugas': users['password_petugas'],
                'profil_petugas': users.get('profil_petugas', '')
            })
        return jsonify({'success': True, 'users': user_list})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/getPetugasByEmail/<emailPetugas>', methods=['GET']) # API baru
@cross_origin()
def getPetugasByEmail(emailPetugas):
    try:
        dataPetugas = db.petugas.find({'email_petugas': emailPetugas})
        user_list = []
        for users in dataPetugas:
            user_list.append({
                'id_petugas': users['id_petugas'],
                'emailLaundry': users['emailLaundry'],
                'nama_petugas': users['nama_petugas'],
                'notelp_petugas': users['notelp_petugas'],
                'email_petugas': users['email_petugas'],
                'password_petugas': users['password_petugas'],
                'profil_petugas': users.get('profil_petugas', '')
            })
        return jsonify({'success': True, 'users': user_list})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/getPetugasId/<id_petugas>/<emailLaundry>', methods=['GET'])
@cross_origin()
def getPetugasId(id_petugas, emailLaundry):
    try:
        petugas = db.petugas.find_one({'id_petugas': id_petugas, 'emailLaundry': emailLaundry})
        if petugas:
            return jsonify({
                'success': True,
                'petugas': {
                    'id_petugas': petugas['id_petugas'],
                    'emailLaundry': petugas['emailLaundry'],
                    'nama_petugas': petugas['nama_petugas'],
                    'notelp_petugas': petugas['notelp_petugas'],
                    'email_petugas': petugas['email_petugas'],
                    'password_petugas': petugas['password_petugas'],
                    'profil_petugas': petugas.get('profil_petugas', '')
                }
            })
        else:
            return jsonify({'success': False, 'error': 'Petugas not found'})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/updatePetugas/<id_petugas>/<emailLaundry>', methods=['PUT'])
@cross_origin()
def updatePetugas(id_petugas, emailLaundry):
    try:
        update_fields = {}

        update_fields['nama_petugas'] = request.form.get('nama_petugas')
        update_fields['notelp_petugas'] = request.form.get('notelp_petugas')
        update_fields['password_petugas'] = request.form.get('password_petugas')
        upload_path = request.form.get('upload_path')

        current_record = db.petugas.find_one({'id_petugas': id_petugas, 'emailLaundry': emailLaundry})
        
        if not current_record:
            return jsonify({'success': False, 'message': 'Petugas not found'})

        profil_petugas = current_record.get('profil_petugas', None)
        if 'profil_petugas' in request.files:
            file = request.files['profil_petugas']
            if file.filename != '':
                filename = secure_filename(file.filename)
                filepath = os.path.join(upload_path, filename)

                if not os.path.exists(upload_path):
                    os.makedirs(upload_path)

                try:
                    file.save(filepath)
                    profil_petugas = filename
                except Exception as e:
                    print(f"Failed to save file {filename} at {filepath}: {str(e)}")
                    return jsonify({'success': False, 'error': f"Failed to save file: {str(e)}"})

        if profil_petugas:
            update_fields['profil_petugas'] = profil_petugas

        result = db.petugas.update_one({'id_petugas': id_petugas, 'emailLaundry': emailLaundry}, {'$set': update_fields})

        if result.matched_count > 0:
            return jsonify({'success': True, 'message': 'Petugas updated successfully'})
        else:
            return jsonify({'success': False, 'error': 'Petugas not found'})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/deletePetugas/<id_petugas>/<emailLaundry>', methods=['DELETE'])
@cross_origin()
def deletePetugas(id_petugas, emailLaundry):
    try:
        result = db.petugas.delete_one({'id_petugas': id_petugas, 'emailLaundry': emailLaundry})

        if result.deleted_count > 0:
            return jsonify({'success': True, 'message': 'Petugas deleted successfully'})
        else:
            return jsonify({'success': False, 'error': 'Petugas not found'})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/getUser', methods=['GET']) # API baru
@cross_origin()
def getUser():
    try:
        dataUser = db.pelanggan.find()
        user_list = []
        for users in dataUser:
            user_list.append({
                'idUser': users['idUser'],
                'nama': users['nama'],
                'notelp': users['notelp'],
                'email': users['email'],
                'password': users['password']
            })
        return jsonify({'success': True, 'users': user_list})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/getUserEmail/<email>', methods=['GET']) # ganti nama API, tampilin idUser
@cross_origin()
def getUserEmail(email):
    try:
        pelanggan = db.pelanggan.find_one({'email': email})
        if pelanggan:
            pelanggan_details = {
                'idUser': pelanggan['idUser'],
                'nama': pelanggan['nama'],
                'notelp': pelanggan['notelp'],
                'email': pelanggan['email'],
                'password': pelanggan['password']
            }

            if 'profilPict' in pelanggan:
                pelanggan_details.update({
                    'profilPict': pelanggan['profilPict']
                })

            return jsonify({
                'success': True,
                'pelanggan': pelanggan_details
            })
        else:
            return jsonify({'success': False, 'error': 'User not found'})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/updateUser/<email>', methods=['PUT']) # updated logic
@cross_origin()
def updateUser(email):
    try:
        update_fields = {}

        update_fields['nama'] = request.form.get('nama')
        update_fields['notelp'] = request.form.get('notelp')
        upload_path = request.form.get('upload_path')

        current_record = db.pelanggan.find_one({'email': email})
        
        if not current_record:
            return jsonify({'success': False, 'message': 'User not found'})

        profilPict = current_record.get('profilPict', None)
        if 'profilPict' in request.files:
            file = request.files['profilPict']
            if file.filename != '':
                filename = secure_filename(file.filename)
                filepath = os.path.join(upload_path, filename)

                if not os.path.exists(upload_path):
                    os.makedirs(upload_path)

                try:
                    file.save(filepath)
                    profilPict = filename
                except Exception as e:
                    print(f"Failed to save file {filename} at {filepath}: {str(e)}")
                    return jsonify({'success': False, 'error': f"Failed to save file: {str(e)}"})

        if profilPict:
            update_fields['profilPict'] = profilPict

        result = db.pelanggan.update_one({'email': email}, {'$set': update_fields})

        if result.matched_count > 0:
            return jsonify({'success': True, 'message': 'User updated successfully'})
        else:
            return jsonify({'success': False, 'error': 'User not found'})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/getAdmin', methods=['GET'])
@cross_origin()
def getAdmin():
    try:
        dataAdmin = db.laundry.find()
        user_list = []
        for users in dataAdmin:
            user_list.append({
                'idAdmin': users['idAdmin'],
                'namaLaundry': users['namaLaundry'],
                'notelp': users['notelp'],
                'email': users['email'],
                'password': users['password'],
                'bukaTutupLaundry': users['bukaTutupLaundry']
            })
        return jsonify({'success': True, 'users': user_list})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/getAllLaundries', methods=['GET']) # API baru
@cross_origin()
def getAllLaundries():
    try:
        laundries = list(db.laundry.find())

        if laundries:
            admin_details = []
            for admin in laundries:
                if 'longitudeLaundry' in admin:
                    admin_details.append({
                        'idAdmin': admin['idAdmin'],
                        'email': admin['email'],
                        'namaLaundry': admin['namaLaundry'],
                        'alamat': admin['alamat'],
                        'kelurahan': admin['kelurahan'],
                        'kecamatan': admin['kecamatan'],
                        'kodePos': admin['kodePos'],
                        'longitudeLaundry': admin['longitudeLaundry'],
                        'latitudeLaundry': admin['latitudeLaundry'],
                        'detailAlamat': admin['detailAlamat'],
                        'profilPict': admin['profilPict'],
                        'bukaTutupLaundry': admin['bukaTutupLaundry']
                    })

            return jsonify({
                'success': True,
                'laundries': admin_details
            })
        else:
            return jsonify({'success': False, 'error': 'Admin not found'})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/getLaundries', methods=['GET'])  # API baru
@cross_origin()
def getLaundries():
    try:
        laundries = list(db.laundry.find())
        categories = list(db.kategori.find())

        if laundries:
            admin_details = []
            for admin in laundries:
                if 'alamat' in admin and 'profilPict' in admin and 'days' in admin:
                    admin_email = admin.get('email')
                    kategori = next((cat for cat in categories if cat.get('emailLaundry') == admin_email), None)

                    if kategori:
                        admin_details.append({
                            'idAdmin': admin['idAdmin'],
                            'email': admin['email'],
                            'namaLaundry': admin['namaLaundry'],
                            'bukaTutupLaundry': admin['bukaTutupLaundry'],
                            'alamat': admin['alamat'],
                            'kelurahan': admin['kelurahan'],
                            'kecamatan': admin['kecamatan'],
                            'kodePos': admin['kodePos'],
                            'longitudeLaundry': admin['longitudeLaundry'],
                            'latitudeLaundry': admin['latitudeLaundry'],
                            'detailAlamat': admin['detailAlamat'],
                            'profilPict': admin['profilPict'],
                            'days': admin.get('days', [
                                {'name': 'Senin', 'jamBuka': '', 'jamTutup': '', 'tutup': False},
                                {'name': 'Selasa', 'jamBuka': '', 'jamTutup': '', 'tutup': False},
                                {'name': 'Rabu', 'jamBuka': '', 'jamTutup': '', 'tutup': False},
                                {'name': 'Kamis', 'jamBuka': '', 'jamTutup': '', 'tutup': False},
                                {'name': 'Jumat', 'jamBuka': '', 'jamTutup': '', 'tutup': False},
                                {'name': 'Sabtu', 'jamBuka': '', 'jamTutup': '', 'tutup': False},
                                {'name': 'Minggu', 'jamBuka': '', 'jamTutup': '', 'tutup': False}
                            ])
                        })

            return jsonify({
                'success': True,
                'laundries': admin_details
            })
        else:
            return jsonify({'success': False, 'error': 'Admin not found'})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/getLaundriesByKat/<categoryType>', methods=['GET']) # API baru
@cross_origin()
def getLaundriesByKat(categoryType):
    try:
        laundries = list(db.laundry.find())
        categories = list(db.kategori.find({'categoryType': categoryType}))

        if laundries:
            admin_details = []
            for admin in laundries:
                if 'alamat' in admin and 'profilPict' in admin and 'days' in admin:
                    admin_email = admin.get('email')
                    kategori = next((cat for cat in categories if cat.get('emailLaundry') == admin_email), None)

                    if kategori:
                        admin_details.append({
                            'idAdmin': admin['idAdmin'],
                            'email': admin['email'],
                            'namaLaundry': admin['namaLaundry'],
                            'bukaTutupLaundry': admin['bukaTutupLaundry'],
                            'alamat': admin['alamat'],
                            'kelurahan': admin['kelurahan'],
                            'kecamatan': admin['kecamatan'],
                            'kodePos': admin['kodePos'],
                            'longitudeLaundry': admin['longitudeLaundry'],
                            'latitudeLaundry': admin['latitudeLaundry'],
                            'detailAlamat': admin['detailAlamat'],
                            'profilPict': admin['profilPict'],
                            'harga': kategori['harga'],
                            'keterangan': kategori['keterangan'],
                            'days': admin.get('days', [
                                {'name': 'Senin', 'jamBuka': '', 'jamTutup': '', 'tutup': False},
                                {'name': 'Selasa', 'jamBuka': '', 'jamTutup': '', 'tutup': False},
                                {'name': 'Rabu', 'jamBuka': '', 'jamTutup': '', 'tutup': False},
                                {'name': 'Kamis', 'jamBuka': '', 'jamTutup': '', 'tutup': False},
                                {'name': 'Jumat', 'jamBuka': '', 'jamTutup': '', 'tutup': False},
                                {'name': 'Sabtu', 'jamBuka': '', 'jamTutup': '', 'tutup': False},
                                {'name': 'Minggu', 'jamBuka': '', 'jamTutup': '', 'tutup': False}
                            ])
                        })

            return jsonify({
                'success': True,
                'laundries': admin_details
            })
        else:
            return jsonify({'success': False, 'error': 'No laundries found'})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/getAdminEmail/<email>', methods=['GET']) # nampilin idAdmin juga
@cross_origin()
def getAdminEmail(email):
    try:
        admin = db.laundry.find_one({'email': email})
        if admin:
            admin_details = {
                'idAdmin': admin['idAdmin'],
                'namaLaundry': admin['namaLaundry'],
                'notelp': admin['notelp'],
                'email': admin['email'],
                'password': admin['password'],
                'bukaTutupLaundry': admin['bukaTutupLaundry']
            }

            if 'profilPict' in admin:
                admin_details.update({
                    'profilPict': admin['profilPict']
                })

            if 'alamat' in admin:
                admin_details.update({
                    'alamat': admin['alamat'],
                    'kelurahan': admin['kelurahan'],
                    'kecamatan': admin['kecamatan'],
                    'kodePos': admin['kodePos'],
                    'longitudeLaundry': admin['longitudeLaundry'],
                    'latitudeLaundry': admin['latitudeLaundry'],
                    'detailAlamat': admin['detailAlamat']
                })

            if 'days' in admin:
                admin_details.update({
                    'days': admin.get('days', [
                        {'name': 'Senin', 'jamBuka': '', 'jamTutup': '', 'tutup': False},
                        {'name': 'Selasa', 'jamBuka': '', 'jamTutup': '', 'tutup': False},
                        {'name': 'Rabu', 'jamBuka': '', 'jamTutup': '', 'tutup': False},
                        {'name': 'Kamis', 'jamBuka': '', 'jamTutup': '', 'tutup': False},
                        {'name': 'Jumat', 'jamBuka': '', 'jamTutup': '', 'tutup': False},
                        {'name': 'Sabtu', 'jamBuka': '', 'jamTutup': '', 'tutup': False},
                        {'name': 'Minggu', 'jamBuka': '', 'jamTutup': '', 'tutup': False}
                    ])
                })

            return jsonify({
                'success': True,
                'admin': admin_details
            })
        else:
            return jsonify({'success': False, 'error': 'Admin not found'})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/getAdminSearch/<namaLaundry>', methods=['GET'])
@cross_origin()
def getAdminSearch(namaLaundry):
    try:
        # Gunakan $regex untuk mendukung pencarian parsial
        admin_cursor = db.laundry.find({'namaLaundry': {'$regex': namaLaundry, '$options': 'i'}})
        
        # List untuk menyimpan hasil pencarian
        admin_list = []

        for admin in admin_cursor:
            admin_details = {
                'idAdmin': admin['idAdmin'],
                'namaLaundry': admin['namaLaundry'],
                'notelp': admin['notelp'],
                'email': admin['email'],
                'password': admin['password'],
                'bukaTutupLaundry': admin['bukaTutupLaundry']
            }

            if 'profilPict' in admin:
                admin_details.update({
                    'profilPict': admin['profilPict']
                })

            if 'alamat' in admin:
                admin_details.update({
                    'alamat': admin['alamat'],
                    'kelurahan': admin['kelurahan'],
                    'kecamatan': admin['kecamatan'],
                    'kodePos': admin['kodePos'],
                    'longitudeLaundry': admin['longitudeLaundry'],
                    'latitudeLaundry': admin['latitudeLaundry'],
                    'detailAlamat': admin['detailAlamat']
                })

            if 'days' in admin:
                admin_details.update({
                    'days': admin.get('days', [
                        {'name': 'Senin', 'jamBuka': '', 'jamTutup': '', 'tutup': False},
                        {'name': 'Selasa', 'jamBuka': '', 'jamTutup': '', 'tutup': False},
                        {'name': 'Rabu', 'jamBuka': '', 'jamTutup': '', 'tutup': False},
                        {'name': 'Kamis', 'jamBuka': '', 'jamTutup': '', 'tutup': False},
                        {'name': 'Jumat', 'jamBuka': '', 'jamTutup': '', 'tutup': False},
                        {'name': 'Sabtu', 'jamBuka': '', 'jamTutup': '', 'tutup': False},
                        {'name': 'Minggu', 'jamBuka': '', 'jamTutup': '', 'tutup': False}
                    ])
                })

            admin_list.append(admin_details)

        if admin_list:
            return jsonify({
                'success': True,
                'admin': admin_list
            })
        else:
            return jsonify({'success': False, 'error': 'Admin not found'})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})


@app.route('/updateAdmin/<email>', methods=['PUT'])
@cross_origin()
def updateAdmin(email):
    try:
        update_fields = {}

        update_fields['namaLaundry'] = request.form.get('namaLaundry')
        update_fields['notelp'] = request.form.get('notelp')
        upload_path = request.form.get('upload_path')

        current_record = db.laundry.find_one({'email': email})
        
        if not current_record:
            return jsonify({'success': False, 'message': 'Admin not found'})

        profilPict = current_record.get('profilPict', None)
        if 'profilPict' in request.files:
            file = request.files['profilPict']
            if file.filename != '':
                filename = secure_filename(file.filename)
                filepath = os.path.join(upload_path, filename)

                if not os.path.exists(upload_path):
                    os.makedirs(upload_path)

                try:
                    file.save(filepath)
                    profilPict = filename
                    print(filepath)
                except Exception as e:
                    print(f"Failed to save file {filename} at {filepath}: {str(e)}")
                    return jsonify({'success': False, 'error': f"Failed to save file: {str(e)}"})

        if profilPict:
            update_fields['profilPict'] = profilPict

        result = db.laundry.update_one({'email': email}, {'$set': update_fields})

        if result.matched_count > 0:
            return jsonify({'success': True, 'message': 'Admin updated successfully'})
        else:
            return jsonify({'success': False, 'error': 'Admin not found'})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/getPembayaran/<emailLaundry>', methods=['GET'])
@cross_origin()
def getPembayaran(emailLaundry):
    try:
        dataMetodePembayaran = db.metodePembayaran.find({'emailLaundry': emailLaundry})
        user_list = []
        payment_method = []
        for users in dataMetodePembayaran:
            user_list.append({
                'idPembayaran': users['idPembayaran'],
                'emailLaundry': users['emailLaundry'],
                'paymentMethod': users['paymentMethod'],
                'namaBank': users['namaBank'],
                'noRekBank': users['noRekBank'],
                'catatan': users['catatan'],
                'qrisImg': users.get('qrisImg', '')
            })

        for methods in dataMetodePembayaran:
            payment_method.append({
                'paymentMethod': methods['paymentMethod']
            })
        return jsonify({'success': True, 'users': user_list, 'methods': payment_method})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/getPembayaranId/<idPembayaran>/<emailLaundry>', methods=['GET'])
@cross_origin()
def getPembayaranId(idPembayaran, emailLaundry):
    try:
        pembayaran = db.metodePembayaran.find_one({'idPembayaran': idPembayaran, 'emailLaundry': emailLaundry})
        if pembayaran:
            return jsonify({
                'success': True,
                'pembayaran': {
                    'idPembayaran': pembayaran['idPembayaran'],
                    'emailLaundry': pembayaran['emailLaundry'],
                    'paymentMethod': pembayaran['paymentMethod'],
                    'namaBank': pembayaran['namaBank'],
                    'noRekBank': pembayaran['noRekBank'],
                    'catatan': pembayaran['catatan'],
                    'qrisImg': pembayaran.get('qrisImg', '')
                }
            })
        else:
            return jsonify({'success': False, 'error': 'Metode Pembayaran not found'})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/addPaymentMethod/<emailLaundry>', methods=['POST'])
@cross_origin()
def addPaymentMethod(emailLaundry):
    try:
        idPembayaran = request.form.get('idPembayaran')
        email_laundry = request.form.get('emailLaundry')
        payment_method = request.form.get('paymentMethod')
        nama_bank = request.form.get('namaBank', '')
        no_rek_bank = request.form.get('noRekBank', '')
        qris_img = None
        catatan = request.form.get('catatan', '')
        upload_path = request.form.get('upload_path')

        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
            print(f"Created upload directory: {upload_path}")

        if 'qrisImg' in request.files:
            file = request.files['qrisImg']
            if file.filename != '':
                filename = secure_filename(file.filename)
                filepath = os.path.join(upload_path, filename)
                try:
                    file.save(filepath)
                    qris_img = filename
                except Exception as e:
                    print(f"Failed to save file {filename} at {filepath}: {str(e)}")
                    return jsonify({'success': False, 'error': f"Failed to save file: {str(e)}"})
            else:
                print("No file uploaded")
        else:
            print("No file part in request")

        metodePembayaran = {
            'idPembayaran': idPembayaran,
            'emailLaundry': email_laundry,
            'paymentMethod': payment_method,
            'namaBank': nama_bank,
            'noRekBank': no_rek_bank,
            'qrisImg': qris_img,
            'catatan': catatan
        }
        db.metodePembayaran.insert_one(metodePembayaran)
        return jsonify({'success': True, 'message': 'Payment method added successfully'})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/editPaymentMethod/<idPembayaran>/<emailLaundry>', methods=['PUT'])
@cross_origin()
def editPaymentMethod(idPembayaran, emailLaundry):
    try:
        emailLaundry = request.form.get('emailLaundry')
        payment_method = request.form.get('paymentMethod')
        nama_bank = request.form.get('namaBank', '')
        no_rek_bank = request.form.get('noRekBank', '')
        catatan = request.form.get('catatan', '')
        upload_path = request.form.get('upload_path')

        current_record = db.metodePembayaran.find_one({'idPembayaran': idPembayaran, 'emailLaundry': emailLaundry})
        
        if not current_record:
            return jsonify({'success': False, 'message': 'Payment method not found'})

        if payment_method == 'qris':
            qris_img = current_record.get('qrisImg', None) 
            if 'qrisImg' in request.files:
                file = request.files['qrisImg']
                if file.filename != '':
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(upload_path, filename)
                    try:
                        file.save(filepath)
                        qris_img = filename
                    except Exception as e:
                        print(f"Failed to save file {filename} at {filepath}: {str(e)}")
                        return jsonify({'success': False, 'error': f"Failed to save file: {str(e)}"})

            db.metodePembayaran.update_one(
                {'idPembayaran': idPembayaran, 'emailLaundry': emailLaundry}, 
                {'$set': {'qrisImg': qris_img, 'catatan': catatan}}
            )
        else:
            db.metodePembayaran.update_one(
                {'idPembayaran': idPembayaran, 'emailLaundry': emailLaundry}, 
                {'$set': {'namaBank': nama_bank, 'noRekBank': no_rek_bank, 'catatan': catatan}}
            )
        
        return jsonify({'success': True, 'message': 'Payment method updated successfully'})

    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/deletePaymentMethod/<idPembayaran>/<emailLaundry>', methods=['DELETE'])
@cross_origin()
def deletePaymentMethod(idPembayaran, emailLaundry):
    try:
        result = db.metodePembayaran.delete_one({'idPembayaran': idPembayaran, 'emailLaundry': emailLaundry})

        if result.deleted_count > 0:
            return jsonify({'success': True, 'message': 'Metode Pembayaran deleted successfully'})
        else:
            return jsonify({'success': False, 'error': 'Metode Pembayaran not found'})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/getKategori/<emailLaundry>', methods=['GET'])
@cross_origin()
def getKategori(emailLaundry):
    try:
        dataKategori = db.kategori.find({'emailLaundry': emailLaundry})
        categories_list = []
        tipe_kategori = []

        for categories in dataKategori:
            categories_list.append({
                'idKategori': categories['idKategori'],
                'emailLaundry': categories['emailLaundry'],
                'categoryType': categories['categoryType'],
                'categoryName': categories['categoryName'],
                'harga': categories['harga'],
                'keterangan': categories['keterangan']
            })

        for category in dataKategori:
            tipe_kategori.append({
                'categoryType': category['categoryType']
            })
        return jsonify({'success': True, 'categories': categories_list, 'category': tipe_kategori})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/getKategoriId/<idKategori>/<emailLaundry>', methods=['GET'])
@cross_origin()
def getKategoriId(idKategori, emailLaundry):
    try:
        kategori = db.kategori.find_one({'idKategori': idKategori, 'emailLaundry': emailLaundry})
        if kategori:
            return jsonify({
                'success': True,
                'kategori': {
                    'idKategori': kategori['idKategori'],
                    'emailLaundry': kategori['emailLaundry'],
                    'categoryType': kategori['categoryType'],
                    'categoryName': kategori['categoryName'],
                    'harga': kategori['harga'],
                    'keterangan': kategori['keterangan']
                }
            })
        else:
            return jsonify({'success': False, 'error': 'Kategori not found'})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/addKategori/<email>', methods=['POST'])
@cross_origin()
def addKategori(email):
    try:
        idKategori = request.form.get('idKategori')
        emailLaundry = request.form.get('emailLaundry')
        categoryType = request.form.get('categoryType')
        categoryName = request.form.get('categoryName')
        harga = request.form.get('harga')
        keterangan = request.form.get('keterangan', '')

        kategori = {
            'idKategori': idKategori,
            'emailLaundry': emailLaundry,
            'categoryType': categoryType,
            'categoryName': categoryName,
            'harga': harga,
            'keterangan': keterangan
        }

        db.kategori.insert_one(kategori)

        return jsonify({'success': True, 'message': 'Kategori added successfully'})
    
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/editKategori/<idKategori>/<emailLaundry>', methods=['PUT'])
@cross_origin()
def editKategori(idKategori, emailLaundry):
    try:
        categoryType = request.form.get('categoryType')
        categoryName = request.form.get('categoryName')
        harga = request.form.get('harga')
        keterangan = request.form.get('keterangan', '')

        db.kategori.update_one(
                {'idKategori': idKategori, 'emailLaundry': emailLaundry}, 
                {'$set': {'categoryType': categoryType, 'categoryName': categoryName, 'harga': harga, 'keterangan': keterangan}}
        )
        
        return jsonify({'success': True, 'message': 'Kategori updated successfully'})

    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/deleteKategori/<idKategori>/<emailLaundry>', methods=['DELETE'])
@cross_origin()
def deleteKategori(idKategori, emailLaundry):
    try:
        result = db.kategori.delete_one({'idKategori': idKategori, 'emailLaundry': emailLaundry})

        if result.deleted_count > 0:
            return jsonify({'success': True, 'message': 'Kategori deleted successfully'})
        else:
            return jsonify({'success': False, 'error': 'Kategori not found'})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/getPesanan', methods=['GET']) # API baru
@cross_origin()
def getPesanan():
    try:
        dataPesanan = db.pesanan.find()
        order_list = []

        for orders in dataPesanan:
            order_list.append({
                'idPesanan': orders['idPesanan'],
                'emailLaundry': orders['emailLaundry'],
                'emailUser': orders['emailUser'],
                'alamatUser': orders['alamatUser'],
                'statusPesanan': orders.get('statusPesanan', [
                    {'status': 'menunggu_konfirmasi', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'menunggu_dijemput', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'sedang_dijemput', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'diproses', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'perlu_diantar', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'sedang_diantar', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'selesai', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'gagal', 'tanggal': '', 'waktu': '', 'active': 'false' }
                ])
            })
        return jsonify({'success': True, 'orders': order_list})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/getNotification', methods=['GET']) # API baru
@cross_origin()
def getNotification():
    try:
        dataNotif = db.notification.find()
        notif_list = []

        for notifs in dataNotif:
            notif_list.append({
                'idNotif': notifs['idNotif'],
                'idPesanan': notifs['idPesanan'],
                'emailLaundry': notifs['emailLaundry'],
                'emailUser': notifs['emailUser'],
                'message': notifs['message']
            })
        return jsonify({'success': True, 'notifs': notif_list})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/getNotifByEmailLaundry/<emailLaundry>', methods=['GET']) # API baru
@cross_origin()
def getNotifByEmailLaundry(emailLaundry):
    try:
        dataNotif = db.notification.find({'emailLaundry': emailLaundry})
        notif_list = []
        for notifs in dataNotif:
            notif_item = {
                'idNotif': notifs['idNotif'],
                'idPesanan': notifs['idPesanan'],
                'emailLaundry': notifs['emailLaundry'],
                'emailUser': notifs['emailUser'],
                'message': notifs['message']
            }

            if 'emailPetugas' in notifs:
                notif_item['emailPetugas'] = notifs['emailPetugas']

            notif_list.append(notif_item)

        return jsonify({'success': True, 'notifs': notif_list})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/getPesananByEmail/<emailUser>', methods=['GET']) # API baru
@cross_origin()
def getPesananByEmail(emailUser):
    try:
        dataPesanan = db.pesanan.find({'emailUser': emailUser})
        order_list = []
        for orders in dataPesanan:
            order_item = {
                'idPesanan': orders['idPesanan'],
                'emailLaundry': orders['emailLaundry'],
                'emailUser': orders['emailUser'],
                'alamatUser': orders['alamatUser'],
                'statusPesanan': orders.get('statusPesanan', [
                    {'status': 'menunggu_konfirmasi', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'menunggu_dijemput', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'sedang_dijemput', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'diproses', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'perlu_diantar', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'sedang_diantar', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'selesai', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'gagal', 'tanggal': '', 'waktu': '', 'active': 'false' }
                ])
            }

            if 'emailPetugas' in orders:
                order_item['emailPetugas'] = orders['emailPetugas']

            if 'isRated' in orders:
                order_item['isRated'] = orders['isRated']

            order_list.append(order_item)

        return jsonify({'success': True, 'orders': order_list})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/getPesananByEmailLaundry/<emailLaundry>', methods=['GET']) # API baru
@cross_origin()
def getPesananByEmailLaundry(emailLaundry):
    try:
        dataPesanan = db.pesanan.find({'emailLaundry': emailLaundry})
        order_list = []
        for orders in dataPesanan:
            order_item = {
                'idPesanan': orders['idPesanan'],
                'emailLaundry': orders['emailLaundry'],
                'emailUser': orders['emailUser'],
                'alamatUser': orders['alamatUser'],
                'statusPesanan': orders.get('statusPesanan', [
                    {'status': 'menunggu_konfirmasi', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'menunggu_dijemput', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'sedang_dijemput', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'diproses', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'perlu_diantar', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'sedang_diantar', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'selesai', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'gagal', 'tanggal': '', 'waktu': '', 'active': 'false' }
                ])
            }

            if 'emailPetugas' in orders:
                order_item['emailPetugas'] = orders['emailPetugas']

            if 'pesanan' in orders:
                order_item['pesanan'] = orders['pesanan']
                order_item['catatan'] = orders['catatan']
                order_item['totalBayar'] = orders['totalBayar']
                order_item['idPembayaran'] = orders['idPembayaran']
                order_item['buktiPembayaran'] = orders['buktiPembayaran']

            order_list.append(order_item)

        return jsonify({'success': True, 'orders': order_list})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

# @app.route('/getPesananByIdPesanan/<idPesanan>', methods=['GET']) # API baru
# @cross_origin()
# def getPesananByIdPesanan(idPesanan):
#     try:
#         dataPesanan = db.pesanan.find({'idPesanan': idPesanan})
#         order_list = []
#         for orders in dataPesanan:
#             order_item = {
#                 'idPesanan': orders['idPesanan'],
#                 'emailLaundry': orders['emailLaundry'],
#                 'emailUser': orders['emailUser'],
#                 'alamatUser': orders['alamatUser'],
#                 'statusPesanan': orders.get('statusPesanan', [
#                     {'status': 'menunggu_konfirmasi', 'tanggal': '', 'waktu': '', 'active': 'false' },
#                     {'status': 'menunggu_dijemput', 'tanggal': '', 'waktu': '', 'active': 'false' },
#                     {'status': 'sedang_dijemput', 'tanggal': '', 'waktu': '', 'active': 'false' },
#                     {'status': 'diproses', 'tanggal': '', 'waktu': '', 'active': 'false' },
#                     {'status': 'perlu_diantar', 'tanggal': '', 'waktu': '', 'active': 'false' },
#                     {'status': 'sedang_diantar', 'tanggal': '', 'waktu': '', 'active': 'false' },
#                     {'status': 'selesai', 'tanggal': '', 'waktu': '', 'active': 'false' },
#                     {'status': 'gagal', 'tanggal': '', 'waktu': '', 'active': 'false' }
#                 ])
#             }

#             if 'emailPetugas' in orders:
#                 order_item['emailPetugas'] = orders['emailPetugas']

#             if 'pesanan' in orders:
#                 order_item['pesanan'] = orders['pesanan'],
#                 order_item['catatan'] = orders['catatan'],
#                 order_item['totalBayar'] = orders['totalBayar'],
#                 order_item['idPembayaran'] = orders['idPembayaran'],
#                 order_item['buktiPembayaran'] = orders['buktiPembayaran']

#             order_list.append(order_item)

#         return jsonify({'success': True, 'orders': order_list})
#     except Exception as e:
#         error_message = f'Error: {str(e)}'
#         print(error_message)
#         return jsonify({'success': False, 'error': error_message})

@app.route('/getPesananByIdEmail/<idPesanan>/<emailPetugas>', methods=['GET']) # API baru
@cross_origin()
def getPesananByIdEmail(idPesanan, emailPetugas):
    try:
        dataPesanan = db.pesanan.find({'idPesanan': idPesanan, 'emailPetugas': emailPetugas})
        order_list = []
        for orders in dataPesanan:
            order_item = {
                'idPesanan': orders['idPesanan'],
                'emailLaundry': orders['emailLaundry'],
                'emailUser': orders['emailUser'],
                'alamatUser': orders['alamatUser'],
                'statusPesanan': orders.get('statusPesanan', [
                    {'status': 'menunggu_konfirmasi', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'menunggu_dijemput', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'sedang_dijemput', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'diproses', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'perlu_diantar', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'sedang_diantar', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'selesai', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'gagal', 'tanggal': '', 'waktu': '', 'active': 'false' }
                ])
            }

            if 'emailPetugas' in orders:
                order_item['emailPetugas'] = orders['emailPetugas']

            if 'pesanan' in orders:
                order_item['pesanan'] = orders['pesanan'],
                order_item['catatan'] = orders['catatan'],
                order_item['totalBayar'] = orders['totalBayar'],
                order_item['idPembayaran'] = orders['idPembayaran'],
                order_item['buktiPembayaran'] = orders['buktiPembayaran']

            order_list.append(order_item)

        return jsonify({'success': True, 'orders': order_list})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/getPesananByIdEmailLaundry/<idPesanan>/<emailLaundry>', methods=['GET']) # API baru
@cross_origin()
def getPesananByIdEmailLaundry(idPesanan, emailLaundry):
    try:
        dataPesanan = db.pesanan.find({'idPesanan': idPesanan, 'emailLaundry': emailLaundry})
        order_list = []
        for orders in dataPesanan:
            order_item = {
                'idPesanan': orders['idPesanan'],
                'emailLaundry': orders['emailLaundry'],
                'emailUser': orders['emailUser'],
                'alamatUser': orders['alamatUser'],
                'statusPesanan': orders.get('statusPesanan', [
                    {'status': 'menunggu_konfirmasi', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'menunggu_dijemput', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'sedang_dijemput', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'diproses', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'perlu_diantar', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'sedang_diantar', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'selesai', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'gagal', 'tanggal': '', 'waktu': '', 'active': 'false' }
                ])
            }

            if 'emailPetugas' in orders:
                order_item['emailPetugas'] = orders['emailPetugas']

            if 'pesanan' in orders:
                order_item['pesanan'] = orders['pesanan'],
                order_item['catatan'] = orders['catatan'],
                order_item['totalBayar'] = orders['totalBayar'],
                order_item['idPembayaran'] = orders['idPembayaran'],
                order_item['buktiPembayaran'] = orders['buktiPembayaran']

            order_list.append(order_item)

        return jsonify({'success': True, 'orders': order_list})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/getPesananByIdEmailUser/<idPesanan>/<emailUser>', methods=['GET']) # API baru
@cross_origin()
def getPesananByIdEmailUser(idPesanan, emailUser):
    try:
        dataPesanan = db.pesanan.find({'idPesanan': idPesanan, 'emailUser': emailUser})
        order_list = []
        for orders in dataPesanan:
            order_item = {
                'idPesanan': orders['idPesanan'],
                'emailLaundry': orders['emailLaundry'],
                'emailUser': orders['emailUser'],
                'alamatUser': orders['alamatUser'],
                'statusPesanan': orders.get('statusPesanan', [
                    {'status': 'menunggu_konfirmasi', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'menunggu_dijemput', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'sedang_dijemput', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'diproses', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'perlu_diantar', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'sedang_diantar', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'selesai', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'gagal', 'tanggal': '', 'waktu': '', 'active': 'false' }
                ])
            }

            if 'emailPetugas' in orders:
                order_item['emailPetugas'] = orders['emailPetugas']

            if 'pesanan' in orders:
                order_item['pesanan'] = orders['pesanan'],
                order_item['catatan'] = orders['catatan'],
                order_item['totalBayar'] = orders['totalBayar'],
                order_item['idPembayaran'] = orders['idPembayaran'],
                order_item['buktiPembayaran'] = orders['buktiPembayaran']

            order_list.append(order_item)

        return jsonify({'success': True, 'orders': order_list})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/getPesananByEmailPetugas/<emailPetugas>', methods=['GET']) # API baru
@cross_origin()
def getPesananByEmailPetugas(emailPetugas):
    try:
        dataPesanan = db.pesanan.find({'emailPetugas': emailPetugas})
        order_list = []
        for orders in dataPesanan:
            order_item = {
                'idPesanan': orders['idPesanan'],
                'emailLaundry': orders['emailLaundry'],
                'emailUser': orders['emailUser'],
                'emailPetugas': orders['emailPetugas'],
                'alamatUser': orders['alamatUser'],
                'statusPesanan': orders.get('statusPesanan', [
                    {'status': 'menunggu_konfirmasi', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'menunggu_dijemput', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'sedang_dijemput', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'diproses', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'perlu_diantar', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'sedang_diantar', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'selesai', 'tanggal': '', 'waktu': '', 'active': 'false' },
                    {'status': 'gagal', 'tanggal': '', 'waktu': '', 'active': 'false' }
                ])
            }

            order_list.append(order_item)

        return jsonify({'success': True, 'orders': order_list})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/addPesanan/<idPesanan>', methods=['POST']) # API baru
@cross_origin()
def addPesanan(idPesanan):
    try:
        idPesanan = request.form.get('idPesanan')
        emailLaundry = request.form.get('emailLaundry')
        emailUser = request.form.get('emailUser')
        alamatUser = request.form.get('alamatUser')
        dataStatusPesanan = request.form.get('statusPesanan')
        statusPesanan = json.loads(dataStatusPesanan)

        pesanan = {
            'idPesanan': idPesanan,
            'emailLaundry': emailLaundry,
            'emailUser': emailUser,
            'alamatUser': alamatUser,
            'statusPesanan': statusPesanan
        }

        db.pesanan.insert_one(pesanan)

        return jsonify({'success': True, 'message': 'Pesanan added successfully'})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/addNotif/<idPesanan>/<idNotif>', methods=['POST']) # API baru
@cross_origin()
def addNotif(idPesanan, idNotif):
    try:
        idNotif = request.form.get('idNotif')
        idPesanan = request.form.get('idPesanan')
        emailLaundry = request.form.get('emailLaundry')
        emailUser = request.form.get('emailUser')
        message = request.form.get('message')

        notification = {
            'idNotif': idNotif,
            'idPesanan': idPesanan,
            'emailLaundry': emailLaundry,
            'emailUser': emailUser,
            'message': message
        }

        db.notification.insert_one(notification)

        return jsonify({'success': True, 'message': 'Notification added successfully'})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/editKonfirmasi/<idPesanan>/<emailLaundry>', methods=['PUT']) # API baru
@cross_origin()
def editKonfirmasi(idPesanan, emailLaundry):
    try:
        emailPetugas = request.form.get('emailPetugas')
        currentDate = request.form.get('currentDate')
        currentTime = request.form.get('currentTime')
        
        current_record = db.pesanan.find_one({'idPesanan': idPesanan, 'emailLaundry': emailLaundry})
        if not current_record:
            return jsonify({'success': False, 'message': 'Pesanan not found'})

        db.pesanan.update_one(
            {'idPesanan': idPesanan, 'emailLaundry': emailLaundry}, 
            {'$set': {
                'statusPesanan.0.active': 'false',
                'statusPesanan.1.active': 'true',
                'statusPesanan.1.tanggal': currentDate,
                'statusPesanan.1.waktu': currentTime,
                'emailPetugas': emailPetugas
            }}
        )
        return jsonify({'success': True, 'message': 'Status updated successfully'})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/editTungguDijemput/<idPesanan>/<emailPetugas>', methods=['PUT']) # API baru
@cross_origin()
def editTungguDijemput(idPesanan, emailPetugas):
    try:
        currentDate = request.form.get('currentDate')
        currentTime = request.form.get('currentTime')
        
        current_record = db.pesanan.find_one({'idPesanan': idPesanan, 'emailPetugas': emailPetugas})
        if not current_record:
            return jsonify({'success': False, 'message': 'Pesanan not found'})

        db.pesanan.update_one(
            {'idPesanan': idPesanan, 'emailPetugas': emailPetugas}, 
            {'$set': {
                'statusPesanan.1.active': 'false',
                'statusPesanan.2.active': 'true',
                'statusPesanan.2.tanggal': currentDate,
                'statusPesanan.2.waktu': currentTime
            }}
        )
        return jsonify({'success': True, 'message': 'Status updated successfully'})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/editSedangDijemput/<idPesanan>/<emailPetugas>', methods=['PUT']) # API baru
@cross_origin()
def editSedangDijemput(idPesanan, emailPetugas):
    try:
        currentDate = request.form.get('currentDate')
        currentTime = request.form.get('currentTime')
        pesanan = request.form.get('pesanan')
        catatan = request.form.get('catatan')
        idPembayaran = request.form.get('idPembayaran')
        totalBayar = request.form.get('totalBayar')
        buktiPembayaran = None
        upload_path = request.form.get('upload_path')

        if 'buktiPembayaran' in request.files:
            file = request.files['buktiPembayaran']

            if file.filename != '':
                filename = secure_filename(file.filename)
                filepath = os.path.join(upload_path, filename)

                if not os.path.exists(upload_path):
                    os.makedirs(upload_path)

                file.save(filepath)
                buktiPembayaran = filename

        pesanan = json.loads(pesanan)
        
        current_record = db.pesanan.find_one({'idPesanan': idPesanan, 'emailPetugas': emailPetugas})
        if not current_record:
            return jsonify({'success': False, 'message': 'Pesanan not found'})

        db.pesanan.update_one(
            {'idPesanan': idPesanan, 'emailPetugas': emailPetugas}, 
            {'$set': {
                'statusPesanan.2.active': 'false',
                'statusPesanan.3.active': 'true',
                'statusPesanan.3.tanggal': currentDate,
                'statusPesanan.3.waktu': currentTime,
                'pesanan': pesanan,
                'catatan': catatan,
                'idPembayaran': idPembayaran,
                'buktiPembayaran': buktiPembayaran,
                'totalBayar': totalBayar
            }}
        )
        return jsonify({'success': True, 'message': 'Status updated successfully'})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/editDiproses/<idPesanan>/<emailLaundry>', methods=['PUT']) # API baru
@cross_origin()
def editDiproses(idPesanan, emailLaundry):
    try:
        currentDate = request.form.get('currentDate')
        currentTime = request.form.get('currentTime')
        
        current_record = db.pesanan.find_one({'idPesanan': idPesanan, 'emailLaundry': emailLaundry})
        if not current_record:
            return jsonify({'success': False, 'message': 'Pesanan not found'})

        db.pesanan.update_one(
            {'idPesanan': idPesanan, 'emailLaundry': emailLaundry}, 
            {'$set': {
                'statusPesanan.3.active': 'false',
                'statusPesanan.4.active': 'true',
                'statusPesanan.4.tanggal': currentDate,
                'statusPesanan.4.waktu': currentTime
            }}
        )
        return jsonify({'success': True, 'message': 'Status updated successfully'})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/editTungguDiantar/<idPesanan>/<emailPetugas>', methods=['PUT']) # API baru
@cross_origin()
def editTungguDiantar(idPesanan, emailPetugas):
    try:
        currentDate = request.form.get('currentDate')
        currentTime = request.form.get('currentTime')
        
        current_record = db.pesanan.find_one({'idPesanan': idPesanan, 'emailPetugas': emailPetugas})
        if not current_record:
            return jsonify({'success': False, 'message': 'Pesanan not found'})

        db.pesanan.update_one(
            {'idPesanan': idPesanan, 'emailPetugas': emailPetugas}, 
            {'$set': {
                'statusPesanan.4.active': 'false',
                'statusPesanan.5.active': 'true',
                'statusPesanan.5.tanggal': currentDate,
                'statusPesanan.5.waktu': currentTime
            }}
        )
        return jsonify({'success': True, 'message': 'Status updated successfully'})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/editSedangDiantar/<idPesanan>/<emailPetugas>', methods=['PUT']) # API baru
@cross_origin()
def editSedangDiantar(idPesanan, emailPetugas):
    try:
        currentDate = request.form.get('currentDate')
        currentTime = request.form.get('currentTime')
        
        current_record = db.pesanan.find_one({'idPesanan': idPesanan, 'emailPetugas': emailPetugas})
        if not current_record:
            return jsonify({'success': False, 'message': 'Pesanan not found'})

        db.pesanan.update_one(
            {'idPesanan': idPesanan, 'emailPetugas': emailPetugas}, 
            {'$set': {
                'statusPesanan.5.active': 'false',
                'statusPesanan.6.active': 'true',
                'statusPesanan.6.tanggal': currentDate,
                'statusPesanan.6.waktu': currentTime
            }}
        )
        return jsonify({'success': True, 'message': 'Status updated successfully'})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/getPenilaian', methods=['GET']) # API baru
@cross_origin()
def getPenilaian():
    try:
        dataPenilaian = db.penilaian.find()
        rating_list = []

        for rates in dataPenilaian:
            rating_list.append({
                'idPenilaian': rates['idPenilaian'],
                'emailLaundry': rates['emailLaundry'],
                'emailUser': rates['emailUser'],
                'tanggal': rates['tanggal'],
                'rate': rates['rate'],
                'ulasan': rates['ulasan']
            })
        return jsonify({'success': True, 'rates': rating_list})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/isRated/<idPesanan>/<emailUser>', methods=['PUT']) # API baru
@cross_origin()
def isRated(idPesanan, emailUser):
    try:
        current_record = db.pesanan.find_one({'idPesanan': idPesanan, 'emailUser': emailUser})
        if not current_record:
            return jsonify({'success': False, 'message': 'Pesanan not found'})

        db.pesanan.update_one(
            {'idPesanan': idPesanan, 'emailUser': emailUser}, 
            {'$set': {
                'isRated': 'true',
            }}
        )
        return jsonify({'success': True, 'message': 'Status updated successfully'})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/addPenilaian', methods=['POST']) # API baru
@cross_origin()
def addPenilaian():
    try:
        idPenilaian = request.form.get('idPenilaian')
        emailLaundry = request.form.get('emailLaundry')
        emailUser = request.form.get('emailUser')
        tanggal = request.form.get('tanggal')
        rate = request.form.get('rate')
        ulasan = request.form.get('ulasan')

        penilaian = {
            'idPenilaian': idPenilaian,
            'emailLaundry': emailLaundry,
            'emailUser': emailUser,
            'tanggal': tanggal,
            'rate': rate,
            'ulasan': ulasan
        }

        db.penilaian.insert_one(penilaian)

        return jsonify({'success': True, 'message': 'Penilaian added successfully'})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/getAllPenilaian/<emailUser>', methods=['GET']) # API baru
@cross_origin()
def getAllPenilaian(emailUser):
    try:
        dataPenilaian = db.penilaian.find({'emailUser': emailUser})
        rate_list = []

        for rates in dataPenilaian:
            rate_list.append({
                'idPenilaian': rates['idPenilaian'],
                'emailLaundry': rates['emailLaundry'],
                'emailUser': rates['emailUser'],
                'tanggal': rates['tanggal'],
                'rate': rates['rate'],
                'ulasan': rates['ulasan']
            })
        return jsonify({'success': True, 'rates': rate_list})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/getAllPenilaianByLaundry/<emailLaundry>', methods=['GET']) # API baru
@cross_origin()
def getAllPenilaianByLaundry(emailLaundry):
    try:
        dataPenilaian = db.penilaian.find({'emailLaundry': emailLaundry})
        rate_list = []

        for rates in dataPenilaian:
            rate_list.append({
                'idPenilaian': rates['idPenilaian'],
                'emailLaundry': rates['emailLaundry'],
                'emailUser': rates['emailUser'],
                'tanggal': rates['tanggal'],
                'rate': rates['rate'],
                'ulasan': rates['ulasan']
            })
        return jsonify({'success': True, 'rates': rate_list})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

# API untuk handle upload yaa
@app.route('/signUpPetugas/<email>', methods=['POST'])
@cross_origin()
def signUpPetugas(email):
    try:
        id_petugas = request.form.get('id_petugas')
        emailLaundry = request.form.get('emailLaundry')
        nama_petugas = request.form.get('nama_petugas')
        notelp_petugas = request.form.get('notelp_petugas')
        email_petugas = request.form.get('email_petugas')
        password_petugas = request.form.get('password_petugas')
        profil_petugas = request.form.get('profil_petugas')

        petugas = {
            'id_petugas': id_petugas,
            'emailLaundry': emailLaundry,
            'nama_petugas': nama_petugas,
            'notelp_petugas': notelp_petugas,
            'email_petugas': email_petugas,
            'password_petugas': password_petugas,
            'profil_petugas': profil_petugas
        }

        db.petugas.insert_one(petugas)
        return jsonify({'success': True})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/updateDataPetugas/<id_petugas>/<emailLaundry>', methods=['PUT'])
@cross_origin()
def updateDataPetugas(id_petugas, emailLaundry):
    try:
        update_fields = {}

        update_fields['nama_petugas'] = request.form.get('nama_petugas')
        update_fields['notelp_petugas'] = request.form.get('notelp_petugas')
        update_fields['password_petugas'] = request.form.get('password_petugas')
        profil_petugas = request.form.get('profil_petugas')

        current_record = db.petugas.find_one({'id_petugas': id_petugas, 'emailLaundry': emailLaundry})
        
        if not current_record:
            return jsonify({'success': False, 'message': 'Petugas not found'})

        if profil_petugas:
            update_fields['profil_petugas'] = profil_petugas

        result = db.petugas.update_one({'id_petugas': id_petugas, 'emailLaundry': emailLaundry}, {'$set': update_fields})

        if result.matched_count > 0:
            return jsonify({'success': True, 'message': 'Petugas updated successfully'})
        else:
            return jsonify({'success': False, 'error': 'Petugas not found'})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/updateDataUser/<email>', methods=['PUT']) # updated logic
@cross_origin()
def updateDataUser(email):
    try:
        update_fields = {}

        update_fields['nama'] = request.form.get('nama')
        update_fields['notelp'] = request.form.get('notelp')
        profilPict = request.form.get('profilPict')

        current_record = db.pelanggan.find_one({'email': email})

        if not current_record:
            return jsonify({'success': False, 'message': 'User not found'})

        if profilPict:
            update_fields['profilPict'] = profilPict

        result = db.pelanggan.update_one({'email': email}, {'$set': update_fields})

        if result.matched_count > 0:
            return jsonify({'success': True, 'message': 'User updated successfully'})
        else:
            return jsonify({'success': False, 'error': 'User not found'})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/updateDataAdmin/<email>', methods=['PUT'])
@cross_origin()
def updateDataAdmin(email):
    try:
        update_fields = {}

        update_fields['namaLaundry'] = request.form.get('namaLaundry')
        update_fields['notelp'] = request.form.get('notelp')
        profilPict = request.form.get('profilPict')

        current_record = db.laundry.find_one({'email': email})
        
        if not current_record:
            return jsonify({'success': False, 'message': 'Admin not found'})

        if profilPict:
            update_fields['profilPict'] = profilPict

        result = db.laundry.update_one({'email': email}, {'$set': update_fields})

        if result.matched_count > 0:
            return jsonify({'success': True, 'message': 'Admin updated successfully'})
        else:
            return jsonify({'success': False, 'error': 'Admin not found'})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/addMetodePembayaran/<emailLaundry>', methods=['POST'])
@cross_origin()
def addMetodePembayaran(emailLaundry):
    try:
        idPembayaran = request.form.get('idPembayaran')
        email_laundry = request.form.get('emailLaundry')
        payment_method = request.form.get('paymentMethod')
        nama_bank = request.form.get('namaBank', '')
        no_rek_bank = request.form.get('noRekBank', '')
        qris_img = request.form.get('qris_img', '')
        catatan = request.form.get('catatan', '')

        metodePembayaran = {
            'idPembayaran': idPembayaran,
            'emailLaundry': email_laundry,
            'paymentMethod': payment_method,
            'namaBank': nama_bank,
            'noRekBank': no_rek_bank,
            'qrisImg': qris_img,
            'catatan': catatan
        }
        db.metodePembayaran.insert_one(metodePembayaran)
        return jsonify({'success': True, 'message': 'Payment method added successfully'})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/editMetodePembayaran/<idPembayaran>/<emailLaundry>', methods=['PUT'])
@cross_origin()
def editMetodePembayaran(idPembayaran, emailLaundry):
    try:
        emailLaundry = request.form.get('emailLaundry')
        payment_method = request.form.get('paymentMethod')
        nama_bank = request.form.get('namaBank', '')
        no_rek_bank = request.form.get('noRekBank', '')
        catatan = request.form.get('catatan', '')
        qrisImg = request.form.get('qrisImg', '')

        current_record = db.metodePembayaran.find_one({'idPembayaran': idPembayaran, 'emailLaundry': emailLaundry})
        
        if not current_record:
            return jsonify({'success': False, 'message': 'Payment method not found'})

        if payment_method == 'qris':
            db.metodePembayaran.update_one(
                {'idPembayaran': idPembayaran, 'emailLaundry': emailLaundry}, 
                {'$set': {'qrisImg': qrisImg, 'catatan': catatan}}
            )
        else:
            db.metodePembayaran.update_one(
                {'idPembayaran': idPembayaran, 'emailLaundry': emailLaundry}, 
                {'$set': {'namaBank': nama_bank, 'noRekBank': no_rek_bank, 'catatan': catatan}}
            )
        
        return jsonify({'success': True, 'message': 'Payment method updated successfully'})

    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

@app.route('/addPesananState/<idPesanan>/<emailPetugas>', methods=['PUT']) # API baru
@cross_origin()
def addPesananState(idPesanan, emailPetugas):
    try:
        currentDate = request.form.get('currentDate')
        currentTime = request.form.get('currentTime')
        pesanan = request.form.get('pesanan')
        catatan = request.form.get('catatan')
        idPembayaran = request.form.get('idPembayaran')
        totalBayar = request.form.get('totalBayar')
        buktiPembayaran = request.form.get('buktiPembayaran')

        pesanan = json.loads(pesanan)
        
        current_record = db.pesanan.find_one({'idPesanan': idPesanan, 'emailPetugas': emailPetugas})
        if not current_record:
            return jsonify({'success': False, 'message': 'Pesanan not found'})

        db.pesanan.update_one(
            {'idPesanan': idPesanan, 'emailPetugas': emailPetugas}, 
            {'$set': {
                'statusPesanan.2.active': 'false',
                'statusPesanan.3.active': 'true',
                'statusPesanan.3.tanggal': currentDate,
                'statusPesanan.3.waktu': currentTime,
                'pesanan': pesanan,
                'catatan': catatan,
                'idPembayaran': idPembayaran,
                'buktiPembayaran': buktiPembayaran,
                'totalBayar': totalBayar
            }}
        )
        return jsonify({'success': True, 'message': 'Status updated successfully'})
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'success': False, 'error': error_message})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)