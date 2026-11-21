import os
import sys
import unittest

# Ensure scripts and apps/portal can be imported
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(BASE_DIR, 'scripts'))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps', 'portal'))

from parse_nginx_traffic import classify_channel, classify_device
from ingest_gsc_data import parse_num, parse_pct, classify_query_intent, ingest_gsc

class TestTrafficAttribution(unittest.TestCase):

    def test_classify_channel_ai_assistants(self):
        # ChatGPT referral
        ch, sub = classify_channel("https://chatgpt.com/", "Mozilla/5.0", "/")
        self.assertEqual(ch, "ai_assistant_referral")
        self.assertEqual(sub, "ChatGPT")

        # Perplexity referral
        ch, sub = classify_channel("https://www.perplexity.ai/search?q=dbert", "Mozilla/5.0", "/")
        self.assertEqual(ch, "ai_assistant_referral")
        self.assertEqual(sub, "Perplexity")

        # Claude referral
        ch, sub = classify_channel("https://claude.ai/chat/123", "Mozilla/5.0", "/")
        self.assertEqual(ch, "ai_assistant_referral")
        self.assertEqual(sub, "Claude")

    def test_classify_channel_ai_crawlers(self):
        # GPTBot crawler
        ch, sub = classify_channel("-", "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; GPTBot/1.2; +https://openai.com/gptbot)", "/")
        self.assertEqual(ch, "ai_crawler")
        self.assertEqual(sub, "Gptbot")

        # ClaudeBot crawler
        ch, sub = classify_channel("-", "Mozilla/5.0 (compatible; ClaudeBot/1.0; +claudebot@anthropic.com)", "/")
        self.assertEqual(ch, "ai_crawler")
        self.assertEqual(sub, "Claudebot")

    def test_classify_channel_organic_and_whatsapp(self):
        # Google search
        ch, sub = classify_channel("https://www.google.com/", "Mozilla/5.0", "/")
        self.assertEqual(ch, "organic_search")
        self.assertEqual(sub, "Google")

        # WhatsApp campaign
        ch, sub = classify_channel("android-app://com.whatsapp", "Mozilla/5.0", "/enroll/1999?utm_source=whatsapp")
        self.assertEqual(ch, "whatsapp_campaign")
        self.assertEqual(sub, "WhatsApp")

        # Direct
        ch, sub = classify_channel("-", "Mozilla/5.0", "/")
        self.assertEqual(ch, "direct")

    def test_classify_device(self):
        # iPhone -> Mobile
        dev = classify_device("Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148 Safari/604.1")
        self.assertEqual(dev, "Mobile")

        # Android phone -> Mobile
        dev = classify_device("Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 Chrome/120.0 Mobile Safari/537.36")
        self.assertEqual(dev, "Mobile")

        # iPad -> Tablet
        dev = classify_device("Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Safari/604.1")
        self.assertEqual(dev, "Tablet")

        # Mac / Windows Chrome -> Desktop
        dev = classify_device("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36")
        self.assertEqual(dev, "Desktop")

    def test_gsc_parsers_and_opportunity(self):
        self.assertEqual(parse_num("1,450"), 1450)
        self.assertEqual(parse_num("12.5"), 12.5)
        self.assertEqual(parse_pct("18.5%"), 18.5)

        self.assertEqual(classify_query_intent("dbert online"), "Brand")
        self.assertEqual(classify_query_intent("full stack internship"), "Internship & Careers")
        self.assertEqual(classify_query_intent("python fastapi microservices"), "Technical & Engineering")

    def test_ingest_gsc_with_sample_data(self):
        google_dir = os.path.join(BASE_DIR, 'data', 'google')
        if os.path.exists(google_dir):
            intel = ingest_gsc(google_dir)
            self.assertGreater(intel['total_queries_indexed'], 0)
            self.assertIn('top_performing_queries', intel)
            self.assertIn('striking_distance_keywords', intel)

if __name__ == '__main__':
    unittest.main()
