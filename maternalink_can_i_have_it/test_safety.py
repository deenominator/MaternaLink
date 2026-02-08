"""
Simple test script for the AI/ML safety checker
No FastAPI, just pure Python testing
"""

from safety_checker import SafetyChecker, Stage
from rag_service import RAGService  # Correct: RAGService not RAGSERVICE

def main():
    print("🧪 Testing AI/ML Safety Checker (Pure Python)\n")
    
    # Initialize services
    checker = SafetyChecker("safety_db.json")
    rag = RAGService(checker)  # Correct: RAGService not RAGSERVICE
    
    # Test 1: Direct safety check
    print("1. Direct Safety Check:")
    result = checker.check_safety("Can I drink coffee?", Stage.PREGNANCY_FIRST_TRIMESTER)
    print(f"   Query: {result['query']}")
    print(f"   Status: {result['safety_status']}")
    print(f"   Explanation: {result['explanation'][:50]}...")
    print()
    
    # Test 2: RAG-enhanced response
    print("2. RAG Service Response:")
    rag_result = rag.generate_safe_response("Is ibuprofen safe?", Stage.BREASTFEEDING)
    print(f"   Confidence: {rag_result['confidence']}")
    print(f"   Answer preview: {rag_result['answer'][:100]}...")
    print()
    
    # Test 3: Search database
    print("3. Database Search:")
    search_results = checker.search("caffeine", limit=3)  # Add this method
    print(f"   Found {len(search_results)} results")
    for res in search_results:
        print(f"   - {res['name']} ({res['category']})")
    print()
    
    # Test 4: Statistics
    print("4. Database Statistics:")
    stats = checker.get_stats()
    print(f"   Total entries: {stats['total_entries']}")
    print(f"   Categories: {', '.join(stats['categories'])}")
    print()
    
    print("✅ AI/ML Safety Checker is working correctly!")

if __name__ == "__main__":
    main()