"""
Simple Telecom System - Flask Application
Minimal backend with beautiful frontend
"""

from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
import json

import os
from flask import Flask

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

app.config['SECRET_KEY'] = 'telecom-secret-key-2024'


# Sample data
SAMPLE_USER = {
    'id': 1,
    'name': 'John Doe',
    'email': 'john@telecom.com',
    'phone': '+91 9876543210',
    'avatar': 'JD'
}

SAMPLE_PLAN = {
    'id': 2,
    'name': 'Standard Plan',
    'price': 599,
    'status': 'active',
    'renewal_date': (datetime.now() + timedelta(days=25)).strftime('%Y-%m-%d'),
    'calls': 1500,
    'sms': 300,
    'data': 15
}

SAMPLE_BILL = {
    'id': 1,
    'amount': 706.82,
    'period': 'January 2024',
    'status': 'pending',
    'due_date': (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')
}

SAMPLE_CALLS = [
    {'number': '+91 9876543210', 'type': 'incoming', 'duration': 435, 'date': '2024-02-20 14:30', 'cost': 0},
    {'number': '+91 9123456789', 'type': 'outgoing', 'duration': 240, 'date': '2024-02-20 13:15', 'cost': 5.00},
    {'number': '+91 9999999999', 'type': 'incoming', 'duration': 180, 'date': '2024-02-20 11:45', 'cost': 0},
    {'number': '+91 8765432109', 'type': 'outgoing', 'duration': 600, 'date': '2024-02-19 20:30', 'cost': 10.00},
    {'number': '+91 9111111111', 'type': 'incoming', 'duration': 120, 'date': '2024-02-19 15:20', 'cost': 0},
]

AVAILABLE_PLANS = [
    {
        'id': 1,
        'name': 'Basic',
        'price': 299,
        'calls': 500,
        'sms': 100,
        'data': 5,
        'features': ['Unlimited roaming', '24/7 Support']
    },
    {
        'id': 2,
        'name': 'Standard',
        'price': 599,
        'calls': 1500,
        'sms': 300,
        'data': 15,
        'features': ['Unlimited roaming', '24/7 Support', 'Priority Support'],
        'popular': True
    },
    {
        'id': 3,
        'name': 'Premium',
        'price': 999,
        'calls': 3000,
        'sms': 500,
        'data': 30,
        'features': ['Unlimited roaming', '24/7 Support', 'Priority Support', 'VIP Benefits']
    }
]

# Routes
@app.route('/')
def index():
    """Home page"""
    return render_template('index.html', user=SAMPLE_USER)

@app.route('/api/user')
def get_user():
    """Get user data"""
    return jsonify(SAMPLE_USER)

@app.route('/api/plan')
def get_plan():
    """Get user's active plan"""
    return jsonify(SAMPLE_PLAN)

@app.route('/api/bill')
def get_bill():
    """Get current bill"""
    return jsonify(SAMPLE_BILL)

@app.route('/api/calls')
def get_calls():
    """Get recent calls"""
    return jsonify(SAMPLE_CALLS)

@app.route('/api/plans')
def get_available_plans():
    """Get available plans"""
    return jsonify(AVAILABLE_PLANS)

@app.route('/api/calls/stats')
def get_call_stats():
    """Get call statistics"""
    total_duration = sum(call['duration'] for call in SAMPLE_CALLS)
    total_cost = sum(call['cost'] for call in SAMPLE_CALLS)
    incoming = sum(1 for call in SAMPLE_CALLS if call['type'] == 'incoming')
    outgoing = sum(1 for call in SAMPLE_CALLS if call['type'] == 'outgoing')
    
    return jsonify({
        'total_minutes': total_duration // 60,
        'total_cost': total_cost,
        'incoming': incoming,
        'outgoing': outgoing,
        'average_duration': (total_duration // len(SAMPLE_CALLS)) if SAMPLE_CALLS else 0
    })

@app.route('/api/usage')
def get_usage():
    """Get usage statistics"""
    plan = SAMPLE_PLAN
    return jsonify({
        'calls_used': 750,
        'calls_limit': plan['calls'],
        'calls_percent': 50,
        'sms_used': 150,
        'sms_limit': plan['sms'],
        'sms_percent': 50,
        'data_used': 7.5,
        'data_limit': plan['data'],
        'data_percent': 50
    })

@app.route('/api/plan/change', methods=['POST'])
def change_plan():
    """Change plan (simulate)"""
    data = request.get_json()
    plan_id = data.get('plan_id')
    
    if plan_id in [p['id'] for p in AVAILABLE_PLANS]:
        return jsonify({'success': True, 'message': 'Plan changed successfully'})
    return jsonify({'success': False, 'message': 'Invalid plan'}), 400

@app.route('/api/bill/pay', methods=['POST'])
def pay_bill():
    """Pay bill (simulate)"""
    data = request.get_json()
    return jsonify({
        'success': True,
        'message': 'Payment processed successfully',
        'transaction_id': 'TXN' + datetime.now().strftime('%Y%m%d%H%M%S')
    })

@app.route('/health')
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)