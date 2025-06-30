import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from sentiment_analyzer import analyze_sentiment, get_sentiment_label
from utils import categorize_sentiment, calculate_metrics
import pandas as pd

class TestSentimentAnalysis(unittest.TestCase):
    """Test sentiment analysis functions"""
    
    def test_positive_sentiment(self):
        """Test positive sentiment detection"""
        text = "I love this product! It's amazing!"
        score = analyze_sentiment(text)
        self.assertGreater(score, 0, "Should detect positive sentiment")
    
    def test_negative_sentiment(self):
        """Test negative sentiment detection"""
        text = "This product is terrible! Waste of money!"
        score = analyze_sentiment(text)
        self.assertLess(score, 0, "Should detect negative sentiment")
    
    def test_neutral_sentiment(self):
        """Test neutral sentiment detection"""
        text = "The product arrived today."
        score = analyze_sentiment(text)
        self.assertAlmostEqual(score, 0, delta=0.3, msg="Should be roughly neutral")
    
    def test_empty_text(self):
        """Test empty text handling"""
        score = analyze_sentiment("")
        self.assertEqual(score, 0.0, "Empty text should return 0")
    
    def test_sentiment_labels(self):
        """Test sentiment label conversion"""
        self.assertEqual(get_sentiment_label(0.5), "Positive")
        self.assertEqual(get_sentiment_label(-0.5), "Negative")
        self.assertEqual(get_sentiment_label(0.05), "Neutral")

class TestUtils(unittest.TestCase):
    """Test utility functions"""
    
    def test_categorize_sentiment(self):
        """Test sentiment categorization"""
        self.assertEqual(categorize_sentiment(0.5), "Positive")
        self.assertEqual(categorize_sentiment(-0.5), "Negative")
        self.assertEqual(categorize_sentiment(0.05), "Neutral")
    
    def test_calculate_metrics(self):
        """Test metrics calculation"""
        # Create sample data
        data = {
            'sentiment': [0.5, -0.3, 0.1, 0.8, -0.2],
            'likes': [10, 5, 8, 15, 7],
            'retweets': [2, 1, 3, 5, 2]
        }
        df = pd.DataFrame(data)
        
        metrics = calculate_metrics(df)
        
        # Check if metrics are calculated
        self.assertIn('total_tweets', metrics)
        self.assertIn('avg_sentiment', metrics)
        self.assertIn('positive_tweets', metrics)
        self.assertEqual(metrics['total_tweets'], 5)

class TestDataProcessing(unittest.TestCase):
    """Test data processing functions"""
    
    def setUp(self):
        """Set up test data"""
        self.sample_tweets = [
            {
                'id': '1',
                'text': 'Great product!',
                'created_at': '2024-01-01',
                'likes': 10,
                'retweets': 2,
                'sentiment': 0.8
            },
            {
                'id': '2',
                'text': 'Not good',
                'created_at': '2024-01-02',
                'likes': 3,
                'retweets': 0,
                'sentiment': -0.6
            }
        ]
    
    def test_data_structure(self):
        """Test that sample data has required fields"""
        for tweet in self.sample_tweets:
            self.assertIn('id', tweet)
            self.assertIn('text', tweet)
            self.assertIn('sentiment', tweet)

def run_all_tests():
    """Run all test cases"""
    print("  Running Tests...")
    print("=" * 30)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestSentimentAnalysis))
    suite.addTests(loader.loadTestsFromTestCase(TestUtils))
    suite.addTests(loader.loadTestsFromTestCase(TestDataProcessing))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 30)
    if result.wasSuccessful():
        print("  All tests passed!")
    else:
        print(f"  {len(result.failures)} test(s) failed")
        print(f"  {len(result.errors)} error(s) occurred")
    
    return result.wasSuccessful()

def quick_functionality_test():
    """Quick test of core functionality"""
    print("  Quick Functionality Test")
    print("-" * 30)
    
    try:
        # Test sentiment analysis
        score = analyze_sentiment("This is a great product!")
        print(f"✓ Sentiment analysis works: {score:.3f}")
        
        # Test label conversion
        label = get_sentiment_label(score)
        print(f"✓ Label conversion works: {label}")
        
        # Test categorization
        category = categorize_sentiment(score)
        print(f"✓ Categorization works: {category}")
        
        print("  All functionality tests passed!")
        return True
    
    except Exception as e:
        print(f"  Test failed: {e}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run tests")
    parser.add_argument("--quick", action="store_true", help="Run quick functionality test")
    parser.add_argument("--full", action="store_true", help="Run full test suite")
    
    args = parser.parse_args()
    
    if args.quick:
        quick_functionality_test()
    elif args.full:
        run_all_tests()
    else:
        # Default: run both
        print("Running both quick and full tests...\n")
        quick_success = quick_functionality_test()
        print()
        full_success = run_all_tests()
        
        if quick_success and full_success:
            print("\n  All tests completed successfully!")
        else:
            print("\n ️  Some tests failed. Check output above.")