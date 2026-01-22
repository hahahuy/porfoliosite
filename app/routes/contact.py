"""Contact form routes"""
from flask import Blueprint, request, jsonify, current_app
from app.utils.form_handler import validate_contact_form, save_contact_submission

contact_bp = Blueprint('contact', __name__)


@contact_bp.route('/contact', methods=['POST'])
def submit_contact():
    """Handle contact form submission"""
    try:
        data = request.get_json() or request.form.to_dict()
        
        # Validate form data
        is_valid, error = validate_contact_form(data)
        if not is_valid:
            return jsonify({'error': error}), 400
        
        # Save to database
        submission = save_contact_submission(
            name=data['name'],
            email=data['email'],
            message=data['message']
        )
        
        current_app.logger.info(f"Contact form submission received from {submission.email}")
        
        return jsonify({
            'success': True,
            'message': 'Thank you for your message! We will get back to you soon.',
            'id': submission.id
        }), 201
        
    except Exception as e:
        current_app.logger.error(f"Error processing contact form: {e}")
        return jsonify({
            'error': 'An error occurred while processing your message. Please try again later.'
        }), 500
