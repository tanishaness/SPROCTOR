# proctor_api.py
from flask import Blueprint, request, jsonify
from typing import Dict, Optional
import logging
from datetime import datetime

# Import from local modules
from proctor_core import ProctorCore
from detection import detect_objects
from face_rec import recognize_face
from head_pose import analyze_head_pose
from peer_comparison_tool import analyze_peer_behavior
from audio import process_audio
from graph import generate_behavior_graph

# Initialize Blueprint for API routes
proctor_api = Blueprint('proctor_api', __name__)
logging.basicConfig(level=logging.INFO)

# Initialize ProctorCore instance
proctor_core = ProctorCore()

def process_video_frame(frame_data):
    """Process video frame data"""
    try:
        frame = cv2.imdecode(frame_data, cv2.IMREAD_COLOR)
        
        # Run detection modules
        objects = detect_objects(frame)
        face_data = recognize_face(frame)
        head_pose = analyze_head_pose(frame)
        
        return {
            'objects': objects,
            'face_data': face_data,
            'head_pose': head_pose
        }
    except Exception as e:
        logging.error(f"Error in video processing: {str(e)}")
        raise

def process_audio_stream(audio_data):
    """Process audio stream data"""
    try:
        audio_events = process_audio(audio_data)
        return audio_events
    except Exception as e:
        logging.error(f"Error in audio processing: {str(e)}")
        raise

@proctor_api.route('/health', methods=['GET'])
def health_check():
    """API health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@proctor_api.route('/validate/session', methods=['POST'])
def validate_session():
    """Validate session credentials and requirements"""
    data = request.get_json()
    required_fields = ['student_id', 'exam_id', 'session_token']
    
    if not all(field in data for field in required_fields):
        return jsonify({
            'error': 'Missing required fields',
            'required': required_fields
        }), 400
        
    return jsonify({
        'status': 'valid',
        'student_id': data['student_id'],
        'exam_id': data['exam_id']
    })

@proctor_api.route('/session/start', methods=['POST'])
def start_monitoring_session():
    """Start a new proctoring session"""
    data = request.get_json()
    
    if not data or 'student_id' not in data:
        return jsonify({'error': 'student_id required'}), 400
        
    try:
        result = proctor_core.start_monitoring(data['student_id'])
        
        if 'error' in result:
            return jsonify(result), 400
            
        return jsonify({
            'status': 'success',
            'session_data': result
        })
        
    except Exception as e:
        logging.error(f"Failed to start monitoring session: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@proctor_api.route('/session/status', methods=['GET'])
def get_session_status():
    """Get current session status"""
    student_id = request.args.get('student_id')
    
    if not student_id:
        return jsonify({'error': 'student_id required'}), 400
        
    if student_id not in proctor_core.sessions:
        return jsonify({'error': 'Session not found'}), 404
        
    session = proctor_core.sessions[student_id]
    
    return jsonify({
        'status': 'active',
        'session_info': {
            'start_time': session['start_time'].isoformat(),
            'detection_count': len(session['detections']),
            'audio_event_count': len(session['audio_events']),
            'suspicious_activity_count': len(session['suspicious_activities'])
        }
    })

@proctor_api.route('/monitor/snapshot', methods=['POST'])
def process_snapshot():
    """Process a single monitoring snapshot (video frame + audio)"""
    if not request.files:
        return jsonify({'error': 'No media files provided'}), 400
        
    student_id = request.form.get('student_id')
    if not student_id or student_id not in proctor_core.sessions:
        return jsonify({'error': 'Invalid session'}), 404
        
    try:
        results = {}
        
        # Process video if provided
        if 'frame' in request.files:
            frame_file = request.files['frame']
            frame_data = np.frombuffer(frame_file.read(), np.uint8)
            video_result = process_video_frame(frame_data)
            results['video'] = video_result
            
        # Process audio if provided
        if 'audio' in request.files:
            audio_file = request.files['audio']
            audio_result = process_audio_stream(audio_file)
            results['audio'] = audio_result
            
        # Update session data
        if student_id in proctor_core.sessions:
            session = proctor_core.sessions[student_id]
            if 'video' in results:
                session['detections'].append({
                    'timestamp': datetime.now().isoformat(),
                    **results['video']
                })
            if 'audio' in results:
                session['audio_events'].extend(results['audio'])
            
        return jsonify({
            'status': 'success',
            'results': results
        })
        
    except Exception as e:
        logging.error(f"Error processing monitoring snapshot: {str(e)}")
        return jsonify({'error': 'Processing error'}), 500

@proctor_api.route('/session/end', methods=['POST'])
def end_monitoring_session():
    """End an active monitoring session"""
    data = request.get_json()
    
    if not data or 'student_id' not in data:
        return jsonify({'error': 'student_id required'}), 400
        
    try:
        student_id = data['student_id']
        if student_id not in proctor_core.sessions:
            return jsonify({'error': 'Session not found'}), 404
            
        session = proctor_core.sessions[student_id]
        duration = (datetime.now() - session['start_time']).total_seconds() / 60
        
        # Generate final report
        report = {
            'student_id': student_id,
            'duration_minutes': duration,
            'total_detections': len(session['detections']),
            'total_audio_events': len(session['audio_events']),
            'suspicious_activities': session['suspicious_activities']
        }
        
        # Cleanup session
        del proctor_core.sessions[student_id]
        
        return jsonify({
            'status': 'success',
            'report': report
        })
        
    except Exception as e:
        logging.error(f"Failed to end monitoring session: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@proctor_api.route('/analysis/report', methods=['GET'])
def get_analysis_report():
    """Get comprehensive analysis report for a session"""
    student_id = request.args.get('student_id')
    
    if not student_id:
        return jsonify({'error': 'student_id required'}), 400
        
    if student_id not in proctor_core.sessions:
        return jsonify({'error': 'Session not found'}), 404
        
    try:
        session = proctor_core.sessions[student_id]
        
        # Get behavior analysis
        peer_analysis = analyze_peer_behavior(session['detections'])
        
        # Generate behavior graph
        behavior_graph = generate_behavior_graph(
            session['detections'],
            session['head_poses'],
            session['audio_events']
        )
        
        duration = (datetime.now() - session['start_time']).total_seconds() / 60
        
        report = {
            'student_id': student_id,
            'duration_minutes': duration,
            'session_stats': {
                'total_detections': len(session['detections']),
                'total_audio_events': len(session['audio_events']),
                'suspicious_activities': session['suspicious_activities']
            },
            'behavior_analysis': {
                'peer_analysis': peer_analysis,
                'behavior_graph': behavior_graph
            }
        }
        
        return jsonify({
            'status': 'success',
            'report': report
        })
        
    except Exception as e:
        logging.error(f"Failed to generate analysis report: {str(e)}")
        return jsonify({'error': 'Report generation failed'}), 500

# Error handlers
@proctor_api.errorhandler(400)
def bad_request(e):
    return jsonify({'error': 'Bad request'}), 400

@proctor_api.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Resource not found'}), 404

@proctor_api.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500