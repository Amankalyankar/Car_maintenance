# Import necessary libraries
from flask import Flask, request, jsonify , render_template
from flask_cors import CORS
import  psycopg2 
from psycopg2.extras import RealDictCursor
import os

# Initialize the Flask application
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS)
CORS(app)

def get_db_connection():
    """Establishes a connection to the PostgreSQL database using the connection URL."""
    try:
        
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        return conn
    except psycopg2.OperationalError as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

# --- API ENDPOINTS ---

@app.route('/api/records', methods=['GET'])
def get_records():
    """API endpoint to fetch and filter records."""
    query_params = request.args
    query = 'SELECT *, (amount - discount) as final_amount FROM service_records'
    filters = []
    values = []

    if 'date' in query_params and query_params['date']:
        filters.append('date = %s')
        values.append(query_params['date'])
    if 'adviser' in query_params and query_params['adviser']:
        filters.append('adviser LIKE %s')
        values.append(f"%{query_params['adviser']}%")
    if 'model' in query_params and query_params['model']:
        filters.append('model LIKE %s')
        values.append(f"%{query_params['model']}%")

    if filters:
        query += ' WHERE ' + ' AND '.join(filters)

    query += ' ORDER BY sr_no ASC'

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, tuple(values))
        records = cur.fetchall()
        cur.close()
        return jsonify(records)
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "Failed to fetch records"}), 500
    finally:
        if conn:
            conn.close()


@app.route('/api/records', methods=['POST'])
def add_record():
    """API endpoint to add a new record."""
    new_record = request.get_json()
    required_fields = ['date', 'carNo', 'model', 'treatmentName', 'roNo', 'invoiceNo', 'adviser', 'amount', 'discount']
    if not all(field in new_record for field in required_fields):
        return jsonify({"error": "Missing data in request"}), 400

    sql = """
        INSERT INTO service_records (date, car_no, model, treatment_name, ro_no, invoice_no, adviser, amount, discount)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING sr_no;
    """
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cur = conn.cursor()
        cur.execute(sql, (
            new_record['date'], new_record['carNo'], new_record['model'],
            new_record['treatmentName'], new_record['roNo'], new_record['invoiceNo'],
            new_record['adviser'], new_record['amount'], new_record['discount']
        ))
        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()

        conn2 = get_db_connection()
        cur2 = conn2.cursor(cursor_factory=RealDictCursor)
        cur2.execute("SELECT *, (amount - discount) as final_amount FROM service_records WHERE sr_no = %s", (new_id,))
        saved_record = cur2.fetchone()
        cur2.close()
        conn2.close()

        return jsonify(saved_record), 201
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
        return jsonify({"error": "Failed to add record"}), 500
    finally:
        if conn:
            conn.close()
# NEW: API endpoint to update a record
@app.route('/api/records/<int:record_id>', methods=['PUT'])
def update_record(record_id):
    """API endpoint to update an existing record."""
    updated_data = request.get_json()
    required_fields = ['date', 'carNo', 'model', 'treatmentName', 'roNo', 'invoiceNo', 'adviser', 'amount', 'discount']
    if not all(field in updated_data for field in required_fields):
        return jsonify({"error": "Missing data in request"}), 400

    sql = """
        UPDATE service_records
        SET date = %s, car_no = %s, model = %s, treatment_name = %s,
            ro_no = %s, invoice_no = %s, adviser = %s, amount = %s, discount = %s
        WHERE sr_no = %s;
    """
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cur = conn.cursor()
        cur.execute(sql, (
            updated_data['date'], updated_data['carNo'], updated_data['model'],
            updated_data['treatmentName'], updated_data['roNo'], updated_data['invoiceNo'],
            updated_data['adviser'], updated_data['amount'], updated_data['discount'],
            record_id
        ))
        conn.commit()
        cur.close()
        if cur.rowcount == 0:
            return jsonify({"error": "Record not found"}), 404
        return jsonify({"message": "Record updated successfully"}), 200
    except Exception as e:
        print(f"An error occurred while updating: {e}")
        conn.rollback()
        return jsonify({"error": "Failed to update record"}), 500
    finally:
        if conn:
            conn.close()

@app.route('/api/records/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    """API endpoint to delete a specific record."""
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM service_records WHERE sr_no = %s", (record_id,))
        conn.commit()
        cur.close()
        if cur.rowcount == 0:
            return jsonify({"error": "Record not found"}), 404
        return jsonify({"message": "Record deleted successfully"}), 200
    except Exception as e:
        print(f"An error occurred while deleting: {e}")
        conn.rollback()
        return jsonify({"error": "Failed to delete record"}), 500
    finally:
        if conn:
            conn.close()

@app.route('/')
def index():
    """Serves the main index.html page."""
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)