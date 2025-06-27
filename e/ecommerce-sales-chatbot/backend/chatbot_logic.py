import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from models import Product, db
from rapidfuzz import fuzz, process

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

class ChatbotLogic:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        
        # Intent patterns
        self.intent_patterns = {
            'greeting': [
                r'\b(hi|hello|hey|good morning|good afternoon|good evening)\b',
                r'\bhow are you\b',
                r'\bwhat\'s up\b'
            ],
            'product_search': [
                r'\b(find|search|look for|show me|get)\b.*\b(product|item|thing)\b',
                r'\b(what|which)\b.*\b(products|items)\b.*\b(do you have|available)\b',
                r'\b(category|categories)\b',
                r'\b(price|cost|expensive|cheap)\b'
            ],
            'product_info': [
                r'\b(tell me about|describe|what is|info about)\b',
                r'\b(details|specifications|features)\b',
                r'\b(how much|price|cost)\b'
            ],
            'add_to_cart': [
                r'\b(add|put|place)\b.*\b(cart|basket)\b',
                r'\b(buy|purchase|order)\b',
                r'\b(quantity|how many)\b'
            ],
            'view_cart': [
                r'\b(cart|basket|shopping cart)\b',
                r'\b(what\'s in|show|display)\b.*\b(cart|basket)\b',
                r'\b(total|amount|cost)\b'
            ],
            'checkout': [
                r'\b(checkout|check out|place order|complete purchase)\b',
                r'\b(pay|payment|buy now)\b'
            ],
            'help': [
                r'\b(help|support|assist|what can you do)\b',
                r'\b(how to|how do i)\b'
            ],
            'goodbye': [
                r'\b(bye|goodbye|see you|thanks|thank you)\b',
                r'\b(end|stop|exit)\b'
            ]
        }
        
        # Response templates
        self.response_templates = {
            'greeting': [
                "Hello! Welcome to our e-commerce store. How can I help you today?",
                "Hi there! I'm here to help you find the perfect products. What are you looking for?",
                "Welcome! I can help you browse products, answer questions, or assist with your purchase."
            ],
            'product_search': [
                "I'd be happy to help you find products! What type of items are you looking for?",
                "Let me search for products that match your needs. Can you tell me more about what you're interested in?",
                "I can help you browse our product categories. What are you looking for today?"
            ],
            'product_info': [
                "I'd be glad to provide more information about our products. Which item would you like to know more about?",
                "Let me get the details for you. What specific product are you interested in?",
                "I can tell you about features, pricing, and availability. Which product would you like to learn about?"
            ],
            'add_to_cart': [
                "Great choice! I can help you add items to your cart. How many would you like?",
                "I'll add that to your cart. What quantity would you prefer?",
                "Perfect! Let me add that to your shopping cart for you."
            ],
            'view_cart': [
                "I'll show you what's currently in your cart.",
                "Let me display your shopping cart contents.",
                "Here's what you have in your cart so far."
            ],
            'checkout': [
                "I'll help you complete your purchase. Let's proceed to checkout!",
                "Great! Let me guide you through the checkout process.",
                "Perfect! I'll help you finalize your order."
            ],
            'help': [
                "I'm here to help! I can assist you with:\n- Browsing products\n- Finding specific items\n- Adding items to cart\n- Checking out\n- Answering questions about products",
                "I can help you shop! Here's what I can do:\n- Search for products\n- Show product details\n- Manage your cart\n- Process orders\n- Answer any questions",
                "I'm your shopping assistant! I can help you find products, manage your cart, and complete purchases."
            ],
            'goodbye': [
                "Thank you for shopping with us! Have a great day!",
                "Thanks for visiting! Come back anytime!",
                "Goodbye! Feel free to return if you need anything else."
            ],
            'unknown': [
                "I'm not sure I understood that. Could you please rephrase or ask for help to see what I can do?",
                "I didn't catch that. Would you like me to help you browse products or assist with something specific?",
                "I'm still learning! Could you try asking in a different way or type 'help' to see what I can do?"
            ]
        }
        
        self.intent_threshold = 80  # Fuzzy match threshold
    
    def preprocess_text(self, text):
        """Preprocess text for better matching"""
        text = text.lower()
        tokens = word_tokenize(text)
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens if token not in self.stop_words]
        return ' '.join(tokens)
    
    def fuzzy_detect_intent(self, message):
        """Fuzzy intent recognition using rapidfuzz"""
        message_lower = message.lower()
        best_intent = 'unknown'
        best_score = 0
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                score = fuzz.partial_ratio(pattern.replace('\\b', ''), message_lower)
                if score > best_score:
                    best_score = score
                    best_intent = intent
        if best_score >= self.intent_threshold:
            return best_intent
        return 'unknown'
    
    def extract_product_keywords(self, message):
        """Extract product-related keywords from message"""
        # Common product categories and keywords
        categories = {
            'electronics': ['phone', 'laptop', 'computer', 'tv', 'headphones', 'mouse', 'keyboard', 'electronic'],
            'furniture': ['chair', 'table', 'desk', 'sofa', 'bed', 'furniture'],
            'fitness': ['gym', 'workout', 'fitness', 'exercise', 'yoga', 'sports'],
            'home': ['kitchen', 'appliance', 'coffee', 'kettle', 'home']
        }
        
        message_lower = message.lower()
        extracted_categories = []
        
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in message_lower:
                    extracted_categories.append(category)
                    break
        
        return extracted_categories
    
    def search_products(self, query, category=None, max_results=5):
        """Search for products based on query and category"""
        try:
            # Get all active products
            products = Product.query.filter_by(is_active=True)
            
            if category:
                products = products.filter(Product.category.ilike(f'%{category}%'))
            
            products = products.all()
            
            if not products:
                return []
            
            # Create product descriptions for vectorization
            product_descriptions = [f"{p.name} {p.description} {p.category}" for p in products]
            
            # Vectorize the descriptions
            tfidf_matrix = self.vectorizer.fit_transform(product_descriptions)
            
            # Vectorize the query
            query_vector = self.vectorizer.transform([query])
            
            # Calculate similarity
            similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
            
            # Get top matches
            top_indices = similarities.argsort()[-max_results:][::-1]
            
            results = []
            for idx in top_indices:
                if similarities[idx] > 0.1:  # Minimum similarity threshold
                    product = products[idx]
                    results.append({
                        'product': product.to_dict(),
                        'similarity': float(similarities[idx])
                    })
            
            return results
            
        except Exception as e:
            print(f"Error searching products: {e}")
            return []
    
    def recommend_products(self, user_id, max_results=3):
        """Recommend products based on recent user chat history"""
        from models import ChatMessage
        # Get last 5 user messages
        recent_msgs = ChatMessage.query.filter_by(user_id=user_id, sender='user').order_by(ChatMessage.timestamp.desc()).limit(5).all()
        keywords = []
        for msg in recent_msgs:
            tokens = word_tokenize(msg.message.lower())
            tokens = [t for t in tokens if t not in self.stop_words]
            keywords.extend(tokens)
        # Use most common keywords for product search
        if keywords:
            from collections import Counter
            common = [k for k, _ in Counter(keywords).most_common(2)]
            query = ' '.join(common)
            results = self.search_products(query, max_results=max_results)
            return results
        return []
    
    def generate_response(self, message, user_id=None):
        """Generate a response based on the user message (with fuzzy intent and recommendations)"""
        # Use fuzzy intent detection
        intent = self.fuzzy_detect_intent(message)
        if intent == 'greeting':
            return self._get_random_response('greeting')
        elif intent == 'product_search':
            categories = self.extract_product_keywords(message)
            if categories:
                results = self.search_products(message, categories[0])
                if results:
                    response = f"I found some {categories[0]} products for you:\n\n"
                    for i, result in enumerate(results[:3], 1):
                        product = result['product']
                        response += f"{i}. **{product['name']}** - ${product['price']}\n"
                        response += f"   {product['description'][:100]}...\n\n"
                    response += "Would you like to know more about any of these products?"
                else:
                    response = self._get_random_response('product_search')
            else:
                # Try context-aware recommendations
                if user_id:
                    recs = self.recommend_products(user_id)
                    if recs:
                        response = "Based on your recent queries, you might like:\n\n"
                        for i, result in enumerate(recs, 1):
                            product = result['product']
                            response += f"{i}. **{product['name']}** - ${product['price']}\n"
                            response += f"   {product['description'][:100]}...\n\n"
                        response += "Would you like to know more about any of these?"
                    else:
                        response = self._get_random_response('product_search')
                else:
                    response = self._get_random_response('product_search')
        elif intent == 'product_info':
            results = self.search_products(message)
            if results:
                product = results[0]['product']
                response = f"Here's information about **{product['name']}**:\n\n"
                response += f"**Price:** ${product['price']}\n"
                response += f"**Category:** {product['category']}\n"
                response += f"**Description:** {product['description']}\n"
                response += f"**Stock:** {product['stock_quantity']} available\n\n"
                response += "Would you like to add this to your cart?"
            else:
                response = "I couldn't find that specific product. Could you try searching for it differently?"
        elif intent == 'add_to_cart':
            response = self._get_random_response('add_to_cart')
        elif intent == 'view_cart':
            response = self._get_random_response('view_cart')
        elif intent == 'checkout':
            response = self._get_random_response('checkout')
        elif intent == 'help':
            response = self._get_random_response('help')
        elif intent == 'goodbye':
            response = self._get_random_response('goodbye')
        else:
            # Try context-aware recommendations for unknowns
            if user_id:
                recs = self.recommend_products(user_id)
                if recs:
                    response = "I'm not sure I understood, but based on your recent queries, you might like:\n\n"
                    for i, result in enumerate(recs, 1):
                        product = result['product']
                        response += f"{i}. **{product['name']}** - ${product['price']}\n"
                        response += f"   {product['description'][:100]}...\n\n"
                    response += "Would you like to know more about any of these?"
                else:
                    response = self._get_random_response('unknown')
            else:
                response = self._get_random_response('unknown')
        return response
    
    def _get_random_response(self, intent):
        """Get a random response for the given intent"""
        import random
        responses = self.response_templates.get(intent, self.response_templates['unknown'])
        return random.choice(responses)
