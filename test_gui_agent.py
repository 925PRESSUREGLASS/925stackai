import unittest
from datetime import datetime

# Minimal mock GUI Agent based on documentation
class GUIAgent:
    def classify_intent(self, message):
        if 'quote' in message.lower():
            return 'quote_request'
        elif 'how' in message.lower() or 'what' in message.lower():
            return 'question'
        elif 'clarify' in message.lower():
            return 'clarification'
        return 'fallback'

    def handle_quote_request(self, message, session_state):
        return 'Quote generated.'

    def handle_general_question(self, message, session_state):
        return 'General answer.'

    def handle_clarification(self, message, session_state):
        return 'Clarification provided.'

    def handle_fallback(self, message, session_state):
        return 'Sorry, I did not understand.'

    def process_user_input(self, message, session_state):
        intent = self.classify_intent(message)
        if intent == 'quote_request':
            return self.handle_quote_request(message, session_state)
        elif intent == 'question':
            return self.handle_general_question(message, session_state)
        elif intent == 'clarification':
            return self.handle_clarification(message, session_state)
        else:
            return self.handle_fallback(message, session_state)

    def format_quote_display(self, quote_data):
        formatted = f"""
        ## Quote Summary
        **Property**: {quote_data['location']}
        **Total**: ${quote_data['total']:.2f}
        ### Breakdown:
        """
        for item in quote_data['line_items']:
            formatted += f"- {item['description']}: ${item['amount']:.2f}\n"
        return formatted

class TestGUIAgent(unittest.TestCase):
    def setUp(self):
        self.agent = GUIAgent()
        self.session_state = {}

    def test_intent_classification(self):
        self.assertEqual(self.agent.classify_intent('Can I get a quote?'), 'quote_request')
        self.assertEqual(self.agent.classify_intent('How does this work?'), 'question')
        self.assertEqual(self.agent.classify_intent('Can you clarify?'), 'clarification')
        self.assertEqual(self.agent.classify_intent('Random text'), 'fallback')

    def test_process_user_input(self):
        self.assertEqual(self.agent.process_user_input('I need a quote', self.session_state), 'Quote generated.')
        self.assertEqual(self.agent.process_user_input('How much is it?', self.session_state), 'General answer.')
        self.assertEqual(self.agent.process_user_input('Please clarify', self.session_state), 'Clarification provided.')
        self.assertEqual(self.agent.process_user_input('???', self.session_state), 'Sorry, I did not understand.')

    def test_format_quote_display(self):
        quote_data = {
            'location': '123 Main St',
            'total': 250.0,
            'line_items': [
                {'description': 'Windows', 'amount': 200.0},
                {'description': 'Travel', 'amount': 50.0}
            ]
        }
        output = self.agent.format_quote_display(quote_data)
        self.assertIn('123 Main St', output)
        self.assertIn('$250.00', output)
        self.assertIn('Windows', output)
        self.assertIn('Travel', output)

if __name__ == '__main__':
    unittest.main()
