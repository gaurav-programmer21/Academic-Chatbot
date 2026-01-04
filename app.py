from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from config import Config
from services.ai_service import AIService
from services.knowledge_service import KnowledgeService
from services.memory_service import MemoryService
import os

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Initialize services
ai_service = AIService(app.config)
knowledge_service = KnowledgeService()
memory_service = MemoryService()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message')
        model = data.get('model', 'openai')
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Get conversation history and knowledge base
        history = memory_service.get_recent_history(10)
        knowledge = knowledge_service.get_all_knowledge()
        
        # Generate AI response
        response = ai_service.generate_response(
            user_message,
            history,
            knowledge,
            model
        )
        
        # Save to memory
        memory_service.add_message('user', user_message)
        memory_service.add_message('assistant', response)
        
        # Extract and save knowledge
        extracted_knowledge = knowledge_service.extract_knowledge(
            user_message,
            response
        )
        if extracted_knowledge:
            knowledge_service.add_knowledge(extracted_knowledge)
        
        return jsonify({
            'response': response,
            'success': True
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    try:
        history = memory_service.get_all_history()
        return jsonify({'history': history, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/knowledge', methods=['GET'])
def get_knowledge():
    try:
        knowledge = knowledge_service.get_all_knowledge()
        return jsonify({'knowledge': knowledge, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clear-history', methods=['POST'])
def clear_history():
    try:
        memory_service.clear_history()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clear-knowledge', methods=['POST'])
def clear_knowledge():
    try:
        knowledge_service.clear_knowledge()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)